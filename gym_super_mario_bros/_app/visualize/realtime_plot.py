"""An object to show a realtime plot of the value of a discrete line."""
from matplotlib import pyplot as plt
from matplotlib.ticker import MaxNLocator


class RealtimePlot(object):
    """A simple realtime plot to show the value of a discrete line."""

    def __init__(self, figsize=(4, 4)):
        """
        Initialize a new realtime plot.

        Args:
            figsize (tuple): the size of the figure to draw

        Returns:
            None

        """
        # setup caches for metrics
        self.data = []
        # set the figsize of this callback
        self.figsize = figsize
        # create a figure
        self.fig = plt.figure(figsize=self.figsize)
        self.ax = self.fig.add_subplot(1, 1, 1)
        plt.xlabel('Step')
        plt.ylabel('Reward')
        # force integer axis tick labels
        plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True))
        # adjust the layout
        plt.tight_layout()
        plt.show(block=False)
        # create the line
        self.line, = self.ax.plot(self.data)

    def __call__(self, datum):
        """
        Update the plot with a new piece of datum.

        Args:
            datum (float): the number to add to the plot

        Returns:
            None

        """
        # append the datum to the list of data
        self.data.append(datum)
        # update the line's data
        self.line.set_data(list(range(len((self.data)))), self.data)
        # draw the canvas
        self.fig.canvas.draw()
        plt.tight_layout()
        plt.show(block=False)
        # recompute the ax.dataLim
        self.ax.relim()
        # update ax.viewLim using the new dataLim
        self.ax.autoscale_view()


# explicitly define the outward facing API of this module
__all__ = [RealtimePlot.__name__]
