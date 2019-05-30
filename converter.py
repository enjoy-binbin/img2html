import sys
import time
from collections import namedtuple
from itertools import cycle

import jinja2
from PIL import Image

Point = namedtuple('Point', ['x', 'y'])  # 命名元组 一个个的像素点, 图片的宽高[width, height]
Pixel = namedtuple('Pixel', ['r', 'g', 'b'])  # 命名元组, 上面一个个像素点的rbg值
RenderItem = namedtuple('RenderItem', ['color', 'char'])  # 命名数组, 最后需要渲染的 字 和 字的颜色
RenderGroup = list  # 我理解为了以后改变数据格式方便
HTMLImage = list
# for c in _c:
# print(c)
_c = cycle(r'/-\|')  # 会把一个序列无限的重复下去, 需要自己手动next或者for循环, 用于进度显示

TEMPLATE = '''
<html>
<head>
    <meta charset="utf-8">
    <title>{{ title }}</title>
    <style type="text/css">
        body {
            margin: 0px; padding: 0px; line-height:100%; letter-spacing:0px; text-align: center;
            min-width: {{ width }}px;
            width: auto !important;
            font-size: {{ size }}px;
            background-color: #{{ background }};
            font-family: {{ font_family }};
        }
    </style>
</head>
<body>
<div>
{% for group in html_image %}
    {% for item in group %}<font color="#{{ item.color }}">{{ item.char }}</font>{% endfor %}
    <br>
{% endfor %}
</div>
</body>
</html>'''


def _progress_callback(percent):
    if percent == 100:  # 百分比
        print('\rConvert Done!')
    else:
        lca = getattr(_progress_callback, '_last_call_at', 0)
        if time.time() - lca > 0.2:  # 0.2秒输出一下进度
            _progress_callback._last_call_at = time.time()
            sys.stdout.write('\r{} progress: {:.2f}%'.format(next(_c), percent))
            sys.stdout.flush()


class Img2HTMLConverter(object):
    def __init__(self,
                 font_size=10,
                 char='爱',
                 background='#000000',
                 title='img2html by xlzd',
                 font_family='monospace',
                 progress_callback=None):
        self.font_size = font_size
        self.char = cycle(char)
        self.background = background
        self.title = title
        self.font_family = font_family
        self._prg_cb = progress_callback or _progress_callback

    def convert(self, source):
        image = Image.open(source)

        width, height = image.size
        row_blocks = (round(float(width) / self.font_size))  # 几行(元素就是一个个的字), N*N内的像素平均成一个
        col_blocks = (round(float(height) / self.font_size))  # 几列

        html_image = HTMLImage()
        progress = 0.0  # 像素平均的百分比进度
        step = 1.0 / (col_blocks * row_blocks)  # 下面循环生成一个字后的百分比步长

        for col in range(col_blocks):
            render_group = RenderGroup()
            for row in range(row_blocks):
                pixels = []
                for y in range(self.font_size):
                    for x in range(self.font_size):
                        point = Point(row * self.font_size + x, col * self.font_size + y)
                        if point.x >= width or point.y >= height:
                            # 当坐标点大于图像的宽高时, 就不进行获取像素值
                            continue
                        pixels.append(Pixel(*image.getpixel(point)[:3]))  # (R, G, B, A), 不取最后的透明度值
                average = self.get_average(pixels=pixels)  # 将N*N范围内的(这里是10*10)的像素颜色求平均后赋值给字
                color = self.rgb2hex(average)
                render_item = RenderItem(color=color, char=next(self.char))
                render_group.append(render_item)

                progress += step
                self._prg_cb(progress * 100)

            html_image.append(render_group)

        self._prg_cb(100)
        return self.render(html_image)

    def render(self, html_image):
        template = jinja2.Template(TEMPLATE)
        return template.render(
            html_image=html_image,
            size=self.font_size,
            background=self.background,
            title=self.title,
            font_family=self.font_family,
            width=self.font_size * len(html_image[0]) * 2
        )

    @staticmethod
    def rgb2hex(pixel):
        return '{:02x}{:02x}{:02x}'.format(*pixel)

    @staticmethod
    def get_average(pixels):
        r, g, b = 0, 0, 0
        for pixel in pixels:
            r += pixel.r
            g += pixel.g
            b += pixel.b
        base = float(len(pixels))
        return Pixel(
            r=int(round(r / base)),
            g=int(round(g / base)),
            b=int(round(b / base)),
        )


if __name__ == '__main__':
    converter = Img2HTMLConverter(char='閔')
    img = 'before.jpg'
    html = converter.convert(img)

    with open('display.html', 'w', encoding='utf-8') as fp:
        fp.write(html)
