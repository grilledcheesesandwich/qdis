/*
 * QEMU 8259 interrupt controller emulation
 *
 * Copyright (c) 2003-2004 Fabrice Bellard
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
 * THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 * THE SOFTWARE.
 */
#include "hw.h"
#include "pc.h"
#include "isa.h"
#include "monitor/monitor.h"
#include "qemu/timer.h"
#include "i8259_internal.h"

/* debug PIC */
//#define DEBUG_PIC

#ifdef DEBUG_PIC
#define DPRINTF(fmt, ...)                                       \
    do { printf("pic: " fmt , ## __VA_ARGS__); } while (0)
#else
#define DPRINTF(fmt, ...)
#endif

//#define DEBUG_IRQ_LATENCY
//#define DEBUG_IRQ_COUNT

#if defined(DEBUG_PIC) || defined(DEBUG_IRQ_COUNT)
static int irq_level[16];
#endif
#ifdef DEBUG_IRQ_COUNT
static uint64_t irq_count[16];
#endif
#ifdef DEBUG_IRQ_LATENCY
static int64_t irq_time[16];
#endif
DeviceState *isa_pic;
static PICCommonState *slave_pic;

/* return the highest priority found in mask (highest = smallest
   number). Return 8 if no irq */
static int get_priority(PICCommonState *s, int mask)
{
    int priority;

    if (mask == 0) {
        return 8;
    }
    priority = 0;
    while ((mask & (1 << ((priority + s->priority_add) & 7))) == 0) {
        priority++;
    }
    return priority;
}

/* return the pic wanted interrupt. return -1 if none */
static int pic_get_irq(PICCommonState *s)
{
    int mask, cur_priority, priority;

    mask = s->irr & ~s->imr;
    priority = get_priority(s, mask);
    if (priority == 8) {
        return -1;
    }
    /* compute current priority. If special fully nested mode on the
       master, the IRQ coming from the slave is not taken into account
       for the priority computation. */
    mask = s->isr;
    if (s->special_mask) {
        mask &= ~s->imr;
    }
    if (s->special_fully_nested_mode && s->master) {
        mask &= ~(1 << 2);
    }
    cur_priority = get_priority(s, mask);
    if (priority < cur_priority) {
        /* higher priority found: an irq should be generated */
        return (priority + s->priority_add) & 7;
    } else {
        return -1;
    }
}

/* Update INT output. Must be called every time the output may have changed. */
static void pic_update_irq(PICCommonState *s)
{
    int irq;

    irq = pic_get_irq(s);
    if (irq >= 0) {
        DPRINTF("pic%d: imr=%x irr=%x padd=%d\n",
                s->master ? 0 : 1, s->imr, s->irr, s->priority_add);
        qemu_irq_raise(s->int_out[0]);
    } else {
        qemu_irq_lower(s->int_out[0]);
    }
}

/* set irq level. If an edge is detected, then the IRR is set to 1 */
static void pic_set_irq(void *opaque, int irq, int level)
{
    PICCommonState *s = opaque;
    int mask = 1 << irq;

#if defined(DEBUG_PIC) || defined(DEBUG_IRQ_COUNT) || \
    defined(DEBUG_IRQ_LATENCY)
    int irq_index = s->master ? irq : irq + 8;
#endif
#if defined(DEBUG_PIC) || defined(DEBUG_IRQ_COUNT)
    if (level != irq_level[irq_index]) {
        DPRINTF("pic_set_irq: irq=%d level=%d\n", irq_index, level);
        irq_level[irq_index] = level;
#ifdef DEBUG_IRQ_COUNT
        if (level == 1) {
            irq_count[irq_index]++;
        }
#endif
    }
#endif
#ifdef DEBUG_IRQ_LATENCY
    if (level) {
        irq_time[irq_index] = qemu_get_clock_ns(vm_clock);
    }
#endif

    if (s->elcr & mask) {
        /* level triggered */
        if (level) {
            s->irr |= mask;
            s->last_irr |= mask;
        } else {
            s->irr &= ~mask;
            s->last_irr &= ~mask;
        }
    } else {
        /* edge triggered */
        if (level) {
            if ((s->last_irr & mask) == 0) {
                s->irr |= mask;
            }
            s->last_irr |= mask;
        } else {
            s->last_irr &= ~mask;
        }
    }
    pic_update_irq(s);
}

/* acknowledge interrupt 'irq' */
static void pic_intack(PICCommonState *s, int irq)
{
    if (s->auto_eoi) {
        if (s->rotate_on_auto_eoi) {
            s->priority_add = (irq + 1) & 7;
        }
    } else {
        s->isr |= (1 << irq);
    }
    /* We don't clear a level sensitive interrupt here */
    if (!(s->elcr & (1 << irq))) {
        s->irr &= ~(1 << irq);
    }
    pic_update_irq(s);
}

int pic_read_irq(DeviceState *d)
{
    PICCommonState *s = DO_UPCAST(PICCommonState, dev.qdev, d);
    int irq, irq2, intno;

    irq = pic_get_irq(s);
    if (irq >= 0) {
        if (irq == 2) {
            irq2 = pic_get_irq(slave_pic);
            if (irq2 >= 0) {
                pic_intack(slave_pic, irq2);
            } else {
                /* spurious IRQ on slave controller */
                irq2 = 7;
            }
            intno = slave_pic->irq_base + irq2;
        } else {
            intno = s->irq_base + irq;
        }
        pic_intack(s, irq);
    } else {
        /* spurious IRQ on host controller */
        irq = 7;
        intno = s->irq_base + irq;
    }

#if defined(DEBUG_PIC) || defined(DEBUG_IRQ_LATENCY)
    if (irq == 2) {
        irq = irq2 + 8;
    }
#endif
#ifdef DEBUG_IRQ_LATENCY
    printf("IRQ%d latency=%0.3fus\n",
           irq,
           (double)(qemu_get_clock_ns(vm_clock) -
                    irq_time[irq]) * 1000000.0 / get_ticks_per_sec());
#endif
    DPRINTF("pic_interrupt: irq=%d\n", irq);
    return intno;
}

static void pic_init_reset(PICCommonState *s)
{
    pic_reset_common(s);
    pic_update_irq(s);
}

static void pic_reset(DeviceState *dev)
{
    PICCommonState *s = DO_UPCAST(PICCommonState, dev.qdev, dev);

    s->elcr = 0;
    pic_init_reset(s);
}

static void pic_ioport_write(void *opaque, hwaddr addr64,
                             uint64_t val64, unsigned size)
{
    PICCommonState *s = opaque;
    uint32_t addr = addr64;
    uint32_t val = val64;
    int priority, cmd, irq;

    DPRINTF("write: addr=0x%02x val=0x%02x\n", addr, val);
    if (addr == 0) {
        if (val & 0x10) {
            pic_init_reset(s);
            s->init_state = 1;
            s->init4 = val & 1;
            s->single_mode = val & 2;
            if (val & 0x08) {
                hw_error("level sensitive irq not supported");
            }
        } else if (val & 0x08) {
            if (val & 0x04) {
                s->poll = 1;
            }
            if (val & 0x02) {
                s->read_reg_select = val & 1;
            }
            if (val & 0x40) {
                s->special_mask = (val >> 5) & 1;
            }
        } else {
            cmd = val >> 5;
            switch (cmd) {
            case 0:
            case 4:
                s->rotate_on_auto_eoi = cmd >> 2;
                break;
            case 1: /* end of interrupt */
            case 5:
                priority = get_priority(s, s->isr);
                if (priority != 8) {
                    irq = (priority + s->priority_add) & 7;
                    s->isr &= ~(1 << irq);
                    if (cmd == 5) {
                        s->priority_add = (irq + 1) & 7;
                    }
                    pic_update_irq(s);
                }
                break;
            case 3:
                irq = val & 7;
                s->isr &= ~(1 << irq);
                pic_update_irq(s);
                break;
            case 6:
                s->priority_add = (val + 1) & 7;
                pic_update_irq(s);
                break;
            case 7:
                irq = val & 7;
                s->isr &= ~(1 << irq);
                s->priority_add = (irq + 1) & 7;
                pic_update_irq(s);
                break;
            default:
                /* no operation */
                break;
            }
        }
    } else {
        switch (s->init_state) {
        case 0:
            /* normal mode */
            s->imr = val;
            pic_update_irq(s);
            break;
        case 1:
            s->irq_base = val & 0xf8;
            s->init_state = s->single_mode ? (s->init4 ? 3 : 0) : 2;
            break;
        case 2:
            if (s->init4) {
                s->init_state = 3;
            } else {
                s->init_state = 0;
            }
            break;
        case 3:
            s->special_fully_nested_mode = (val >> 4) & 1;
            s->auto_eoi = (val >> 1) & 1;
            s->init_state = 0;
            break;
        }
    }
}

static uint64_t pic_ioport_read(void *opaque, hwaddr addr,
                                unsigned size)
{
    PICCommonState *s = opaque;
    int ret;

    if (s->poll) {
        ret = pic_get_irq(s);
        if (ret >= 0) {
            pic_intack(s, ret);
            ret |= 0x80;
        } else {
            ret = 0;
        }
        s->poll = 0;
    } else {
        if (addr == 0) {
            if (s->read_reg_select) {
                ret = s->isr;
            } else {
                ret = s->irr;
            }
        } else {
            ret = s->imr;
        }
    }
    DPRINTF("read: addr=0x%02x val=0x%02x\n", addr, ret);
    return ret;
}

int pic_get_output(DeviceState *d)
{
    PICCommonState *s = DO_UPCAST(PICCommonState, dev.qdev, d);

    return (pic_get_irq(s) >= 0);
}

static void elcr_ioport_write(void *opaque, hwaddr addr,
                              uint64_t val, unsigned size)
{
    PICCommonState *s = opaque;
    s->elcr = val & s->elcr_mask;
}

static uint64_t elcr_ioport_read(void *opaque, hwaddr addr,
                                 unsigned size)
{
    PICCommonState *s = opaque;
    return s->elcr;
}

static const MemoryRegionOps pic_base_ioport_ops = {
    .read = pic_ioport_read,
    .write = pic_ioport_write,
    .impl = {
        .min_access_size = 1,
        .max_access_size = 1,
    },
};

static const MemoryRegionOps pic_elcr_ioport_ops = {
    .read = elcr_ioport_read,
    .write = elcr_ioport_write,
    .impl = {
        .min_access_size = 1,
        .max_access_size = 1,
    },
};

static void pic_init(PICCommonState *s)
{
    memory_region_init_io(&s->base_io, &pic_base_ioport_ops, s, "pic", 2);
    memory_region_init_io(&s->elcr_io, &pic_elcr_ioport_ops, s, "elcr", 1);

    qdev_init_gpio_out(&s->dev.qdev, s->int_out, ARRAY_SIZE(s->int_out));
    qdev_init_gpio_in(&s->dev.qdev, pic_set_irq, 8);
}

void pic_info(Monitor *mon)
{
    int i;
    PICCommonState *s;

    if (!isa_pic) {
        return;
    }
    for (i = 0; i < 2; i++) {
        s = i == 0 ? DO_UPCAST(PICCommonState, dev.qdev, isa_pic) : slave_pic;
        monitor_printf(mon, "pic%d: irr=%02x imr=%02x isr=%02x hprio=%d "
                       "irq_base=%02x rr_sel=%d elcr=%02x fnm=%d\n",
                       i, s->irr, s->imr, s->isr, s->priority_add,
                       s->irq_base, s->read_reg_select, s->elcr,
                       s->special_fully_nested_mode);
    }
}

void irq_info(Monitor *mon)
{
#ifndef DEBUG_IRQ_COUNT
    monitor_printf(mon, "irq statistic code not compiled.\n");
#else
    int i;
    int64_t count;

    monitor_printf(mon, "IRQ statistics:\n");
    for (i = 0; i < 16; i++) {
        count = irq_count[i];
        if (count > 0) {
            monitor_printf(mon, "%2d: %" PRId64 "\n", i, count);
        }
    }
#endif
}

qemu_irq *i8259_init(ISABus *bus, qemu_irq parent_irq)
{
    qemu_irq *irq_set;
    ISADevice *dev;
    int i;

    irq_set = g_malloc(ISA_NUM_IRQS * sizeof(qemu_irq));

    dev = i8259_init_chip("isa-i8259", bus, true);

    qdev_connect_gpio_out(&dev->qdev, 0, parent_irq);
    for (i = 0 ; i < 8; i++) {
        irq_set[i] = qdev_get_gpio_in(&dev->qdev, i);
    }

    isa_pic = &dev->qdev;

    dev = i8259_init_chip("isa-i8259", bus, false);

    qdev_connect_gpio_out(&dev->qdev, 0, irq_set[2]);
    for (i = 0 ; i < 8; i++) {
        irq_set[i + 8] = qdev_get_gpio_in(&dev->qdev, i);
    }

    slave_pic = DO_UPCAST(PICCommonState, dev, dev);

    return irq_set;
}

static void i8259_class_init(ObjectClass *klass, void *data)
{
    PICCommonClass *k = PIC_COMMON_CLASS(klass);
    DeviceClass *dc = DEVICE_CLASS(klass);

    k->init = pic_init;
    dc->reset = pic_reset;
}

static const TypeInfo i8259_info = {
    .name       = "isa-i8259",
    .instance_size = sizeof(PICCommonState),
    .parent     = TYPE_PIC_COMMON,
    .class_init = i8259_class_init,
};

static void pic_register_types(void)
{
    type_register_static(&i8259_info);
}

type_init(pic_register_types)
