import fractal


class Mandelbrot(fractal.Fractal):
    __slots__ = ('__w', '__h', '__max_iter', '__grid')

    def __init__(self, re_start, re_end, im_start, im_end, max_iter=100, w=600, h=400):
        self.__max_iter = max_iter
        self.__w = w
        self.__h = h
        self.__grid = self.make_grid(re_start, re_end, im_start, im_end)

    def __compute(self, c):
        z = 0
        n = 0
        while abs(z) <= 4 and n < self.__max_iter:
            z = z*z + c
            n += 1
        return n

    def evaluate(self):
        import numpy as np
        compute_v = np.vectorize(self.__compute)
        return compute_v(self.__grid)

    def get_color(self, pt):
        # Smooth coloring scheme, others exist.
        hue = int(255 * pt / self.__max_iter)
        saturation = 255
        value = 255 if pt < self.__max_iter else 0
        return hue, saturation, value

    @property
    def height(self):
        return self.__h

    @property
    def width(self):
        return self.__w

    def make_image(self, evaluated):
        from PIL import Image, ImageDraw

        im = Image.new('HSV', (self.__w, self.__h), (0, 0, 0))
        draw = ImageDraw.Draw(im)

        for i in range(self.__w):
            for j in range(self.__h):
                img_pt = evaluated[i, j]
                color = self.get_color(img_pt)
                draw.point([i, j], color)

        return im.convert('RGB')


class Newton(fractal.Fractal):
    __slots__ = ('__w', '__h', '__max_err', '__max_iter', '__decimals', '__grid', '__palette', '__color_dict')

    def __init__(self, re_start, re_end, im_start, im_end, w=600, h=400,
                 max_err=1e-5, max_iter=1e4, decimals=8):
        self.__w = w
        self.__h = h
        self.__max_err = max_err
        self.__max_iter = max_iter
        self.__decimals = decimals
        self.__grid = self.make_grid(re_start, re_end, im_start, im_end)
        self.__palette = ['#023E8A', '#0077B6', '#90E0EF', '#CAF0F8', '#03045E']
        self.__color_dict = {}

    def __compute(self, c, func, func_der):
        f_c = func(c)
        count = 0
        output = None
        while abs(f_c.real) >= self.__max_err or abs(f_c.imag) >= self.__max_err:
            f_prime_c = func_der(c)
            if f_prime_c == 0:
                output = c
                break
            c -= f_c / f_prime_c
            f_c = func(c)
            count += 1
            if count >= self.__max_iter:
                output = 0
                break
            output = c
        if abs(c.imag) <= 1e-10:
            output = c.real
        return complex(round(output, self.__decimals), 0) if isinstance(output, float) else \
            complex(round(output.real, self.__decimals), round(output.imag, self.__decimals))

    def evaluate(self, func, func_der):
        import warnings
        import numpy as np
        compute_v = np.vectorize(self.__compute)
        computed = compute_v(self.__grid, func, func_der)

        roots = np.unique(computed.flatten())
        roots_len = len(roots)
        palette_len = len(self.__palette)
        self.__color_dict = {roots[i]: i for i in range(roots_len)}
        if palette_len < roots_len:
            print(roots)
            pad_len = roots_len - palette_len
            self.__palette += ['#000000'] * pad_len
            warnings.warn(f'Palette provided had length {palette_len}, but there were {roots_len} roots. ' +
                          f'Palette was padded with {pad_len} times black.')

        return computed

    def get_color(self, pt):
        return self.__palette[self.__color_dict[pt]]

    @property
    def height(self):
        return self.__h

    @property
    def width(self):
        return self.__w


def func(x):
    # return x ** 5 - 3j * x**3 - (5 + 2j) + x
    # return x ** 5 - 3j * x**3 - (5 + 2j) * x ** 2 + 3*x + 1
    return x**3 - 2*x + 2


def func_der(x):
    # return 5 * x ** 4 - 9j * x**2 + 1
    # return 5 * x ** 4 - 9j * x**2 - 10 * x - 4j * x + 3
    return 3 * x**2 - 2


if __name__ == '__main__':

    mdb = Mandelbrot(-2, 1, -1, 1, w=int(1024 * 3/2), h=1024)
    evaluated = mdb.evaluate()
    im = mdb.make_image(evaluated)
    im.save('images/mdb.jpg', 'JPEG')

    # newt = Newton(-4, 4, -4, 4, w=1024, h=1024, max_err=1e-10, max_iter=1e2, decimals=9)
    # evaluated = newt.evaluate(func, func_der)
    # im = newt.make_image(evaluated)
    # im.save('images/zzz2.jpg', 'JPEG')
