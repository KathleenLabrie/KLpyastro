import matplotlib.pyplot as plt

class Plot:
    def __init__(self, title=None):
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(1,1,1)
        if title is not None:
            self.set_title(title)
    
    def set_title(self, title):
        self.ax.set_title(title)

class SpPlot(Plot):
    def __init__(self, title=None):
        Plot.__init__(self, title)
    
    def plot_spectrum(sp, title=None):
        if title is not None:
            self.set_title(title)
        self.ax.set_xlabel(''.join['Wavelength [', sp.wunit.name,']'])
        self.ax.set_ylabel('Counts')
        self.ax.plot(sp.wlen, sp.counts)
        
        return

    def annotate_lines():
        return

    def draw_band_limits():
        return

    def write_png():
        return