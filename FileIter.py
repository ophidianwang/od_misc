# -*- coding: utf-8 -*-
"""
Created on Tue Dec 29 10:07:46 2015

@author: USER
"""
import json

class FileIter(object):
    """
    This class works like "with open(path,"r") as f" statement.
    usage:
    f = FileIter(path)
    for line in f:
        #do something
    """
    def __init__(self, file_path, limit=None):
        self.limit = limit
        self.file = open(file_path,"r")

    def __exit__(self, exc_type, exc_value, traceback):
        self.file.close()

    def __iter__(self):
        return self

    def __next__(self): # Python 2: def next(self)
        if self.limit is not None:
            if self.limit==0:
                raise StopIteration
            self.limit-=1
        line = self.file.readline()
        if line=='':
            raise StopIteration
        return line.strip()


class FieldIter(FileIter):
    """
    an iterable class on a specified field in a file (csv, tsv, json per line)
    """
    def __init__(self, file_path, file_type, field, limit=None):
        """
        specify type of the input file
        if it's a csv or tsv, the first line supposed to be header
        """
        super().__init__(file_path, limit)
        self.file_type = file_type
        if file_type=="csv":
            header = self.file.readline().strip().split(",")
            self.iter_field = header.index(field)
        elif file_type=="tsv":
            header = self.file.readline().strip().split("\t")
            self.iter_field = header.index(field)
        elif file_type=="json":
            self.iter_field = field
        else:
            raise AttributeError("file_type should be csv/tsv/json, given " + str(file_type))
            
    def __next__(self):
        """
        return the specified field
        """
        line = super().__next__()
        if self.file_type == "csv":
            fields = line.split(",")
        elif self.file_type == "tsv":
            fields = line.split("\t")
        elif self.file_type == "json":
            fields = json.loads(line)
        return fields[self.iter_field]
    

class FieldsIter(FileIter):
    """
    an iterable object on several specified fields in a file (csv, tsv, json per line)
    """
    def __init__(self, file_path, file_type, fields, limit=None):
        """
        specify type of the input file
        if it's a csv or tsv, the first line supposed to be header
        """
        super().__init__(file_path, limit)
        self.file_type = file_type
        self.iter_fields = []
        
        if file_type=="csv":
            header = self.file.readline().strip().split(",")
            for field in fields:
                index = header.index(field)
                if index!=-1:
                    self.iter_fields.append(  )
        elif file_type=="tsv":
            header = self.file.readline().strip().split("\t")
            for field in fields:
                index = header.index(field)
                if index!=-1:
                    self.iter_fields.append(  )
        elif file_type=="json":
            self.iter_fields = fields
        else:
            raise AttributeError("file_type should be csv/tsv/json, given " + str(file_type))
            
    def __next__(self):
        """
        return several specified field
        """
        line = super().__next__()
        if self.file_type == "csv":
            fields = line.split(",")
        elif self.file_type == "tsv":
            fields = line.split("\t")
        elif self.file_type == "json":
            fields = json.loads(line)
        return_fields = []
        for index in self.iter_fields:
            return_fields.append( fields[index] )
        return return_fields
        