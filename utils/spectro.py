# spectro.py
"""
Classes and definitions related to spectroscopic data.
"""

import numpy as np
from astropy import wcs
from astropy import units as u

class Line:
    """
    Class to represent a spectral line.
    
    A Line contains information about the rest wavelength, the observed
    wavelength, the redshift, and its name.  Those characteristics can
    be set when the instance is created, or set or calculated later with 
    a method.  If only some of the parameters are set, the constructor
    will try to set the other attributes.  For example, if the rest wavelength
    and the redshift are given, the construction will calculate and set the
    observed wavelength.
    
    Parameters
    ----------
    restwlen : float or Quantity, optional
        Rest wavelength.
    obswlen : float or Quantity, optional
        Observed wavelength.
    redshift : float, optional
        Redshift that links the rest and observed wavelengths.
    name : str, optional
        The line identification.
    
    Attributes
    ----------
    restwlen : float or Quantity
        Rest wavelength.
    obswlen : float or Quantity
        Observed wavelength.
    redshift : float
        Redshift that links the rest and observed wavelengths.  The redshift
        is 'z', not a velocity.
    name : str
        The line identification.
    
    Methods
    -------
    set_obswlen(obswlen)
        Set the obswlen attribute.  If obswlen parameter is None, try to use
        the other attributes to calculate obswlen.
    set_restwlen(restwlen)
        Set the restwlen attribute.  If restwlen parameter is None, try to use
        the other attributes to calculate restwlen.
    set_redshift(redshift)
        Set the redshift attribute.  If redshift parameter is None, try to use
        the other attributes to calculate redshift.
    set_name(name)
        Set the name of the line.
    validate_wavelengths()
        
    
    Raises
    ------
    Notes
    -----
    It is recommended to use the "set" methods to set the attributes.
    
    Examples
    --------
    >>> myline = Line(restwlen=0.5876*u.micron, redshift=1.)
    >>> myline.__dict__
    {'name': None, 'obswlen': <Quantity 1.1752 micron>, '
    restwlen': <Quantity 0.5876 micron>, 'redshift': 1.0}
    
    Note that the obswlen attribute has been automatically calculated from
    the rest wavelength and the redshift specified in the construction call.
    
    >>> myline = Line()
    >>> myline.set_restwlen(0.5876*u.micron)
    >>> myline.set_redshift(1.)
    >>> myline.set_obswlen()
    
    Two of the three wavelength attributes must be set in order to calculate
    the third.
    """
    
    def __init__(self, restwlen=None, obswlen=None, redshift=None, name=None):
        self.restwlen = restwlen
        self.obswlen = obswlen
        self.redshift = redshift
        self.name = name
        
        # try to set undefined attributes from the others.
        self.set_obswlen(obswlen)
        self.set_restwlen(restwlen)
        self.set_redshift(redshift)
    
    def set_obswlen(self, obswlen=None):
        """
        Set or calculate the observed wavelength.
        
        The observed wavelength for the line is set to the obswlen provided as
        input.  If no input is given and the rest wavelength and redshift are
        already set, then the observed wavelength will be calculated from those
        instead.
        
        Parameters
        ----------
        obswlen : float or Quantity, optional
            Observed wavelength.  If specified, that value will be used to set
            the obswlen attribute.  If it is not specified as input, the method
            will try to calculate it from the rest wavelength and the redshift,
            if those are already set.
        
        Examples
        --------
        >>> myline = Line(restwlen=0.5876*u.micron, redshift=1.)
        >>> myline.set_obswlen()
        >>> myline.obswlen
        <Quantity 1.1752 micron>

        """
        if obswlen is None:
            if self.restwlen is not None and self.redshift is not None:
                #apply the redshift to restwlen to get obswlen
                obswlen = (self.redshift + 1) * self.restwlen
        self.obswlen = obswlen            
        return
    
    def set_restwlen(self, restwlen=None):
        """
        Set or calculate the restwlen wavelength.
        
        The rest wavelength for the line is set to the restwlen provided as
        input.  If no input is given and the observed wavelength and redshift 
        are already set, then the rest wavelength will be calculated from 
        those instead.
        
        Parameters
        ----------
        restwlen : float or Quantity, optional
            Rest wavelength.  If specified, that value will be used to set
            the restwlen attribute.  If it is not specified as input, the 
            method will try to calculate it from the observed wavelength 
            and the redshift, if those are already set.
        
        Examples
        --------
        >>> myline = Line(obswlen=1.1752*u.micron, redshift=1.)
        >>> myline.set_restwlen()
        >>> myline.restwlen
        <Quantity 0.5876*u.micron>

        """        
        if restwlen is None:
            if self.obswlen is not None and self.redshift is not None:
                #apply the redshift to obswlen to get restwlen
                restwlen = self.obswlen / (self.redshift + 1.)
        self.restwlen = restwlen
        return
    
    def set_redshift(self, redshift=None):
        """
        Set or calculate the redshift.
        
        The redshift for the line is set to the redshift provided as
        input.  If no input is given and the observed and rest wavelengths
        are already set, then the redshift will be calculated from 
        those instead.
        
        Parameters
        ----------
        redshift : float, optional
            Redshift.  If specified, that value will be used to set
            the redshift attribute.  If it is not specified as input, the 
            method will try to calculate it from the observed and the
            rest wavelengths, if those are already set.
        
        Examples
        --------
        >>> myline = Line(restwlen=0.5876*u.micron, obswlen=1.1752*u.micron)
        >>> myline.set_redshift()
        >>> myline.redshift
        1.0

        """        
        if redshift is None:
            if self.restwlen is not None and self.obswlen is not None:
                # use the restwlen and obswlen to calculated the redshift
                redshift = (self.obswlen - self.restwlen) / self.restwlen
        self.redshift = redshift
        return
    
    def set_name(self, name):
        """
        Set the line name.
        
        Parameters
        ----------
        name : str
            Name to assign to this line.
        """
        self.name = name
        return

    def validate_wavelengths(self):
        """
        Check that the rest wavelength, observed wavelength, and redshift are
        coherent with each others.
        
        If the rest and observed wavelength, and the redshift are set 
        independently, it is possible that they would be incoherent with
        each other, eg. the observed wavelength does not match the rest 
        wavelength and the redshift.  This method will do a quick validation
        of the three values, checking if they match.  If they don't, an
        AssertionError is returned.
        
        Raises
        ------
        AssertionError
            Raised if the attributes restwlen, obswlen, and redshift are not
            coherent with each other.
        """
        assert self.obswlen == (self.redshift + 1) * self.restwlen

