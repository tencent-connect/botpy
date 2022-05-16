#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import unittest

from botpy.core.util.json_util import JsonUtil


class JsonUtilTestCase(unittest.TestCase):
    def test_json2obj(self):
        class Score:
            def __init__(self):
                self.chinese = ""
                self.math = ""

        class Book:
            def __init__(self):
                self.type = ""
                self.name = ""

        class Student:
            def __init__(self, data=None):
                self.books = [Book()]
                self.score = Score()
                self.name = ""
                self.id = ""
                if data:
                    self.__dict__ = data

        json_str = (
            '{"id":"123", "score":{"math":100, "chinese":98}, '
            '"books":[{"name":"math", "type":"study"}, '
            '{"name":"The Little Prince", "type":"literature"}]} '
        )
        # student = Student()
        # JsonUtil.json_str2obj(json_data, student)
        test: Student = json.loads(json_str, object_hook=Student)
        print(isinstance(test, Student))
        print(test.__dict__)
        self.assertEqual("123", test.id)  # add assertion here
        self.assertEqual("math", test.books[0].name)  # add assertion here

    def test_obj2json(self):
        class Person:
            def __init__(self, data=None):
                self.name = ""
                self.surname = ""
                if data:
                    self.__dict__ = data

        person = Person()
        person.name = "Hello"
        person.surname = "World"
        json_str = JsonUtil.obj2json_str(person)

        person2 = json.loads(json_str, object_hook=Person)
        self.assertEqual("Hello", person2.name)  # add assertion


if __name__ == "__main__":
    unittest.main()
