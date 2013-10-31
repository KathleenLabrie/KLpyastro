import spectro
from astropy import units as u
from astrodata import AstroData
from astropy.io import fits as pf
from nose.tools import assert_equal
from nose.tools import assert_list_equal
from nose.tools import assert_almost_equal
from numpy.testing import assert_array_equal
import numpy as np
import os.path

class TestLine:
    
    @classmethod
    def setup_class(cls):
        TestLine.line = spectro.Line(restwlen=1.282,
                                     obswlen=2.564,
                                     redshift=1.,
                                     name='Pa_beta')
        TestLine.expected_result = [1.282,2.564,1.,'Pa_beta']
    
    @classmethod
    def teardown_class(cls):
        pass
    
    def setup(self):
        TestLine.newline = spectro.Line(restwlen=1.282,
                                        obswlen=2.564,
                                        redshift=1.,
                                        name='Pa_beta')
    
    def teardown(self):
        del TestLine.newline
    
    def test_init1(self):
        # empty initialization
        expected_result = [None,None,None,None]
        line = spectro.Line()
        result = [line.restwlen,line.obswlen,line.redshift,line.name]
        assert_list_equal(result, expected_result)
    
    def test_init2(self):
        # full initialization
        expected_result = TestLine.expected_result
        line = spectro.Line(restwlen=1.282, obswlen=2.564,
                            redshift=1., name='Pa_beta')
        result = [line.restwlen,line.obswlen,line.redshift,line.name]
        assert_list_equal(result, expected_result)      

    def test_init3(self):
        # partial initialization
        expected_result = TestLine.expected_result
        line = spectro.Line(restwlen=1.282,
                            redshift=1., name='Pa_beta')
        result = [line.restwlen,line.obswlen,line.redshift,line.name]
        assert_list_equal(result, expected_result)
    
    def test_set_obswlen1(self):
        # no calculations, set by argument.
        expected_result = 3.
        line = TestLine.newline
        line.set_obswlen(3.)
        result = line.obswlen
        assert_equal(result, expected_result)
    
    def test_set_obswlen2(self):
        # calculate
        expected_result = TestLine.line.obswlen
        line = spectro.Line(restwlen=1.282,
                            redshift=1., name='Pa_beta')
        line.set_obswlen()
        result = line.obswlen
        assert_equal(result, expected_result)

    def test_set_obswlen3(self):
        # with Quantity objects
        expected_result = TestLine.line.obswlen * u.micron
        line = spectro.Line(restwlen=1.282*u.micron,
                            redshift=1., name='Pa_beta')
        line.set_obswlen()
        result = line.obswlen
        assert_equal(result, expected_result)
        
    def test_set_restwlen1(self):
        # no calculations, set by argument.
        expected_result = 3.
        line = TestLine.newline
        line.set_restwlen(3.)
        result = line.restwlen
        assert_equal(result, expected_result)
    
    def test_set_restwlen2(self):
        # calculate
        expected_result = TestLine.line.restwlen
        line = spectro.Line(obswlen=2.564,
                            redshift=1., name='Pa_beta')
        line.set_restwlen()
        result = line.restwlen
        assert_equal(result, expected_result)

    def test_set_redshift1(self):
        # no calculations, set by argument.
        expected_result = 3.
        line = TestLine.newline
        line.set_redshift(3.)
        result = line.redshift
        assert_equal(result, expected_result)
    
    def test_set_redshift2(self):
        # calculate
        expected_result = TestLine.line.redshift
        line = spectro.Line(restwlen=1.282, obswlen=2.564,
                            name='Pa_beta')
        line.set_redshift()
        result = line.redshift
        assert_equal(result, expected_result)

    def test_set_name(self):
        expected_result = 'Pa_alpha'
        line = TestLine.newline
        line.set_name('Pa_alpha')
        result = line.name
        assert_equal(result, expected_result)


class TestLineList:
        
    @classmethod
    def setup_class(cls):
        TestLineList.quasar_rest = \
                [ ('HeI', 0.5876 * u.micron),
                  ('HeI', 1.083 * u.micron),
                  ('H_alpha', 0.6563 * u.micron),
                  ('Pa_epsilon', 0.9546 * u.micron),
                  ('Pa_delta', 1.005 * u.micron),
                  ('Pa_gamma', 1.094 * u.micron),
                  ('Pa_beta', 1.282 * u.micron),
                  ('Pa_alpha', 1.875 * u.micron)
                 ]
    
    @classmethod
    def teardown_class(cls):
        pass
    
    def setup(self):
        TestLineList.linelist = spectro.LineList('quasar')
    
    def teardown(self):
        del TestLineList.linelist
    
    def test_init(self):
        # setup init a LineList
        expected_result = TestLineList.quasar_rest
        expected_result.extend(['quasar', 0.])
        result = []
        for line in TestLineList.linelist.lines:
            result.append( (line.name, line.restwlen) )
        result.extend([TestLineList.linelist.name, TestLineList.linelist.redshift])
        assert_list_equal(result,expected_result)
    
    def test_get_lines_from_list(self):
        expected_result = TestLineList.quasar_rest
        result = []
        for line in TestLineList.linelist.lines:
            result.append( (line.name, line.restwlen) )
        assert_list_equal(result,expected_result)
            
    def test_apply_redshift(self):
        expected_result = []
        for (name, wlen) in TestLineList.quasar_rest:
          expected_result.append((name,wlen*2))
        TestLineList.linelist.apply_redshift(1.)
        result = []
        for line in TestLineList.linelist.lines:
            result.append( (line.name, line.obswlen) )
        assert_list_equal(result, expected_result)
       
    
