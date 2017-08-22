import os
import glob

def imdelete(inputstring, silent=True):
    """
    Delete .fits files a-la IRAF imdelete.

    Parameters
    ----------
    inputstring : str
        Allowed inputs:
            prefix@sci.lis
            @sci.lis
            S20001010S0001
            S20001010S0001.fits
            S*.fits
            S20001010S0001.fits, S20001010S0010.fits
            prefix@sci.lis, @sci.lis, S*.fits, S20001010S0001.fits

        .fits extension: optional, will be added if missing

    """

    # split input string on commas
    input_elements = [s.strip() for s in inputstring.split(',')]

    filelist = []
    for element in input_elements:
        if '@' in element:
            filelist.extend(getatlist(element))
        elif '*' in element:
            filelist.extend(glob.glob(element))
        elif '?' in element:
            filelist.extend(glob.glob(element))
        else:
            filelist.append(element)

    filelist = [s+'.fits' if not s.endswith('.fits') else s for s in filelist]

    for fname in filelist:
        try:
            os.remove(fname)
        except OSError:
            if not silent:
                print('%s not found' % fname)

    return

def getatlist(atlist):
    """
    Returns a list containing the expanded and prefixed content of
    the input file.

    Parameters
    ----------
    atlist : str
        A string with an '@' in it to indicate that we are interested in
        the list content for a file.  Any characters before the '@' is
        consider a prefix to the string inside the file.
        Eg. @sci.lis, rg@sci.lis

    Returns
    -------
    A list containing the expanded and prefixed content of the input file.
    """

    (prefix, listname) = atlist.split('@')
    filelist = []
    for rootname in getlines(listname):
        if len(rootname) > 0:
            filelist.append(prefix+rootname)
    return filelist


def getlines(fname):
    """
    Returns the content of a file as a list of lines, striped of the '\n'
    and trainling spaces.

    Parameters
    ----------
    fname : str
        Text file to open.

    Returns
    -------
    List of lines

    """
    with open(fname) as f:
        content = f.readlines()
    return [line.rstrip() for line in content]

