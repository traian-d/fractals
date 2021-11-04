import abc


class Fractal(abc.ABC):

    @abc.abstractmethod
    def evaluate(self, *args):
        """This method should evaluate the fractal on a point grid."""

    @abc.abstractmethod
    def make_image(self, *args):
        """This method should return an image of the fractal evaluated on a point grid."""
