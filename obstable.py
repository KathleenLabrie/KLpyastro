# obstable.py
"""
Table access Classes
"""

# pylint: disable=C0301
# Targetname rootname  band grism  datatype applyto     filerange exptime LNRS rdmode
#SDSS..       S20130719 HK   HK     Science  None        496-499   90      6    faint
#SDSS..       S20130719 HK   HK     Dark     Science,Arc 592-595   90      1    faint
#SDSS..       S20130719 HK   HK     Flat     Science,Arc 501       4       1    bright
#SDSS..       S20130719 HK   HK     Dark     Flat        588-591   4       1    bright
#etc.
# pylint: enable=C0301

class ObsTable:
    """
    Represents an observations summary table.  Create or extend
    an observations summary table.  The object can be created empty
    with the information like file name and records added later.
    
    :param filename: File name of the table.  If the file does not
        exist, create it.  [Default: None]
    :type filename: str
    :param records: List of observation records, each containing the
        information for one line of the table.  [Default: None]
    :type records: ObsRecords
    """
    
    def __init__(self, filename=None, records=None):
        self.records = []
        self.add_records_to_table(records)
        self.length = len(self.records)
        self.filename = ObsTable.validate_filename(filename)
        if self.filename != None:
            self.read_table(self.filename)
        self.titlebar = "# %s\t\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s" % \
            ('Targetname','rootname', 'band', 'grism', 'datatype', 'applyto',
            'filerange', 'exptime', 'LNRS', 'rdmode')
        return        
        
    @classmethod
    def validate_filename(cls, filename):
        """
        Runs checks on file and returns the filename if everything
        checks out.
        WARNING: It doesn't do any checks right now.
        
        :param filename: File name of the table.
        :type filename: str
        :rtype: str
        """
        # TODO: add some file checking.  
        #       does it exists? if it does, is it a file? 
        #       Can it be open for reading?
        return filename
    
    def add_records_to_table(self, records):
        """
        Add a record (type ObsRecord) or a list of records (type list) 
        to the table.
        
        :param records: Record to add to the table.  Each record
            is one line in the table.
        :type records: ObsRecord or list of ObsRecord
        """
        
        if isinstance(records, list):
            self.records.extend(records)
        elif isinstance(records, ObsRecord):
            self.records.append(records)
        elif records is None:
            pass
        else:
            raise RuntimeError
        self.length = len(self.records)           
        return

#    def select_records_from_table(self, criteria):
#        # criteria is a dictionary
#        #   targetname: ["selection string",equals/contain]
#        #   rootname:  ["selection string", equals/contain]
#        #   band: ["string", equals]
#        #   grism: ["string", equals]
#        #   datatype: ["string", equals]
#        #   applyto:  ["string", equals]
#        #   exptime:  [float, equals]
#        #   LNRS:     [integer, equals]
#        #   rdmode:   [string, equals]
#        #
#        selected_records = []
#        return selected_records
    
    def print_table(self):
        """
        Print formatted table to the screen.
        """
        print self.titlebar
        for record in self.records:
            print record.print_record()
        return
    
    def read_table(self, filename=None):
        """
        Read table from file on disk.
        
        :param filename: Name of the file to read.  If filename is None,
            then the instance's filename attribute must be defined.
        :type filename: str
        """
        
        if filename is None and self.filename is None:
            raise ValueError
        elif filename is None:
            filename = self.filename
            
        try:
            with open(filename, 'r') as table:
                # reset the instance.
                self.records = []
                self.length = 0
                for line in table:
                    if line.startswith('#'):
                        continue
                    try:
                        record = ObsRecord()
                        record.read_record(line)
                        self.add_records_to_table(record)
                    except ValueError:
                        #probably the title bar  
                        # (pretty format doesn't start with #)
                        continue
        except IOError:
            raise
        table.close()

        return
    
    def write_table(self, filename=None, clobber=True):
        """
        Write table to file on disk.
        
        :param filename: Name of the file to write to.  If filename is
            None, then the instance's filename attribute must be set.
        :type filename: str
        :param clobber: Set whether the file can be overwritten or not.
            [Default: True]
        :type clobber: bool
        
        """
        import os
        
        if filename is None and self.filename is None:
            raise IOError
        elif filename is None:
            filename = self.filename

        try:
            if os.path.exists(filename) and clobber==False:
                print "Error: File exists (%s) and overwrite not allowed\n" % \
                    filename
                raise IOError
            with open(filename, 'w') as table:
                table.write(self.titlebar)
                table.write("\n")
                for record in self.records:
                    table.write(record.print_record())
                    table.write("\n")
        except IOError:
            raise
        table.close()

        return
    
