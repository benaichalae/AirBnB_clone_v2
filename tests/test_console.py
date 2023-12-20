#!/usr/bin/python3
"""Unit tests for the Console module"""

import unittest
from unittest.mock import patch
from io import StringIO
import pep8
import os
import json
from console import HBNBCommand
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models.engine.file_storage import FileStorage


class TestConsole(unittest.TestCase):
    """Test cases for the Console module"""

    @classmethod
    def setUpClass(cls):
        """Set up for the tests"""
        cls.console = HBNBCommand()

    @classmethod
    def tearDownClass(cls):
        """Clean up after the tests"""
        del cls.console

    def tearDown(self):
        """Remove temporary file (file.json) created as a result"""
        try:
            os.remove("file.json")
        except Exception:
            pass

    def test_pep8_console(self):
        """Pep8 console.py"""
        style = pep8.StyleGuide(quiet=True)
        p = style.check_files(["console.py"])
        self.assertEqual(p.total_errors, 0, 'fix Pep8')

    def test_docstrings_in_console(self):
        """Checking for docstrings"""
        self.assertIsNotNone(console.__doc__)
        self.assertIsNotNone(HBNBCommand.emptyline.__doc__)
        self.assertIsNotNone(HBNBCommand.do_quit.__doc__)
        self.assertIsNotNone(HBNBCommand.do_EOF.__doc__)
        self.assertIsNotNone(HBNBCommand.do_create.__doc__)
        self.assertIsNotNone(HBNBCommand.do_show.__doc__)
        self.assertIsNotNone(HBNBCommand.do_destroy.__doc__)
        self.assertIsNotNone(HBNBCommand.do_all.__doc__)
        self.assertIsNotNone(HBNBCommand.do_update.__doc__)
        self.assertIsNotNone(HBNBCommand.count.__doc__)
        self.assertIsNotNone(HBNBCommand.strip_clean.__doc__)
        self.assertIsNotNone(HBNBCommand.default.__doc__)

    def test_emptyline(self):
        """Test empty line input"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("\n")
            self.assertEqual('', f.getvalue())

    def test_quit(self):
        """Test quit command input"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("quit")
            self.assertEqual('', f.getvalue())

    @unittest.skipIf(os.getenv("HBNB_TYPE_STORAGE") == "db", "No apply for db")
    def test_create(self):
        """Test create command input"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("create")
            self.assertEqual(
                "** class name missing **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("create asdfsfsd")
            self.assertEqual(
                "** class doesn't exist **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("create User")
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("all User")
            self.assertEqual(
                "[[User]", f.getvalue()[:7])

        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd('create State name="California"\
            lat=7.5 zip=513')
            obj_id = f.getvalue().strip("\n")
        all_dict = storage.all()
        class_key = "State."
        s_name = all_dict[class_key + obj_id].name
        s_lat = all_dict[class_key + obj_id].lat
        s_zip = all_dict[class_key + obj_id].zip
        self.assertEqual(s_name, "California")
        self.assertTrue(isinstance(s_name, str))
        self.assertEqual(s_lat, 7.5)
        self.assertTrue(isinstance(s_lat, float))
        self.assertEqual(s_zip, 513)
        self.assertTrue(isinstance(s_zip, int))

        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd('create User name="Larry_Moon"\
            nik="El\\"Macho"')
            obj_id = f.getvalue().strip("\n")
        all_dict = storage.all()
        class_key = "User."
        u_name = all_dict[class_key + obj_id].name
        u_nick = all_dict[class_key + obj_id].nik
        self.assertEqual(u_name, "Larry Moon")
        self.assertTrue(isinstance(u_name, str))
        self.assertEqual(u_nick, 'El"Macho')
        self.assertTrue(isinstance(u_nick, str))

    def test_show(self):
        """Test show command input"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("show")
            self.assertEqual(
                "** class name missing **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("show asdfsdrfs")
            self.assertEqual(
                "** class doesn't exist **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("show BaseModel")
            self.assertEqual(
                "** instance id missing **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("show BaseModel abcd-123")
            self.assertEqual(
                "** no instance found **\n", f.getvalue())

   def test_destroy(self):
    """Test alternate destroy command input"""
    with patch('sys.stdout', new=StringIO()) as f:
        self.consol.onecmd("Galaxy.destroy()")
        self.assertEqual(
            "** class doesn't exist **\n", f.getvalue())
    with patch('sys.stdout', new=StringIO()) as f:
        self.consol.onecmd("User.destroy(12345)")
        self.assertEqual(
            "** no instance found **\n", f.getvalue())

    @unittest.skipIf(os.getenv("HBNB_TYPE_STORAGE") == "db", "No apply for db")
    def test_update(self):
        """Test alternate update command input"""
    with patch('sys.stdout', new=StringIO()) as f:
        self.consol.onecmd("sldkfjsl.update()")
        self.assertEqual(
            "** class doesn't exist **\n", f.getvalue())
    with patch('sys.stdout', new=StringIO()) as f:
        self.consol.onecmd("User.update(12345)")
        self.assertEqual(
            "** no instance found **\n", f.getvalue())
    with patch('sys.stdout', new=StringIO()) as f:
        self.consol.onecmd("all User")
        obj = f.getvalue()
    my_id = obj[obj.find('(') + 1:obj.find(')')]
    with patch('sys.stdout', new=StringIO()) as f:
        self.consol.onecmd("User.update(" + my_id + ")")
        self.assertEqual(
            "** attribute name missing **\n", f.getvalue())
    with patch('sys.stdout', new=StringIO()) as f:
        self.consol.onecmd("User.update(" + my_id + ", name)")
        self.assertEqual(
            "** value missing **\n", f.getvalue())

if __name__ == "__main__":
    unittest.main()

