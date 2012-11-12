'''Wrapper for disass.h

Generated with:
/home/orion/upstream/python/ctypesgen-read-only/ctypesgen.py -lqdis disass.h -L .

Do not modify this file.
'''

__docformat__ =  'restructuredtext'

# Begin preamble

import ctypes, os, sys
from ctypes import *

_int_types = (c_int16, c_int32)
if hasattr(ctypes, 'c_int64'):
    # Some builds of ctypes apparently do not have c_int64
    # defined; it's a pretty good bet that these builds do not
    # have 64-bit pointers.
    _int_types += (c_int64,)
for t in _int_types:
    if sizeof(t) == sizeof(c_size_t):
        c_ptrdiff_t = t
del t
del _int_types

class c_void(Structure):
    # c_void_p is a buggy return type, converting to int, so
    # POINTER(None) == c_void_p is actually written as
    # POINTER(c_void), so it can be treated as a real pointer.
    _fields_ = [('dummy', c_int)]

def POINTER(obj):
    p = ctypes.POINTER(obj)

    # Convert None to a real NULL pointer to work around bugs
    # in how ctypes handles None on 64-bit platforms
    if not isinstance(p.from_param, classmethod):
        def from_param(cls, x):
            if x is None:
                return cls()
            else:
                return x
        p.from_param = classmethod(from_param)

    return p

class UserString:
    def __init__(self, seq):
        if isinstance(seq, basestring):
            self.data = seq
        elif isinstance(seq, UserString):
            self.data = seq.data[:]
        else:
            self.data = str(seq)
    def __str__(self): return str(self.data)
    def __repr__(self): return repr(self.data)
    def __int__(self): return int(self.data)
    def __long__(self): return long(self.data)
    def __float__(self): return float(self.data)
    def __complex__(self): return complex(self.data)
    def __hash__(self): return hash(self.data)

    def __cmp__(self, string):
        if isinstance(string, UserString):
            return cmp(self.data, string.data)
        else:
            return cmp(self.data, string)
    def __contains__(self, char):
        return char in self.data

    def __len__(self): return len(self.data)
    def __getitem__(self, index): return self.__class__(self.data[index])
    def __getslice__(self, start, end):
        start = max(start, 0); end = max(end, 0)
        return self.__class__(self.data[start:end])

    def __add__(self, other):
        if isinstance(other, UserString):
            return self.__class__(self.data + other.data)
        elif isinstance(other, basestring):
            return self.__class__(self.data + other)
        else:
            return self.__class__(self.data + str(other))
    def __radd__(self, other):
        if isinstance(other, basestring):
            return self.__class__(other + self.data)
        else:
            return self.__class__(str(other) + self.data)
    def __mul__(self, n):
        return self.__class__(self.data*n)
    __rmul__ = __mul__
    def __mod__(self, args):
        return self.__class__(self.data % args)

    # the following methods are defined in alphabetical order:
    def capitalize(self): return self.__class__(self.data.capitalize())
    def center(self, width, *args):
        return self.__class__(self.data.center(width, *args))
    def count(self, sub, start=0, end=sys.maxint):
        return self.data.count(sub, start, end)
    def decode(self, encoding=None, errors=None): # XXX improve this?
        if encoding:
            if errors:
                return self.__class__(self.data.decode(encoding, errors))
            else:
                return self.__class__(self.data.decode(encoding))
        else:
            return self.__class__(self.data.decode())
    def encode(self, encoding=None, errors=None): # XXX improve this?
        if encoding:
            if errors:
                return self.__class__(self.data.encode(encoding, errors))
            else:
                return self.__class__(self.data.encode(encoding))
        else:
            return self.__class__(self.data.encode())
    def endswith(self, suffix, start=0, end=sys.maxint):
        return self.data.endswith(suffix, start, end)
    def expandtabs(self, tabsize=8):
        return self.__class__(self.data.expandtabs(tabsize))
    def find(self, sub, start=0, end=sys.maxint):
        return self.data.find(sub, start, end)
    def index(self, sub, start=0, end=sys.maxint):
        return self.data.index(sub, start, end)
    def isalpha(self): return self.data.isalpha()
    def isalnum(self): return self.data.isalnum()
    def isdecimal(self): return self.data.isdecimal()
    def isdigit(self): return self.data.isdigit()
    def islower(self): return self.data.islower()
    def isnumeric(self): return self.data.isnumeric()
    def isspace(self): return self.data.isspace()
    def istitle(self): return self.data.istitle()
    def isupper(self): return self.data.isupper()
    def join(self, seq): return self.data.join(seq)
    def ljust(self, width, *args):
        return self.__class__(self.data.ljust(width, *args))
    def lower(self): return self.__class__(self.data.lower())
    def lstrip(self, chars=None): return self.__class__(self.data.lstrip(chars))
    def partition(self, sep):
        return self.data.partition(sep)
    def replace(self, old, new, maxsplit=-1):
        return self.__class__(self.data.replace(old, new, maxsplit))
    def rfind(self, sub, start=0, end=sys.maxint):
        return self.data.rfind(sub, start, end)
    def rindex(self, sub, start=0, end=sys.maxint):
        return self.data.rindex(sub, start, end)
    def rjust(self, width, *args):
        return self.__class__(self.data.rjust(width, *args))
    def rpartition(self, sep):
        return self.data.rpartition(sep)
    def rstrip(self, chars=None): return self.__class__(self.data.rstrip(chars))
    def split(self, sep=None, maxsplit=-1):
        return self.data.split(sep, maxsplit)
    def rsplit(self, sep=None, maxsplit=-1):
        return self.data.rsplit(sep, maxsplit)
    def splitlines(self, keepends=0): return self.data.splitlines(keepends)
    def startswith(self, prefix, start=0, end=sys.maxint):
        return self.data.startswith(prefix, start, end)
    def strip(self, chars=None): return self.__class__(self.data.strip(chars))
    def swapcase(self): return self.__class__(self.data.swapcase())
    def title(self): return self.__class__(self.data.title())
    def translate(self, *args):
        return self.__class__(self.data.translate(*args))
    def upper(self): return self.__class__(self.data.upper())
    def zfill(self, width): return self.__class__(self.data.zfill(width))

class MutableString(UserString):
    """mutable string objects

    Python strings are immutable objects.  This has the advantage, that
    strings may be used as dictionary keys.  If this property isn't needed
    and you insist on changing string values in place instead, you may cheat
    and use MutableString.

    But the purpose of this class is an educational one: to prevent
    people from inventing their own mutable string class derived
    from UserString and than forget thereby to remove (override) the
    __hash__ method inherited from UserString.  This would lead to
    errors that would be very hard to track down.

    A faster and better solution is to rewrite your program using lists."""
    def __init__(self, string=""):
        self.data = string
    def __hash__(self):
        raise TypeError("unhashable type (it is mutable)")
    def __setitem__(self, index, sub):
        if index < 0:
            index += len(self.data)
        if index < 0 or index >= len(self.data): raise IndexError
        self.data = self.data[:index] + sub + self.data[index+1:]
    def __delitem__(self, index):
        if index < 0:
            index += len(self.data)
        if index < 0 or index >= len(self.data): raise IndexError
        self.data = self.data[:index] + self.data[index+1:]
    def __setslice__(self, start, end, sub):
        start = max(start, 0); end = max(end, 0)
        if isinstance(sub, UserString):
            self.data = self.data[:start]+sub.data+self.data[end:]
        elif isinstance(sub, basestring):
            self.data = self.data[:start]+sub+self.data[end:]
        else:
            self.data =  self.data[:start]+str(sub)+self.data[end:]
    def __delslice__(self, start, end):
        start = max(start, 0); end = max(end, 0)
        self.data = self.data[:start] + self.data[end:]
    def immutable(self):
        return UserString(self.data)
    def __iadd__(self, other):
        if isinstance(other, UserString):
            self.data += other.data
        elif isinstance(other, basestring):
            self.data += other
        else:
            self.data += str(other)
        return self
    def __imul__(self, n):
        self.data *= n
        return self

