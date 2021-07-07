# plottools.py
"""
Collection of classes to help create plots.
"""
import matplotlib.pyplot as plt


class Plot(object):
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
        :type label: str
        :param axis: Name of the axis, x or y
        :type axis: str
        """
        if axis == 'x':
            self.axplot.set_xlabel(label)
        elif axis == 'y':
            self.axplot.set_ylabel(label)
        else:
            errmsg = 'Valid axis names are x and y.'
            raise ValueError(errmsg)


class SpPlot(Plot):
    """
    Class to create and customize a spectrum plot. Subclasses Plot.

    :param title: Title to assign to the plot.
    :type title: str
    """
    def __init__(self, title=None):
        Plot.__init__(self, title)

    def plot_spectrum(self, sp1d, title=None, color='k'):
        """
        Plot the spectrum (counts vs wavelength) with title and axis labels.

        :param sp1d: A Spectrum instance.
        :type sp1d: Spectrum object.
        :param title: Title for the plot. Optional.
        :type title: str
        :param color: Colour of the line
        :type color: str
        """
        if title is not None:
            self.set_title(title)
        self.set_axis_label(''.join(['Wavelength [', sp1d.wunit.name, ']']),
                            'x')
        self.set_axis_label('Counts', 'y')
        self.axplot.plot(sp1d.wlen, sp1d.counts, color)
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
            if xlow < line[0] < xhigh:
                self.axplot.text(line[0], ypos-(i*ydelta)-ydelta*1.25, '|',
                                 horizontalalignment='center',
                                 verticalalignment='center', fontsize=10)
                self.axplot.text(line[0], ypos-(i*ydelta), line[1],
                                 horizontalalignment='center',
                                 verticalalignment='center', fontsize=10)
                i += 1
        self.fig.canvas.draw()

        return

    # def draw_band_limits(self):
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


class MultiPlot(object):
    def __init__(self, nrows=1, ncols=1, title=None):
        self.nrows = nrows
        self.ncols = ncols
        if title is not None:
            self.title = title
        self.plots_titles = None
        self.plots_labels = None
        self.plots_data = None
        self.pdf = None

    def add_data(self, plots_data, plots_labels=None):
        """

        Parameters
        ----------
        plot_data : list of tuple
            tuples of x and y data, one tuple per plot

        """
        self.plots_data = plots_data
        if plots_labels is not None:
            self.add_labels(plots_labels)

    def add_labels(self, plots_labels):
        self.plots_labels = plots_labels

    def add_titles(self, plots_titles):
        self.plots_titles = plots_titles

    def set_size(self, width, height):
        self.width = width
        self.height = height

    def plot(self, png=False, filename='multiplot.png', pdf=None):
        self.fig, self.axs = plt.subplots(self.nrows, self.ncols)
        self.fig.suptitle(self.title)
        self.fig.set_size_inches(self.width, self.height)

        nplots = len(self.plots_data)
        plotid = 0
        for axrow in self.axs:
            for ax in axrow:
                xlabel = None
                ylabel = None
                title = None

                if plotid == nplots:
                    break   # fewer plots then slots

                x = self.plots_data[plotid][0]
                y = self.plots_data[plotid][1]
                if len(self.plots_labels) == 1:
                    xlabel = self.plots_labels[0][0]
                    ylabel = self.plots_labels[0][1]
                elif self.plots_labels is not None:
                    xlabel = self.plots_labels[plotid][0]
                    ylabel = self.plots_labels[plotid][1]
                if self.plots_titles is not None:
                    title = self.plots_titles[plotid]

                ax.plot(x, y)
                ax.set_title(title)
                ax.set(xlabel=xlabel, ylabel=ylabel)
                plotid += 1

        self.fig.tight_layout(rect=[0, 0.03, 1, 0.95])

        if pdf:
            pdf.savefig()

        if png:
            plt.savefig(filename)
        else:
            plt.show()

    def save_plot(self, filename='multiplot.png'):
        self.plot(save=True, filename=filename)

    def close(self):
        plt.close()




"""
import plottools
from importlib import reload
import numpy as np

x = np.linspace(0, 2 * np.pi, 400)
y = np.sin(x ** 2)

m = plottools.MultiPlot(2,2,'test')
plot_data = [(x,y), (x,-y), (-x, y), (-x, -y)]
plot_labels = [('x axis', 'y axis'),('x axis', '-y axis'),('-x axis', 'y axis'),('-x axis', '-y axis')]

m.add_data(plot_data, plot_labels)
m.plot()

"""