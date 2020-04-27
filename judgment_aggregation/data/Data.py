import os
import shlex
from ..JAError import JAError


def get_file_in_path(file, path, get_all=False):
    """Get a file which can be found in one of the folders in the given path.
    """
    found_files = []
    for root, dirs, files in os.walk(path):
        if file in files:
            found_files.append(os.path.join(root, file))
            if not get_all:
                return found_files[0]
    return found_files


class Data:
    """Standard class for reading files and storing Data"""
    def __init__(self, path="./"):
        self.path = path
        self.reset()

    def reset(self):
        """Should reset the current Data object to have no contents whatsoever
        """
        raise NotImplementedError("Data object should not be directly created")

    def load_lines(self, iterable):
        """Load the contents of a iterable of strings, such as a file or
        list of strings. The strings need to be in the valid format
        args:
            iterable: the iterable object with the correctly formatted lines
            path: is used to resolve the location of files which may be needed
                by the scenario."""
        self.lines = 0
        for line in iterable:
            self.lines += 1
            contents = shlex.split(line.replace('\n', ''))
            if contents == []:
                continue
            fun = self.__getattribute__("load_" + contents[0] + "_line")
            fun(*contents[1:])
        self.lines = 0
        self.finalise()

    def load_c_line(self, *args):
        """Load a 'c' line; 'c' lines are comments, thus do nothing"""
        pass

    def load_string(self, string, delimiter='\n'):
        """"""
        self.load_lines(string.split(delimiter))

    def load_file(self, file):
        """"""
        if not os.path.isfile(file) and self.path:
            found = get_file_in_path(file, self.path)
            if found == []:
                self.throw_error("File '%s' not found in path '%s'" %
                                 (file, self.path))
            file = found

        with open(file, "r") as f:
            self.load_lines(f)

    def check_initialised(self):
        """Check if the Data object is initialised, and throw an error if it
        turns out to be not initialised."""
        if not self.p_initialised:
            self.throw_error(
                "Trying to add data to uninitialised %s object. "
                "Initialize the object by passing a file to the constructor or"
                " by using one of the initialisation functions." %
                type(self).__name__)

    def finalise(self):
        """Execute an eventual finalisation function."""
        pass

    def throw_error(self, message):
        """Throw an error while constructing the Data object"""
        if self.lines > 0:
            raise JAError(message + " on line %s" % self.lines)
        else:
            raise JAError(message)

    def merge_data(self, other):
        raise NotImplementedError("'merge_data' function not implemented "
                                  "for %s class" % type(self).__name__)
