#Table access functions

class ObsTable:
    def __init__(self, filename=None, records=None):
        self.records = []
        self.add_records_to_table(records)
        self.length = len(self.records)
        self.filename = self.set_filename(filename)
        if self.filename != None:
            self.read_table(self.filename)
        self.titlebar = "# %s\t\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s" % \
            ('Targetname','rootname', 'band', 'grism', 'datatype', 'applyto',
            'filerange', 'exptime', 'LNRS', 'rdmode')
        return        
        
    def set_filename(self, filename):
        # might want to add some file checking
        return filename
    
    def add_records_to_table(self, records):
        """
        Add a record (type ObsRecord) or a list of records (type list) to the table.
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

    def select_records_from_table(self, criteria):
        # criteria is a dictionary
        #   targetname: ["selection string",equals/contain]
        #   rootname:  ["selection string", equals/contain]
        #   band: ["string", equals]
        #   grism: ["string", equals]
        #   datatype: ["string", equals]
        #   applyto:  ["string", equals]
        #   exptime:  [float, equals]
        #   LNRS:     [integer, equals]
        #   rdmode:   [string, equals]
        #
        selected_records = []
        return selected_records
    
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
        """
        
        if filename is None and self.filename is None:
            raise IOError
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
                    record = ObsRecord()
                    record.read_record(line)
                    self.add_records_to_table(record)
        except IOError:
            raise
        table.close()

        return
    
    def write_table(self, filename=None, clobber=True):
        """
        Write table to file on disk.
        """
        import os
        
        if filename is None and self.filename is None:
            raise IOError
        elif filename is None:
            filename = self.filename

        try:
            if os.path.exists(filename) and clobber==False:
                print "Error: File exists (%s) and overwrite not allowed\n" % filename
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
    
    def append_table(self, filename=None):
        # use case:  file on disk.  ObsTable contains all new records.  Append new records.
        # no checks whether there are duplication.  keep it simple for now.
        # Not sure if I really need this.  Probably easier to have the whole table
        # in memory in the ObsTable.  It's easy enough to merge the records if I have
        # two ObsTable.
        return
    
class ObsRecord:
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
        """
        
        record_string = "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%.1f\t%d\t%s" % \
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
        """
        
        (self.targetname, self.rootname,
         self.band, self.grism,
         self.datatype, self.applyto,
         self.filerange, self.exptime,
         self.lnrs, self.rdmode) = line.split()
        
        self.exptime = float(self.exptime)
        self.lnrs = int(self.lnrs)
         
        return
 
# Targetname rootname  band grism  datatype applyto     filerange exptime LNRS rdmode
#SDSS..       S20130719 HK   HK     Science  None        496-499   90      6    faint
#SDSS..       S20130719 HK   HK     Dark     Science,Arc 592-595   90      1    faint
#SDSS..       S20130719 HK   HK     Flat     Science,Arc 501       4       1    bright
#SDSS..       S20130719 HK   HK     Dark     Flat        588-591   4       1    bright
#etc.
