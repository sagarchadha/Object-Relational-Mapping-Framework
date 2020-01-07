#!/usr/bin/python3
#
# fields.py
#
# Definitions for all the fields in easyORM
#

from datetime import datetime

# base field type
class Field:
    implemented = True # boolean to check whether the field is implemented
    defaultValues = [0, 0., ""]
    defaultTypes = [int, float, str]

    def __init__(self, blank, default, choices, fType):

        if fType not in Field.defaultTypes:
            print("Field type is not an int, float or str")
            raise ValueError

        # check that the default is of the proper field type
        if not isinstance(default, fType):
            print("default value is not of type %s" %fType)
            raise TypeError
        
        #check if each element in choices is of the correct field type
        for i in choices:
            if not isinstance(i, fType):
                print("choice value is not of type %s" %fType)
                raise TypeError

        #if blank is true, see if default is valid
        if blank and default not in Field.defaultValues or not isinstance(default, fType):
            print("default must be specified")
            raise AttributeError
        else:
            self.blank = blank

        self.default = default
        self.choices = choices
        self.fType = fType


# INTEGER TYPE
class Integer(Field):
     def __init__(self, blank=False, default=0, choices=()):
        super().__init__(blank, default, choices, int)
       
# FLOAT TYPE
class Float(Field):
    def __init__(self, blank=False, default=0., choices=()):
        # if choices are either ints or floats, it passes
        super().__init__(blank, default, choices, float)

# STRING TYPE
class String(Field):
    def __init__(self, blank=False, default="", choices=()):
        # Implement or change me.
        super().__init__(blank, default, choices, str)
        
# FOREIGN KEY TYPE
class Foreign(Field):
    def __init__(self, table, blank=False):
        self.table = table
        self.blank = blank

# DATETIME TYPE
class DateTime(Field):
    implemented = False
    default = datetime.now()

# COORDINATE TYPE
class Coordinate(Field):
    implemented = False
