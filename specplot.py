# plot spectrum
# mask bands where atmosphere or response goes to zero  (see matplotlib note in Evernote)
# ID lines

import spectro
import plottools

def specplot(hdulist, spec_ext, title=None, line_list_name=None, 
             redshift=0., draw_band_limits=False,
             output_plot_name=None):
    # hdulist can be either astropy fits or pyfits
    
    sp = spectro.Spectrum(hdulist[spec_ext])
    if line_list_name is not None:
        linelist = spectro.LineList(line_list_name, redshift)
    if draw_band_limits == True:
        bandlist = spectro.BandList(sp.wlen[0],sp.wlen[-1])
    
    p = plottools.SpPlot()
    p.plot_spectrum(sp.wlen, sp.counts)
    
    if line_list_name is not None:
        p.annotate_lines()
    if draw_band_limits == True:
        p.draw_band_limits()
    
    if output_plot_name is not None:
        p.write_png()
    
    return


def example():
    import numpy as np
    import matplotlib.pyplot as plt
    from astropy import wcs
    from astrodata import AstroData
    
    ad = AstroData('JHK.fits')
    x = np.arange(ad.get_key_value('NAXIS1'))
    
    w = wcs.WCS(ad.header.tostring())
    wlen = w.wcs_pix2world(zip(x), 0)
    
    plt.plot(wlen,ad.data)
    plt.xlabel('Wavelength [Angstrom]')
    plt.ylabel('Counts')
    plt.axis('tight')
    plt.ylim(-100,800)
    plt.show()
    
    ad.close()

    #plt.axis[[-100,1000,ymin,ymax]]