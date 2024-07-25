# files/excel.py

from api.files.interfaces import IFile

class ExcelFile(IFile):
    def __init__(self) -> None:
        ...

    # Implement this later
    def validation(self):
        ...
        return True

    # Urgent Implementation
    def analysis(self):
        ...
    
    # Urgent Implementation
    def output(self):
        ...