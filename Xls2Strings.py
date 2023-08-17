# -*- coding:utf-8 -*-

from optparse import OptionParser
from XlsFileUtil import XlsFileUtil
from StringsFileUtil import StringsFileUtil
from Log import Log
import os
import time


def addParser():
    parser = OptionParser()

    parser.add_option("-f", "--fileDir",
                      help="Xls files directory.",
                      metavar="fileDir")

    parser.add_option("-t", "--targetDir",
                      help="The directory where the strings files will be saved.",
                      metavar="targetDir")

    parser.add_option("-e", "--excelStorageForm",
                      type="string",
                      default="multiple",
                      help="The excel(.xls) file storage forms including single(single file), multiple(multiple files), default is multiple.",
                      metavar="excelStorageForm")

    parser.add_option("-a", "--additional",
                      help="additional info.",
                      metavar="additional")

    (options, args) = parser.parse_args()
    Log.info("options: %s, args: %s" % (options, args))

    return options

def convertFromMultipleForm(options, fileDir, targetDir):
    print('convertFromMultipleForm')
    for _, _, filenames in os.walk(fileDir):
        xlsFilenames = [fi for fi in filenames if fi.endswith(".xlsx")]
        # 遍历目录下的每个文件
        for file in xlsFilenames:
            xlsFileUtil = XlsFileUtil(fileDir + "/" + file)
            xlsxFolderPath = targetDir + "/" + file.replace(".xlsx", "")
            if not os.path.exists(xlsxFolderPath):
                print('makedirs %s', xlsxFolderPath)
                os.makedirs(xlsxFolderPath)
            # 处理每个表
            for sheet in xlsFileUtil.getAllTables():
                # 用sheet标题当做文件名
                file_name = sheet.title
                # 先取所有词条存到keys
                keys = []
                for cell in sheet['A']:
                    if isCellNotEmpty(cell):
                        keys.append(cell.value)
                # 每一列对应一种语言
                for column in sheet.columns:
                    if isCellNotEmpty(column[0]):
                        language = column[0].value
                        values = []
                        for cell in column:
                            if cell.row == 1:
                                # 第一行不是词条，跳过
                                continue
                            else:
                                values.append(cell.value)
                        StringsFileUtil.writeToFile(keys, values, xlsxFolderPath + "/" + language + ".lproj/",
                                                    file_name + ".strings", options.additional)
        print('Convert %s successfully! you can see strings file in %s' % (fileDir, targetDir))


def isCellNotEmpty(cell):
    str = cell.value
    return str is not None and str.strip() is not None and len(str.strip()) > 0


def startConvert(options):
    fileDir = options.fileDir
    targetDir = options.targetDir

    print('Start converting')

    if fileDir is None:
        print('xls files directory can not be empty! try -h for help.')
        return

    if targetDir is None:
        print('Target file directory can not be empty! try -h for help.')
        return

    targetDir = targetDir + "/xls-files-to-strings_" + \
                time.strftime("%Y%m%d_%H%M%S")
    if not os.path.exists(targetDir):
        os.makedirs(targetDir)

    convertFromMultipleForm(options, fileDir, targetDir)


def main():
    options = addParser()
    startConvert(options)


main()
