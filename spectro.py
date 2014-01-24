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

    def validate_wavelengths(self):
        assert self.obswlen == (self.redshift + 1) * self.restwlen

class Spectrum:
    def __init__(self, hdu, wunit=None):
        self.counts = self.get_counts_array_from_hdu(hdu)
        self.pix = self.get_pixel_array_from_hdu(hdu)
        self.wcs = self.get_wcs_from_hdu(hdu)
        self.wlen = self.apply_wcs_to_pixels()
        self.wunit = wunit
        
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