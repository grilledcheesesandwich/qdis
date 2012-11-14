#!/bin/bash
# Generate Python binding for disass.h
# Uses http://code.google.com/p/ctypesgen/source/checkout
# Strip current path
DIR="$( cd -P "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
ctypesgen.py --strip-build-path=${DIR} -lqdis qdis.h -L . > qdis.py
