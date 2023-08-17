#!/usr/bin/python
# -*- coding: UTF-8 -*-

# import xlrd
import sys
import os

import importlib
import  openpyxl
from openpyxl import Workbook

class XlsFileUtil:
    'xls file util'

    def __init__(self, filePath):
        self.filePath = filePath
        # get all sheets
        importlib.reload(sys)
        # sys.setdefaultencoding('utf-8')
        self.data = openpyxl.load_workbook(filePath)
        # self.data = xlrd.open_workbook(filePath)

    def getAllTables(self):
        return self.data.worksheets

    def getTableByIndex(self, index):
        if index >= 0 and index < len(self.data.worksheets):
            return self.data.worksheets[index]
        else:
            print("XlsFileUtil error -- getTable:index")

    # def getTableByName(self, name):
    #     return self.data.sheet_by_name(name)
