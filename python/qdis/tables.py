'''
Tables with higher-level information about enums in qdis.
'''
import qdis
from collections import namedtuple

# Instruction type properties
ITP = namedtuple('ITP', ['is_jump', 'is_call', 'is_return', 'name'])
ITYPE = {
qdis.ITYPE_UNKNOWN: ITP(  False,     False,     False,      'UNKNOWN'),
qdis.ITYPE_DEFAULT: ITP(  False,     False,     False,      'DEFAULT'),
qdis.ITYPE_JMP:     ITP(  True,      False,     False,      'JMP'),
qdis.ITYPE_JMP_IND: ITP(  True,      False,     False,      'JMP_IND'),
qdis.ITYPE_COND_JMP:ITP(  True,      False,     False,      'COND_JMP'),
qdis.ITYPE_COND_JMP_IND:ITP(True,    False,     False,      'COND_JMP_IND'),
qdis.ITYPE_CALL:    ITP(  False,     True,      False,      'CALL'),
qdis.ITYPE_CALL_IND:ITP(  False,     True,      False,      'CALL_IND'),
qdis.ITYPE_REP:     ITP(  False,     False,     False,      'REP'),
qdis.ITYPE_RET:     ITP(  False,     False,     True,       'RET'),
}

