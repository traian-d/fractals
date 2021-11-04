
def mandelbrot(c, max_iter=80):
    z = 0
    n = 0
    while abs(z) <= 2 and n < max_iter:
        z = z*z + c
        n += 1
    return n


def newton(c, max_err=1e-5, max_iter=1e4, decimals=8):
    f_c = func(c)
    count = 0
    output = None
    while abs(f_c.real) >= max_err or abs(f_c.imag) >= max_err:
        f_prime_c = func_der(c)
        if f_prime_c == 0:
            output = c
            break
        c -= f_c / f_prime_c
        f_c = func(c)
        count += 1
        if count >= max_iter:
            output = 0
            break
        output = c
    if abs(c.imag) <= 1e-10:
        output = c.real
    return round(output, decimals) if isinstance(output, float) else complex(round(output.real, decimals), round(output.imag, decimals))


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


def evaluate_function(grid, max_err, max_iter, decimals, algo):
    return {pt: algo(complex(pt[0], pt[1]), max_err, max_iter, decimals) for pt in grid}


def make_image(root_dict, grid, palette, image_file, width, height, file_format='JPEG'):
    import warnings
    from PIL import Image, ImageDraw, ImageColor

    roots = list(set(root_dict.values()))
    roots_len = len(roots)
    palette_len = len(palette)
    color_dict = {roots[i]: i for i in range(roots_len)}
    print(roots)
    if palette_len < roots_len:
        print(roots)
        pad_len = roots_len - palette_len
        palette += ['#000000'] * pad_len
        warnings.warn(f'Palette provided had length {palette_len}, but there were {roots_len} roots. ' +
                      f'Palette was padded with {pad_len} times black.')

    im = Image.new('RGB', (width, height), (0, 0, 0))
    draw = ImageDraw.Draw(im)

    for pt in root_dict:
        img_pt = grid[pt]
        draw.point([img_pt[0], img_pt[1]], ImageColor.getrgb(palette[color_dict[root_dict[pt]]]))

    im.save(image_file, file_format)


if __name__ == '__main__':
    hues = ['#023E8A', '#0077B6', '#90E0EF', '#CAF0F8', '#03045E']

    WIDTH = 10
    HEIGHT = 10

    print('start')
    # grid = make_evaluation_grid(-4, 0, -3, 1, w=WIDTH, h=HEIGHT)
    grid = make_evaluation_grid(-1, 1, -1, 1, w=WIDTH, h=HEIGHT)
    print('made grid')

    evaluated_roots = evaluate_function(grid, max_err=1e-10, max_iter=1e4, algo=newton, decimals=9)
    print('evaluated')

    make_image(evaluated_roots, grid, hues, image_file='images/zzz.jpg', width=WIDTH, height=HEIGHT)
    print('colored')