class ExtensionHandler: 
    """
    This class is used to detect the extension of a file.
    """

    def __init__(self, input_file): 
        self.input_file = input_file

    def get_extension(self): 
        extension = self.input_file[::-1].split('.')[0][::-1].lower()
        return extension if len(extension) else None