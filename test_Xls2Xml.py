import unittest
import xml.etree.ElementTree as ET
from pathlib import Path
from tempfile import TemporaryDirectory

from openpyxl import Workbook

import Xls2Xml


class Xls2XmlTests(unittest.TestCase):
    def test_escape_android_string_value(self):
        self.assertEqual(
            Xls2Xml.escape_android_string_value(
                "Riceverai un'email per reimpostare la password"
            ),
            "Riceverai un\\'email per reimpostare la password",
        )

    def test_does_not_double_escape_apostrophe(self):
        self.assertEqual(
            Xls2Xml.escape_android_string_value("L\\'amour"),
            "L\\'amour",
        )

    def test_normalizes_typographic_apostrophe_for_latin_language(self):
        self.assertEqual(
            Xls2Xml.escape_android_string_value(
                "Errore durante l’analisi della risposta", "it"
            ),
            "Errore durante l\\'analisi della risposta",
        )

    def test_preserves_typographic_apostrophe_for_non_latin_language(self):
        value = "保留 l’analisi"
        self.assertEqual(
            Xls2Xml.escape_android_string_value(value, "zh-Hans"),
            value,
        )

    def test_conversion_writes_android_escaped_value(self):
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            input_directory = root / "input"
            output_directory = root / "output"
            input_directory.mkdir()

            workbook = Workbook()
            sheet = workbook.active
            sheet.title = "strings"
            sheet.append(["key", "it"])
            sheet.append([
                "email_to_receive_code_description",
                "Riceverai un’email per reimpostare la password",
            ])
            workbook.save(input_directory / "strings.xlsx")

            Xls2Xml.convertFromMultipleForm(
                None, str(input_directory), str(output_directory)
            )

            output_file = (
                output_directory
                / "strings"
                / "values-it"
                / "strings.xml"
            )
            string_element = ET.parse(output_file).find("string")
            self.assertEqual(
                string_element.text,
                "Riceverai un\\'email per reimpostare la password",
            )


if __name__ == "__main__":
    unittest.main()
