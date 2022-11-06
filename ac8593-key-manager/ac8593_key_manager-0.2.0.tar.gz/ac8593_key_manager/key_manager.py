
class KeyManager:

    """
    A class that manages keys for the user.
    input:
    :param filename: - name of a file which contains the key in a text format

    Description:
    Save the key in a .txt file and provide the name of the file to your key manager
    the key manager will load the key for you
    """

    def __init__(self,filename):
        key = None
        try:
            with open(filename,'r') as f:
                key = f.read()
        except:
            print('failed to load the key from the given filename')
        self.key = key
    
    def get_key(self):
        return self.key
         

