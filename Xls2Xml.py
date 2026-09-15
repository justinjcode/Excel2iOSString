# -*- coding:utf-8 -*-

from optparse import OptionParser

import XmlFileUtil
from XlsFileUtil import XlsFileUtil
from StringsFileUtil import StringsFileUtil
from Log import Log
import os
import time


LATIN_LANGUAGE_CODES = frozenset({
    "af", "az", "bs", "ca", "cs", "cy", "da", "de", "en", "es",
    "et", "eu", "fi", "fr", "ga", "gl", "hr", "hu", "id", "is",
    "it", "la", "lt", "lv", "ms", "mt", "nl", "no", "pl", "pt",
    "ro", "sk", "sl", "sq", "sv", "sw", "tr", "vi",
})
LATIN_APOSTROPHE_TRANSLATION = str.maketrans({
    "‘": "'",
    "’": "'",
    "＇": "'",
})


def is_latin_language(language):
    """Return whether a language header identifies a Latin-script locale."""
    if language is None:
        return False

    language_code = str(language).strip().replace("_", "-").split("-")[0].lower()
    return language_code in LATIN_LANGUAGE_CODES


def normalize_latin_apostrophes(value, language=None):
    """Normalize typographic/full-width apostrophes in Latin locales."""
    if value is None:
        return None

    value = str(value)
    if not is_latin_language(language):
        return value

    return value.translate(LATIN_APOSTROPHE_TRANSLATION)


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
                    # 第一行不是词条，跳过
                    if cell.row == 1:
                        continue
                    keys.append(cell.value)
                # 每一列对应一种语言
                for column in sheet.columns:
                    if isCellNotEmpty(column[0]):
                        language = str(column[0].value).strip()
                        values = []
                        for cell in column:
                            if cell.row == 1:
                                # 第一行不是词条，跳过
                                continue
                            else:
                                values.append(escape_android_string_value(cell.value, language))
                        XmlFileUtil.write_localization_xml(xlsxFolderPath + "/values-" + language + "/", file_name + ".xml", keys, values)
        print('Convert %s successfully! you can see strings file in %s' % (fileDir, targetDir))


def escape_android_string_value(value, language=None):
    """Escape apostrophes in a value according to Android string rules.

    XML permits an apostrophe in element text, but Android resource values
    require it to be escaped with a backslash. Latin locale values are
    normalized first so typographic/full-width apostrophes from Excel do not
    leak into the generated resource. Keep an existing escape intact and
    account for an even number of preceding backslashes, where the apostrophe
    would still be unescaped by Android's resource parser.
    """
    value = normalize_latin_apostrophes(value, language)
    if value is None:
        return None

    if "'" not in value:
        return value

    escaped_value = []
    preceding_backslashes = 0
    for character in value:
        if character == "'":
            if preceding_backslashes % 2 == 0:
                escaped_value.append("\\")
            escaped_value.append(character)
            preceding_backslashes = 0
        else:
            escaped_value.append(character)
            if character == "\\":
                preceding_backslashes += 1
            else:
                preceding_backslashes = 0

    return "".join(escaped_value)


def isCellNotEmpty(cell):
    value = cell.value
    if value is not None:
        s = str(cell.value)
        return s.strip() is not None and len(s.strip()) > 0
    else:
        return False


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


if __name__ == '__main__':
    main()
