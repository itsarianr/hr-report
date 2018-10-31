import os


DIRECTORY_PATH = r"C:\Users\ASUS\Dropbox\Dunro - Reports"


class Date:
    def __init__(self, str_date=None):
        str_splitted_date = str_date.split('-')
        self.year = int(str_splitted_date[0])
        self.month = int(str_splitted_date[1])
        self.day = int(str_splitted_date[2])

    def get_tommorow(self):
        tommorow = Date(self.get_str())
        if self.day == 31:
            if self.month == 12:
                tommorow.year = self.year + 1
                tommorow.month = 1
                tommorow.day = 1
                return tommorow
            tommorow.month = self.month + 1
            tommorow.day = 1
            return tommorow
        tommorow.day = self.day + 1
        return tommorow

    def get_str(self):
        return str(self.year) + '-' + str(self.month).zfill(2) + '-' + str(self.day).zfill(2)

    def equals(self, date):
        return self.get_str() == date.get_str()

    def get_directory_path(self):
        return os.path.join(DIRECTORY_PATH, str(self.year), str(
            self.month).zfill(2), self.get_str())
