# specplot.py
"""
Utility function to plot a spectrum and annotate.
"""

# mask bands where atmosphere or response goes to zero
# (see matplotlib note in Evernote)
# ID lines

from klpyastro.sciformats import spectro
from klpyastro.plot import plottools
from klpyastro.utils.bookkeeping import get_valid_extension
import numpy as np

def specplot(hdulist, spec_ext, var_ext, annotations=None,
             ylimits=None, output_plot_name=None):
    """
    Plot a 1-D spectrum and annotates.

    This is utility function to do most of the work for plotting a spectrum.
    The axes are labeled automatically using information from the extension
    in the input HDU list.

    Lines can be annotated provide that the list is defined
    in the spectro.py module.  A redshift can be applied to the line list.
    The user can reset the y-axis limits.  Work in progress is the ability
    to draw band limits to identify where the signal is not good due to
    atmospheric absorption.  The plot can be saved as PNG.

    Parameters
    ----------
    hdulist : HDUList
        hdulist can be either from astropy.io.fits or from pyfits.
        Unfortunately the two versions are giving incompatible hdulists.
        The code here uses a workaround that allows both, until the
        old pyfits is deprecated.
    spec_ext : int or str
        The extension that contains the spectrum.  The extension identifier
        can be an int or a string representation with extname and extver,
        eg. 'sci,1'.
    var_ext : int or str
        The extension that contains the variance.  The extension identifier
        can be an int or a string representation with extname and extver,
        eg. 'var,1'.
    annotations : SpecPlotAnnotation, optional
        An instance of SpecPlotAnnotation containing annotation information
        for plot, eg. title, line list names, redshift, whether to draw the
        band limits.
    ylimits : list, optional
        The lower and upper limits for the y-axis.  Individual values
        are int or float.
    output_plot_name : str, optional
        If set, the plot will be saved to a file of that name. The .png
        filename extension is optional, it will be added appropriately.
        The plot will be display on screen as well as being saved to disk.

    Returns
    _______
    No return values. A plot is produced on screen, and it can be saved
    to disk.

    Raises
    ______
    NotImplementedError
        Some features are not yet implemented.

    See Also
    --------
    splot : An app that uses this function and is callable from the shell.

    Examples
    --------
    TODO : add examples for specplot()
    """

    # ----- Get the information needed to produce the plot

    # Get the spectrum.
    # print 'debug - specplot - Extension parsed as:',
    #    get_valid_extension(spec_ext)
    # print 'debug - specplot - The hdulist is:', hdulist.info()
    spectrum = spectro.Spectrum(hdulist[get_valid_extension(spec_ext)])
    if var_ext is not None:
        error = spectro.Spectrum(hdulist[get_valid_extension(var_ext)])
        error.counts = np.sqrt(error.counts)
    else:
        error = None

    # To simplify the rest of the scripts, create an instance of
    # SpecPlotAnnotations that has everything set to False if no
    # annotations were defined.
    if annotations is None:
        # create an instance that has everything set to False
        annotations = SpecPlotAnnotations()

    # Get the line list and redshift it.
    if annotations.annotate_lines:
        linelist = spectro.LineList(annotations.line_list_name,
                                    annotations.redshift)
    else:
        linelist = None

    # Get the band limits.
    if annotations.draw_bands_limits:
        errmsg = 'Draw bands limits feature not implemented.'
        raise NotImplementedError(errmsg)
#        bandlist = spectro.BandList(spectrum.wlen[0], spectrum.wlen[-1])


    # ----- START PLOTTING
    #
    # Plot the spectrum and set y-axis limits
    plot = plottools.SpPlot(title=annotations.title)
    plot.plot_spectrum(spectrum)
    if error is not None:
        plot.plot_spectrum(error, color='g')
    if ylimits is not None:
        plot.adjust_ylimits(ylimits[0], ylimits[1])

    # Annotate the lines.
    if linelist is not None:
        lines_to_plot = []
        for line in linelist.lines:
            lines_to_plot.append((line.obswlen.to(spectrum.wunit).value,
                                  line.name))
        plot.annotate_lines(lines_to_plot)

    # Draw the band limits
#    if annotations.draw_band_limits:
#        plot.draw_band_limits()

    # Save the plot to disk.
    if output_plot_name is not None:
        plot.write_png(output_plot_name)

    return


class SpecPlotAnnotations(object):
    """
    A collection of information for the plot annotations.

    Check and store the information necessary to control the plot
    annotations.  Use the methods to set the attributes.

    Parameters
    ----------
    title : str, optional
        Title for the plot.  Can also be set with a method later.

    Attributes
    ----------
    annotate_lines : bool
        Toggle on line identification annotation.  If True, line_list_name
        must be set to a valid name. Default = False.
    draw_bands_limits : bool
        Toggle on the drawing of the band limits.  Not implemented yet.
        Default = False.
    line_list_name : str, optional
        Name of the line list to use.  The lists are defined in
        spectro.LINELIST_DICT.  line_list_name must be set if annotate_lines
        is set to True.
    redshift : float, optional
        Redshift to apply to the line list. Default = 0.
    title : str, optional
        Title for the plot.

    See Also
    --------
    spectro.LINELIST_DICT : Defined line lists.
    """
    def __init__(self, title=None):
        self.title = title
        self.annotate_lines = False
        self.draw_bands_limits = False
        self.line_list_name = None
        self.redshift = 0.

    def set_line_list_name(self, line_list_name):
        """
        Set the line_list_name attribute and set annotate_lines to True.

        Parameters
        ----------
        line_list_name : str
            Name of the line list as defined in spectro.LINELIST_DICT.

        Raises
        ------
        KeyError
            The line list name is invalid.  It is not defined in
            spectro.LINELIST_DICT.

        See Also
        --------
        spectro.LINELIST_DICT : Line list are defined in there.  Only
                those names are valid.
        """
        if line_list_name in spectro.LINELIST_DICT.keys():
            self.line_list_name = line_list_name
            self.annotate_lines = True
        else:
            print('ERROR: line_list_name "%s" invalid.' % line_list_name)
            print('ERROR: Valid lists are: ',
                                        list(spectro.LINELIST_DICT.keys()))
            raise KeyError(line_list_name)

        return

    def set_redshift(self, redshift):
        """
        Set the redshift attribute.

        Parameters
        ----------
        redshift : float
            Redshift to apply to the line list.
        """
        self.redshift = redshift
        return

    def set_title(self, title):
        """
        Set the title attribute.

        Parameters
        ----------
        title : str
            Title for the plot.
        """
        self.title = title
        return

# TODO: reactivate once the new astrodata is available for Python 3
# def example():
#     """
#     This is just an example.  Cut and paste that on the python prompt.
#     It can also be run as specplot.example().
#     """
#     # import numpy as np
#     import matplotlib.pyplot as plt
#     from astropy import wcs
#     from astrodata import AstroData
#
#     ad = AstroData('JHK.fits')
#     x_values = np.arange(ad.get_key_value('NAXIS1'))
#
#     wcs_ad = wcs.WCS(ad.header.tostring())
#     wlen = wcs_ad.wcs_pix2world(zip(x_values), 0)
#
#     plt.plot(wlen, ad.data)
#     plt.xlabel('Wavelength [Angstrom]')
#     plt.ylabel('Counts')
#     plt.axis('tight')
#     plt.ylim(-100, 800)
#     plt.show()
#
#     ad.close()
#
#     # plt.axis[[-100,1000,ymin,ymax]]
