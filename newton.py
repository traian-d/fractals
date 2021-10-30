from PIL import Image, ImageDraw, ImageColor


def mandelbrot(c, iters=80):
    z = 0
    n = 0
    while abs(z) <= 2 and n < iters:
        z = z*z + c
        n += 1
    return n


def newton(c, max_err=1e-5, max_iter=1e4):
    f_c = func(c)
    count = 0
    while abs(f_c.real) >= max_err or abs(f_c.imag) >= max_err:
        f_prime_c = func_der(c)
        if f_prime_c == 0:
            return c
        c -= f_c / f_prime_c
        f_c = func(c)
        count += 1
        if count >= max_iter:
            return 0
    if abs(c.imag) <= 1e-10:
        return c.real
    return c


def func(x):
    return x ** 5 - 3j * x**3 - (5 + 2j) + x
    # return x ** 5 - 3j * x**3 - (5 + 2j) * x ** 2 + 3*x + 1
    # return x**3 - 2*x + 2


def func_der(x):
    return 5 * x ** 4 - 9j * x**2 + 1
    # return 5 * x ** 4 - 9j * x**2 - 10 * x - 4j * x + 3
    # return 3 * x**2 - 2


def linear_interpolation(color1, color2, t):
    return color1 * (1 - t) + color2 * t


def make_evaluation_grid(re_start, re_end, im_start, im_end, w=600, h=400):
    range_re = re_end - re_start
    range_im = im_end - im_start
    return {(re_start + (x / w) * range_re, im_start + (y / h) * range_im): (x, y) for x in range(0, w) for y in range(0, h)}


def evaluate_function(grid, max_err, max_iter, algo):
    return {pt: algo(complex(pt[0], pt[1]), max_err, max_iter) for pt in grid}


def get_pixel_colors(root_dict, grid, palette, decimals=8):
    import warnings
    root_dict = {k: round(v, decimals) if isinstance(v, float) else complex(round(v.real, decimals), round(v.imag, decimals)) for (k, v) in root_dict.items()}
    roots = list(set(root_dict.values()))
    roots_len = len(roots)
    palette_len = len(palette)
    color_dict = {roots[i]: i for i in range(roots_len)}
    if palette_len < roots_len:
        print(roots)
        pad_len = roots_len - palette_len
        palette += ['#000000'] * pad_len
        warnings.warn(f'Palette provided had length {palette_len}, but there were {roots_len} roots. ' +
                      f'Palette was padded with {pad_len} times black.')
    return {grid[pt]: ImageColor.getrgb(palette[color_dict[root_dict[pt]]]) for pt in root_dict}


if __name__ == '__main__':
    # hues = ['#0d1b2a', '#1B263B', '#415A77', '#778DA9', '#E0E1DD']
    # hues = ['#0B132B', '#1C2541', '#3A506B', '#5BC0BE', '#6FFFE9']
    # hues = ['#004E64', '#00A5CF', '#9FFFCB', '#25A18E', '#7AE582']
    # hues = ['#99D98C', '#52B69A', '#168AAD', '#1E6091', '#D9ED92']
    hues = ['#023E8A', '#0077B6', '#90E0EF', '#CAF0F8', '#03045E'] #nuante de albastru
    # hues = ['#FF0000', '#000000', '#ffffff', '#0000ff', '#ffff00']
    # hues = [(0, 8, 20), (0, 29, 61), (0, 53, 102), (255, 195, 0), (255, 214, 10)]
    # hues = [(217, 100, 42), (212, 100, 53), (209, 100, 62), (47, 100, 99), (50, 100, 100)]

    WIDTH = 400
    HEIGHT = 400

    # -2, 1, 0, 1
    # -3, 1, -0.8, 1.25 - for narrow  x ** 5 - 3j * x**3 - (5 + 2j) * x ** 2 + 3*x + 1
    print('start')
    grid = make_evaluation_grid(-4, 0, -3, 1, w=WIDTH, h=HEIGHT)
    print('made grid')
    evaluated_roots = evaluate_function(grid, max_err=1e-10, max_iter=1e4, algo=newton)
    print('evaluated')
    pixel_colors = get_pixel_colors(evaluated_roots, grid, hues, decimals=9)
    print('colored')
    im = Image.new('RGB', (WIDTH, HEIGHT), (0, 0, 0))
    draw = ImageDraw.Draw(im)

    for pt in pixel_colors:
        draw.point([pt[0], pt[1]], pixel_colors[pt])

    im.save('zzz.jpg', 'JPEG')
