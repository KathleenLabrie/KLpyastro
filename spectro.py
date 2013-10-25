import numpy as np
from astropy import wcs
from astropy.io import ascii
from astropy import units as u

class Line:
    # redshift is z, not velocity
    def __init__(self, restwlen=None, obswlen=None, redshift=None, name=None):
        self.restwlen=restwlen
        self.obswlen=obswlen
        self.redshift=redshift
        self.name=name
        
        # try to set undefined attributes from the others.
        self.set_obswlen(obswlen)
        self.set_restwlen(restwlen)
        self.set_redshift(redshift)
    
    def set_obswlen(self, obswlen=None):
        if obswlen is None:
            if self.restwlen is not None and self.redshift is not None:
                #apply the redshift to restwlen to get obswlen
                obswlen = (self.redshift + 1) * self.restwlen
        self.obswlen = obswlen            
        return
    
    def set_restwlen(self, restwlen=None):
        if restwlen is None:
            if self.obswlen is not None and self.redshift is not None:
                #apply the redshift to obswlen to get restwlen
                restwlen = self.obswlen / (self.redshift + 1.)
        self.restwlen = restwlen
        return
    
    def set_redshift(self, redshift=None):
        if redshift is None:
            if self.restwlen is not None and self.obswlen is not None:
                # use the restwlen and obswlen to calculated the redshift
                redshift = (self.obswlen - self.restwlen) / self.restwlen
        self.redshift = redshift
        return
    
    def set_name(self, name):
        self.name = name
        return


class Spectrum:
    def __init__(self, hdu):
        self.counts = self.get_counts_array_from_hdu(hdu)
        self.pix = self.get_pixel_array_from_hdu(hdu)
        self.wcs = self.get_wcs_from_hdu(hdu)
        self.wlen = self.apply_wcs_to_pixels()
        self.wunit = self.get_wunit(hdu)
    
    def get_counts_array_from_hdu(self, hdu):
        return hdu.data
    
    def get_pixel_array_from_hdu(self, hdu):
        return np.arange(len(hdu.data))
    
    def get_wcs_from_hdu(self, hdu):
        return wcs.WCS(hdu.header.tostring())
    
    def apply_wcs_to_pixels(self):
        return self.wcs.wcs_pix2world(zip(self.pix), 0)
    
    def get_wunit(self, hdu):
        return u.Unit(hdu.header['WAT1_001'].split[2].split('=')[1])

    
class AtmosphericTransparency:
    def __init__(self, filename, wunit='Angstrom'):
        data = ascii.read(filename)
        self.wlen = data.field('wlen').data
        self.transmission = data.field('T').data
        self.wunit = u.Unit(wunit)
        #data.field('wlen').units
    
    def get_blocked_regions(self, cutoff=0.8, lower=None, upper=None):
        blocked_regions = []
        # wlength range with T < 0.5 = blocked region
        cutoff_positions = np.where(self.transmission < cutoff)
        wblocks = []
        tolerance = 10
        current_block_starts=0
        current_block_ends=0
        for pos in cutoff_positions:
            if (pos - current_block_ends) <= tolerance:
                current_block_ends=pos
                prev_pos = pos
            else:
                # end of a block
                wlow = self.wlen[current_block_starts] 
                whigh = self.wlen[current_block_ends]
                wblocks.append((wlow,whigh))
        
        # to save an if in the loop I just let the first
        # block at position 0 be appended to the wblocks
        # Here I just remove it.  (I make sure it's a 0-0)
        if wblocks[0][0] == wblocks[0][1]:
            wblocks = wblocks[1:]
        
        return block_regions

class TransmissionBand:
    # transmission: ndarray of values 0 to 1
    # central wavelength: Angstrom
    def __init__(self, name):
        self.name = name
        (self.wlen, self.transmission) = self.get_transmission_curve(name)
    
    def get_transmission_curve(self, name):
        data = ascii.read(''.join([name,'.dat']))
        wlen = data.field('wlen').data
        transmission = data.field('T').data
        return (wlen, transmission)
    
    def get_central_wlen(self):
        cwlen = 0.
        return cwlen
    
    def get_bandwidth(self, cutoff=0.2):
        bandwidth = 0.
        return bandwidth
        
 
class BandList:
    def __init__(self, lower, upper):  
        # lower and upper are Quantity objects.  (astropy.units) 
        self.bands = self.get_bands_for_range(lower, upper)
    
    def get_bands_for_range(self, lower, upper):
        bands = []
        for (wlen, name) in bands_table:
            if wlen >= lower and wlen <= upper:
                band = TransmissionBand(name)
                bands.append(band)
        return bands

class LineList:
    def __init__(self, name, redshift=0.):
        self.name = name
        self.redshift = redshift
        self.lines = self.get_lines_from_list(name, redshift)

    def get_lines_from_list(self, name, redshift):
        lines = []
        for line_data in linelist_dict(name):
            line = Line(restwlen=line_data[1], redshift=redshift, 
                        name=line_data[0])        
        return lines
        
    def apply_redshift(self, redshift):   
        for line in self.lines:
            line.set_redshift(redshift)
            line.set_obswlen()


# -------------------------------

linelist_dict = {
    'quasar' : [  ('HeI', 0.5876 * u.micron),
                  ('HeI', 1.083 * u.micron),
                  ('Pa_epsilon', 0.9546 * u.micron),
                  ('Pa_delta', 1.005 * u.micron),
                  ('Pa_gamma', 1.094 * u.micron),
                  ('Pa_beta', 1.282 * u.micron),
                  ('Pa_alpha', 1.875 * u.micron)
                ],
    'paschen' : [ ('Pa_epsilon', 0.9546 * u.micron),
                  ('Pa_delta', 1.005 * u.micron),
                  ('Pa_gamma', 1.094 * u.micron),
                  ('Pa_beta', 1.282 * u.micron),
                  ('Pa_alpha', 1.875 * u.micron)
                ]
    }

bands_table = [(1.2 * u.micron, 'J-band'),
               (1.6 * u.micron, 'H-band'),
               (2.2 * u.micron, 'K-band')
               ]
