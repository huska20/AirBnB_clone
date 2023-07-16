#!/usr/bin/python3

"""__init__the method for models directory"""
from models.engine.file_storage import FileStorage

storage = FileStorage()
storage.reload()