class TestSpectrum:
    
    @classmethod
    def setup_class(cls):
        testdir = os.path.dirname(os.path.abspath(__file__))
        
        TestSpectrum.testfile = os.path.join(testdir, 'JHK.fits')
        TestSpectrum.wcs_string = "WCSAXES =                    1 / Number of coordinate axes                      CRPIX1  =                    1 / Pixel coordinate of reference point            PC1_1   =        6.57288848851 / Coordinate transformation matrix element       CDELT1  =                    1 / Coordinate increment at reference point        CTYPE1  = 'LINEAR'             / Coordinate type code                           CRVAL1  =        9719.45605469 / Coordinate value at reference point            LATPOLE =                   90 / [deg] Native latitude of celestial pole        RESTFRQ =                    0 / [Hz] Line rest frequency                       RESTWAV =                    0 / [Hz] Line rest wavelength                      RADESYS = 'FK5'                / Equatorial coordinate system                   MJD-OBS =        56580.1992188 / [d] MJD of observation matching DATE-OBS       DATE-OBS= '2013-10-15T04:46:52.500' / ISO-8601 observation date matching MJD-OBS"

    
    @classmethod
    def teardown_class(cls):
        pass
    
    def setup(self):
        TestSpectrum.ad = AstroData(TestSpectrum.testfile)
        TestSpectrum.adhdu = TestSpectrum.ad['SCI',1]
        TestSpectrum.apf = pf.open(TestSpectrum.testfile)
        TestSpectrum.apfhdu = TestSpectrum.apf[0]
    
    def teardown(self):
        TestSpectrum.ad.close()
        TestSpectrum.apf.close()
        
    def test_get_counts_array_from_hdu1(self):
        # test passing an ad
        expected_result = TestSpectrum.adhdu.data
        sp = spectro.Spectrum(TestSpectrum.adhdu, wunit=u.Angstrom)
        result = sp.counts
        assert_array_equal(result, expected_result)

    def test_get_counts_array_from_hdu2(self):
        # test passing an astropy hdu
        expected_result = TestSpectrum.adhdu.data
        sp = spectro.Spectrum(TestSpectrum.apfhdu, wunit=u.Angstrom)
        result = sp.counts
        assert_array_equal(result, expected_result)
            
    def test_get_pixel_array_from_hdu1(self):
        expected_result = np.arange(TestSpectrum.apfhdu.header['NAXIS1'])
        sp = spectro.Spectrum(TestSpectrum.adhdu, wunit=u.Angstrom)
        result = sp.pix
        assert_array_equal(result, expected_result)

    def test_get_pixel_array_from_hdu2(self):
        expected_result = np.arange(TestSpectrum.apfhdu.header['NAXIS1'])
        sp = spectro.Spectrum(TestSpectrum.apfhdu, wunit=u.Angstrom)
        result = sp.pix
        assert_array_equal(result, expected_result)
    
    def test_get_wcs_from_hdu1(self):
        expected_result = TestSpectrum.wcs_string
        sp = spectro.Spectrum(TestSpectrum.adhdu, wunit=u.Angstrom)
        result = sp.wcs.wcs.to_header()
        assert_equal(result, expected_result)
    
    def test_get_wcs_from_hdu2(self):
        expected_result = TestSpectrum.wcs_string
        sp = spectro.Spectrum(TestSpectrum.apfhdu, wunit=u.Angstrom)
        result = sp.wcs.wcs.to_header()
        assert_equal(result, expected_result)
    
    def test_get_wunit1(self):
        expected_result = u.Angstrom
        sp = spectro.Spectrum(TestSpectrum.adhdu)
        result = sp.wunit
        assert_equal(result, expected_result)

    def test_get_wunit2(self):
        expected_result = u.Angstrom
        sp = spectro.Spectrum(TestSpectrum.apfhdu)
        result = sp.wunit
        assert_equal(result, expected_result)
    
    def test_apply_wcs_to_pixels(self):
        expected_result = [9719.456, 16292.345, 24981.703]
        sp = spectro.Spectrum(TestSpectrum.adhdu)
        result = [sp.wlen[0],sp.wlen[1000],sp.wlen[-1]]
        assert_almost_equal(result[0], expected_result[0],3)
        assert_almost_equal(result[1], expected_result[1],3)
        assert_almost_equal(result[2], expected_result[2],3)


class TestAtmosphericTransparency:

    @classmethod
    def setup_class(cls):
        pass
    
    @classmethod
    def teardown_class(cls):
        pass
    
    def setup(self):
        pass
    
    def teardown(self):
        pass

    def test_init(self):
        pass
   
    
class TestTransmissionBand:
    
    @classmethod
    def setup_class(cls):
        pass
    
    @classmethod
    def teardown_class(cls):
        pass
    
    def setup(self):
        pass
    
    def teardown(self):
        pass

    def test_init(self):
        pass
    
class TestBandList:
    
    @classmethod
    def setup_class(cls):
        pass
    
    @classmethod
    def teardown_class(cls):
        pass
    
    def setup(self):
        pass
    
    def teardown(self):
        pass
    

    