"""
Contains base and derived classes of Error objects.
Errors created regarding database entries
"""

class Error(object):
    def __init__(self, cause):
        self.cause = str(cause)
    def name(self):
        return self.__class__.__name__

class NameError(Error):
    def __str__(self):
        return "Error: Name '{}' is invalid.".format(self.cause)

class AddressError(Error):
    def __str__(self):
        return "Error: Address '{}' is invalid.".format(self.cause)

class DateError(Error):
    def __str__(self):
        return "Error: Date '{}' is ".format(self.cause) + \
               "invalid. Must be of the form YYYY-MM-DD"
