#%%
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog
from nptdms import TdmsFile
from pathlib import Path
from pros_noisefiltering.WT_NoiProc import (WT_NoiseChannelProc,
                                            Graph_data_container
                                            )
import pyqtgraph as pg
import pyqtgraph.exporters
import numpy as np


class FFT_new:
    """This class is used to calculate the fourier transform for raw signal."""

    def __init__(self, signal, title):
        """Construct the appropriate object to manipulate the signal.

        We should be able to integrate this in WT_Noi_proc.
        """
        self.Title = title
        self.sr = signal.fs_Hz
        self.sig = signal.data
        self.ind = signal.data_as_Series.index
        self.dt = 1 / int(self.sr)
        self.time_sec = self.ind * self.dt

        self._channel_data = signal._channel_data

    def fft_calc(self):
        """Func body for calculation of the frequency domain of raw data."""
        n = len(self.time_sec)
        fhat = np.fft.fft(self.sig, n)                  # compute fft
        PSD = fhat * np.conj(fhat) / n                  # Power spectrum (pr/f)
        freq = (1/(self.dt*n)) * np.arange(n)           # create x-axis (freqs)
        L = np.arange(1, np.floor(n/2), dtype=int)      # plot only first half
        return Graph_data_container(freq[L], abs(PSD[L]),
                                    label="fft transform")


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

    def plot_signal_all_doms(self, sig):

        filtrd = sig.filter(fc_Hz=2000, desc="butterworth low")
        freq_dom_filtrd = FFT_new(filtrd, title='')
        win = pg.GraphicsLayoutWidget(show=True,
                                      title="Basic plotting examples",
                                      size=(1920, 1080))
        win.resize(1920, 1080)
        win.setWindowTitle('pyqtgraph example: Plotting')
        # Enable antialiasing for prettier plots
        pg.setConfigOptions(antialias=True)

        p1 = win.addPlot(row=0,
                         col=0,
                         colspan=1,
                         title=f"{sig.description}")
        p1.setLabels(bottom='time duration (s)', left='Raw sensor Voltage')
        p1.showGrid(y=True)
        p1.plot(freq_dom_filtrd.time_sec,
                sig.data,
                pen=(0, 255, 0, 35),
                name="Raw signal")

        p1_filt = win.addPlot(row=0,
                              col=1,
                              title='Filtered signal')
        p1_filt.setLabels(bottom='time duration (s)')
        p1_filt.showGrid(y=True)
        p1_filt.addLegend()
        p1_filt.setYRange(filtrd.data.min() - 0.1,
                          filtrd.data.max() + 0.1)
        p1_filt.plot(freq_dom_filtrd.time_sec,
                     filtrd.data,
                     pen=(0, 0, 255),
                     name=f"{filtrd.description}-{filtrd.operations.__getitem__(1)} Hz")

        p2 = win.addPlot(row=1,
                         col=0,
                         rowspan=1,
                         colspan=2,
                         padding=10,
                         title="Filtered signal Frequency domain representation")
        data = freq_dom_filtrd.fft_calc()
        p2.setLogMode(x=True, y=True)
        p2.showGrid(x=True, y=True)
        p2.setLabels(bottom='Frequencies in Hz',
                     left='Power/Freq',
                     top='')
        p2.plot(data.x, data.y,
                pen=(50, 50, 250),
                fillLevel=-18,
                brush=(250, 50, 50, 100))

        p3 = win.addPlot(row=2,
                         col=0,
                         rowspan=1,
                         colspan=2,
                         padding=10,
                         title="Filtered signal Spectral density (welch)")
        welch = filtrd.calc_spectrum_gen(nperseg=1024 << 6)
        p3.setLogMode(x=True, y=True)
        p3.showGrid(x=True, y=True)
        p3.setLabels(bottom='Frequencies in Hz', left='dB',
                     top='')
        p3.plot(welch.x, welch.y,
                pen=(50, 50, 250), fillLevel=-18, brush=(250, 50, 50, 100))

        # save to a file somewhere
        # exporter = pg.exporters.ImageExporter(win.scene())
        # exporter.parameters()['width'] = 1920   # also effects the height param
        # exporter.parameters()['antialias'] = True
        # exporter.export('./sig_proc_plots/test.jpg')
        pg.exec()

    def recursive_file_opener(self):
        file = TdmsFile(Path(self.filename))

        title = App.title_from_file_path(self)
        GROUP_NAME = "Wind Measurement"
        CHAN_NAME = "Wind2"
        df_tdms_sample = WT_NoiseChannelProc.from_tdms(file
                                                       [GROUP_NAME]
                                                       [CHAN_NAME],
                                                       desc=title)

        self.plot_signal_all_doms(df_tdms_sample)
        App().recursive_file_opener()
        # return df_tdms_sample

        # TODO
        # not working for now but i can use initUi to give a message...
        # should investigate more...
        # except ValueError:
        #     print("canceled")
        #     self.deleteLater()
        #     sys.exit()


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    file = App().recursive_file_opener()
    sys.exit(app.exec_())
