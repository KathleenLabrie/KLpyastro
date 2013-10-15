import obstable
from nose.tools import assert_list_equal
from nose.tools import assert_equal
from nose.tools import assert_raises
from nose.tools import assert_multi_line_equal

class TestObsRecord:
    
    @classmethod
    def setup_class(cls):
        TestObsRecord.asciiline = "SDSSJ000429.46-002142.8\tS20130719\tHK\tHK\tScience\tNone\t496-499\t90.0\t6\tfaint"
        TestObsRecord.obsrecord = obstable.ObsRecord(targetname='SDSSJ000429.46-002142.8', 
                                                     rootname='S20130719', 
                                                     band='HK', grism='HK', 
                                                     datatype='Science', applyto='None', 
                                                     filerange='496-499', exptime=90,
                                                     lnrs=6, rdmode='faint')
    
    @classmethod
    def teardown_class(cls):
        pass
    
    def setup(self):
        pass
    
    def teardown(self):
        pass
        
    def test_print_record(self):
        expected_result = "%s" % (TestObsRecord.asciiline)
        result = TestObsRecord.obsrecord.print_record()
        assert_equal(result, expected_result)
    
    def test_read_records(self):
        expected_result = ['SDSSJ000429.46-002142.8', 'S20130719', 'HK', 'HK', 
                           'Science', 'None', '496-499', 90, 6, 'faint']
        record = obstable.ObsRecord()
        record.read_record(TestObsRecord.asciiline)
        result = [record.targetname, record.rootname, record.band, record.grism,
                  record.datatype, record.applyto, record.filerange, record.exptime,
                  record.lnrs, record.rdmode]
        assert_list_equal(result, expected_result)


class TestObsTable(): 
    @classmethod
    def setup_class(cls):
        TestObsTable.filename = 'testtable.dat'
        TestObsTable.obsrecord = obstable.ObsRecord(targetname='SDSSJ000429.46-002142.8', 
                                                     rootname='S20130719', 
                                                     band='HK', grism='HK', 
                                                     datatype='Science', applyto='None', 
                                                     filerange='496-499', exptime=90,
                                                     lnrs=6, rdmode='faint')
        TestObsTable.asciiline = "SDSSJ000429.46-002142.8\tS20130719\tHK\tHK\tScience\tNone\t496-499\t90.0\t6\tfaint"
    
    @classmethod
    def teardown_class(cls):
        pass
    
    def setup(self):
        TestObsTable.obstable = obstable.ObsTable()
        try:
            with open(TestObsTable.filename, 'w') as table:
                table.write(TestObsTable.obstable.titlebar)
                table.write("\n")
                table.write(TestObsTable.asciiline)
                table.write("\n")
                table.write(TestObsTable.asciiline)
                table.write("\n")
        except IOError:
            raise
        table.close()
   
    def teardown(self):
        import os
        del(TestObsTable.obstable)
        os.remove(TestObsTable.filename)

    
    def test_add_records_to_table1(self):
        expected_result = [1,[TestObsTable.obsrecord]]
        TestObsTable.obstable.add_records_to_table(TestObsTable.obsrecord)
        result = []
        result.append(TestObsTable.obstable.length)
        result.append(TestObsTable.obstable.records)
        assert_list_equal(result, expected_result)

    def test_add_records_to_table2(self):
        expected_result = [2,[TestObsTable.obsrecord,TestObsTable.obsrecord]]
        TestObsTable.obstable.add_records_to_table([TestObsTable.obsrecord,TestObsTable.obsrecord])
        result = []
        result.append(TestObsTable.obstable.length)
        result.append(TestObsTable.obstable.records)
        assert_list_equal(result, expected_result)
    
    def test_select_records_from_table(self):
        pass
    
    def test_print_table(self):
        import sys
        from StringIO import StringIO
        saved_stdout = sys.stdout
        
        expected_result = "%s\n%s\n%s\n" % (TestObsTable.obstable.titlebar,TestObsTable.asciiline,TestObsTable.asciiline)
        try:
            out = StringIO()
            sys.stdout = out
            TestObsTable.obstable.add_records_to_table([TestObsTable.obsrecord,TestObsTable.obsrecord])
            TestObsTable.obstable.print_table()
            result = out.getvalue()
            assert_equal(result, expected_result)
        finally:
            sys.stdout = saved_stdout
    
    def test_read_table1(self):
        expected_result = [TestObsTable.obsrecord,TestObsTable.obsrecord]
        TestObsTable.obstable.filename = TestObsTable.filename
        TestObsTable.obstable.read_table()
        result = TestObsTable.obstable.records
        assert_list_equal(result, expected_result)

    def test_read_table2(self):
        expected_result = [TestObsTable.obsrecord,TestObsTable.obsrecord]
        obstable2 = obstable.ObsTable(filename=TestObsTable.filename)
        # this read_table is not necessary but tests whether the
        # a new call to read_table clears records and start clean.
        obstable2.read_table()
        result = obstable2.records
        assert_list_equal(result, expected_result)
    
    def test_write_table1(self):
        # Test file exist when clobber False
        TestObsTable.obstable.add_records_to_table([TestObsTable.obsrecord,TestObsTable.obsrecord])
        TestObsTable.obstable.filename = TestObsTable.filename
        assert_raises(IOError, TestObsTable.obstable.write_table, clobber=False)

    def test_write_table2(self):
        import os
        TestObsTable.obstable.add_records_to_table([TestObsTable.obsrecord,TestObsTable.obsrecord])
        TestObsTable.obstable.filename = 'testtable2.dat'
        TestObsTable.obstable.write_table()
        expected_result = open(TestObsTable.filename, 'r').read()
        result = open('testtable2.dat', 'r').read()
        os.remove('testtable2.dat')
        assert_multi_line_equal(result, expected_result)
    
    def test_append_table(self):
        pass

    
    
    
    
