from extensions import ExtensionHandler
from sanitizer import sanitize_string


def read_docx(f):
    """
    This function gets the alphanumeric content in a docx file.

    Args:
        f: This is the input file to be read.

    Returns: 
        An alphanumeric string representation of the contents of f.
    
    Raises:
        ImportError: Module python-docx needs to be installed first.
    """ 
    try: 
        import docx
    except ImportError: 
        print 'You need to install docx. Try, sudo pip install python-docx'
        return None
    document = docx.Document(f)
    return ''.join([sanitize_string(p.text) for p in document.paragraphs])


def read_txt(f):
    """
    This function gets the alphanumeric content in a txt file.

    Args:
        f: This is the input file to be read.

    Returns: 
        An alphanumeric string representation of the contents of f.
    
    Raises:
        None.
    """ 
    with open(f, 'r') as input_file: 
        return sanitize_string(input_file.read())


class FileReader(ExtensionHandler): 
    """
    This class inherits from ExtensionHandler to detect file extensions
    and lets you read the contents of a file.
    """

    def __init__(self, input_file): 
        ExtensionHandler.__init__(self, input_file)

    def read(self): 
        extension = self.get_extension()

        if extension == 'docx': 
            return read_docx(self.input_file)

        elif extension == 'txt': 
            return read_txt(self.input_file)
        else: 
            print '\nThis is an unsupported file of type {}\n'.format(extension)
            return None