class Spectrum:
    """
    Class representing a spectrum.
    
    A 1-D spectrum is loaded from an FITS HDU.  Information about the pixels
    and their values, and information about the WCS and units are obtained
    directly from the HDU.
    
    Parameters
    ----------
    hdu : HDU
        The FITS Header Data Unit, in other words, a FITS extension.  Those
        can be obtained from an AstroData object or with pyfits/astropy.io.fits.
    wunit : Unit, optional
        The units for the wavelengths.  The Unit class comes from the
        astropy.units module.  If it is not provided as an argument, the 
        constructor will try to get the information from the headers, in
        particular from the 'WAT1_001' keyword.
    """
    def __init__(self, hdu, wunit=None):
        self.counts = self.get_counts_array_from_hdu(hdu)
        self.pix = self.get_pixel_array_from_hdu(hdu)
        self.wcs = self.get_wcs_from_hdu(hdu)
        self.wlen = self.apply_wcs_to_pixels()
        self.wunit = wunit
        #print 'debug - Spectrum init - length counts:', self.counts.size
        #print 'debug - Spectrum init - length pix:', self.pix.size
        #print 'debug - Spectrum init - wcs:', self.wcs
        #print 'debug - Spectrum init - length wlen:', self.wlen.size
        
        if self.wunit is None:
            self.wunit = self.get_wunit(hdu)
    
    @classmethod
    def get_counts_array_from_hdu(cls, hdu):
        return hdu.data
    
    @classmethod
    def get_pixel_array_from_hdu(cls, hdu):
        return np.arange(len(hdu.data))
    
    @classmethod
    def get_wcs_from_hdu(cls, hdu):
        return wcs.WCS(hdu.header.tostring())
    
    @classmethod
    def get_wunit(cls, hdu):
        unit_str = hdu.header['WAT1_001'].split()[2].split('=')[1]
        if unit_str.endswith('s'):
            unit_str = unit_str[:-1]
        return u.Unit(unit_str)

    def apply_wcs_to_pixels(self):
        #print 'debug - in apply_wcs_to_pixels:', zip(self.pix)[0:3]
        return self.wcs.wcs_pix2world(zip(self.pix), 0)
    

