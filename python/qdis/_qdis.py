'''Wrapper for qdis.h

Generated with:
/home/orion/upstream/python/ctypesgen/ctypesgen.py -lqdis qdis.h -L .

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

enum_anon_20 = c_int # qdis.h: 16

QDIS_OK = 0 # qdis.h: 16

QDIS_ERR_OUT_OF_BOUNDS_ACCESS = 1 # qdis.h: 16

QDIS_ERR_BUFFER_TOO_SMALL = 2 # qdis.h: 16

QDIS_ERR_NULLPOINTER = 3 # qdis.h: 16

QDIS_ERR_ALIGNMENT = 4 # qdis.h: 16

QDIS_ERR_NOT_FOUND = 5 # qdis.h: 16

QDisStatus = enum_anon_20 # qdis.h: 16

enum_anon_21 = c_int # qdis.h: 45

QDIS_TGT_8BIT = 0 # qdis.h: 45

QDIS_TGT_16BIT = 4096 # qdis.h: 45

QDIS_TGT_32BIT = 8192 # qdis.h: 45

QDIS_TGT_64BIT = 12288 # qdis.h: 45

QDIS_TGT_ARM = (0 | QDIS_TGT_32BIT) # qdis.h: 45

QDIS_TGT_X86_64 = (1 | QDIS_TGT_64BIT) # qdis.h: 45

QDIS_TGT_ALPHA = (2 | QDIS_TGT_64BIT) # qdis.h: 45

QDIS_TGT_CRIS = (3 | QDIS_TGT_32BIT) # qdis.h: 45

QDIS_TGT_LM32 = (4 | QDIS_TGT_32BIT) # qdis.h: 45

QDIS_TGT_M68K = (5 | QDIS_TGT_32BIT) # qdis.h: 45

QDIS_TGT_MICROBLAZE = (6 | QDIS_TGT_32BIT) # qdis.h: 45

QDIS_TGT_MIPS_64 = (7 | QDIS_TGT_64BIT) # qdis.h: 45

QDIS_TGT_OPENRISC = (8 | QDIS_TGT_32BIT) # qdis.h: 45

QDIS_TGT_PPC_64 = (9 | QDIS_TGT_64BIT) # qdis.h: 45

QDIS_TGT_S390X = (10 | QDIS_TGT_64BIT) # qdis.h: 45

QDIS_TGT_SH4 = (11 | QDIS_TGT_32BIT) # qdis.h: 45

QDIS_TGT_SPARC_64 = (12 | QDIS_TGT_64BIT) # qdis.h: 45

QDIS_TGT_UNICORE32 = (13 | QDIS_TGT_32BIT) # qdis.h: 45

QDIS_TGT_XTENSA = (14 | QDIS_TGT_32BIT) # qdis.h: 45

QDisTarget = enum_anon_21 # qdis.h: 45

enum_anon_22 = c_int # qdis.h: 87

QDIS_FEATURE_END = 0 # qdis.h: 87

QDIS_ARM_FEATURE_VFP = (QDIS_FEATURE_END + 1) # qdis.h: 87

QDIS_ARM_FEATURE_AUXCR = (QDIS_ARM_FEATURE_VFP + 1) # qdis.h: 87

QDIS_ARM_FEATURE_XSCALE = (QDIS_ARM_FEATURE_AUXCR + 1) # qdis.h: 87

QDIS_ARM_FEATURE_IWMMXT = (QDIS_ARM_FEATURE_XSCALE + 1) # qdis.h: 87

QDIS_ARM_FEATURE_V6 = (QDIS_ARM_FEATURE_IWMMXT + 1) # qdis.h: 87

QDIS_ARM_FEATURE_V6K = (QDIS_ARM_FEATURE_V6 + 1) # qdis.h: 87

QDIS_ARM_FEATURE_V7 = (QDIS_ARM_FEATURE_V6K + 1) # qdis.h: 87

QDIS_ARM_FEATURE_THUMB2 = (QDIS_ARM_FEATURE_V7 + 1) # qdis.h: 87

QDIS_ARM_FEATURE_MPU = (QDIS_ARM_FEATURE_THUMB2 + 1) # qdis.h: 87

QDIS_ARM_FEATURE_VFP3 = (QDIS_ARM_FEATURE_MPU + 1) # qdis.h: 87

QDIS_ARM_FEATURE_VFP_FP16 = (QDIS_ARM_FEATURE_VFP3 + 1) # qdis.h: 87

QDIS_ARM_FEATURE_NEON = (QDIS_ARM_FEATURE_VFP_FP16 + 1) # qdis.h: 87

QDIS_ARM_FEATURE_THUMB_DIV = (QDIS_ARM_FEATURE_NEON + 1) # qdis.h: 87

QDIS_ARM_FEATURE_M = (QDIS_ARM_FEATURE_THUMB_DIV + 1) # qdis.h: 87

QDIS_ARM_FEATURE_OMAPCP = (QDIS_ARM_FEATURE_M + 1) # qdis.h: 87

QDIS_ARM_FEATURE_THUMB2EE = (QDIS_ARM_FEATURE_OMAPCP + 1) # qdis.h: 87

QDIS_ARM_FEATURE_V7MP = (QDIS_ARM_FEATURE_THUMB2EE + 1) # qdis.h: 87

QDIS_ARM_FEATURE_V4T = (QDIS_ARM_FEATURE_V7MP + 1) # qdis.h: 87

QDIS_ARM_FEATURE_V5 = (QDIS_ARM_FEATURE_V4T + 1) # qdis.h: 87

QDIS_ARM_FEATURE_STRONGARM = (QDIS_ARM_FEATURE_V5 + 1) # qdis.h: 87

QDIS_ARM_FEATURE_VAPA = (QDIS_ARM_FEATURE_STRONGARM + 1) # qdis.h: 87

QDIS_ARM_FEATURE_ARM_DIV = (QDIS_ARM_FEATURE_VAPA + 1) # qdis.h: 87

QDIS_ARM_FEATURE_VFP4 = (QDIS_ARM_FEATURE_ARM_DIV + 1) # qdis.h: 87

QDIS_ARM_FEATURE_GENERIC_TIMER = (QDIS_ARM_FEATURE_VFP4 + 1) # qdis.h: 87

QDIS_ARM_FEATURE_MVFR = (QDIS_ARM_FEATURE_GENERIC_TIMER + 1) # qdis.h: 87

QDIS_ARM_FEATURE_DUMMY_C15_REGS = (QDIS_ARM_FEATURE_MVFR + 1) # qdis.h: 87

QDIS_ARM_FEATURE_CACHE_TEST_CLEAN = (QDIS_ARM_FEATURE_DUMMY_C15_REGS + 1) # qdis.h: 87

QDIS_ARM_FEATURE_CACHE_DIRTY_REG = (QDIS_ARM_FEATURE_CACHE_TEST_CLEAN + 1) # qdis.h: 87

QDIS_ARM_FEATURE_CACHE_BLOCK_OPS = (QDIS_ARM_FEATURE_CACHE_DIRTY_REG + 1) # qdis.h: 87

QDIS_ARM_FEATURE_MPIDR = (QDIS_ARM_FEATURE_CACHE_BLOCK_OPS + 1) # qdis.h: 87

QDIS_ARM_FEATURE_PXN = (QDIS_ARM_FEATURE_MPIDR + 1) # qdis.h: 87

QDIS_ARM_FEATURE_LPAE = (QDIS_ARM_FEATURE_PXN + 1) # qdis.h: 87

QDisCPUFeature = enum_anon_22 # qdis.h: 87

# qdis.h: 163
class struct_QDisassembler_(Structure):
    pass

QDisassembler = struct_QDisassembler_ # qdis.h: 163

enum_anon_23 = c_int # qdis.h: 171

QDIS_OPTIMIZE_NONE = 0 # qdis.h: 171

QDIS_OPTIMIZE_LIVENESS = 1 # qdis.h: 171

QDIS_OPTIMIZE_GENERAL = 2 # qdis.h: 171

QDIS_OPTIMIZE_FULL = (QDIS_OPTIMIZE_LIVENESS | QDIS_OPTIMIZE_GENERAL) # qdis.h: 171

QDIS_OPTIMIZE_NOTEXT = 4 # qdis.h: 171

QDisOptimizeFlags = enum_anon_23 # qdis.h: 171

enum_anon_24 = c_int # qdis.h: 178

QDIS_SYM_LOCAL = 1 # qdis.h: 178

QDIS_SYM_TEMP = 2 # qdis.h: 178

QDisSymType = enum_anon_24 # qdis.h: 178

enum_anon_25 = c_int # qdis.h: 188

QDIS_SIZE_UNKNOWN = 0 # qdis.h: 188

QDIS_SIZE_8 = 8 # qdis.h: 188

QDIS_SIZE_16 = 16 # qdis.h: 188

QDIS_SIZE_32 = 32 # qdis.h: 188

QDIS_SIZE_64 = 64 # qdis.h: 188

QDisBitsize = enum_anon_25 # qdis.h: 188

# qdis.h: 195
class struct_anon_26(Structure):
    pass

struct_anon_26.__slots__ = [
    'type',
    'size',
]
struct_anon_26._fields_ = [
    ('type', QDisSymType),
    ('size', QDisBitsize),
]

QDisSym = struct_anon_26 # qdis.h: 195

enum_anon_27 = c_int # qdis.h: 215

QDIS_COND_NEVER = (((0 | 0) | 0) | 0) # qdis.h: 215

QDIS_COND_ALWAYS = (((0 | 0) | 0) | 1) # qdis.h: 215

QDIS_COND_EQ = (((8 | 0) | 0) | 0) # qdis.h: 215

QDIS_COND_NE = (((8 | 0) | 0) | 1) # qdis.h: 215

QDIS_COND_LT = (((0 | 0) | 2) | 0) # qdis.h: 215

QDIS_COND_GE = (((0 | 0) | 2) | 1) # qdis.h: 215

QDIS_COND_LE = (((8 | 0) | 2) | 0) # qdis.h: 215

QDIS_COND_GT = (((8 | 0) | 2) | 1) # qdis.h: 215

QDIS_COND_LTU = (((0 | 4) | 0) | 0) # qdis.h: 215

QDIS_COND_GEU = (((0 | 4) | 0) | 1) # qdis.h: 215

QDIS_COND_LEU = (((8 | 4) | 0) | 0) # qdis.h: 215

QDIS_COND_GTU = (((8 | 4) | 0) | 1) # qdis.h: 215

QDisConditionCode = enum_anon_27 # qdis.h: 215

# qdis.h: 221
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

QDisOp = struct_anon_28 # qdis.h: 221

enum_anon_29 = c_int # qdis.h: 235

QDIS_ARG_GLOBAL = 1 # qdis.h: 235

QDIS_ARG_TEMP = 2 # qdis.h: 235

QDIS_ARG_COND = 8 # qdis.h: 235

QDIS_ARG_LABEL = 16 # qdis.h: 235

QDIS_ARG_CALLFLAGS = 64 # qdis.h: 235

QDIS_ARG_CALLTARGET = 128 # qdis.h: 235

QDIS_ARG_INPUT = 256 # qdis.h: 235

QDIS_ARG_OUTPUT = 512 # qdis.h: 235

QDIS_ARG_CONSTANT = 1024 # qdis.h: 235

QDisArgFlags = enum_anon_29 # qdis.h: 235

QDisVal = c_uint64 # qdis.h: 237

# qdis.h: 245
class struct_anon_30(Structure):
    pass

struct_anon_30.__slots__ = [
    'value',
    'size',
    'flags',
]
struct_anon_30._fields_ = [
    ('value', QDisVal),
    ('size', QDisBitsize),
    ('flags', c_uint16),
]

QDisArg = struct_anon_30 # qdis.h: 245

enum_anon_31 = c_int # qdis.h: 374

QDIS_OP_END = 0 # qdis.h: 374

QDIS_OP_NOP = 1 # qdis.h: 374

QDIS_OP_NOP1 = 2 # qdis.h: 374

QDIS_OP_NOP2 = 3 # qdis.h: 374

QDIS_OP_NOP3 = 4 # qdis.h: 374

QDIS_OP_NOPN = 5 # qdis.h: 374

QDIS_OP_DISCARD = 6 # qdis.h: 374

QDIS_OP_SET_LABEL = 7 # qdis.h: 374

QDIS_OP_CALL = 8 # qdis.h: 374

QDIS_OP_BR = 9 # qdis.h: 374

QDIS_OP_MOV_I32 = 10 # qdis.h: 374

QDIS_OP_MOVI_I32 = 11 # qdis.h: 374

QDIS_OP_SETCOND_I32 = 12 # qdis.h: 374

QDIS_OP_MOVCOND_I32 = 13 # qdis.h: 374

QDIS_OP_LD8U_I32 = 14 # qdis.h: 374

QDIS_OP_LD8S_I32 = 15 # qdis.h: 374

QDIS_OP_LD16U_I32 = 16 # qdis.h: 374

QDIS_OP_LD16S_I32 = 17 # qdis.h: 374

QDIS_OP_LD_I32 = 18 # qdis.h: 374

QDIS_OP_ST8_I32 = 19 # qdis.h: 374

QDIS_OP_ST16_I32 = 20 # qdis.h: 374

QDIS_OP_ST_I32 = 21 # qdis.h: 374

QDIS_OP_ADD_I32 = 22 # qdis.h: 374

QDIS_OP_SUB_I32 = 23 # qdis.h: 374

QDIS_OP_MUL_I32 = 24 # qdis.h: 374

QDIS_OP_DIV_I32 = 25 # qdis.h: 374

QDIS_OP_DIVU_I32 = 26 # qdis.h: 374

QDIS_OP_REM_I32 = 27 # qdis.h: 374

QDIS_OP_REMU_I32 = 28 # qdis.h: 374

QDIS_OP_DIV2_I32 = 29 # qdis.h: 374

QDIS_OP_DIVU2_I32 = 30 # qdis.h: 374

QDIS_OP_AND_I32 = 31 # qdis.h: 374

QDIS_OP_OR_I32 = 32 # qdis.h: 374

QDIS_OP_XOR_I32 = 33 # qdis.h: 374

QDIS_OP_SHL_I32 = 34 # qdis.h: 374

QDIS_OP_SHR_I32 = 35 # qdis.h: 374

QDIS_OP_SAR_I32 = 36 # qdis.h: 374

QDIS_OP_ROTL_I32 = 37 # qdis.h: 374

QDIS_OP_ROTR_I32 = 38 # qdis.h: 374

QDIS_OP_DEPOSIT_I32 = 39 # qdis.h: 374

QDIS_OP_BRCOND_I32 = 40 # qdis.h: 374

QDIS_OP_ADD2_I32 = 41 # qdis.h: 374

QDIS_OP_SUB2_I32 = 42 # qdis.h: 374

QDIS_OP_BRCOND2_I32 = 43 # qdis.h: 374

QDIS_OP_MULU2_I32 = 44 # qdis.h: 374

QDIS_OP_SETCOND2_I32 = 45 # qdis.h: 374

QDIS_OP_EXT8S_I32 = 46 # qdis.h: 374

QDIS_OP_EXT16S_I32 = 47 # qdis.h: 374

QDIS_OP_EXT8U_I32 = 48 # qdis.h: 374

QDIS_OP_EXT16U_I32 = 49 # qdis.h: 374

QDIS_OP_BSWAP16_I32 = 50 # qdis.h: 374

QDIS_OP_BSWAP32_I32 = 51 # qdis.h: 374

QDIS_OP_NOT_I32 = 52 # qdis.h: 374

QDIS_OP_NEG_I32 = 53 # qdis.h: 374

QDIS_OP_ANDC_I32 = 54 # qdis.h: 374

QDIS_OP_ORC_I32 = 55 # qdis.h: 374

QDIS_OP_EQV_I32 = 56 # qdis.h: 374

QDIS_OP_NAND_I32 = 57 # qdis.h: 374

QDIS_OP_NOR_I32 = 58 # qdis.h: 374

QDIS_OP_MOV_I64 = 59 # qdis.h: 374

QDIS_OP_MOVI_I64 = 60 # qdis.h: 374

QDIS_OP_SETCOND_I64 = 61 # qdis.h: 374

QDIS_OP_MOVCOND_I64 = 62 # qdis.h: 374

QDIS_OP_LD8U_I64 = 63 # qdis.h: 374

QDIS_OP_LD8S_I64 = 64 # qdis.h: 374

QDIS_OP_LD16U_I64 = 65 # qdis.h: 374

QDIS_OP_LD16S_I64 = 66 # qdis.h: 374

QDIS_OP_LD32U_I64 = 67 # qdis.h: 374

QDIS_OP_LD32S_I64 = 68 # qdis.h: 374

QDIS_OP_LD_I64 = 69 # qdis.h: 374

QDIS_OP_ST8_I64 = 70 # qdis.h: 374

QDIS_OP_ST16_I64 = 71 # qdis.h: 374

QDIS_OP_ST32_I64 = 72 # qdis.h: 374

QDIS_OP_ST_I64 = 73 # qdis.h: 374

QDIS_OP_ADD_I64 = 74 # qdis.h: 374

QDIS_OP_SUB_I64 = 75 # qdis.h: 374

QDIS_OP_MUL_I64 = 76 # qdis.h: 374

QDIS_OP_DIV_I64 = 77 # qdis.h: 374

QDIS_OP_DIVU_I64 = 78 # qdis.h: 374

QDIS_OP_REM_I64 = 79 # qdis.h: 374

QDIS_OP_REMU_I64 = 80 # qdis.h: 374

QDIS_OP_DIV2_I64 = 81 # qdis.h: 374

QDIS_OP_DIVU2_I64 = 82 # qdis.h: 374

QDIS_OP_AND_I64 = 83 # qdis.h: 374

QDIS_OP_OR_I64 = 84 # qdis.h: 374

QDIS_OP_XOR_I64 = 85 # qdis.h: 374

QDIS_OP_SHL_I64 = 86 # qdis.h: 374

QDIS_OP_SHR_I64 = 87 # qdis.h: 374

QDIS_OP_SAR_I64 = 88 # qdis.h: 374

QDIS_OP_ROTL_I64 = 89 # qdis.h: 374

QDIS_OP_ROTR_I64 = 90 # qdis.h: 374

QDIS_OP_DEPOSIT_I64 = 91 # qdis.h: 374

QDIS_OP_BRCOND_I64 = 92 # qdis.h: 374

QDIS_OP_EXT8S_I64 = 93 # qdis.h: 374

QDIS_OP_EXT16S_I64 = 94 # qdis.h: 374

QDIS_OP_EXT32S_I64 = 95 # qdis.h: 374

QDIS_OP_EXT8U_I64 = 96 # qdis.h: 374

QDIS_OP_EXT16U_I64 = 97 # qdis.h: 374

QDIS_OP_EXT32U_I64 = 98 # qdis.h: 374

QDIS_OP_BSWAP16_I64 = 99 # qdis.h: 374

QDIS_OP_BSWAP32_I64 = 100 # qdis.h: 374

QDIS_OP_BSWAP64_I64 = 101 # qdis.h: 374

QDIS_OP_NOT_I64 = 102 # qdis.h: 374

QDIS_OP_NEG_I64 = 103 # qdis.h: 374

QDIS_OP_ANDC_I64 = 104 # qdis.h: 374

QDIS_OP_ORC_I64 = 105 # qdis.h: 374

QDIS_OP_EQV_I64 = 106 # qdis.h: 374

QDIS_OP_NAND_I64 = 107 # qdis.h: 374

QDIS_OP_NOR_I64 = 108 # qdis.h: 374

QDIS_OP_DEBUG_INSN_START = 109 # qdis.h: 374

QDIS_OP_EXIT_TB = 110 # qdis.h: 374

QDIS_OP_GOTO_TB = 111 # qdis.h: 374

QDIS_OP_QEMU_LD8U = 112 # qdis.h: 374

QDIS_OP_QEMU_LD8S = 113 # qdis.h: 374

QDIS_OP_QEMU_LD16U = 114 # qdis.h: 374

QDIS_OP_QEMU_LD16S = 115 # qdis.h: 374

QDIS_OP_QEMU_LD32 = 116 # qdis.h: 374

QDIS_OP_QEMU_LD32U = 117 # qdis.h: 374

QDIS_OP_QEMU_LD32S = 118 # qdis.h: 374

QDIS_OP_QEMU_LD64 = 119 # qdis.h: 374

QDIS_OP_QEMU_ST8 = 120 # qdis.h: 374

QDIS_OP_QEMU_ST16 = 121 # qdis.h: 374

QDIS_OP_QEMU_ST32 = 122 # qdis.h: 374

QDIS_OP_QEMU_ST64 = 123 # qdis.h: 374

QDisOpcode = enum_anon_31 # qdis.h: 374

enum_anon_32 = c_int # qdis.h: 389

QDIS_ITYPE_UNKNOWN = (-1) # qdis.h: 389

QDIS_ITYPE_DEFAULT = 0 # qdis.h: 389

QDIS_ITYPE_JMP = (QDIS_ITYPE_DEFAULT + 1) # qdis.h: 389

QDIS_ITYPE_JMP_IND = (QDIS_ITYPE_JMP + 1) # qdis.h: 389

QDIS_ITYPE_COND_JMP = (QDIS_ITYPE_JMP_IND + 1) # qdis.h: 389

QDIS_ITYPE_COND_JMP_IND = (QDIS_ITYPE_COND_JMP + 1) # qdis.h: 389

QDIS_ITYPE_CALL = (QDIS_ITYPE_COND_JMP_IND + 1) # qdis.h: 389

QDIS_ITYPE_CALL_IND = (QDIS_ITYPE_CALL + 1) # qdis.h: 389

QDIS_ITYPE_REP = (QDIS_ITYPE_CALL_IND + 1) # qdis.h: 389

QDIS_ITYPE_RET = (QDIS_ITYPE_REP + 1) # qdis.h: 389

QDisInstType = enum_anon_32 # qdis.h: 389

# qdis.h: 414
class struct_anon_33(Structure):
    pass

struct_anon_33.__slots__ = [
    'total_size',
    'num_ops',
    'ops',
    'num_args',
    'args',
    'num_syms',
    'syms',
    'num_labels',
    'inst_type',
    'inst_size',
    'inst_text',
    '_padding',
]
struct_anon_33._fields_ = [
    ('total_size', c_size_t),
    ('num_ops', c_size_t),
    ('ops', POINTER(QDisOp)),
    ('num_args', c_size_t),
    ('args', POINTER(QDisArg)),
    ('num_syms', c_size_t),
    ('syms', POINTER(QDisSym)),
    ('num_labels', c_size_t),
    ('inst_type', QDisInstType),
    ('inst_size', c_size_t),
    ('inst_text', String),
    ('_padding', c_size_t * 8),
]

QDisResult = struct_anon_33 # qdis.h: 414

enum_anon_34 = c_int # qdis.h: 437

QDIS_INFO_OP = 1 # qdis.h: 437

QDIS_INFO_COND = 2 # qdis.h: 437

QDIS_INFO_CALLFLAG = 3 # qdis.h: 437

QDIS_INFO_NUM_OPS = 256 # qdis.h: 437

QDIS_INFO_HELPER = 513 # qdis.h: 437

QDIS_INFO_HELPER_BY_ADDR = 514 # qdis.h: 437

QDIS_INFO_GLOBAL = 515 # qdis.h: 437

QDIS_INFO_PC_OFFSET = 768 # qdis.h: 437

QDIS_INFO_SP_OFFSET = 769 # qdis.h: 437

QDIS_INFO_PC_GLOBAL = 770 # qdis.h: 437

QDIS_INFO_SP_GLOBAL = 771 # qdis.h: 437

QDIS_INFO_NUM_HELPERS = 772 # qdis.h: 437

QDIS_INFO_NUM_GLOBALS = 773 # qdis.h: 437

QDIS_INFO_GLOBAL_SIZE = 774 # qdis.h: 437

QDIS_INFO_GLOBAL_OFFSET = 775 # qdis.h: 437

QDIS_INFO_STATE_SIZE = 776 # qdis.h: 437

QDisInfoType = enum_anon_34 # qdis.h: 437

enum_anon_35 = c_int # qdis.h: 449

QDIS_CALL_NO_READ_GLOBALS = 16 # qdis.h: 449

QDIS_CALL_NO_WRITE_GLOBALS = 32 # qdis.h: 449

QDIS_CALL_NO_SIDE_EFFECTS = 64 # qdis.h: 449

QDisCallFlags = enum_anon_35 # qdis.h: 449

enum_anon_36 = c_int # qdis.h: 457

QDIS_HELPER_GET_TB_CPU_STATE = 1 # qdis.h: 457

QDIS_HELPER_GET_CPU_STATE_TB = 2 # qdis.h: 457

QDisHelperID = enum_anon_36 # qdis.h: 457

# qdis.h: 464
if hasattr(_libs['qdis'], 'qdis_Create'):
    qdis_Create = _libs['qdis'].qdis_Create
    qdis_Create.argtypes = [QDisTarget, POINTER(QDisCPUFeature)]
    qdis_Create.restype = POINTER(QDisassembler)

# qdis.h: 469
if hasattr(_libs['qdis'], 'qdis_Disassemble'):
    qdis_Disassemble = _libs['qdis'].qdis_Disassemble
    qdis_Disassemble.argtypes = [POINTER(QDisassembler), POINTER(c_uint8), c_size_t, c_uint64, c_uint64, c_uint32, POINTER(None), c_size_t]
    qdis_Disassemble.restype = QDisStatus

# qdis.h: 475
if hasattr(_libs['qdis'], 'qdis_LookupName'):
    qdis_LookupName = _libs['qdis'].qdis_LookupName
    qdis_LookupName.argtypes = [POINTER(QDisassembler), QDisInfoType, c_size_t]
    if sizeof(c_int) == sizeof(c_void_p):
        qdis_LookupName.restype = ReturnString
    else:
        qdis_LookupName.restype = String
        qdis_LookupName.errcheck = ReturnString

# qdis.h: 479
if hasattr(_libs['qdis'], 'qdis_LookupValue'):
    qdis_LookupValue = _libs['qdis'].qdis_LookupValue
    qdis_LookupValue.argtypes = [POINTER(QDisassembler), QDisInfoType, c_size_t]
    qdis_LookupValue.restype = c_size_t

# qdis.h: 483
if hasattr(_libs['qdis'], 'qdis_GetHelper'):
    qdis_GetHelper = _libs['qdis'].qdis_GetHelper
    qdis_GetHelper.argtypes = [POINTER(QDisassembler), QDisVal, POINTER(None), c_size_t]
    qdis_GetHelper.restype = QDisStatus

# qdis.h: 487
if hasattr(_libs['qdis'], 'qdis_Dump'):
    qdis_Dump = _libs['qdis'].qdis_Dump
    qdis_Dump.argtypes = [POINTER(QDisassembler)]
    qdis_Dump.restype = None

# qdis.h: 491
if hasattr(_libs['qdis'], 'qdis_Destroy'):
    qdis_Destroy = _libs['qdis'].qdis_Destroy
    qdis_Destroy.argtypes = [POINTER(QDisassembler)]
    qdis_Destroy.restype = None

# qdis.h: 94
try:
    QDIS_INST_ARM_THUMB_SHIFT = 0
except:
    pass

# qdis.h: 95
try:
    QDIS_INST_ARM_THUMB_MASK = (1 << QDIS_INST_ARM_THUMB_SHIFT)
except:
    pass

# qdis.h: 96
try:
    QDIS_INST_ARM_VECLEN_SHIFT = 1
except:
    pass

# qdis.h: 97
try:
    QDIS_INST_ARM_VECLEN_MASK = (7 << QDIS_INST_ARM_VECLEN_SHIFT)
except:
    pass

# qdis.h: 98
try:
    QDIS_INST_ARM_VECSTRIDE_SHIFT = 4
except:
    pass

# qdis.h: 99
try:
    QDIS_INST_ARM_VECSTRIDE_MASK = (3 << QDIS_INST_ARM_VECSTRIDE_SHIFT)
except:
    pass

# qdis.h: 100
try:
    QDIS_INST_ARM_PRIV_SHIFT = 6
except:
    pass

# qdis.h: 101
try:
    QDIS_INST_ARM_PRIV_MASK = (1 << QDIS_INST_ARM_PRIV_SHIFT)
except:
    pass

# qdis.h: 102
try:
    QDIS_INST_ARM_VFPEN_SHIFT = 7
except:
    pass

# qdis.h: 103
try:
    QDIS_INST_ARM_VFPEN_MASK = (1 << QDIS_INST_ARM_VFPEN_SHIFT)
except:
    pass

# qdis.h: 104
try:
    QDIS_INST_ARM_CONDEXEC_SHIFT = 8
except:
    pass

# qdis.h: 105
try:
    QDIS_INST_ARM_CONDEXEC_MASK = (255 << QDIS_INST_ARM_CONDEXEC_SHIFT)
except:
    pass

# qdis.h: 106
try:
    QDIS_INST_ARM_BSWAP_CODE_SHIFT = 16
except:
    pass

# qdis.h: 107
try:
    QDIS_INST_ARM_BSWAP_CODE_MASK = (1 << QDIS_INST_ARM_BSWAP_CODE_SHIFT)
except:
    pass

# qdis.h: 110
try:
    QDIS_INST_X86_CPL_SHIFT = 0
except:
    pass

# qdis.h: 111
try:
    QDIS_INST_X86_SOFTMMU_SHIFT = 2
except:
    pass

# qdis.h: 112
try:
    QDIS_INST_X86_INHIBIT_IRQ_SHIFT = 3
except:
    pass

# qdis.h: 113
try:
    QDIS_INST_X86_CS32_SHIFT = 4
except:
    pass

# qdis.h: 114
try:
    QDIS_INST_X86_SS32_SHIFT = 5
except:
    pass

# qdis.h: 115
try:
    QDIS_INST_X86_ADDSEG_SHIFT = 6
except:
    pass

# qdis.h: 116
try:
    QDIS_INST_X86_PE_SHIFT = 7
except:
    pass

# qdis.h: 117
try:
    QDIS_INST_X86_TF_SHIFT = 8
except:
    pass

# qdis.h: 118
try:
    QDIS_INST_X86_MP_SHIFT = 9
except:
    pass

# qdis.h: 119
try:
    QDIS_INST_X86_EM_SHIFT = 10
except:
    pass

# qdis.h: 120
try:
    QDIS_INST_X86_TS_SHIFT = 11
except:
    pass

# qdis.h: 121
try:
    QDIS_INST_X86_IOPL_SHIFT = 12
except:
    pass

# qdis.h: 122
try:
    QDIS_INST_X86_LMA_SHIFT = 14
except:
    pass

# qdis.h: 123
try:
    QDIS_INST_X86_CS64_SHIFT = 15
except:
    pass

# qdis.h: 124
try:
    QDIS_INST_X86_RF_SHIFT = 16
except:
    pass

# qdis.h: 125
try:
    QDIS_INST_X86_VM_SHIFT = 17
except:
    pass

# qdis.h: 126
try:
    QDIS_INST_X86_AC_SHIFT = 18
except:
    pass

# qdis.h: 127
try:
    QDIS_INST_X86_SMM_SHIFT = 19
except:
    pass

# qdis.h: 128
try:
    QDIS_INST_X86_SVME_SHIFT = 20
except:
    pass

# qdis.h: 129
try:
    QDIS_INST_X86_SVMI_SHIFT = 21
except:
    pass

# qdis.h: 130
try:
    QDIS_INST_X86_OSFXSR_SHIFT = 22
except:
    pass

# qdis.h: 131
try:
    QDIS_INST_X86_SMAP_SHIFT = 23
except:
    pass

# qdis.h: 133
try:
    QDIS_INST_X86_CPL_MASK = (3 << QDIS_INST_X86_CPL_SHIFT)
except:
    pass

# qdis.h: 134
try:
    QDIS_INST_X86_SOFTMMU_MASK = (1 << QDIS_INST_X86_SOFTMMU_SHIFT)
except:
    pass

# qdis.h: 135
try:
    QDIS_INST_X86_INHIBIT_IRQ_MASK = (1 << QDIS_INST_X86_INHIBIT_IRQ_SHIFT)
except:
    pass

# qdis.h: 136
try:
    QDIS_INST_X86_CS32_MASK = (1 << QDIS_INST_X86_CS32_SHIFT)
except:
    pass

# qdis.h: 137
try:
    QDIS_INST_X86_SS32_MASK = (1 << QDIS_INST_X86_SS32_SHIFT)
except:
    pass

# qdis.h: 138
try:
    QDIS_INST_X86_ADDSEG_MASK = (1 << QDIS_INST_X86_ADDSEG_SHIFT)
except:
    pass

# qdis.h: 139
try:
    QDIS_INST_X86_PE_MASK = (1 << QDIS_INST_X86_PE_SHIFT)
except:
    pass

# qdis.h: 140
try:
    QDIS_INST_X86_TF_MASK = (1 << QDIS_INST_X86_TF_SHIFT)
except:
    pass

# qdis.h: 141
try:
    QDIS_INST_X86_MP_MASK = (1 << QDIS_INST_X86_MP_SHIFT)
except:
    pass

# qdis.h: 142
try:
    QDIS_INST_X86_EM_MASK = (1 << QDIS_INST_X86_EM_SHIFT)
except:
    pass

# qdis.h: 143
try:
    QDIS_INST_X86_TS_MASK = (1 << QDIS_INST_X86_TS_SHIFT)
except:
    pass

# qdis.h: 144
try:
    QDIS_INST_X86_IOPL_MASK = (3 << QDIS_INST_X86_IOPL_SHIFT)
except:
    pass

# qdis.h: 145
try:
    QDIS_INST_X86_LMA_MASK = (1 << QDIS_INST_X86_LMA_SHIFT)
except:
    pass

# qdis.h: 146
try:
    QDIS_INST_X86_CS64_MASK = (1 << QDIS_INST_X86_CS64_SHIFT)
except:
    pass

# qdis.h: 147
try:
    QDIS_INST_X86_RF_MASK = (1 << QDIS_INST_X86_RF_SHIFT)
except:
    pass

# qdis.h: 148
try:
    QDIS_INST_X86_VM_MASK = (1 << QDIS_INST_X86_VM_SHIFT)
except:
    pass

# qdis.h: 149
try:
    QDIS_INST_X86_AC_MASK = (1 << QDIS_INST_X86_AC_SHIFT)
except:
    pass

# qdis.h: 150
try:
    QDIS_INST_X86_SMM_MASK = (1 << QDIS_INST_X86_SMM_SHIFT)
except:
    pass

# qdis.h: 151
try:
    QDIS_INST_X86_SVME_MASK = (1 << QDIS_INST_X86_SVME_SHIFT)
except:
    pass

# qdis.h: 152
try:
    QDIS_INST_X86_SVMI_MASK = (1 << QDIS_INST_X86_SVMI_SHIFT)
except:
    pass

# qdis.h: 153
try:
    QDIS_INST_X86_OSFXSR_MASK = (1 << QDIS_INST_X86_OSFXSR_SHIFT)
except:
    pass

# qdis.h: 154
try:
    QDIS_INST_X86_SMAP_MASK = (1 << QDIS_INST_X86_SMAP_SHIFT)
except:
    pass

# qdis.h: 157
try:
    QDIS_IFLAGS_DEFAULT_ARM = QDIS_INST_ARM_VFPEN_MASK
except:
    pass

# qdis.h: 158
try:
    QDIS_IFLAGS_DEFAULT_THUMB = (QDIS_INST_ARM_VFPEN_MASK | QDIS_INST_ARM_THUMB_MASK)
except:
    pass

# qdis.h: 159
try:
    QDIS_IFLAGS_DEFAULT_I386 = ((QDIS_INST_X86_PE_MASK | QDIS_INST_X86_CS32_MASK) | QDIS_INST_X86_SS32_MASK)
except:
    pass

# qdis.h: 160
try:
    QDIS_IFLAGS_DEFAULT_AMD64 = ((((QDIS_INST_X86_PE_MASK | QDIS_INST_X86_CS32_MASK) | QDIS_INST_X86_SS32_MASK) | QDIS_INST_X86_CS64_MASK) | QDIS_INST_X86_LMA_MASK)
except:
    pass

# qdis.h: 394
try:
    QDIS_BUFFER_SIZE = 16384
except:
    pass

# qdis.h: 397
try:
    QDIS_INVALID = (-1)
except:
    pass

QDisassembler_ = struct_QDisassembler_ # qdis.h: 163

# No inserted files