class String(MutableString, Union):

    _fields_ = [('raw', POINTER(c_char)),
                ('data', c_char_p)]

    def __init__(self, obj=""):
        if isinstance(obj, (str, unicode, UserString)):
            self.data = str(obj)
        else:
            self.raw = obj

    def __len__(self):
        return self.data and len(self.data) or 0

    def from_param(cls, obj):
        # Convert None or 0
        if obj is None or obj == 0:
            return cls(POINTER(c_char)())

        # Convert from String
        elif isinstance(obj, String):
            return obj

        # Convert from str
        elif isinstance(obj, str):
            return cls(obj)

        # Convert from c_char_p
        elif isinstance(obj, c_char_p):
            return obj

        # Convert from POINTER(c_char)
        elif isinstance(obj, POINTER(c_char)):
            return obj

        # Convert from raw pointer
        elif isinstance(obj, int):
            return cls(cast(obj, POINTER(c_char)))

        # Convert from object
        else:
            return String.from_param(obj._as_parameter_)
    from_param = classmethod(from_param)

def ReturnString(obj, func=None, arguments=None):
    return String.from_param(obj)

# As of ctypes 1.0, ctypes does not support custom error-checking
# functions on callbacks, nor does it support custom datatypes on
# callbacks, so we must ensure that all callbacks return
# primitive datatypes.
#
# Non-primitive return values wrapped with UNCHECKED won't be
# typechecked, and will be converted to c_void_p.
def UNCHECKED(type):
    if (hasattr(type, "_type_") and isinstance(type._type_, str)
        and type._type_ != "P"):
        return type
    else:
        return c_void_p

# ctypes doesn't have direct support for variadic functions, so we have to write
# our own wrapper class
class _variadic_function(object):
    def __init__(self,func,restype,argtypes):
        self.func=func
        self.func.restype=restype
        self.argtypes=argtypes
    def _as_parameter_(self):
        # So we can pass this variadic function as a function pointer
        return self.func
    def __call__(self,*args):
        fixed_args=[]
        i=0
        for argtype in self.argtypes:
            # Typecheck what we can
            fixed_args.append(argtype.from_param(args[i]))
            i+=1
        return self.func(*fixed_args+list(args[i:]))

# End preamble

_libs = {}
_libdirs = ['.']

# Begin loader

# ----------------------------------------------------------------------------
# Copyright (c) 2008 David James
# Copyright (c) 2006-2008 Alex Holkner
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in
#    the documentation and/or other materials provided with the
#    distribution.
#  * Neither the name of pyglet nor the names of its
#    contributors may be used to endorse or promote products
#    derived from this software without specific prior written
#    permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
# ----------------------------------------------------------------------------

import os.path, re, sys, glob
import ctypes
import ctypes.util

def _environ_path(name):
    if name in os.environ:
        return os.environ[name].split(":")
    else:
        return []

class LibraryLoader(object):
    def __init__(self):
        self.other_dirs=[]

    def load_library(self,libname):
        """Given the name of a library, load it."""
        paths = self.getpaths(libname)

        for path in paths:
            if os.path.exists(path):
                return self.load(path)

        raise ImportError("%s not found." % libname)

    def load(self,path):
        """Given a path to a library, load it."""
        try:
            # Darwin requires dlopen to be called with mode RTLD_GLOBAL instead
            # of the default RTLD_LOCAL.  Without this, you end up with
            # libraries not being loadable, resulting in "Symbol not found"
            # errors
            if sys.platform == 'darwin':
                return ctypes.CDLL(path, ctypes.RTLD_GLOBAL)
            else:
                return ctypes.cdll.LoadLibrary(path)
        except OSError,e:
            raise ImportError(e)

    def getpaths(self,libname):
        """Return a list of paths where the library might be found."""
        if os.path.isabs(libname):
            yield libname
        else:
            # FIXME / TODO return '.' and os.path.dirname(__file__)
            for path in self.getplatformpaths(libname):
                yield path

            path = ctypes.util.find_library(libname)
            if path: yield path

    def getplatformpaths(self, libname):
        return []

# Darwin (Mac OS X)

class DarwinLibraryLoader(LibraryLoader):
    name_formats = ["lib%s.dylib", "lib%s.so", "lib%s.bundle", "%s.dylib",
                "%s.so", "%s.bundle", "%s"]

    def getplatformpaths(self,libname):
        if os.path.pathsep in libname:
            names = [libname]
        else:
            names = [format % libname for format in self.name_formats]

        for dir in self.getdirs(libname):
            for name in names:
                yield os.path.join(dir,name)

    def getdirs(self,libname):
        '''Implements the dylib search as specified in Apple documentation:

        http://developer.apple.com/documentation/DeveloperTools/Conceptual/
            DynamicLibraries/Articles/DynamicLibraryUsageGuidelines.html

        Before commencing the standard search, the method first checks
        the bundle's ``Frameworks`` directory if the application is running
        within a bundle (OS X .app).
        '''

        dyld_fallback_library_path = _environ_path("DYLD_FALLBACK_LIBRARY_PATH")
        if not dyld_fallback_library_path:
            dyld_fallback_library_path = [os.path.expanduser('~/lib'),
                                          '/usr/local/lib', '/usr/lib']

        dirs = []

        if '/' in libname:
            dirs.extend(_environ_path("DYLD_LIBRARY_PATH"))
        else:
            dirs.extend(_environ_path("LD_LIBRARY_PATH"))
            dirs.extend(_environ_path("DYLD_LIBRARY_PATH"))

        dirs.extend(self.other_dirs)
        dirs.append(".")
        dirs.append(os.path.dirname(__file__))

        if hasattr(sys, 'frozen') and sys.frozen == 'macosx_app':
            dirs.append(os.path.join(
                os.environ['RESOURCEPATH'],
                '..',
                'Frameworks'))

        dirs.extend(dyld_fallback_library_path)

        return dirs

# Posix

class PosixLibraryLoader(LibraryLoader):
    _ld_so_cache = None

    def _create_ld_so_cache(self):
        # Recreate search path followed by ld.so.  This is going to be
        # slow to build, and incorrect (ld.so uses ld.so.cache, which may
        # not be up-to-date).  Used only as fallback for distros without
        # /sbin/ldconfig.
        #
        # We assume the DT_RPATH and DT_RUNPATH binary sections are omitted.

        directories = []
        for name in ("LD_LIBRARY_PATH",
                     "SHLIB_PATH", # HPUX
                     "LIBPATH", # OS/2, AIX
                     "LIBRARY_PATH", # BE/OS
                    ):
            if name in os.environ:
                directories.extend(os.environ[name].split(os.pathsep))
        directories.extend(self.other_dirs)
        directories.append(".")
        directories.append(os.path.dirname(__file__))

        try: directories.extend([dir.strip() for dir in open('/etc/ld.so.conf')])
        except IOError: pass

        directories.extend(['/lib', '/usr/lib', '/lib64', '/usr/lib64'])

        cache = {}
        lib_re = re.compile(r'lib(.*)\.s[ol]')
        ext_re = re.compile(r'\.s[ol]$')
        for dir in directories:
            try:
                for path in glob.glob("%s/*.s[ol]*" % dir):
                    file = os.path.basename(path)

                    # Index by filename
                    if file not in cache:
                        cache[file] = path

                    # Index by library name
                    match = lib_re.match(file)
                    if match:
                        library = match.group(1)
                        if library not in cache:
                            cache[library] = path
            except OSError:
                pass

        self._ld_so_cache = cache

    def getplatformpaths(self, libname):
        if self._ld_so_cache is None:
            self._create_ld_so_cache()

        result = self._ld_so_cache.get(libname)
        if result: yield result

        path = ctypes.util.find_library(libname)
        if path: yield os.path.join("/lib",path)

# Windows

class _WindowsLibrary(object):
    def __init__(self, path):
        self.cdll = ctypes.cdll.LoadLibrary(path)
        self.windll = ctypes.windll.LoadLibrary(path)

    def __getattr__(self, name):
        try: return getattr(self.cdll,name)
        except AttributeError:
            try: return getattr(self.windll,name)
            except AttributeError:
                raise

class WindowsLibraryLoader(LibraryLoader):
    name_formats = ["%s.dll", "lib%s.dll", "%slib.dll"]

    def load_library(self, libname):
        try:
            result = LibraryLoader.load_library(self, libname)
        except ImportError:
            result = None
            if os.path.sep not in libname:
                for name in self.name_formats:
                    try:
                        result = getattr(ctypes.cdll, name % libname)
                        if result:
                            break
                    except WindowsError:
                        result = None
            if result is None:
                try:
                    result = getattr(ctypes.cdll, libname)
                except WindowsError:
                    result = None
            if result is None:
                raise ImportError("%s not found." % libname)
        return result

    def load(self, path):
        return _WindowsLibrary(path)

    def getplatformpaths(self, libname):
        if os.path.sep not in libname:
            for name in self.name_formats:
                dll_in_current_dir = os.path.abspath(name % libname)
                if os.path.exists(dll_in_current_dir):
                    yield dll_in_current_dir
                path = ctypes.util.find_library(name % libname)
                if path:
                    yield path

