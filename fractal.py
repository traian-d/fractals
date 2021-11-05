import abc


class Fractal(abc.ABC):

    @abc.abstractmethod
    def evaluate(self, *args):
        """This method should evaluate the fractal on a point grid."""

    @abc.abstractmethod
    def get_color(self, pt):
        """This method should return the desired color for a point (given as a complex number)"""

    @property
    @abc.abstractmethod
    def height(self):
        """Returns grid height."""

    @property
    @abc.abstractmethod
    def width(self):
        """Returns grid width."""

    def make_grid(self, re_start, re_end, im_start, im_end):
        import numpy as np
        range_re = re_end - re_start
        range_im = im_end - im_start
        return np.transpose(np.array([[complex(re_start + (x / self.width) * range_re,
                                               im_start + (y / self.height) * range_im) for x in range(self.width)]
                                      for y in range(self.height)]))

    def make_image(self, evaluated):
        from PIL import Image, ImageDraw, ImageColor

        im = Image.new('RGB', (self.width, self.height), (0, 0, 0))
        draw = ImageDraw.Draw(im)

        for i in range(self.width):
            for j in range(self.height):
                img_pt = evaluated[i, j]
                draw.point([i, j], ImageColor.getrgb(self.get_color(img_pt)))

        return im
