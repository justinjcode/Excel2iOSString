import os
import xml.etree.ElementTree as ET
from xml.dom import minidom


def write_localization_xml( directory, filename, keys, values):
    if not os.path.exists(directory):
        os.makedirs(directory)
    # 创建<resources>根元素
    resources = ET.Element("resources")

    # 将每个key-value对添加到<resources>中
    for key, value in zip(keys, values):
        string_element = ET.SubElement(resources, "string", name=key)
        string_element.text = value

    # 将XML转换为字符串，并格式化
    xml_str = ET.tostring(resources, encoding='utf-8')
    parsed_xml = minidom.parseString(xml_str)
    pretty_xml_as_string = parsed_xml.toprettyxml(indent="    ")

    # 写入文件
    with open(directory + '/' + filename, 'w', encoding='utf-8') as xml_file:
        xml_file.write(pretty_xml_as_string)