# Platform switching

# If your value of sys.platform does not appear in this dict, please contact
# the Ctypesgen maintainers.

loaderclass = {
    "darwin":   DarwinLibraryLoader,
    "cygwin":   WindowsLibraryLoader,
    "win32":    WindowsLibraryLoader
}

loader = loaderclass.get(sys.platform, PosixLibraryLoader)()

def add_library_search_dirs(other_dirs):
    loader.other_dirs = other_dirs

load_library = loader.load_library

del loaderclass

# End loader

add_library_search_dirs(['.'])

# Begin libraries

_libs["qdis"] = load_library("qdis")

# 1 libraries
# End libraries

# No modules

enum_anon_20 = c_int # /store/orion/upstream/bitblaze/qemu/python/disass.h: 15

DIS_OK = 0 # /store/orion/upstream/bitblaze/qemu/python/disass.h: 15

DIS_ERR_OUT_OF_BOUNDS_ACCESS = 1 # /store/orion/upstream/bitblaze/qemu/python/disass.h: 15

DIS_ERR_BUFFER_TOO_SMALL = 2 # /store/orion/upstream/bitblaze/qemu/python/disass.h: 15

DIS_ERR_NULLPOINTER = 3 # /store/orion/upstream/bitblaze/qemu/python/disass.h: 15

DIS_ERR_ALIGNMENT = 4 # /store/orion/upstream/bitblaze/qemu/python/disass.h: 15

DisStatus = enum_anon_20 # /store/orion/upstream/bitblaze/qemu/python/disass.h: 15

enum_anon_21 = c_int # /store/orion/upstream/bitblaze/qemu/python/disass.h: 44

DIS_TGT_8BIT = 0 # /store/orion/upstream/bitblaze/qemu/python/disass.h: 44

DIS_TGT_16BIT = 4096 # /store/orion/upstream/bitblaze/qemu/python/disass.h: 44

DIS_TGT_32BIT = 8192 # /store/orion/upstream/bitblaze/qemu/python/disass.h: 44

DIS_TGT_64BIT = 12288 # /store/orion/upstream/bitblaze/qemu/python/disass.h: 44

DIS_TGT_ARM = (0 | DIS_TGT_32BIT) # /store/orion/upstream/bitblaze/qemu/python/disass.h: 44

DIS_TGT_X86_32 = (1 | DIS_TGT_32BIT) # /store/orion/upstream/bitblaze/qemu/python/disass.h: 44

DIS_TGT_X86_64 = (1 | DIS_TGT_64BIT) # /store/orion/upstream/bitblaze/qemu/python/disass.h: 44

DIS_TGT_ALPHA = (2 | DIS_TGT_64BIT) # /store/orion/upstream/bitblaze/qemu/python/disass.h: 44

DIS_TGT_CRIS = (3 | DIS_TGT_32BIT) # /store/orion/upstream/bitblaze/qemu/python/disass.h: 44

DIS_TGT_LM32 = (4 | DIS_TGT_32BIT) # /store/orion/upstream/bitblaze/qemu/python/disass.h: 44

DIS_TGT_M68K = (5 | DIS_TGT_32BIT) # /store/orion/upstream/bitblaze/qemu/python/disass.h: 44

DIS_TGT_MICROBLAZE = (6 | DIS_TGT_32BIT) # /store/orion/upstream/bitblaze/qemu/python/disass.h: 44

DIS_TGT_MIPS_32 = (7 | DIS_TGT_32BIT) # /store/orion/upstream/bitblaze/qemu/python/disass.h: 44

DIS_TGT_MIPS_64 = (7 | DIS_TGT_64BIT) # /store/orion/upstream/bitblaze/qemu/python/disass.h: 44

DIS_TGT_OPENRISC = (8 | DIS_TGT_32BIT) # /store/orion/upstream/bitblaze/qemu/python/disass.h: 44

DIS_TGT_PPC_32 = (9 | DIS_TGT_32BIT) # /store/orion/upstream/bitblaze/qemu/python/disass.h: 44

DIS_TGT_PPC_64 = (9 | DIS_TGT_64BIT) # /store/orion/upstream/bitblaze/qemu/python/disass.h: 44

DIS_TGT_S390X = (10 | DIS_TGT_64BIT) # /store/orion/upstream/bitblaze/qemu/python/disass.h: 44

DIS_TGT_SH4 = (11 | DIS_TGT_32BIT) # /store/orion/upstream/bitblaze/qemu/python/disass.h: 44

DIS_TGT_SPARC_32 = (12 | DIS_TGT_32BIT) # /store/orion/upstream/bitblaze/qemu/python/disass.h: 44

DIS_TGT_SPARC_64 = (12 | DIS_TGT_64BIT) # /store/orion/upstream/bitblaze/qemu/python/disass.h: 44

DIS_TGT_UNICORE32 = (13 | DIS_TGT_32BIT) # /store/orion/upstream/bitblaze/qemu/python/disass.h: 44

DIS_TGT_XTENSA = (14 | DIS_TGT_32BIT) # /store/orion/upstream/bitblaze/qemu/python/disass.h: 44

DisTarget = enum_anon_21 # /store/orion/upstream/bitblaze/qemu/python/disass.h: 44

enum_anon_22 = c_int # /store/orion/upstream/bitblaze/qemu/python/disass.h: 84

DIS_FEATURE_END = 0 # /store/orion/upstream/bitblaze/qemu/python/disass.h: 84

DIS_ARM_FEATURE_VFP = (DIS_FEATURE_END + 1) # /store/orion/upstream/bitblaze/qemu/python/disass.h: 84

DIS_ARM_FEATURE_AUXCR = (DIS_ARM_FEATURE_VFP + 1) # /store/orion/upstream/bitblaze/qemu/python/disass.h: 84

DIS_ARM_FEATURE_XSCALE = (DIS_ARM_FEATURE_AUXCR + 1) # /store/orion/upstream/bitblaze/qemu/python/disass.h: 84

DIS_ARM_FEATURE_IWMMXT = (DIS_ARM_FEATURE_XSCALE + 1) # /store/orion/upstream/bitblaze/qemu/python/disass.h: 84

DIS_ARM_FEATURE_V6 = (DIS_ARM_FEATURE_IWMMXT + 1) # /store/orion/upstream/bitblaze/qemu/python/disass.h: 84

DIS_ARM_FEATURE_V6K = (DIS_ARM_FEATURE_V6 + 1) # /store/orion/upstream/bitblaze/qemu/python/disass.h: 84

DIS_ARM_FEATURE_V7 = (DIS_ARM_FEATURE_V6K + 1) # /store/orion/upstream/bitblaze/qemu/python/disass.h: 84

DIS_ARM_FEATURE_THUMB2 = (DIS_ARM_FEATURE_V7 + 1) # /store/orion/upstream/bitblaze/qemu/python/disass.h: 84

DIS_ARM_FEATURE_MPU = (DIS_ARM_FEATURE_THUMB2 + 1) # /store/orion/upstream/bitblaze/qemu/python/disass.h: 84

DIS_ARM_FEATURE_VFP3 = (DIS_ARM_FEATURE_MPU + 1) # /store/orion/upstream/bitblaze/qemu/python/disass.h: 84

DIS_ARM_FEATURE_VFP_FP16 = (DIS_ARM_FEATURE_VFP3 + 1) # /store/orion/upstream/bitblaze/qemu/python/disass.h: 84

DIS_ARM_FEATURE_NEON = (DIS_ARM_FEATURE_VFP_FP16 + 1) # /store/orion/upstream/bitblaze/qemu/python/disass.h: 84

DIS_ARM_FEATURE_THUMB_DIV = (DIS_ARM_FEATURE_NEON + 1) # /store/orion/upstream/bitblaze/qemu/python/disass.h: 84

DIS_ARM_FEATURE_M = (DIS_ARM_FEATURE_THUMB_DIV + 1) # /store/orion/upstream/bitblaze/qemu/python/disass.h: 84

DIS_ARM_FEATURE_OMAPCP = (DIS_ARM_FEATURE_M + 1) # /store/orion/upstream/bitblaze/qemu/python/disass.h: 84

DIS_ARM_FEATURE_THUMB2EE = (DIS_ARM_FEATURE_OMAPCP + 1) # /store/orion/upstream/bitblaze/qemu/python/disass.h: 84

DIS_ARM_FEATURE_V7MP = (DIS_ARM_FEATURE_THUMB2EE + 1) # /store/orion/upstream/bitblaze/qemu/python/disass.h: 84

