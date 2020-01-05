#!/usr/bin/python3
#
# __init__.py
#
# Definition for setup and export function, as well as the Table class
#
#from types import ClassType

import orm.easydb
from inspect import *

# all the classes that we export as a package
from orm.table import MetaTable
from orm.table import Table
from orm.fields import Integer, Float, String, Foreign, DateTime, Coordinate, datetime

# Return a database object that is initialized, but not yet connected.
#   database_name: str, database name
#   module: module, the module that contains the schema
def setup(database_name, module):
    # Check if the database name is "easydb".
    if database_name != "easydb":
        raise NotImplementedError("EasyORM has not implemented " + str(database_name))

    reserved_words = ["pk", "id", "version", "save", "delete"]
    schema = []

    #go through all of the classes
    for i in MetaTable.my_classes:
        schemaTup = []
        className = i.__name__
        members = MetaTable.my_attributes[i]
        #check to make sure that the class's module matches the module being passed in
        #duplicate class names may appear, but are a part of different modules
        if i.__module__ is module.__name__:
            fields = []
            schemaTup.append(className)

            for j in range(len(members)):
                memberField = list(members.items())[j][1]
                memberName = list(members.items())[j][0]
                #check if membername contains any reserved key words or underscores
                if memberName in reserved_words:
                    raise AttributeError

                if "_" in memberName:
                    raise AttributeError

                #set member with appropriate type
                if isinstance(memberField, orm.fields.String):
                    fields.append((memberName, str))
                elif isinstance(memberField, orm.fields.Float):
                    fields.append((memberName,float))
                elif isinstance(memberField, orm.fields.Integer):
                    fields.append((memberName,int))
                elif isinstance(memberField, orm.fields.Foreign):
                    attr = getattr(memberField, 'table')
                    fields.append((memberName, attr.__name__))
            schemaTup.append(tuple(fields))
            schema.append(tuple(schemaTup))

    return orm.easydb.Database(tuple(schema)) 

# Return a string which can be read by the underlying database to create the 
# corresponding database tables.
#   database_name: str, database name
#   module: module, the module that contains the schema
def export(database_name, module):
    # Check if the database name is "easydb".
    if database_name != "easydb":
        raise NotImplementedError("EasyORM has not implemented " + str(database_name))

    reserved_words = ["pk", "id", "version", "save", "delete"]
    # Implement me.
    schema = []
    for i in MetaTable.my_classes:
        className = i.__name__
        members = MetaTable.my_attributes[i]
        
        #check to make sure that the class's module matches the module being passed in
        #duplicate class names may appear, but are a part of different modules
        if i.__module__ is module.__name__:
            string = className + " {\n"

            for j in range(len(members)):
                memberField = list(members.items())[j][1]
                memberName = list(members.items())[j][0]

                #check if membername contains any reserved key words or underscores
                if memberName in reserved_words:
                    raise AttributeError

                if "_" in memberName:
                    raise AttributeError

                #set member with appropriate type
                if isinstance(memberField, orm.fields.String):
                    string += "    " + memberName + ": string;\n"
                elif isinstance(memberField, orm.fields.Float):
                    string += "    " + memberName + ": float;\n"
                elif isinstance(memberField, orm.fields.Integer):
                    string += "    " + memberName + ": integer;\n"
                elif isinstance(memberField, orm.fields.Foreign):
                    attr = getattr(memberField, 'table')
                    string += "    " + memberName + ": " + attr.__name__ + ";\n"
            string += "}\n"
            schema.append(string) 

    strSchema = '\n'.join(schema)
    return strSchema
