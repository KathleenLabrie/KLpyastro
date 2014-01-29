import sys
from math import pi
from astropy.io import fits
import numpy as np
import matplotlib.pyplot as plt
import stsci.convolve._lineshape as ls

# In KLpy
import fitpy.fittools as ft

# Utility function to open and plot original spectrum
def openNplot1d (filename, extname=('SCI',1)):
    hdulist = fits.open(filename, 'readonly')
    sp = hdulist[extname].data
    x = np.arange(sp.shape[0])
    plt.clf()
    plt.plot (x, sp)
    
    return hdulist

# Interactive specification of the section around the feature to work on
def getsubspec (sp):
    # here it should be graphical, but I'm still working on that
    x1 = input("Left edge pixel: ")
    x2 = input("Right edge pixel: ")
    
    flux = sp[x1:x2]
    pixel = np.arange(x1,x2,1)
    
    sub = np.zeros((2,flux.shape[0]))
    sub[0] = pixel
    sub[1] = flux
    
    #plt.clf()
    #plt.plot (pixel, flux)
    
    #input('continue')

    return sub

def plotresult (sp, bf, nsp):
    plt.clf()
    x = np.arange(0,sp.shape[0],1)
    plt.plot (x, sp)
    plt.plot (x, nsp)
    x = np.arange(0,bf.shape[0],1)
    plt.plot (x, bf)

def rmfeature (inspec, outspec, params=None, profile='voigt'):
    #---- plot and get data
    spin = openNplot1d(inspec)
    specdata = spin['SCI'].data
    spin.close()

    #---- Get data for section around feature
    linedata = getsubspec(specdata)
    
    #---- Calculate and set initial parameter from linedata

    if params==None:
        contslope = (linedata[1][0] - linedata[1][-1]) / \
                    (linedata[0][0] - linedata[0][-1])
        contlevel = linedata[1][0] - (contslope * linedata[0][0])
        lineindex = linedata.argmin(1)[1]
        lineposition = linedata[0][lineindex]
        linestrength = linedata[1][lineindex] - \
                       ((contslope*linedata[0][lineindex]) + contlevel)
        linewidth = 20.   # pixels.  should find a better way.

        cte = ft.Parameter(contlevel)
        m = ft.Parameter(contslope)
        A = ft.Parameter(linestrength)
        mu = ft.Parameter(lineposition)
        fwhmL = ft.Parameter(linewidth)
        fwhmD = ft.Parameter(linewidth)
    else:
        cte = ft.Parameter(params[0])
        m = ft.Parameter(params[1])
        A = ft.Parameter(params[2])
        mu = ft.Parameter(params[3])
        fwhmL = ft.Parameter(params[4])
        fwhmD = ft.Parameter(params[5])

    #---- Define function [linear (continuum) + lorentz (feature)]
    #     I don't know where the factor 10 I need to apply to A() comes from.
    #     I'll need to figure it out.
    #
    #     Also, those functions apparently need to be defined after the
    #     cte(), m(), etc. Parameter instances are defined.

    def line(x):
        return cte() + m()*x

    def lorentz(x):     # The version in numarray.convolve._lineshape is wrong
        amp = A() * fwhmL() * pi / 2.
        return amp * (fwhmL()/(2.*pi))/((x-mu())**2. + (fwhmL()/2.)**2.)

    def voigt(x):   # import numarray.convolve._lineshape as ls
    #    a = sqrt(log(2.)) * fwhmL() / (2. * fwhmD())
    #    b = 2. * sqrt(log(2.)) * (x - mu()) / fwhmD()
    #    H = exp(-(b**2)) + a/(sqrt(pi)*b**2.)
        amp = A() * 1.      # not right
#        amp = A() * (1. + (fwhmL()/fwhmD())*(fwhmL()*pi/2.))
        return amp * ls.voigt(x, (fwhmD(),fwhmL()), mu())

    def contlorentz(x):
        return line(x) + lorentz(x)

    def contvoigt(x):
        return line(x) + voigt(x)

    #---- Non-linear least square fit (optimize.leastsq)
    if (params==None):
        if profile=='voigt':    # Get initial params from Lorentz fit.
            ft.nlfit(contlorentz, [cte, m, A, mu, fwhmL], linedata[1], x=linedata[0])
            ft.nlfit(contvoigt, [cte, m, A, mu, fwhmD, fwhmL], linedata[1], x=linedata[0]) 
        elif profile=='lorentz':
            ft.nlfit(contlorentz, [cte, m, A, mu, fwhmL], linedata[1], x=linedata[0])
            fwhmD=ft.Parameter(None)
    else:
        pass

    #---- retrieve line profile parameters only and create a profile 
    #     with zero continuum for the entire range for the original spectrum
    #     Then remove the feature

    if profile=='voigt':
        newspecdata = specdata - voigt(np.arange(0,specdata.shape[0],1))
        bestfit = contvoigt(np.arange(0,specdata.shape[0],1))
    elif profile=='lorentz':
        newspecdata = specdata - lorentz(np.arange(0,specdata.shape[0],1))
        bestfit = contlorentz(np.arange(0,specdata.shape[0],1))

    #---- display the original spectrum, the best fit and the
    #     new spectrum.  The feature should be gone

    plotresult(specdata, bestfit, newspecdata)
    print "Best Fit Parameters:"
    print " section = ",linedata[0][0],",",linedata[0][-1]+1
    print "     cte = ",cte()
    print "       m = ",m()
    print "       A = ",A()
    print "      mu = ",mu()
    print "   fwhmL = ",fwhmL()
    print "   fwhmD = ",fwhmD()

    write = raw_input('Write corrected spectrum to '+outspec+'? (y/n): ')

    #---- write output spectrum
    if write=='y':
        spout = fits.open(inspec,'readonly')  # just to create copy of HDUList
        spout['SCI'].data = newspecdata
        spout.writeto(outspec, output_verify='ignore')
        #print ("Not implemented yet, but it isn't the app cool!")
    else:
        print ("Too bad.")


if __name__ == '__main__':
    if len(sys.argv) == 3:
        rmfeature(sys.argv[1], sys.argv[2])
    elif len(sys.argv) > 3:
        params = sys.argv[3:size(sys.argv)]
        rmfeature(sys.argv[1], sys.argv[2], params=params)
    else:
        print "Usage: rmfeature in.fits out.fits <params>"
        
        

