# utility script to perform file & folder operations

import os


class FileHandler:

    def list_files(self, directory):
        return os.listdir(directory)

    def read_file(self, filename):
        with open(filename, 'r', encoding='latin1') as file:
            return file.read()
