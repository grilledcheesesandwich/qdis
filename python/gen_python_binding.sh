#!/bin/bash
# Generate Python binding for disass.h
# Uses http://code.google.com/p/ctypesgen/source/checkout
ctypesgen.py -lqdis disass.h -L . > disass.py
