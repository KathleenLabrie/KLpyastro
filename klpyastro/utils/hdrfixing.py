# hdrfixing.py
"""
Collection of functions to fix various problems in the
fits headers.
"""

def rm_extrawcs_hdr(hdr, baddim, verbose=False):
    """
    Remove leftover WCS headers referring to a dimension that
    does not exist in the data.  For example, remove WCS headers
    referring to the second axis of an extracted 1-D spectrum.

    The header is modified in-place.

    Parameters
    ----------
    hdr : pyfits.header.Header
        The header to be corrected.
    baddim : integer
        The dimension or axis that does not exist anymore and
        for which the header still contain WCS information.
    verbose : boolean
        Toggle on or off the verbose mode

    Raises
    ------
    See Also
    --------
    Examples
    --------
    """
    cdx_x = 'CD' + str(baddim) + '_' + str(baddim)
    ctypex = 'CTYPE' + str(baddim)
    ltmx_x = 'LTM' + str(baddim) + '_' + str(baddim)

    keywords_to_remove = [cdx_x, ctypex, ltmx_x]
    for keyword in keywords_to_remove:
        try:
            hdr.remove(keyword)
            if verbose:
                print 'Removing ', keyword
        except ValueError, e:
            print e
            print '    Nothing to fix.'

    return
