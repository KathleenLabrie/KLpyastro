from astropy.io import ascii
from astropy import units as u

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
        current_block_starts = 0
        current_block_ends = 0
        for pos in cutoff_positions:
            if (pos - current_block_ends) <= tolerance:
                current_block_ends = pos
                prev_pos = pos
            else:
                # end of a block
                wlow = self.wlen[current_block_starts] 
                whigh = self.wlen[current_block_ends]
                wblocks.append((wlow, whigh))
        
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

BANDS_TABLE = [(1.2 * u.micron, 'J-band'),
               (1.6 * u.micron, 'H-band'),
               (2.2 * u.micron, 'K-band')
               ]