DIS_ARM_FEATURE_V4T = (DIS_ARM_FEATURE_V7MP + 1) # /store/orion/upstream/bitblaze/qemu/python/disass.h: 84

DIS_ARM_FEATURE_V5 = (DIS_ARM_FEATURE_V4T + 1) # /store/orion/upstream/bitblaze/qemu/python/disass.h: 84

DIS_ARM_FEATURE_STRONGARM = (DIS_ARM_FEATURE_V5 + 1) # /store/orion/upstream/bitblaze/qemu/python/disass.h: 84

DIS_ARM_FEATURE_VAPA = (DIS_ARM_FEATURE_STRONGARM + 1) # /store/orion/upstream/bitblaze/qemu/python/disass.h: 84

DIS_ARM_FEATURE_ARM_DIV = (DIS_ARM_FEATURE_VAPA + 1) # /store/orion/upstream/bitblaze/qemu/python/disass.h: 84

DIS_ARM_FEATURE_VFP4 = (DIS_ARM_FEATURE_ARM_DIV + 1) # /store/orion/upstream/bitblaze/qemu/python/disass.h: 84

DIS_ARM_FEATURE_GENERIC_TIMER = (DIS_ARM_FEATURE_VFP4 + 1) # /store/orion/upstream/bitblaze/qemu/python/disass.h: 84

DIS_ARM_FEATURE_MVFR = (DIS_ARM_FEATURE_GENERIC_TIMER + 1) # /store/orion/upstream/bitblaze/qemu/python/disass.h: 84

DIS_ARM_FEATURE_DUMMY_C15_REGS = (DIS_ARM_FEATURE_MVFR + 1) # /store/orion/upstream/bitblaze/qemu/python/disass.h: 84

DIS_ARM_FEATURE_CACHE_TEST_CLEAN = (DIS_ARM_FEATURE_DUMMY_C15_REGS + 1) # /store/orion/upstream/bitblaze/qemu/python/disass.h: 84

DIS_ARM_FEATURE_CACHE_DIRTY_REG = (DIS_ARM_FEATURE_CACHE_TEST_CLEAN + 1) # /store/orion/upstream/bitblaze/qemu/python/disass.h: 84

DIS_ARM_FEATURE_CACHE_BLOCK_OPS = (DIS_ARM_FEATURE_CACHE_DIRTY_REG + 1) # /store/orion/upstream/bitblaze/qemu/python/disass.h: 84

DIS_ARM_FEATURE_MPIDR = (DIS_ARM_FEATURE_CACHE_BLOCK_OPS + 1) # /store/orion/upstream/bitblaze/qemu/python/disass.h: 84

DIS_ARM_FEATURE_PXN = (DIS_ARM_FEATURE_MPIDR + 1) # /store/orion/upstream/bitblaze/qemu/python/disass.h: 84

DIS_ARM_FEATURE_LPAE = (DIS_ARM_FEATURE_PXN + 1) # /store/orion/upstream/bitblaze/qemu/python/disass.h: 84

DisCPUFeature = enum_anon_22 # /store/orion/upstream/bitblaze/qemu/python/disass.h: 84

# /store/orion/upstream/bitblaze/qemu/python/disass.h: 150
class struct_Disassembler_(Structure):
    pass

Disassembler = struct_Disassembler_ # /store/orion/upstream/bitblaze/qemu/python/disass.h: 150

enum_anon_23 = c_int # /store/orion/upstream/bitblaze/qemu/python/disass.h: 157

DIS_OPTIMIZE_NONE = 0 # /store/orion/upstream/bitblaze/qemu/python/disass.h: 157

DIS_OPTIMIZE_LIVENESS = 1 # /store/orion/upstream/bitblaze/qemu/python/disass.h: 157

DIS_OPTIMIZE_GENERAL = 2 # /store/orion/upstream/bitblaze/qemu/python/disass.h: 157

DIS_OPTIMIZE_FULL = (DIS_OPTIMIZE_LIVENESS | DIS_OPTIMIZE_GENERAL) # /store/orion/upstream/bitblaze/qemu/python/disass.h: 157

DisOptimizeFlags = enum_anon_23 # /store/orion/upstream/bitblaze/qemu/python/disass.h: 157

enum_anon_24 = c_int # /store/orion/upstream/bitblaze/qemu/python/disass.h: 164

DIS_SYM_LOCAL = 1 # /store/orion/upstream/bitblaze/qemu/python/disass.h: 164

DIS_SYM_TEMP = 2 # /store/orion/upstream/bitblaze/qemu/python/disass.h: 164

DisSymType = enum_anon_24 # /store/orion/upstream/bitblaze/qemu/python/disass.h: 164

enum_anon_25 = c_int # /store/orion/upstream/bitblaze/qemu/python/disass.h: 174

DIS_SIZE_UNKNOWN = 0 # /store/orion/upstream/bitblaze/qemu/python/disass.h: 174

DIS_SIZE_8 = 8 # /store/orion/upstream/bitblaze/qemu/python/disass.h: 174

DIS_SIZE_16 = 16 # /store/orion/upstream/bitblaze/qemu/python/disass.h: 174

DIS_SIZE_32 = 32 # /store/orion/upstream/bitblaze/qemu/python/disass.h: 174

DIS_SIZE_64 = 64 # /store/orion/upstream/bitblaze/qemu/python/disass.h: 174

DisBitsize = enum_anon_25 # /store/orion/upstream/bitblaze/qemu/python/disass.h: 174

# /store/orion/upstream/bitblaze/qemu/python/disass.h: 181
class struct_anon_26(Structure):
    pass

struct_anon_26.__slots__ = [
    'type',
    'size',
]
struct_anon_26._fields_ = [
    ('type', DisSymType),
    ('size', DisBitsize),
]

DisSym = struct_anon_26 # /store/orion/upstream/bitblaze/qemu/python/disass.h: 181

enum_anon_27 = c_int # /store/orion/upstream/bitblaze/qemu/python/disass.h: 201

DIS_COND_NEVER = (((0 | 0) | 0) | 0) # /store/orion/upstream/bitblaze/qemu/python/disass.h: 201

DIS_COND_ALWAYS = (((0 | 0) | 0) | 1) # /store/orion/upstream/bitblaze/qemu/python/disass.h: 201

DIS_COND_EQ = (((8 | 0) | 0) | 0) # /store/orion/upstream/bitblaze/qemu/python/disass.h: 201

DIS_COND_NE = (((8 | 0) | 0) | 1) # /store/orion/upstream/bitblaze/qemu/python/disass.h: 201

DIS_COND_LT = (((0 | 0) | 2) | 0) # /store/orion/upstream/bitblaze/qemu/python/disass.h: 201

DIS_COND_GE = (((0 | 0) | 2) | 1) # /store/orion/upstream/bitblaze/qemu/python/disass.h: 201

DIS_COND_LE = (((8 | 0) | 2) | 0) # /store/orion/upstream/bitblaze/qemu/python/disass.h: 201

DIS_COND_GT = (((8 | 0) | 2) | 1) # /store/orion/upstream/bitblaze/qemu/python/disass.h: 201

DIS_COND_LTU = (((0 | 4) | 0) | 0) # /store/orion/upstream/bitblaze/qemu/python/disass.h: 201

DIS_COND_GEU = (((0 | 4) | 0) | 1) # /store/orion/upstream/bitblaze/qemu/python/disass.h: 201

DIS_COND_LEU = (((8 | 4) | 0) | 0) # /store/orion/upstream/bitblaze/qemu/python/disass.h: 201

DIS_COND_GTU = (((8 | 4) | 0) | 1) # /store/orion/upstream/bitblaze/qemu/python/disass.h: 201

DisConditionCode = enum_anon_27 # /store/orion/upstream/bitblaze/qemu/python/disass.h: 201

# /store/orion/upstream/bitblaze/qemu/python/disass.h: 207
class struct_anon_28(Structure):
    pass

struct_anon_28.__slots__ = [
    'opcode',
    'args',
]
struct_anon_28._fields_ = [
    ('opcode', c_uint16),
    ('args', c_uint8),
]

DisOp = struct_anon_28 # /store/orion/upstream/bitblaze/qemu/python/disass.h: 207

enum_anon_29 = c_int # /store/orion/upstream/bitblaze/qemu/python/disass.h: 222

DIS_ARG_GLOBAL = 1 # /store/orion/upstream/bitblaze/qemu/python/disass.h: 222

