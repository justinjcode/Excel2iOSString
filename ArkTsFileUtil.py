#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
from Log import Log
import codecs
import re
import io
import json


def removeComments(s):
    for x in re.findall(r'("[^\n]*"(?!\\))|(//[^\n]*$|/(?!\\)\*[\s\S]*?\*(?!\\)/)', s, 8):
        s = s.replace(x[1], '')
    return s


class ArkTsFileUtil:
    'ArkTs Localizable.strings file util'

    @staticmethod
    def writeToFile(keys, values, directory, name, additional):
        if not os.path.exists(directory):
            os.makedirs(directory)

        Log.info("Creating ArkTS strings file: " + os.path.join(directory, name))

        # 目标路径
        file_path = os.path.join(directory, name)

        string_items = []
        for x in range(len(keys)):
            key = str(keys[x]).strip()
            value = values[x]

            if value is None or value == '':
                Log.error(f"Key: {key}\'s value is None. Index: {x + 1}")
                continue

            string_items.append({
                "name": key,
                "value": str(value)
            })

        # 生成最终结构
        output_data = {
            "string": string_items
        }

        # 写入 JSON，再把转义的 \n 变成真实换行
        json_str = json.dumps(output_data, ensure_ascii=False, indent=2)
         # 再把 \\n 替换为 \n（保留为两个字符）
        json_str = json_str.replace('\\\\n', '\\n')

        with open(file_path, "w", encoding="utf-8") as fo:
            fo.write(json_str)

        Log.info("File generated successfully: " + file_path)

