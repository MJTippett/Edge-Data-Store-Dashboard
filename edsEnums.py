'''
Defines some enumeration sets used by EDS
'''


from enum import Enum


# namespaces available in EDS, currently only default and diagnostics are allowed
class namespaces(Enum):
    default = 0
    diagnostics = 1


# Value boundary types for data calls
class sdsBoundaryType(Enum):
    exact = 0
    inside = 1
    outside = 2
    exactorcalculated = 3


# Modes for returning single (distinct) values
class sdsSearchMode(Enum):
    exact = 0
    exactornext = 1
    next = 2
    exactorprevious = 3
    previous = 4