class LineList:
    """
    Create a list of Line objects from a line list defined in LINELIST_DICT.
    
    Parameters
    ----------
    name : str
        Name of the line list to retrieve from LINELIST_DICT.
    redshift : float, optional
        Redshift to apply to the lines.  Note that the redshift is only 
        stored. To apply it run the method apply_redshift().  Default = 0.
    
    Attributes
    ----------
    name : str
        Name of the line list to retrieve from LINELIST_DICT.
    redshift : float
        Redshift to apply to the lines.
    lines : list of Line
        List of Line instances.  This is the attribute to access once the 
        LineList instance has been created.
    
    Methods
    -------
    reapply_redshift()
        If the redshift attribute has been changed, reapply the redshift 
        to the lines.
    
    Raises
    ------
    KeyError
        Raised if the line list name is invalid.
        
    See Also
    --------
    The Line class.
    
    Examples
    --------
    >>> mylinelist = LineList('quasar')
    >>> mylinelist.lines
    [<spectro.Line instance at 0x10339ddd0>, <spectro.Line instance ...
    <spectro.Line instance at 0x10339d050>, <spectro.Line instance ...
    <spectro.Line instance at 0x10339fb00>, <spectro.Line instance ...
    <spectro.Line instance at 0x10339f7e8>, <spectro.Line instance ...]
    
    >>> mylinelist.lines[0].obswlen
    <Quantity 0.5876 micron>
    >>> mylinelist.redshift = 1.
    >>> mylinelist.reapply_redshift()
    >>> ll.lines[0].obswlen
    <Quantity 1.1752 micron>
    """
    
    def __init__(self, name, redshift=0.):
        self.name = name
        self.redshift = redshift
        self.lines = self._get_lines_from_list()

    def _get_lines_from_list(self, name=None):
        """
        Load the line list as list of Line instances and apply the redshift.
        
        The private method will check that the list's name is valid and 
        retrieve that list from the line dictionary.  Each line is loaded
        into a Line instance and the redshift is applied.  The redshift 
        is taken from the instance's "redshift" attribute.
        
        Parameters
        ----------
        name : str, optional
            Name of the line list to retrieve.  If not specified, use the
            instance's "name" attribute.
        
        Returns
        -------
        list of Line instances
        
        Raises
        ------
        KeyError
            Raised if the line list name is invalid.
        
        See Also
        --------
        LINELIST_DICT for valid line lists.
        The Line class.
        """

        if name is None:
            name = self.name
        
        lines = []
        try:
            for line_data in LINELIST_DICT[name]:
                line = Line(restwlen=line_data[1], redshift=self.redshift, 
                            name=line_data[0]) 
                lines.append(line)
        except KeyError:
            print 'ERROR: Line list name, "%s", invalid.' % (name)
            print 'ERROR: Valid lists are:', LINELIST_DICT.keys()
            raise
        
        return lines
        
    def append_linelist(self, name):
        """
        Append a line list to an existing list.
        
        A line list is appended to the "lines" attribute.  This is a simmple
        append; the duplicates are not removed, the combined list is not
        sorted.  The LineList "name" attribute is set to a new string
        formatted as "oldname+newname".
        
        Parameters
        ----------
        name : str
            Name of the line list to append.
        
        Examples
        --------
        >>> mylinelist = LineList('quasar')
        >>> mylinelist.append_linelist('paschen')
        """
        # duplicates are not removed.
        # list is not sorted
        new_lines = self._get_lines_from_list(name)
        self.lines.extend(new_lines)
        self.name = '%s+%s' % (self.name, name)
        
    def reapply_redshift(self):
        """
        Re-apply the redshift to the lines.
        
        Re-apply the redshift to the lines.  This is useful when the
        redshift attribute is changed.
        
        Examples
        --------
        >>> mylinelist = LineList('quasar', redshift=0.5)
        >>> mylinelist.redshift = 1.0
        >>> mylinelist.reapply_redshift()
        """
        for line in self.lines:
            line.set_redshift(self.redshift)
            line.set_obswlen()


# -------------------------------

# pylint: disable=E1101
#  This disable is to ignore the u.micron errors (dynamic loading)
LINELIST_DICT = {
    'quasar' : [  ('HeI', 0.5876 * u.micron),
                  ('HeI', 1.083 * u.micron),
                  ('H_alpha', 0.6563 * u.micron),
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

# pylint: enable=E1101