DIS_ARG_TEMP = 2 # /store/orion/upstream/bitblaze/qemu/python/disass.h: 222

DIS_ARG_COND = 8 # /store/orion/upstream/bitblaze/qemu/python/disass.h: 222

DIS_ARG_DUMMY = 16 # /store/orion/upstream/bitblaze/qemu/python/disass.h: 222

DIS_ARG_CALLFLAGS = 64 # /store/orion/upstream/bitblaze/qemu/python/disass.h: 222

DIS_ARG_CALLTARGET = 128 # /store/orion/upstream/bitblaze/qemu/python/disass.h: 222

DIS_ARG_INPUT = 256 # /store/orion/upstream/bitblaze/qemu/python/disass.h: 222

DIS_ARG_OUTPUT = 512 # /store/orion/upstream/bitblaze/qemu/python/disass.h: 222

DIS_ARG_CONSTANT = 1024 # /store/orion/upstream/bitblaze/qemu/python/disass.h: 222

DisArgFlags = enum_anon_29 # /store/orion/upstream/bitblaze/qemu/python/disass.h: 222

# /store/orion/upstream/bitblaze/qemu/python/disass.h: 230
class struct_anon_30(Structure):
    pass

struct_anon_30.__slots__ = [
    'value',
    'size',
    'flags',
]
struct_anon_30._fields_ = [
    ('value', c_size_t),
    ('size', DisBitsize),
    ('flags', c_uint16),
]

DisArg = struct_anon_30 # /store/orion/upstream/bitblaze/qemu/python/disass.h: 230

enum_anon_31 = c_int # /store/orion/upstream/bitblaze/qemu/python/disass.h: 359

DIS_OP_END = 0 # /store/orion/upstream/bitblaze/qemu/python/disass.h: 359

DIS_OP_NOP = 1 # /store/orion/upstream/bitblaze/qemu/python/disass.h: 359

DIS_OP_NOP1 = 2 # /store/orion/upstream/bitblaze/qemu/python/disass.h: 359

DIS_OP_NOP2 = 3 # /store/orion/upstream/bitblaze/qemu/python/disass.h: 359

DIS_OP_NOP3 = 4 # /store/orion/upstream/bitblaze/qemu/python/disass.h: 359

DIS_OP_NOPN = 5 # /store/orion/upstream/bitblaze/qemu/python/disass.h: 359

DIS_OP_DISCARD = 6 # /store/orion/upstream/bitblaze/qemu/python/disass.h: 359

DIS_OP_SET_LABEL = 7 # /store/orion/upstream/bitblaze/qemu/python/disass.h: 359

DIS_OP_CALL = 8 # /store/orion/upstream/bitblaze/qemu/python/disass.h: 359

DIS_OP_BR = 9 # /store/orion/upstream/bitblaze/qemu/python/disass.h: 359

DIS_OP_MOV_I32 = 10 # /store/orion/upstream/bitblaze/qemu/python/disass.h: 359

DIS_OP_MOVI_I32 = 11 # /store/orion/upstream/bitblaze/qemu/python/disass.h: 359

DIS_OP_SETCOND_I32 = 12 # /store/orion/upstream/bitblaze/qemu/python/disass.h: 359

DIS_OP_MOVCOND_I32 = 13 # /store/orion/upstream/bitblaze/qemu/python/disass.h: 359

DIS_OP_LD8U_I32 = 14 # /store/orion/upstream/bitblaze/qemu/python/disass.h: 359

DIS_OP_LD8S_I32 = 15 # /store/orion/upstream/bitblaze/qemu/python/disass.h: 359

DIS_OP_LD16U_I32 = 16 # /store/orion/upstream/bitblaze/qemu/python/disass.h: 359

DIS_OP_LD16S_I32 = 17 # /store/orion/upstream/bitblaze/qemu/python/disass.h: 359

DIS_OP_LD_I32 = 18 # /store/orion/upstream/bitblaze/qemu/python/disass.h: 359

DIS_OP_ST8_I32 = 19 # /store/orion/upstream/bitblaze/qemu/python/disass.h: 359

DIS_OP_ST16_I32 = 20 # /store/orion/upstream/bitblaze/qemu/python/disass.h: 359

DIS_OP_ST_I32 = 21 # /store/orion/upstream/bitblaze/qemu/python/disass.h: 359

DIS_OP_ADD_I32 = 22 # /store/orion/upstream/bitblaze/qemu/python/disass.h: 359

DIS_OP_SUB_I32 = 23 # /store/orion/upstream/bitblaze/qemu/python/disass.h: 359

DIS_OP_MUL_I32 = 24 # /store/orion/upstream/bitblaze/qemu/python/disass.h: 359

DIS_OP_DIV_I32 = 25 # /store/orion/upstream/bitblaze/qemu/python/disass.h: 359

DIS_OP_DIVU_I32 = 26 # /store/orion/upstream/bitblaze/qemu/python/disass.h: 359

DIS_OP_REM_I32 = 27 # /store/orion/upstream/bitblaze/qemu/python/disass.h: 359

DIS_OP_REMU_I32 = 28 # /store/orion/upstream/bitblaze/qemu/python/disass.h: 359

DIS_OP_DIV2_I32 = 29 # /store/orion/upstream/bitblaze/qemu/python/disass.h: 359

DIS_OP_DIVU2_I32 = 30 # /store/orion/upstream/bitblaze/qemu/python/disass.h: 359

DIS_OP_AND_I32 = 31 # /store/orion/upstream/bitblaze/qemu/python/disass.h: 359

DIS_OP_OR_I32 = 32 # /store/orion/upstream/bitblaze/qemu/python/disass.h: 359

DIS_OP_XOR_I32 = 33 # /store/orion/upstream/bitblaze/qemu/python/disass.h: 359

DIS_OP_SHL_I32 = 34 # /store/orion/upstream/bitblaze/qemu/python/disass.h: 359

DIS_OP_SHR_I32 = 35 # /store/orion/upstream/bitblaze/qemu/python/disass.h: 359

DIS_OP_SAR_I32 = 36 # /store/orion/upstream/bitblaze/qemu/python/disass.h: 359

DIS_OP_ROTL_I32 = 37 # /store/orion/upstream/bitblaze/qemu/python/disass.h: 359

DIS_OP_ROTR_I32 = 38 # /store/orion/upstream/bitblaze/qemu/python/disass.h: 359

DIS_OP_DEPOSIT_I32 = 39 # /store/orion/upstream/bitblaze/qemu/python/disass.h: 359

DIS_OP_BRCOND_I32 = 40 # /store/orion/upstream/bitblaze/qemu/python/disass.h: 359

DIS_OP_ADD2_I32 = 41 # /store/orion/upstream/bitblaze/qemu/python/disass.h: 359

DIS_OP_SUB2_I32 = 42 # /store/orion/upstream/bitblaze/qemu/python/disass.h: 359

DIS_OP_BRCOND2_I32 = 43 # /store/orion/upstream/bitblaze/qemu/python/disass.h: 359

DIS_OP_MULU2_I32 = 44 # /store/orion/upstream/bitblaze/qemu/python/disass.h: 359

DIS_OP_SETCOND2_I32 = 45 # /store/orion/upstream/bitblaze/qemu/python/disass.h: 359

DIS_OP_EXT8S_I32 = 46 # /store/orion/upstream/bitblaze/qemu/python/disass.h: 359

DIS_OP_EXT16S_I32 = 47 # /store/orion/upstream/bitblaze/qemu/python/disass.h: 359

DIS_OP_EXT8U_I32 = 48 # /store/orion/upstream/bitblaze/qemu/python/disass.h: 359

DIS_OP_EXT16U_I32 = 49 # /store/orion/upstream/bitblaze/qemu/python/disass.h: 359

DIS_OP_BSWAP16_I32 = 50 # /store/orion/upstream/bitblaze/qemu/python/disass.h: 359

DIS_OP_BSWAP32_I32 = 51 # /store/orion/upstream/bitblaze/qemu/python/disass.h: 359

DIS_OP_NOT_I32 = 52 # /store/orion/upstream/bitblaze/qemu/python/disass.h: 359

DIS_OP_NEG_I32 = 53 # /store/orion/upstream/bitblaze/qemu/python/disass.h: 359

DIS_OP_ANDC_I32 = 54 # /store/orion/upstream/bitblaze/qemu/python/disass.h: 359

DIS_OP_ORC_I32 = 55 # /store/orion/upstream/bitblaze/qemu/python/disass.h: 359

DIS_OP_EQV_I32 = 56 # /store/orion/upstream/bitblaze/qemu/python/disass.h: 359

