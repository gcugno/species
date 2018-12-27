"""
Read module.
"""

import os
import configparser

import h5py
import numpy as np

from .. core import box
from .. data import database
from . import read_filter


class ReadSpectrum:
    """
    Text
    """

    def __init__(self, spectrum, filter_name):
        """
        :param spectrum: Spectral library.
        :type spectrum: str
        :param filter_name: Filter name. Full spectrum is read if filter_name is set to None.
        :type filter_name: str

        :return: None
        """

        self.spectrum = spectrum
        self.filter_name = filter_name

        if filter_name is None:
            self.wl_range = None

        else:
            transmission = read_filter.ReadFilter(filter_name)
            self.wl_range = transmission.wavelength_range()

        config_file = os.path.join(os.getcwd(), 'species_config.ini')

        config = configparser.ConfigParser()
        config.read_file(open(config_file))

        self.database = config['species']['database']

    def get_spectrum(self, ignore_nan=True, sptype=None):
        """
        :return:
        :rtype: species.core.box.SpectrumBox
        """

        h5_file = h5py.File(self.database, 'r')

        try:
            h5_file['spectra/'+self.spectrum]

        except KeyError:
            h5_file.close()
            species_db = database.Database()
            species_db.add_spectrum(self.spectrum)
            h5_file = h5py.File(self.database, 'r')

        list_wavelength = []
        list_flux = []
        list_name = []
        list_simbad = []
        list_sptype = []
        list_distance = []

        for item in h5_file['spectra/'+self.spectrum]:
            data = h5_file['spectra/'+self.spectrum+'/'+item]

            wavelength = data[0, :] # [micron]
            flux = data[1, :] # [W m-2 micron-1]

            if data.shape[0] == 3:
                error = data[2, :] # [W m-2 micron-1]

            if ignore_nan:
                indices = np.isnan(flux)
                indices = np.logical_not(indices)
                indices = np.where(indices)[0]

                wavelength = wavelength[indices]
                flux = flux[indices]

                if data.shape[0] == 3:
                    error = error[indices]

            if self.wl_range is None:
                wl_index = np.arange(0, len(wavelength), 1)

            else:
                wl_index = (flux > 0.) & (wavelength > self.wl_range[0]) & \
                           (wavelength < self.wl_range[1])

            count = np.count_nonzero(wl_index)

            if count > 0:
                index = np.where(wl_index)[0]

                if index[0] > 0:
                    wl_index[index[0] - 1] = True

                if index[-1] < len(wl_index)-1:
                    wl_index[index[-1] + 1] = True

                list_wavelength.append(wavelength[wl_index])
                list_flux.append(flux[wl_index])

                attrs = data.attrs
                if 'name' in attrs:
                    list_name.append(data.attrs['name'])

                if 'simbad' in attrs:
                    list_simbad.append(data.attrs['simbad'])

                if 'sptype' in attrs:
                    list_sptype.append(data.attrs['sptype'])

                if 'distance' in attrs:
                    list_distance.append(data.attrs['distance'])

        specbox = box.SpectrumBox()

        specbox.spectrum = self.spectrum
        specbox.wavelength = np.asarray(list_wavelength)
        specbox.flux = np.asarray(list_flux)

        if list_name:
            specbox.name = np.asarray(list_name)

        if list_simbad:
            specbox.simbad = np.asarray(list_simbad)

        if list_sptype:
            specbox.sptype = np.asarray(list_sptype)

        if list_distance:
            specbox.distance = np.asarray(list_distance)

        if sptype is not None:
            indices = np.where(np.chararray.startswith(specbox.sptype, sptype))[0]

            specbox.wavelength = specbox.wavelength[indices]
            specbox.flux = specbox.flux[indices]
            specbox.name = specbox.name[indices]
            specbox.simbad = specbox.simbad[indices]
            specbox.sptype = specbox.sptype[indices]
            specbox.distance = specbox.distance[indices]

        return specbox