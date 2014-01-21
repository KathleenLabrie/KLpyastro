# specplot.py
"""
Utility function to plot a spectrum and annotate.
"""

# mask bands where atmosphere or response goes to zero  
# (see matplotlib note in Evernote)
# ID lines

import spectro
import plottools

def specplot(hdulist, spec_ext, title=None, line_list_name=None, 
             redshift=0., draw_band_limits=False,
             output_plot_name=None, ylimits=None):
    # hdulist can be either astropy fits or pyfits
    
    spectrum = spectro.Spectrum(hdulist[get_valid_extension(spec_ext)])
    if line_list_name is not None:
        linelist = spectro.LineList(line_list_name, redshift)
    if draw_band_limits == True:
        bandlist = spectro.BandList(spectrum.wlen[0], spectrum.wlen[-1])
    
    plot = plottools.SpPlot(title=title)
    plot.plot_spectrum(spectrum)
    if ylimits is not None:
        plot.adjust_ylimits(ylimits[0], ylimits[1])
    
    if line_list_name is not None:
        lines_to_plot = []
        for line in linelist.lines:
            lines_to_plot.append( (line.obswlen.to(spectrum.wunit).value, 
                                   line.name) )
        plot.annotate_lines(lines_to_plot)
        
#    if draw_band_limits == True:
#        plot.draw_band_limits()
    
    if output_plot_name is not None:
        plot.write_png(output_plot_name)
    
    return

def get_valid_extension(extension_string):
    ext = extension_string.split(',')
    if ext[0].isdigit():
        valid_extension = int(ext[0])
    else:
        valid_extension = (ext[0].upper(), int(ext[1]))
    
    return valid_extension

def example():
    import numpy as np
    import matplotlib.pyplot as plt
    from astropy import wcs
    from astrodata import AstroData
    
    ad = AstroData('JHK.fits')
    x_values = np.arange(ad.get_key_value('NAXIS1'))
    
    wcs_ad = wcs.WCS(ad.header.tostring())
    wlen = wcs_ad.wcs_pix2world(zip(x_values), 0)
    
    plt.plot(wlen, ad.data)
    plt.xlabel('Wavelength [Angstrom]')
    plt.ylabel('Counts')
    plt.axis('tight')
    plt.ylim(-100, 800)
    plt.show()
    
    ad.close()

    #plt.axis[[-100,1000,ymin,ymax]]