DIS_OP_NAND_I32 = 57 # /store/orion/upstream/bitblaze/qemu/python/disass.h: 359

DIS_OP_NOR_I32 = 58 # /store/orion/upstream/bitblaze/qemu/python/disass.h: 359

DIS_OP_MOV_I64 = 59 # /store/orion/upstream/bitblaze/qemu/python/disass.h: 359

DIS_OP_MOVI_I64 = 60 # /store/orion/upstream/bitblaze/qemu/python/disass.h: 359

DIS_OP_SETCOND_I64 = 61 # /store/orion/upstream/bitblaze/qemu/python/disass.h: 359

DIS_OP_MOVCOND_I64 = 62 # /store/orion/upstream/bitblaze/qemu/python/disass.h: 359

DIS_OP_LD8U_I64 = 63 # /store/orion/upstream/bitblaze/qemu/python/disass.h: 359

DIS_OP_LD8S_I64 = 64 # /store/orion/upstream/bitblaze/qemu/python/disass.h: 359

DIS_OP_LD16U_I64 = 65 # /store/orion/upstream/bitblaze/qemu/python/disass.h: 359

DIS_OP_LD16S_I64 = 66 # /store/orion/upstream/bitblaze/qemu/python/disass.h: 359

DIS_OP_LD32U_I64 = 67 # /store/orion/upstream/bitblaze/qemu/python/disass.h: 359

DIS_OP_LD32S_I64 = 68 # /store/orion/upstream/bitblaze/qemu/python/disass.h: 359

DIS_OP_LD_I64 = 69 # /store/orion/upstream/bitblaze/qemu/python/disass.h: 359

DIS_OP_ST8_I64 = 70 # /store/orion/upstream/bitblaze/qemu/python/disass.h: 359

DIS_OP_ST16_I64 = 71 # /store/orion/upstream/bitblaze/qemu/python/disass.h: 359

DIS_OP_ST32_I64 = 72 # /store/orion/upstream/bitblaze/qemu/python/disass.h: 359

DIS_OP_ST_I64 = 73 # /store/orion/upstream/bitblaze/qemu/python/disass.h: 359

DIS_OP_ADD_I64 = 74 # /store/orion/upstream/bitblaze/qemu/python/disass.h: 359

DIS_OP_SUB_I64 = 75 # /store/orion/upstream/bitblaze/qemu/python/disass.h: 359

DIS_OP_MUL_I64 = 76 # /store/orion/upstream/bitblaze/qemu/python/disass.h: 359

DIS_OP_DIV_I64 = 77 # /store/orion/upstream/bitblaze/qemu/python/disass.h: 359

DIS_OP_DIVU_I64 = 78 # /store/orion/upstream/bitblaze/qemu/python/disass.h: 359

DIS_OP_REM_I64 = 79 # /store/orion/upstream/bitblaze/qemu/python/disass.h: 359

DIS_OP_REMU_I64 = 80 # /store/orion/upstream/bitblaze/qemu/python/disass.h: 359

DIS_OP_DIV2_I64 = 81 # /store/orion/upstream/bitblaze/qemu/python/disass.h: 359

DIS_OP_DIVU2_I64 = 82 # /store/orion/upstream/bitblaze/qemu/python/disass.h: 359

DIS_OP_AND_I64 = 83 # /store/orion/upstream/bitblaze/qemu/python/disass.h: 359

DIS_OP_OR_I64 = 84 # /store/orion/upstream/bitblaze/qemu/python/disass.h: 359

DIS_OP_XOR_I64 = 85 # /store/orion/upstream/bitblaze/qemu/python/disass.h: 359

DIS_OP_SHL_I64 = 86 # /store/orion/upstream/bitblaze/qemu/python/disass.h: 359

DIS_OP_SHR_I64 = 87 # /store/orion/upstream/bitblaze/qemu/python/disass.h: 359

DIS_OP_SAR_I64 = 88 # /store/orion/upstream/bitblaze/qemu/python/disass.h: 359

DIS_OP_ROTL_I64 = 89 # /store/orion/upstream/bitblaze/qemu/python/disass.h: 359

DIS_OP_ROTR_I64 = 90 # /store/orion/upstream/bitblaze/qemu/python/disass.h: 359

DIS_OP_DEPOSIT_I64 = 91 # /store/orion/upstream/bitblaze/qemu/python/disass.h: 359

DIS_OP_BRCOND_I64 = 92 # /store/orion/upstream/bitblaze/qemu/python/disass.h: 359

DIS_OP_EXT8S_I64 = 93 # /store/orion/upstream/bitblaze/qemu/python/disass.h: 359

DIS_OP_EXT16S_I64 = 94 # /store/orion/upstream/bitblaze/qemu/python/disass.h: 359

DIS_OP_EXT32S_I64 = 95 # /store/orion/upstream/bitblaze/qemu/python/disass.h: 359

DIS_OP_EXT8U_I64 = 96 # /store/orion/upstream/bitblaze/qemu/python/disass.h: 359

DIS_OP_EXT16U_I64 = 97 # /store/orion/upstream/bitblaze/qemu/python/disass.h: 359

DIS_OP_EXT32U_I64 = 98 # /store/orion/upstream/bitblaze/qemu/python/disass.h: 359

DIS_OP_BSWAP16_I64 = 99 # /store/orion/upstream/bitblaze/qemu/python/disass.h: 359

DIS_OP_BSWAP32_I64 = 100 # /store/orion/upstream/bitblaze/qemu/python/disass.h: 359

DIS_OP_BSWAP64_I64 = 101 # /store/orion/upstream/bitblaze/qemu/python/disass.h: 359

DIS_OP_NOT_I64 = 102 # /store/orion/upstream/bitblaze/qemu/python/disass.h: 359

DIS_OP_NEG_I64 = 103 # /store/orion/upstream/bitblaze/qemu/python/disass.h: 359

DIS_OP_ANDC_I64 = 104 # /store/orion/upstream/bitblaze/qemu/python/disass.h: 359

DIS_OP_ORC_I64 = 105 # /store/orion/upstream/bitblaze/qemu/python/disass.h: 359

DIS_OP_EQV_I64 = 106 # /store/orion/upstream/bitblaze/qemu/python/disass.h: 359

DIS_OP_NAND_I64 = 107 # /store/orion/upstream/bitblaze/qemu/python/disass.h: 359

DIS_OP_NOR_I64 = 108 # /store/orion/upstream/bitblaze/qemu/python/disass.h: 359

DIS_OP_DEBUG_INSN_START = 109 # /store/orion/upstream/bitblaze/qemu/python/disass.h: 359

DIS_OP_EXIT_TB = 110 # /store/orion/upstream/bitblaze/qemu/python/disass.h: 359

DIS_OP_GOTO_TB = 111 # /store/orion/upstream/bitblaze/qemu/python/disass.h: 359

DIS_OP_QEMU_LD8U = 112 # /store/orion/upstream/bitblaze/qemu/python/disass.h: 359

DIS_OP_QEMU_LD8S = 113 # /store/orion/upstream/bitblaze/qemu/python/disass.h: 359

DIS_OP_QEMU_LD16U = 114 # /store/orion/upstream/bitblaze/qemu/python/disass.h: 359

DIS_OP_QEMU_LD16S = 115 # /store/orion/upstream/bitblaze/qemu/python/disass.h: 359

DIS_OP_QEMU_LD32 = 116 # /store/orion/upstream/bitblaze/qemu/python/disass.h: 359

DIS_OP_QEMU_LD32U = 117 # /store/orion/upstream/bitblaze/qemu/python/disass.h: 359

DIS_OP_QEMU_LD32S = 118 # /store/orion/upstream/bitblaze/qemu/python/disass.h: 359

DIS_OP_QEMU_LD64 = 119 # /store/orion/upstream/bitblaze/qemu/python/disass.h: 359

DIS_OP_QEMU_ST8 = 120 # /store/orion/upstream/bitblaze/qemu/python/disass.h: 359

DIS_OP_QEMU_ST16 = 121 # /store/orion/upstream/bitblaze/qemu/python/disass.h: 359

DIS_OP_QEMU_ST32 = 122 # /store/orion/upstream/bitblaze/qemu/python/disass.h: 359

DIS_OP_QEMU_ST64 = 123 # /store/orion/upstream/bitblaze/qemu/python/disass.h: 359

DisOpcode = enum_anon_31 # /store/orion/upstream/bitblaze/qemu/python/disass.h: 359

# /store/orion/upstream/bitblaze/qemu/python/disass.h: 379
class struct_anon_32(Structure):
    pass

