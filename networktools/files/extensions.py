import os, sys

try: 
    ONLINE = eval(os.environ['ONLINE'])
except: 
    print """You must set ONLINE env variable first.\nIt can either be 0 or 1."""
    sys.exit()


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