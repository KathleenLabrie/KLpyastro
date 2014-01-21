# plottools.py
"""
Collection of classes to help create plots.
"""
import matplotlib.pyplot as plt

class Plot:
    """
    Base class for a plot.
    
    :param title: Plot title. Optional.
    :type title: str
    """
    def __init__(self, title=None):
        self.fig = plt.figure()
        self.axplot = self.fig.add_subplot(1, 1, 1)
        for item in [self.fig, self.axplot]:
            item.patch.set_visible(False)
        if title is not None:
            self.set_title(title)
    
    def set_title(self, title):
        """
        Add a title to the plot.
        
        :param title: Title to assign to the plot.
        :type title: str
        """
        self.axplot.set_title(title)

    def set_axis_label(self, label, axis):
        """
        Add an axis label to the plot.
        
        :param label: Label to assign to axis.
        :type title: str
        :param axis: Name of the axis, x or y
        :type axis: str
        """
        if axis == 'x':
            self.axplot.set_xlabel(label)
        elif axis == 'y':
            self.axplot.set_ylabel(label)
        else:
            errmsg = 'Valid axis names are x and y.'
            raise ValueError, errmsg


class SpPlot(Plot):
    """
    Class to create and customize a spectrum plot. Subclasses Plot.
    
    :param title: Title to assign to the plot.
    :type title: str
    """
    def __init__(self, title=None):
        Plot.__init__(self, title)
    
    def plot_spectrum(self, sp1d, title=None):
        """
        Plot the spectrum (counts vs wavelength) with title and axis labels.
        
        :param sp1d: A Spectrum instance.
        :type sp1d: Spectrum object.
        :param title: Title for the plot. Optional.
        :type title: str
        """
        if title is not None:
            self.set_title(title)
        self.set_axis_label(''.join(['Wavelength [', sp1d.wunit.name,']']), 'x')
        self.set_axis_label('Counts', 'y')
        self.axplot.plot(sp1d.wlen, sp1d.counts, 'k')
        self.axplot.axis('tight')
        self.fig.canvas.draw()
        return

    def adjust_ylimits(self, ylim1, ylim2):
        """
        Adjust the lower and upper bounds to the y-axis.
        
        :param ylim1: Lower limit for the y-axis.
        :type ylim1: float
        :param ylim2: Upper limit for the y-axis.
        :type ylim2: float
        """
        self.axplot.set_ylim(ylim1, ylim2)
        self.fig.canvas.draw()
        return

    def erase_plot(self, line_position=0):
        """
        Erase the spectrum but not the box and axes.
        
        :param line_position: Position on the stack of the spectrum to
            erase.
        :type line_position: int
        """
        self.axplot.lines.pop(line_position).remove
        self.fig.canvas.draw()
        return

    def annotate_lines(self, lines):
        """
        Annotate the plot with spectra line identifications.
        
        :param lines: The line list to add to the plot. The lines are stored
            in a list of tuples with (obswlen, name), where obswlen is a float
            and name is a string.
        :type lines: list of tuples
        """
        # lines is list of tuple (obswlen, name)
        (xlow, xhigh) = self.axplot.get_xlim()
        (_, yhigh) = self.axplot.get_ylim()
        ypos = yhigh * 0.8
        ydelta = yhigh * 0.05
        i = 0
        for line in lines:
            if line[0] > xlow and line[0] < xhigh:
                self.axplot.text(line[0], ypos-(i*ydelta)-ydelta*1.25, '|',
                             horizontalalignment='center',
                             verticalalignment='center',
                             fontsize=10)
                self.axplot.text(line[0], ypos-(i*ydelta), line[1],
                             horizontalalignment='center',
                             verticalalignment='center',
                             fontsize=10)
                i += 1
        self.fig.canvas.draw()

        return

    #def draw_band_limits(self):
    #    return

    def write_png(self, output_name):
        """
        Write the figure to a PNG file.
        
        :param output_name: Name of the output file. 
            ??Is the extension .png required or is it added automatically??
        :type output_name: str
        """        
        self.fig.savefig(output_name)
        return
    
    