#%%
# from PyQt5.QtCore import
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog
from PyQt5.QtGui import QIcon
import matplotlib.pyplot as plt
import numpy as np
from nptdms import TdmsFile
from pathlib import Path
from pros_noisefiltering.WT_NoiProc import WT_NoiseChannelProc
from pros_noisefiltering.WT_NoiProc import (filt_butter_factory,
                                            plot_comparative_response)


class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = "PyQt5 file dialogs - pythonspot.com"
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.initUI()
        # self.filename = self.openFileNameDialog()


    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.filename = self.openFileNameDialog()
        # self.openFileNamesDialog()
        # self.saveFileDialog()

        # self.show()

    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,
                                                  "QFileDialog.getOpenFileName()",
                                                  "",
                                                  "All Files (*);;Python Files (*.py)",
                                                  options=options)
        if fileName:
            print(fileName)
        return fileName

    def openFileNamesDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        files, _ = QFileDialog.getOpenFileNames(self,
                                                "QFileDialog.getOpenFileNames()",
                                                "",
                                                "All Files (*);;Python Files (*.py)",
                                                options=options)
        if files:
            print(files)

    def saveFileDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self,
                                                  "QFileDialog.getSaveFileName()",
                                                  "",
                                                  "All Files (*);;Text Files (*.txt)",
                                                  options=options)
        if fileName:
            print(fileName)

    def title_from_file_path(self):
        wt_speeds = ["_0.", "_5.", "_10.", "_15.", "_20."]
        ca_speeds = ["_0.", "_5.", "_10."]
        for items in wt_speeds:
            if "in1_" in self.filename and self.filename.find(items) != -1:
                # print()
                speed = items.replace("_", "").replace(".", "")
                title = f'Inverter ON, wind speed = {speed} m/s wind tunnel measurements'
            elif "in0_" in self.filename and self.filename.find(items) != -1:
                speed = items.replace("_", "").replace(".", "")
                title = f'Inverter OFF, wind speed = {speed} m/s wind tunnel measurements'
            else:
                continue
        for elems in ca_speeds:
            if "ca1_" in self.filename and self.filename.find(elems) != -1:
                # print()
                speed = elems.replace("_", "").replace(".", "")
                title = f'Inverter ON, wind speed = {speed} m/s compressed air'
            elif "ca0_" in self.filename and self.filename.find(elems) != -1:
                speed = elems.replace("_", "").replace(".", "")
                title = f'Inverter OFF, wind speed = {speed} m/s compressed air'
            else:
                continue
        return title

    def recursive_file_opener(self):
        file = TdmsFile(Path(self.filename))

        title = App.title_from_file_path(self)
        GROUP_NAME = "Wind Measurement"
        CHAN_NAME = "Wind2"
        df_tdms_sample = WT_NoiseChannelProc.from_tdms(file
                                                       [GROUP_NAME]
                                                       [CHAN_NAME],
                                                       desc=title)
        filter_Butter_200 = filt_butter_factory(filt_order=2, fc_Hz=100)
        FIGSIZE_SQR_L = (8, 10)
        plot_comparative_response(df_tdms_sample,
                                  filter_func=filter_Butter_200,
                                  response_offset=2e-4,
                                  Kolmogorov_offset=4e0,
                                  nperseg=1_024*100,
                                  figsize=FIGSIZE_SQR_L)
        plt.show()

        # TODO
        # not working for now but i can use initUi to give a message...
        # should investigate more...
        # except ValueError:
        #     print("canceled")
        #     self.deleteLater()
        #     sys.exit()

        App().recursive_file_opener()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    App().recursive_file_opener()