struct_anon_32.__slots__ = [
    'num_ops',
    'ops',
    'num_args',
    'args',
    'num_syms',
    'syms',
    '_padding',
]
struct_anon_32._fields_ = [
    ('num_ops', c_size_t),
    ('ops', POINTER(DisOp)),
    ('num_args', c_size_t),
    ('args', POINTER(DisArg)),
    ('num_syms', c_size_t),
    ('syms', POINTER(DisSym)),
    ('_padding', c_size_t * 10),
]

DisResult = struct_anon_32 # /store/orion/upstream/bitblaze/qemu/python/disass.h: 379

enum_anon_33 = c_int # /store/orion/upstream/bitblaze/qemu/python/disass.h: 400

DIS_INFO_OP = 1 # /store/orion/upstream/bitblaze/qemu/python/disass.h: 400

DIS_INFO_COND = 2 # /store/orion/upstream/bitblaze/qemu/python/disass.h: 400

DIS_INFO_CALLFLAG = 3 # /store/orion/upstream/bitblaze/qemu/python/disass.h: 400

DIS_INFO_NUM_OPS = 256 # /store/orion/upstream/bitblaze/qemu/python/disass.h: 400

DIS_INFO_HELPER = 513 # /store/orion/upstream/bitblaze/qemu/python/disass.h: 400

DIS_INFO_HELPER_BY_ADDR = 514 # /store/orion/upstream/bitblaze/qemu/python/disass.h: 400

DIS_INFO_GLOBAL = 515 # /store/orion/upstream/bitblaze/qemu/python/disass.h: 400

DIS_INFO_PC_OFFSET = 768 # /store/orion/upstream/bitblaze/qemu/python/disass.h: 400

DIS_INFO_SP_OFFSET = 769 # /store/orion/upstream/bitblaze/qemu/python/disass.h: 400

DIS_INFO_NUM_HELPERS = 770 # /store/orion/upstream/bitblaze/qemu/python/disass.h: 400

DIS_INFO_NUM_GLOBALS = 771 # /store/orion/upstream/bitblaze/qemu/python/disass.h: 400

DIS_INFO_GLOBAL_SIZE = 772 # /store/orion/upstream/bitblaze/qemu/python/disass.h: 400

DIS_INFO_GLOBAL_OFFSET = 773 # /store/orion/upstream/bitblaze/qemu/python/disass.h: 400

DIS_INFO_STATE_SIZE = 774 # /store/orion/upstream/bitblaze/qemu/python/disass.h: 400

DisInfoType = enum_anon_33 # /store/orion/upstream/bitblaze/qemu/python/disass.h: 400

enum_anon_34 = c_int # /store/orion/upstream/bitblaze/qemu/python/disass.h: 412

DIS_CALL_NO_READ_GLOBALS = 16 # /store/orion/upstream/bitblaze/qemu/python/disass.h: 412

DIS_CALL_NO_WRITE_GLOBALS = 32 # /store/orion/upstream/bitblaze/qemu/python/disass.h: 412

DIS_CALL_NO_SIDE_EFFECTS = 64 # /store/orion/upstream/bitblaze/qemu/python/disass.h: 412

DisCallFlags = enum_anon_34 # /store/orion/upstream/bitblaze/qemu/python/disass.h: 412

# /store/orion/upstream/bitblaze/qemu/python/disass.h: 419
if hasattr(_libs['qdis'], 'dis_Create'):
    dis_Create = _libs['qdis'].dis_Create
    dis_Create.argtypes = [DisTarget, POINTER(DisCPUFeature)]
    dis_Create.restype = POINTER(Disassembler)

# /store/orion/upstream/bitblaze/qemu/python/disass.h: 424
if hasattr(_libs['qdis'], 'dis_Disassemble'):
    dis_Disassemble = _libs['qdis'].dis_Disassemble
    dis_Disassemble.argtypes = [POINTER(Disassembler), POINTER(c_uint8), c_size_t, c_uint64, c_uint64, c_uint32, POINTER(None), c_size_t]
    dis_Disassemble.restype = DisStatus

# /store/orion/upstream/bitblaze/qemu/python/disass.h: 430
if hasattr(_libs['qdis'], 'dis_LookupName'):
    dis_LookupName = _libs['qdis'].dis_LookupName
    dis_LookupName.argtypes = [POINTER(Disassembler), DisInfoType, c_size_t]
    if sizeof(c_int) == sizeof(c_void_p):
        dis_LookupName.restype = ReturnString
    else:
        dis_LookupName.restype = String
        dis_LookupName.errcheck = ReturnString

# /store/orion/upstream/bitblaze/qemu/python/disass.h: 434
if hasattr(_libs['qdis'], 'dis_LookupValue'):
    dis_LookupValue = _libs['qdis'].dis_LookupValue
    dis_LookupValue.argtypes = [POINTER(Disassembler), DisInfoType, c_size_t]
    dis_LookupValue.restype = c_size_t

# /store/orion/upstream/bitblaze/qemu/python/disass.h: 438
if hasattr(_libs['qdis'], 'dis_Dump'):
    dis_Dump = _libs['qdis'].dis_Dump
    dis_Dump.argtypes = [POINTER(Disassembler)]
    dis_Dump.restype = None

# /store/orion/upstream/bitblaze/qemu/python/disass.h: 442
if hasattr(_libs['qdis'], 'dis_Destroy'):
    dis_Destroy = _libs['qdis'].dis_Destroy
    dis_Destroy.argtypes = [POINTER(Disassembler)]
    dis_Destroy.restype = None

# /store/orion/upstream/bitblaze/qemu/python/disass.h: 88
try:
    DIS_INST_ARM_THUMB_SHIFT = 0
except:
    pass

# /store/orion/upstream/bitblaze/qemu/python/disass.h: 89
try:
    DIS_INST_ARM_THUMB_MASK = (1 << DIS_INST_ARM_THUMB_SHIFT)
except:
    pass

# /store/orion/upstream/bitblaze/qemu/python/disass.h: 90
try:
    DIS_INST_ARM_VECLEN_SHIFT = 1
except:
    pass

# /store/orion/upstream/bitblaze/qemu/python/disass.h: 91
try:
    DIS_INST_ARM_VECLEN_MASK = (7 << DIS_INST_ARM_VECLEN_SHIFT)
except:
    pass

# /store/orion/upstream/bitblaze/qemu/python/disass.h: 92
try:
    DIS_INST_ARM_VECSTRIDE_SHIFT = 4
except:
    pass

# /store/orion/upstream/bitblaze/qemu/python/disass.h: 93
try:
    DIS_INST_ARM_VECSTRIDE_MASK = (3 << DIS_INST_ARM_VECSTRIDE_SHIFT)
except:
    pass

# /store/orion/upstream/bitblaze/qemu/python/disass.h: 94
try:
    DIS_INST_ARM_PRIV_SHIFT = 6
except:
    pass

# /store/orion/upstream/bitblaze/qemu/python/disass.h: 95
try:
    DIS_INST_ARM_PRIV_MASK = (1 << DIS_INST_ARM_PRIV_SHIFT)
except:
    pass

# /store/orion/upstream/bitblaze/qemu/python/disass.h: 96
try:
    DIS_INST_ARM_VFPEN_SHIFT = 7
except:
    pass

# /store/orion/upstream/bitblaze/qemu/python/disass.h: 97
try:
    DIS_INST_ARM_VFPEN_MASK = (1 << DIS_INST_ARM_VFPEN_SHIFT)
except:
    pass

# /store/orion/upstream/bitblaze/qemu/python/disass.h: 98
try:
    DIS_INST_ARM_CONDEXEC_SHIFT = 8
except:
    pass

# /store/orion/upstream/bitblaze/qemu/python/disass.h: 99
try:
    DIS_INST_ARM_CONDEXEC_MASK = (255 << DIS_INST_ARM_CONDEXEC_SHIFT)
except:
    pass

# /store/orion/upstream/bitblaze/qemu/python/disass.h: 100
try:
    DIS_INST_ARM_BSWAP_CODE_SHIFT = 16
except:
    pass

# /store/orion/upstream/bitblaze/qemu/python/disass.h: 101
try:
    DIS_INST_ARM_BSWAP_CODE_MASK = (1 << DIS_INST_ARM_BSWAP_CODE_SHIFT)
except:
    pass

# /store/orion/upstream/bitblaze/qemu/python/disass.h: 104
try:
    DIS_INST_X86_CPL_SHIFT = 0
except:
    pass

