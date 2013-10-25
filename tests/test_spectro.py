import spectro
from nose.tools import assert_equal
from nose.tools import assert_list_equal

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
        pass
    
    @classmethod
    def teardown_class(cls):
        pass
    
    def setup(self):
        pass
    
    def teardown(self):
        pass
    
    def test_get_lines_from_list(self):
        pass
    
    def test_apply_redshift(self):
        pass

    
class TestSpectrum:
    
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
        
    def test_get_counts_array_from_hdu(self):
        pass
    
    def test_get_pixel_array_from_hdu(self):
        pass
    
    def test_get_wcs_from_hdu(self):
        pass
    
    def test_apply_wcs_to_pixels(self):
        pass
    

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
    

    