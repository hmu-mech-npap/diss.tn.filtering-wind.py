'''Open a file.
Experiment with the qt5 framework and file dialogs.

Author : Papadakis Nikos
'''
# %%
#
# from PyQt5.QtCore import
import sys
from PyQt5.QtWidgets import QFileDialog, QWidget, QApplication
#
#                              QInputDialog, QLineEdit,
#                              )
# # from PyQt5.QtGui import QIcon
import matplotlib.pyplot as plt
import numpy as np


class App(QWidget):
    '''App constructor.
    create the basic dimentions for the dialog box.
    '''

    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 file dialogs - pythonspot.com'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.init_ui()

    def init_ui(self):
        '''Initialize a window with title and dimentions'''
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.filename = self.open_file_name_dialog()
        # self.open_file_names_dialog()
        # self.saveFileDialog()

        self.show()

    def open_file_name_dialog(self):
        '''Open the chosen file.
        This should open one file and we specify some
        extentions.'''
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getOpenFileName(
            self, "QFileDialog.getOpenFileName()",
            "", "All Files (*);;Python Files (*.py)",
            options=options)
        if file_name:
            print(file_name)
        return file_name

    def open_file_names_dialog(self):
        '''Choose multiple files.
        This allows the user to choose multiple files
        in the dialog box and mayby is more easy to
        use for many datasets.'''
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        files, _ = QFileDialog.getOpenFileNames(
            self, "QFileDialog.getOpenFileNames()",
            "", "All Files (*);;Python Files (*.py)",
            options=options)
        if files:
            print(files)

    def save_file_dialog(self):
        '''Save a file.
        Save some file to a folder and print the file name
        in the command line (or return it with `return ...`)'''
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getSaveFileName(
            self,
            "QFileDialog.getSaveFileName()",
            "", "All Files (*);;Text Files (*.txt)",
            options=options)
        if file_name:
            print(file_name)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())

    x = np.linspace(0, 10, 100)
    y = 2.7*np.sin(x) + 1.3
    plt.plot(x, y)
    plt.title(ex.filename)
    plt.show()
# %%
