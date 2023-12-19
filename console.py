#!/usr/bin/python3
"""
Module containing the HBNBCommand class definition
"""

import cmd
import shlex
import models
from models.user import User
from models.city import City
from datetime import datetime
from models.state import State
from models.place import Place
from models.review import Review
from models.amenity import Amenity
from models.base_model import BaseModel

classes = {
            'BaseModel': BaseModel, 'User': User, 'Place': Place,
            'State': State, 'City': City, 'Amenity': Amenity,
            'Review': Review
            }


class HBNBCommand(cmd.Cmd):
    """Custom command-line interpreter for HBNB"""
    prompt = '(hbnb) '

    def do_EOF(self, arg):
        """Exits the console"""
        return True

    def emptyline(self):
        """Overwriting the emptyline method"""
        return False

    def do_quit(self, arg):
        """Quit command to exit the program"""
        return True

    def key_value_parser(self, args):
        """Parses a list of strings into a dictionary.
        Args:
            args (list): A list of strings in the format "key=value".
        Returns:
            dict: A dictionary with parsed key-value pairs.
        """
        new_dict = {}
        for arg in args:
            if "=" in arg:
                key, value = arg.split('=', 1)
                if value[0] == value[-1] == '"':
                    value = shlex.split(value)[0].replace('_', ' ')
                else:
                    try:
                        value = int(value)
                    except ValueError:
                        try:
                            value = float(value)
                        except ValueError:
                            continue
                new_dict[key] = value
        return new_dict

    def do_create(self, arg):
        """Create an object of any class"""
        args = arg.split()

        if not args:
            print("** class name missing **")
            return False

        class_name = args[0]

        if class_name not in classes:
            print("** class doesn't exist **")
            return False

        if len(args) > 1:
            new_dict = self.key_value_parser(args[1:])
            instance = classes[class_name](**new_dict)
        else:
            instance = classes[class_name]()

        print(instance.id)
        instance.save()

    def do_show(self, arg):
        """Method to show an individual object"""
        args = shlex.split(arg)

        if not args:
            print("** class name missing **")
            return False

        class_name = args[0]

        if class_name not in classes:
            print("** class doesn't exist **")
            return False

        if len(args) > 1:
            instance_id = args[1]
            key = f"{class_name}.{instance_id}"

            if key in models.storage.all():
                print(models.storage.all()[key])
            else:
                print("** no instance found **")
        else:
            print("** instance id missing **")

    def do_destroy(self, arg):
        """Destroys a specified object"""
        args = shlex.split(arg)

        if not args:
            print("** class name missing **")
        elif args[0] in classes:
            if len(args) > 1:
                instance_id = args[1]
                key = f"{args[0]}.{instance_id}"

                if key in models.storage.all():
                    del models.storage.all()[key]
                    models.storage.save()
                else:
                    print("** no instance found **")
            else:
                print("** instance id missing **")
        else:
            print("** class doesn't exist **")

    def do_all(self, arg):
        """ Shows all objects, or all objects of a class"""
        args = shlex.split(arg)
        obj_list = []

        if not args:
            obj_dict = models.storage.all()
        elif args[0] in classes:
            obj_dict = models.storage.all(classes[args[0]])
        else:
            print("** class doesn't exist **")
            return False

        for key in obj_dict:
            obj_list.append(str(obj_dict[key]))

        print("[", end="")
        print(", ".join(obj_list), end="")
        print("]")

    def do_update(self, arg):
        """ Updates a certain object with new info """
        try:
            if not line:
                raise SyntaxError()
            my_list = split(line, " ")
            if my_list[0] not in classes:
                raise NameError()
            if len(my_list) < 2:
                raise IndexError()

            key = my_list[0] + '.' + my_list[1]
            try:
                instance = models.storage.all()[key]
            except KeyError:
                raise KeyError("** no instance found **")

            if len(my_list) < 3:
                raise AttributeError("** attribute name missing **")
            if len(my_list) < 4:
                raise ValueError("** value missing **")

            attribute_name = my_list[2]
            try:
                value = eval(my_list[3])
            except Exception:
                value = my_list[3]

            setattr(instance, attribute_name, value)
            instance.save()

        except SyntaxError:
            print("** class name missing **")
        except NameError:
            print("** class doesn't exist **")
        except IndexError:
            print("** instance id missing **")
        except KeyError as e:
            print(str(e))
        except AttributeError as e:
            print(str(e))
        except ValueError as e:
            print(str(e))


if __name__ == '__main__':
    HBNBCommand().cmdloop()
