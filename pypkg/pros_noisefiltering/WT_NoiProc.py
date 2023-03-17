"""Main Class for processing tdms dataset from the Lab."""
# %%

import logging
from matplotlib import pyplot as plt
import scipy.signal as signal
import numpy as np
import pandas as pd

import nptdms

from pros_noisefiltering.gen_functions import spect
from pros_noisefiltering.Graph_data_container import Graph_data_container
logging.basicConfig(level=logging.WARNING)


# %% Functions and classes
def filt_butter_factory(filt_order=2, fc_hz: float = 100):
    """Create a function for a butterworth filter.

    Produces a BUTTERWORTH filter function
    with a filter order and a cutoff frequency

    Args:
        filt_order (int, optional)  : Filter order. Defaults to 2.
        fc_hz (float, optional)     : cut off frequency in Hz (defaults to 100)
    """
    def filt_butter(sig_r: np.ndarray, fs_hz: float,
                    fc_hz: float = fc_hz,
                    filt_order=filt_order):
        """Apply filtering.

        To np.array with fs_hz data, with cuffoff frequency
        Args:
            sig_r (np.ndarray): _description_
            fs_hz (float): _description_
            fc_hz (int, optional):
                    cutoff frequency of filter (low pass).Defaults to 100.
            filt_order (int, optional):
                    _description_. Defaults to 2.
        Returns:
            _type_: _description_
        """
        sos = signal.butter(filt_order, fc_hz, 'lp', fs=fs_hz, output='sos')
        filtered = signal.sosfilt(sos, sig_r-sig_r[0])+sig_r[0]
        return filtered
    # additional decoration sith params dictionary
    # this is used instead of a class
    filt_butter.params = {'filter order': filt_order, 'fc_hz': fc_hz}
    return filt_butter


filter_Butter_default = filt_butter_factory(filt_order=2, fc_hz=100)


