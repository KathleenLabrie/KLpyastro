import matplotlib.pyplot as plt

class Plot:
    def __init__(self, title=None):
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(1,1,1)
        for item in [self.fig, self.ax]:
            item.patch.set_visible(False)
        if title is not None:
            self.set_title(title)
    
    def set_title(self, title):
        self.ax.set_title(title)

class SpPlot(Plot):
    def __init__(self, title=None):
        Plot.__init__(self, title)
    
    def plot_spectrum(self, sp, title=None):
        if title is not None:
            self.set_title(title)
        self.ax.set_xlabel(''.join(['Wavelength [', sp.wunit.name,']']))
        self.ax.set_ylabel('Counts')
        self.ax.plot(sp.wlen, sp.counts, 'k')
        self.ax.axis('tight')
        self.fig.canvas.draw()
        return

    def adjust_ylimits(self, y1, y2):
        self.ax.set_ylim(y1,y2)
        self.fig.canvas.draw()
        return

    def erase_plot(self, line_position=0):
        self.ax.lines.pop(line_position).remove
        self.fig.canvas.draw()
        return

    def annotate_lines(self, lines):
        # lines is list of tuple (obswlen, name)
        (xlow, xhigh) = self.ax.get_xlim()
        (ylow, yhigh) = self.ax.get_ylim()
        ypos = yhigh * 0.8
        ydelta = yhigh * 0.05
        i=0
        for line in lines:
            if line[0] > xlow and line[0] < xhigh:
                self.ax.text(line[0], ypos-(i*ydelta)-ydelta*1.25, '|',
                             horizontalalignment='center',
                             verticalalignment='center',
                             fontsize=10)
                self.ax.text(line[0], ypos-(i*ydelta), line[1],
                             horizontalalignment='center',
                             verticalalignment='center',
                             fontsize=10)
                i+=1
        self.fig.canvas.draw()

        return

    def draw_band_limits(self):
        return

    def write_png(self, output_name):        
        self.fig.savefig(output_name)
        return
    
    