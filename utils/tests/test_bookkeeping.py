import os
import os.path
import bookkeeping
from nose.tools import assert_list_equal
from nose.tools import assert_dict_equal
from astrodata import AstroData

class TestBookkeeping:
    
    @classmethod
    def setup_class(cls):
        TestBookkeeping.f2sciencefile=os.path.join('tests','S20131002S0046.fits')
        TestBookkeeping.f2darkfile=os.path.join('tests','S20131002S0217.fits')
        TestBookkeeping.f2flatfile=os.path.join('tests','S20131002S0055.fits')
        TestBookkeeping.f2arcfile=os.path.join('tests','S20131002S0054.fits')
   
    @classmethod
    def teardown_class(cls):
        pass
    
    def setup(self):
        pass
    
    def teardown(self):
        pass
    
    def test_query_header1(self):
        expected_result = { #'targetname':'SDSSJ022721.25-010445.8',
                            'band':'JH',
                            'grism':'JH',
                            'exptime':90.,
                            'lnrs': 6,
                            'rdmode': 'Faint'
                           }
        ad = AstroData(TestBookkeeping.f2sciencefile)
        result = {}
        #result['targetname'] = bookkeeping.query_header(ad, 'targetname')
        result['band'] = bookkeeping.query_header(ad, 'band')
        result['grism'] = bookkeeping.query_header(ad, 'grism')
        result['exptime'] = bookkeeping.query_header(ad, 'exptime')
        result['lnrs'] = bookkeeping.query_header(ad, 'lnrs')
        result['rdmode'] = bookkeeping.query_header(ad, 'rdmode')
        assert_dict_equal(result, expected_result)

    def test_query_header2(self):
        expected_result = { 'band':'dark',
                            'grism':'Open',
                            'exptime':8.,
                            'lnrs': 1,
                            'rdmode': 'Bright'
                           }
        ad = AstroData(TestBookkeeping.f2darkfile)
        result = {}
        result['band'] = bookkeeping.query_header(ad, 'band')
        result['grism'] = bookkeeping.query_header(ad, 'grism')
        result['exptime'] = bookkeeping.query_header(ad, 'exptime')
        result['lnrs'] = bookkeeping.query_header(ad, 'lnrs')
        result['rdmode'] = bookkeeping.query_header(ad, 'rdmode')
        assert_dict_equal(result, expected_result)

    def test_query_header3(self):
        expected_result = { 'band':'JH',
                            'grism':'JH',
                            'exptime':8.,
                            'lnrs': 1,
                            'rdmode': 'Bright'
                           }
        ad = AstroData(TestBookkeeping.f2flatfile)
        result = {}
        result['band'] = bookkeeping.query_header(ad, 'band')
        result['grism'] = bookkeeping.query_header(ad, 'grism')
        result['exptime'] = bookkeeping.query_header(ad, 'exptime')
        result['lnrs'] = bookkeeping.query_header(ad, 'lnrs')
        result['rdmode'] = bookkeeping.query_header(ad, 'rdmode')
        assert_dict_equal(result, expected_result)
    
    def test_query_header4(self):
        expected_result = { 'band':'JH',
                            'grism':'JH',
                            'exptime':30.,
                            'lnrs': 6,
                            'rdmode': 'Faint'
                           }
        ad = AstroData(TestBookkeeping.f2arcfile)
        result = {}
        result['band'] = bookkeeping.query_header(ad, 'band')
        result['grism'] = bookkeeping.query_header(ad, 'grism')
        result['exptime'] = bookkeeping.query_header(ad, 'exptime')
        result['lnrs'] = bookkeeping.query_header(ad, 'lnrs')
        result['rdmode'] = bookkeeping.query_header(ad, 'rdmode')
        assert_dict_equal(result, expected_result)

    def test_create_record(self):
        pass
    
    def test_parse_filerange(self):
        filerange1 = '210-214'
        filerange2 = '215'
        filerange3 = '216,217'
        filerange4 = '218-221,223-225'
        filerange5 = '226,227-228,230,232-234'
        expected_result = [210,211,212,213,214,215,216,217,218,219,220,221,
                           223,224,225,226,227,228,230,232,233,234]
        result = bookkeeping.parse_filerange(filerange1)
        result.extend(bookkeeping.parse_filerange(filerange2))
        result.extend(bookkeeping.parse_filerange(filerange3))
        result.extend(bookkeeping.parse_filerange(filerange4))
        result.extend(bookkeeping.parse_filerange(filerange5))
        
        assert_list_equal(result,expected_result)
    
    #@attr('interactive')
    def test_mktable_helper(self):
        pass
    
    def test_mkdirectories(self):
        import shutil
        
        program='GS-2013-Q-73'
        targetname='SDSSJ022721.25-010445.8'
        obsdate='20131002'
        reduxdate='15Oct2013'
        bands=['JH','HK']
        expected_result = [('GS-2013-Q-73', ['raw', 'SDSSJ022721.25-010445.8'], []), ('GS-2013-Q-73/raw', [], []), ('GS-2013-Q-73/SDSSJ022721.25-010445.8', ['20131002-15Oct2013', 'sciproducts'], []), ('GS-2013-Q-73/SDSSJ022721.25-010445.8/20131002-15Oct2013', ['reduxHK', 'reduxJH'], ['README']), ('GS-2013-Q-73/SDSSJ022721.25-010445.8/20131002-15Oct2013/reduxHK', [], []), ('GS-2013-Q-73/SDSSJ022721.25-010445.8/20131002-15Oct2013/reduxJH', [], []), ('GS-2013-Q-73/SDSSJ022721.25-010445.8/sciproducts', [], [])]
        bookkeeping.mkdirectories(program, targetname, obsdate,
                                  reduxdate, bands)
        result = []
        for dirstruct in os.walk(program):
            result.append(dirstruct)
        shutil.rmtree(program)
        assert_list_equal(result, expected_result)   
        