# /store/orion/upstream/bitblaze/qemu/python/disass.h: 105
try:
    DIS_INST_X86_SOFTMMU_SHIFT = 2
except:
    pass

# /store/orion/upstream/bitblaze/qemu/python/disass.h: 106
try:
    DIS_INST_X86_INHIBIT_IRQ_SHIFT = 3
except:
    pass

# /store/orion/upstream/bitblaze/qemu/python/disass.h: 107
try:
    DIS_INST_X86_CS32_SHIFT = 4
except:
    pass

# /store/orion/upstream/bitblaze/qemu/python/disass.h: 108
try:
    DIS_INST_X86_SS32_SHIFT = 5
except:
    pass

# /store/orion/upstream/bitblaze/qemu/python/disass.h: 109
try:
    DIS_INST_X86_ADDSEG_SHIFT = 6
except:
    pass

# /store/orion/upstream/bitblaze/qemu/python/disass.h: 110
try:
    DIS_INST_X86_PE_SHIFT = 7
except:
    pass

# /store/orion/upstream/bitblaze/qemu/python/disass.h: 111
try:
    DIS_INST_X86_TF_SHIFT = 8
except:
    pass

# /store/orion/upstream/bitblaze/qemu/python/disass.h: 112
try:
    DIS_INST_X86_MP_SHIFT = 9
except:
    pass

# /store/orion/upstream/bitblaze/qemu/python/disass.h: 113
try:
    DIS_INST_X86_EM_SHIFT = 10
except:
    pass

# /store/orion/upstream/bitblaze/qemu/python/disass.h: 114
try:
    DIS_INST_X86_TS_SHIFT = 11
except:
    pass

# /store/orion/upstream/bitblaze/qemu/python/disass.h: 115
try:
    DIS_INST_X86_IOPL_SHIFT = 12
except:
    pass

# /store/orion/upstream/bitblaze/qemu/python/disass.h: 116
try:
    DIS_INST_X86_LMA_SHIFT = 14
except:
    pass

# /store/orion/upstream/bitblaze/qemu/python/disass.h: 117
try:
    DIS_INST_X86_CS64_SHIFT = 15
except:
    pass

# /store/orion/upstream/bitblaze/qemu/python/disass.h: 118
try:
    DIS_INST_X86_RF_SHIFT = 16
except:
    pass

# /store/orion/upstream/bitblaze/qemu/python/disass.h: 119
try:
    DIS_INST_X86_VM_SHIFT = 17
except:
    pass

# /store/orion/upstream/bitblaze/qemu/python/disass.h: 120
try:
    DIS_INST_X86_AC_SHIFT = 18
except:
    pass

# /store/orion/upstream/bitblaze/qemu/python/disass.h: 121
try:
    DIS_INST_X86_SMM_SHIFT = 19
except:
    pass

# /store/orion/upstream/bitblaze/qemu/python/disass.h: 122
try:
    DIS_INST_X86_SVME_SHIFT = 20
except:
    pass

# /store/orion/upstream/bitblaze/qemu/python/disass.h: 123
try:
    DIS_INST_X86_SVMI_SHIFT = 21
except:
    pass

# /store/orion/upstream/bitblaze/qemu/python/disass.h: 124
try:
    DIS_INST_X86_OSFXSR_SHIFT = 22
except:
    pass

# /store/orion/upstream/bitblaze/qemu/python/disass.h: 125
try:
    DIS_INST_X86_SMAP_SHIFT = 23
except:
    pass

# /store/orion/upstream/bitblaze/qemu/python/disass.h: 127
try:
    DIS_INST_X86_CPL_MASK = (3 << DIS_INST_X86_CPL_SHIFT)
except:
    pass

# /store/orion/upstream/bitblaze/qemu/python/disass.h: 128
try:
    DIS_INST_X86_SOFTMMU_MASK = (1 << DIS_INST_X86_SOFTMMU_SHIFT)
except:
    pass

# /store/orion/upstream/bitblaze/qemu/python/disass.h: 129
try:
    DIS_INST_X86_INHIBIT_IRQ_MASK = (1 << DIS_INST_X86_INHIBIT_IRQ_SHIFT)
except:
    pass

# /store/orion/upstream/bitblaze/qemu/python/disass.h: 130
try:
    DIS_INST_X86_CS32_MASK = (1 << DIS_INST_X86_CS32_SHIFT)
except:
    pass

# /store/orion/upstream/bitblaze/qemu/python/disass.h: 131
try:
    DIS_INST_X86_SS32_MASK = (1 << DIS_INST_X86_SS32_SHIFT)
except:
    pass

# /store/orion/upstream/bitblaze/qemu/python/disass.h: 132
try:
    DIS_INST_X86_ADDSEG_MASK = (1 << DIS_INST_X86_ADDSEG_SHIFT)
except:
    pass

# /store/orion/upstream/bitblaze/qemu/python/disass.h: 133
try:
    DIS_INST_X86_PE_MASK = (1 << DIS_INST_X86_PE_SHIFT)
except:
    pass

# /store/orion/upstream/bitblaze/qemu/python/disass.h: 134
try:
    DIS_INST_X86_TF_MASK = (1 << DIS_INST_X86_TF_SHIFT)
except:
    pass

# /store/orion/upstream/bitblaze/qemu/python/disass.h: 135
try:
    DIS_INST_X86_MP_MASK = (1 << DIS_INST_X86_MP_SHIFT)
except:
    pass

# /store/orion/upstream/bitblaze/qemu/python/disass.h: 136
try:
    DIS_INST_X86_EM_MASK = (1 << DIS_INST_X86_EM_SHIFT)
except:
    pass

# /store/orion/upstream/bitblaze/qemu/python/disass.h: 137
try:
    DIS_INST_X86_TS_MASK = (1 << DIS_INST_X86_TS_SHIFT)
except:
    pass

# /store/orion/upstream/bitblaze/qemu/python/disass.h: 138
try:
    DIS_INST_X86_IOPL_MASK = (3 << DIS_INST_X86_IOPL_SHIFT)
except:
    pass

# /store/orion/upstream/bitblaze/qemu/python/disass.h: 139
try:
    DIS_INST_X86_LMA_MASK = (1 << DIS_INST_X86_LMA_SHIFT)
except:
    pass

# /store/orion/upstream/bitblaze/qemu/python/disass.h: 140
try:
    DIS_INST_X86_CS64_MASK = (1 << DIS_INST_X86_CS64_SHIFT)
except:
    pass

# /store/orion/upstream/bitblaze/qemu/python/disass.h: 141
try:
    DIS_INST_X86_RF_MASK = (1 << DIS_INST_X86_RF_SHIFT)
except:
    pass

# /store/orion/upstream/bitblaze/qemu/python/disass.h: 142
try:
    DIS_INST_X86_VM_MASK = (1 << DIS_INST_X86_VM_SHIFT)
except:
    pass

# /store/orion/upstream/bitblaze/qemu/python/disass.h: 143
try:
    DIS_INST_X86_AC_MASK = (1 << DIS_INST_X86_AC_SHIFT)
except:
    pass

# /store/orion/upstream/bitblaze/qemu/python/disass.h: 144
try:
    DIS_INST_X86_SMM_MASK = (1 << DIS_INST_X86_SMM_SHIFT)
except:
    pass

# /store/orion/upstream/bitblaze/qemu/python/disass.h: 145
try:
    DIS_INST_X86_SVME_MASK = (1 << DIS_INST_X86_SVME_SHIFT)
except:
    pass

# /store/orion/upstream/bitblaze/qemu/python/disass.h: 146
try:
    DIS_INST_X86_SVMI_MASK = (1 << DIS_INST_X86_SVMI_SHIFT)
except:
    pass

# /store/orion/upstream/bitblaze/qemu/python/disass.h: 147
try:
    DIS_INST_X86_OSFXSR_MASK = (1 << DIS_INST_X86_OSFXSR_SHIFT)
except:
    pass

# /store/orion/upstream/bitblaze/qemu/python/disass.h: 148
try:
    DIS_INST_X86_SMAP_MASK = (1 << DIS_INST_X86_SMAP_SHIFT)
except:
    pass

# /store/orion/upstream/bitblaze/qemu/python/disass.h: 364
try:
    DIS_BUFFER_SIZE = 16384
except:
    pass

# /store/orion/upstream/bitblaze/qemu/python/disass.h: 367
try:
    DIS_INVALID = (-1)
except:
    pass

Disassembler_ = struct_Disassembler_ # /store/orion/upstream/bitblaze/qemu/python/disass.h: 150

# No inserted files
