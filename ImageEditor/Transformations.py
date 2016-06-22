class Translate:
    def __init__(self):
        pass


# def translate(im, params):
#     params = parse_qs(params)
#     print(params['X'])
#     dx = int(params['X'][0])
#     dy = int(params['Y'][0])
#     x_size = im.size[0]
#     y_size = im.size[1]
#     curr = im.load()
#     new_img = Image.new('RGB', (x_size, y_size))
#     for x in range(x_size):
#         for y in range(y_size):
#             rgb_val = curr[x, y]
#             x_new = x + dx
#             y_new = y + dy
#
#             if x_new in range(x_size) and y_new in range(y_size):
#                 new_img.putpixel((x_new, y_new), rgb_val)
#
#     return new_img

class Rotate:
    def __init__(self):
        pass
