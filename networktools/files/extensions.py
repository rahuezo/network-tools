import os, sys


class ExtensionHandler: 
    """
    This class is used to detect the extension of a file.
    """

    def __init__(self, f):         
        self.f = f
        self.filename = f.name 

    def get_extension(self): 
        extension = self.filename[::-1].split('.')[0][::-1].lower()
        return extension if len(extension) else None