class WT_NoiseChannelProc():
    """Main class for parsing a .tdms dataframe.

    Class for processing a tdms file for noise processing
    """

    __measurement_history = []

    def __init__(self, desc: str, fs_hz: float, data: np.ndarray,
                 channel_name: str, group_name: str, _channel_data,
                 operations: list):
        """Initialize the self of the signal to be processed."""
        self._channel_data = _channel_data
        self.set_description(desc=desc)
        # process details
        self.fs_hz = fs_hz
        self.data = data
        self.channel_name = channel_name
        self.group_name = group_name
        self.__measurement_history = operations

    def set_description(self, desc):
        """Set the description of the file.

        Args:
            desc (_type_): _description_
        """
        self.description = desc

    @property
    def operations(self):
        """Capture the processing history."""
        return self.__measurement_history

    @property
    def data_as_Series(self) -> pd.Series:
        """Return the raw data as a pd.Series.

        Returns:
            _type_: _description_
        """
        return pd.Series(self.data, name=f'{self.channel_name}:raw')

    def average(self, fr_Hz: float = 100, desc: str = None):
        """Return the averaged signal.

        Args:
            fr_Hz (float) : recording frequency (with averaging)
            desc (str) : description (Defaults to None: ie.
                       add suffix _Av:<fr_Hz>)
        """
        sig_r = self.data_as_Series
        fs_hz = self.fs_hz

        sig_r_fr = sig_r.groupby(sig_r.index // (fs_hz/fr_Hz)).mean().values

        description = desc if desc is not None else self.description + f"_Av:{fr_Hz}"
        # TODO need to think better the naming conventions
        # (consider using a dictionary with multiple keys
        # e.g. different for plots etc)
        new_operations = self.operations.copy()
        new_operations.append(f'Apply Averaging :{fr_Hz}')
        return WT_NoiseChannelProc(desc=description,
                                   fs_hz=fr_Hz, data=sig_r_fr,
                                   channel_name=self.channel_name,
                                   group_name=self.group_name,
                                   _channel_data=None,
                                   operations=new_operations
                                   )

    def set_desc(self, desc: str):
        """Set the description for the processes.

        Applyied to each signal as it is
        passing through the class.
        """
        return WT_NoiseChannelProc.from_obj(self,
                                            operation=None,
                                            desc=desc)

    def decimate(self, dec: int, offset: int = 0):
        """# Returns a decimated data seires.

        Args:
        -----------
            dec (int): decimation factor
            offset (int): initial offset

        Returns:
            _type_: a decimated data series.
        """
        decimated_fs_hz = self.fs_hz/dec

        new_operation = f'Decimation factor:{dec}, Offset:{offset},\
        new fs_hz:{decimated_fs_hz}'
        return WT_NoiseChannelProc.from_obj(self,
                                            operation=new_operation,
                                            fs_hz=decimated_fs_hz,
                                            data=self.data[offset::dec])

    def _filter(self, fc_hz: float,
                filter_func=filter_Butter_default,
                fs_hz=None) -> pd.Series:
        """Return a filtered signal based on.

        Args:
            - fc_hz (float): cut off frequency in Hz
            - filter_func (filt_butter_factory, optional):
                filtering function that thates two arguments (sig_r, fs_hz).
                Defaults to 100, filt_order = 2).
            - fs_hz (None): sampling frequency in Hz (#TODO SHOULD BE REMOVED)


        Returns:
            _type_: _description_
        """
        if fs_hz is not None:
            logging.warning(
                f'issued {fs_hz} sampling frequency\
                while the default is {self.fs_hz}')
        fs_hz = fs_hz if fs_hz is not None else self.fs_hz
        filtered = filter_func(sig_r=self.data, fs_hz=fs_hz, fc_hz=fc_hz)
        return pd.Series(filtered,
                         name=f'{self.channel_name}:filt_fc_{fc_hz}')

    def filter(self,
               fc_hz: float,
               filter_func=filter_Butter_default,
               fs_hz=None, desc=None):
        """Return a object with filtering data."""
        sig_r_filt = self._filter(fc_hz=fc_hz,
                                  filter_func=filter_func,
                                  fs_hz=fs_hz)
        description = desc if desc is not None else self.description + f"_fc:{fc_hz}"
        return WT_NoiseChannelProc.from_obj(self,
                                            desc=description,
                                            data=sig_r_filt.values,
                                            operation=f'pass filter {fc_hz}'
                                            )

    def calc_spectrum(self, window='flattop',
                      nperseg=1_024,
                      scaling='density') -> Graph_data_container:
        """Return a Graph_data_container object.

        Also provides the power spectrum of the signal.
        uses the decimation function also chained.

        Returns:
            _type_: _description_
        """
        gobj = self.calc_spectrum_gen(dec=1,
                                      window=window,
                                      nperseg=nperseg,
                                      scaling=scaling)
        return gobj

    def calc_spectrum_gen(self,
                          dec: int = 1,
                          offset: int = 0,
                          window='flattop',
                          nperseg=1_024,
                          scaling='density') -> Graph_data_container:
        """Create a function for calculating the spectrum.

        Time series signal is used and return a
        Graph_data_container object with the power
        spectrum of the **decimated** data.

        Args:
            dec (int): decimation factor
            offset (int, optional): offset. Defaults to 0.

        Returns:
            Graph_data_container: _description_
        """
        decimated_fs_hz = self.fs_hz/dec
        # this has a BUG but may not affect this...
        # who knows .....
        x_r, y_r = spect(self.data[offset::dec],
                         FS=decimated_fs_hz,
                         window=window,
                         nperseg=nperseg,
                         scaling=scaling)
        if dec == 1:
            label = f'{self.description}'
            # TODO the new chain method approach does not require this.
            # This is a remnant from the original approach.
        else:
            label = f'{self.description}-{self.channel_name}-\
            fs:{decimated_fs_hz/1000:.1f}kHz '

        return Graph_data_container(_x=x_r,
                                    _y=y_r,
                                    label=label)

    def plot_filtered_th(self, filter_func):
        """Plot the time history.

        Args:
            fc_hz (_type_): _description_
        """
        plt.plot(self.data, label='raw')
        plt.plot(self.filter(filter_func=filter_func),
                 label=f'filtered: {filter_func.params}')

    @classmethod
    def from_tdms(cls,
                  tdms_channel: nptdms.tdms.TdmsChannel,
                  desc: str):
        """Create a factory methor that generates an object class.

        #TOD need to change the init function and test.

        Args:
            tdms_channel (nptdms.tdms.TdmsChannel): tmds channel
            desc (str): descirption (used)
        """
        _channel_data = tdms_channel
        # desc

        fs_hz = 1/_channel_data.properties['wf_increment']
        data = _channel_data.data
        channel_name = _channel_data.name
        group_name = _channel_data.group_name

        return cls(desc, fs_hz, data, channel_name, group_name, _channel_data,
                   operations=[f'Loaded from tdms file {group_name}/\
                   {channel_name}, {fs_hz}'])

    @classmethod
    def from_obj(cls, obj, operation: str = None, **kwargs):
        """Create a factory methor that generates an object class.

        if parameters are not provided the obj values are used.

        Args:
            tdms_channel (nptdms.tdms.TdmsChannel): tmds channel
            desc (str): descirption (used)
        """
        assert isinstance(operation, str) or None is None
        # the following line allows to pass a description maybe
        desc = obj.description if kwargs.get(
            'desc', None) is None else kwargs.get(
                'desc', None)

        _channel_data = kwargs.get('_channel_data',
                                   obj._channel_data)
        fs_hz = kwargs.get('fs_Hz', obj.fs_hz)
        data = kwargs.get('data', obj.data)
        channel_name = kwargs.get('channel_name', obj.channel_name)
        group_name = kwargs.get('group_name', obj.group_name)

        new_ops = obj.operations.copy()
        if operation is not None:
            new_ops.append(operation)
        return cls(desc, fs_hz, data, channel_name, group_name, _channel_data,
                   operations=new_ops)


# %%
# class Plotter_Class():
#     # TODO Not Implemented
#     """# TODO this is a class that can take different object
#     and takes their raw data and plot:
#     - Time histories
#     - spectrums
#     """
#     pass


def plot_comparative_response(wt_obj,        # cutoff frequency
                              filter_func,
                              response_offset=2e-4,
                              Kolmogorov_offset=1,
                              figsize=(16, 9),
                              nperseg=1024,
                              xlim=[1e1, 1e5],
                              ylim=[1e-8, 1e-1],
                              plot_th=False):
    # TODO make this part of WT_NoiProc
    """Plot a comparison of raw and filtered dignal.

    Args:
        wt_obj (_type_): _description_
        response_offset (_type_, optional): _description_. Defaults to 2e-4.
        figsize (tuple, optional): _description_. Defaults to (16,9).
    """
    sig = wt_obj.data
    fs_hz = wt_obj.fs_hz

    filt_p = filter_func.params
    sos = signal.butter(N=filt_p['filter order'], Wn=filt_p['fc_hz'],
                        btype='lp', fs=fs_hz, output='sos')

    filtered = filter_func(sig, fs_hz)

    # calculate spectrum
    f, Pxx_spec = signal.welch(sig, fs_hz, window='flattop',
                               nperseg=nperseg, scaling='density')
    f, Pxx_spec_filt = signal.welch(filtered, fs_hz, window='flattop',
                                    nperseg=nperseg, scaling='density')

    # #TODO: this is for testing
    # Pxx_spec= Pxx_spec**2
    # Pxx_spec_filt = Pxx_spec_filt**2

    if plot_th:
        t = np.arange(0, len(sig), 1, dtype='int')/fs_hz
        # plot time domain
        fig1, (ax1, ax2) = plt.subplots(2, 1, sharex=True, sharey=True,
                                        figsize=figsize)
        fig1.suptitle(
            'Time Domain Filtering of signal with\
            f1=10[Hz], f2=20[Hz] and noise')
        ax1.plot(t, sig)
        ax1.set_title('raw signal')
        # ax1.axis([0, 1, -2, 2])
        ax2.plot(t, filtered)
        ax2.set_title('After filter')
        # ax2.axis([0, 1, -2, 2])
        ax2.set_xlabel('Time [seconds]')
        plt.tight_layout()

    wb, hb = signal.sosfreqz(sos, worN=np.logspace(start=1, stop=5),
                             whole=True, fs=fs_hz)
    fb = wb  # /(2*np.pi) # convert rad/s to Hz

    fig2, ax2 = plt.subplots(1, 1, sharex=True, figsize=figsize)
    ax2.plot(fb, response_offset*abs(np.array(hb)), '--', lw=3,
             label='filter response')
    ax2.semilogy(f, np.sqrt(Pxx_spec), '.', label='raw')
    ax2.semilogy(f, np.sqrt(Pxx_spec_filt), '.', label='filtered')
    if Kolmogorov_offset is not None:
        KOLMOGORV_CONSTANT = - 5.0/3
        xs = f[1:]
        ys = xs**(KOLMOGORV_CONSTANT)*Kolmogorov_offset
        ax2.plot(xs, ys, 'r--', label='Kolmogorov -5/3')

    ax2.set_title('Filter frequency response (cutoff: {}Hz) -  {}'.format(
        filter_func.params.get('fc_hz', None),
        wt_obj.description))
    ax2.set_xlabel('Frequency [Hz]')
    ax2.set_ylabel('Power Spectrum density [V**2/Hz]')
    ax2.set_xscale('log')
    ax2.set_yscale('log')
    ax2.margins(0, 0.1)
    ax2.grid(which='both', axis='both')
    ax2.set_xlim(xlim)
    ax2.set_ylim(ylim)
    ax2.legend()
    # plt.savefig('Bessel Filter Freq Response.png')
# %%