#    def append_table(self, filename=None):
#        # use case:  file on disk.  ObsTable contains all new records.  
#        # Append new records.
#        # no checks whether there are duplication.  keep it simple for now.
#        # Not sure if I really need this.  Probably easier to have the whole 
#        # table in memory in the ObsTable.  It's easy enough to merge the 
#        # records if I have two ObsTable.
#        return

    def pretty_table(self):
        """
        Rewrite the table into a pretty format to make it more human
        readable.  The write_table routine does a good job but the
        ascii.write() function makes it even better.  Unfortunately,
        for ascii.write to work well, the table must be read from disk
        by ascii.read.  This means double the i/o.  If the table were
        big that would be a performance hit, but for now, it is not
        a problem.
        """
        from astropy.io import ascii
        table = ascii.read(self.filename)
        ascii.write(table, output=self.filename, 
                    Writer=ascii.FixedWidth, bookend=False, 
                    delimiter=None)
        return

# pylint: disable=R0902
class ObsRecord:
    """
    Record that contains all the information needed for one line
    of the observation summary table.
    
    :param targetname: Name of the target. 'Targetname' column.
    :type targetname: str
    :param rootname: Root name for the dataset. 'rootname' column. Eg. S200130719.
    :type rootname: str
    :param band: Name of the band for the filter. 'band' column. Eg. HK.
    :type band: str
    :param grism: Name of the grism. 'grism' column. Eg. HK.
    :type grism: str
    :param datatype: Type of data. 'datatype' column. Eg. Science, Dark, Flat, Arc,
        Telluric.
    :type datatype: str
    :param applyto: Type of data these dataset can be applied to. 'applyto' column.
        Eg. None, Flat, Science,Arc (for multiple apply), etc.
    :type applyto: str
    :param filerange: String representation of the range of file number.  'filerange'
        column.  Eg. 496-499, 501, 58,60-62.
    :type filerange: str
    :param exptime: Exposure time. 'exptime' column.
    :type exptime: float or str
    :param lnrs: Number of non-destructive read pairs from headers.  Note 
        that at this time the true number is LNRS_header+2 for LNRS>1.  
        For the table, all that matters is that the LNRS matches so the 
        erroneous value from the header will do. 'LNRS' column.
    :type lnrs: int or str
    :param rdmode: Read mode.  'rdmode' column.  Eg. faint, bright, medium(?)
    :type rdmode: str
    """
    # pylint: disable=R0913
    def __init__(self, targetname=None, rootname=None, band=None, grism=None, 
                 datatype=None, applyto=None, filerange=None, exptime=None,
                 lnrs=None, rdmode=None):
        self.targetname = targetname
        self.rootname = rootname
        self.band = band
        self.grism = grism
        self.datatype = datatype
        self.applyto = applyto
        self.filerange = filerange
        self.exptime = float(exptime) if (exptime is not None) else exptime
        self.lnrs = int(lnrs) if (lnrs is not None) else lnrs
        self.rdmode = rdmode
        return
    # pylint: enable=R0913
    
    def __cmp__(self, other):
        assert isinstance(other, ObsRecord)
        return cmp((self.targetname, self.rootname, self.band,
                    self.grism, self.datatype, self.applyto,
                    self.filerange, self.exptime, self.lnrs,
                    self.rdmode),
                   (other.targetname, other.rootname, other.band,
                    other.grism, other.datatype, other.applyto,
                    other.filerange, other.exptime, other.lnrs,
                    other.rdmode))

    def print_record(self):
        """
        Convert a record to a formatted string that can then be
        printed to screen or sent to file.
        
        :rtype: str
        """
        
        # TODO: print_record will fail if one of the attribute is 
        # TODO: set to None.  Add checks.
        record_string = "%s\t%s\t%s\t%s\t%s\t\t%s\t%s\t\t%.1f\t%d\t%s" % \
            (self.targetname,
            self.rootname,
            self.band,
            self.grism,
            self.datatype,
            self.applyto,
            self.filerange,
            self.exptime,
            self.lnrs,
            self.rdmode)
        return record_string
    
    def read_record(self, line):
        """
        Parse an ascii representation of a record.  The string is a line
        from the table on disk.
        
        :param line: A line from the table on disk.
        :type line: str
        """
        
        (self.targetname, self.rootname,
         self.band, self.grism,
         self.datatype, self.applyto,
         self.filerange, self.exptime,
         self.lnrs, self.rdmode) = line.split()
        
        self.exptime = float(self.exptime)
        self.lnrs = int(self.lnrs)
         
        return
# pylint: enable:R0902

