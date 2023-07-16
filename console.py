#!/usr/bin/python3
"""
    Entry point of the command interpreter
"""
import cmd
import sys
import models
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class HBNBCommand(cmd.Cmd):
    prompt = '(hbnb) '

    def do_quit(self, arg):
        """Quit command to exit the program"""
        return True

    def do_EOF(self, arg):
        """EOF command to exit the program"""
        print()
        return True

    def emptyline(self):
        """Handles empty lines"""
        pass

    def do_create(self, arg):
        """Creates a new instance of BaseModel"""
        if not arg:
            print("** class name missing **")
            return
        try:
            new_instance = eval(arg)()
            new_instance.save()
            print(new_instance.id)
        except NameError:
            print("** class doesn't exist **")

    def do_show(self, arg):
        """Prints the string representation of an instance"""
        if not arg:
            print("** class name missing **")
            return
        arg_list = arg.split()
        if arg_list[0] not in models.classes.keys():
            print("** class doesn't exist **")
            return
        if len(arg_list) < 2:
            print("** instance id missing **")
            return
        key = "{}.{}".format(arg_list[0], arg_list[1])
        objects = models.storage.all()
        if key in objects:
            print(objects[key])
        else:
            print("** no instance found **")

    def do_destroy(self, arg):
        """Deletes an instance based on the class name and id"""
        if not arg:
            print("** class name missing **")
            return
        arg_list = arg.split()
        if arg_list[0] not in models.classes.keys():
            print("** class doesn't exist **")
            return
        if len(arg_list) < 2:
            print("** instance id missing **")
            return
        key = "{}.{}".format(arg_list[0], arg_list[1])
        objects = models.storage.all()
        if key in objects:
            del objects[key]
            models.storage.save()
        else:
            print("** no instance found **")

    def do_all(self, arg):
        """Prints all string representations of instances"""
        objects = models.storage.all()
        if not arg:
            print([str(obj) for obj in objects.values()])
        else:
            arg_list = arg.split()
            if arg_list[0] not in models.classes.keys():
                print("** class doesn't exist **")
                return
            print([str(obj) for obj in objects.values() if
                   type(obj).__name__ == arg_list[0]])

    def do_update(self, arg):
        """Updates an instance based on the class name and id"""
        if not arg:
            print("** class name missing **")
            return
        arg_list = arg.split()
        if arg_list[0] not in models.classes.keys():
            print("** class doesn't exist **")
            return
        if len(arg_list) < 2:
            print("** instance id missing **")
            return
        key = "{}.{}".format(arg_list[0], arg_list[1])
        objects = models.storage.all()
        if key not in objects:
            print("** no instance found **")
            return
        if len(arg_list) < 3:
            print("** attribute name missing **")
            return
        if len(arg_list) < 4:
            print("** value missing **")
            return
        setattr(objects[key], arg_list[2], arg_list[3])
        models.storage.save()

    def default(self, arg):
        """Default behavior for command not found"""
        cmd_list = arg.split('.')
        if len(cmd_list) >= 2 and cmd_list[0] in models.classes.keys():
            if cmd_list[1] == "all()":
                self.do_all(cmd_list[0])
            elif cmd_list[1] == "count()":
                count = sum([1 for obj in models.storage.all().values()
                             if type(obj).__name__ == cmd_list[0]])
                print(count)
            else:
                cmd_str = "{} {}".format(cmd_list[0], cmd_list[1])
                if cmd_list[1].startswith("show"):
                    self.do_show(cmd_str)
                elif cmd_list[1].startswith("destroy"):
                    self.do_destroy(cmd_str)
                elif cmd_list[1].startswith("update"):
                    attr_list = cmd_list[1].split('(')[1].split(')')[0]
                    attr_args = attr_list.split(', ')
                    attr_args.insert(0, cmd_list[0])
                    self.do_update(' '.join(attr_args))
                else:
                    print("*** Unknown syntax: {}".format(arg))
        else:
            print("*** Unknown syntax: {}".format(arg))


if __name__ == '__main__':
    HBNBCommand().cmdloop()

