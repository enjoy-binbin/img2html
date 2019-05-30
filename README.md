# img2html: Convert a image to HTML

`img2html` 用于将图片转化为 HTML 页面，原出于知乎大佬xlzd

```
实现思路：
	将图片每 N*N 个像素合并成一个像素，并取这 N*N 像素的平均值当做合成的像素的颜色。
	然后渲染为 HTML 页面中对应位置的文字颜色。
	代码中虽然使用了 4 个 for 语句，但是其实只是遍历了图片中每个像素一次。
	使用jinja2作为模板引擎，由于用到图片，也会需要PIL库。

注释：
	代码文件里有一些步骤的注释

运行平台:
	win10 x86，Python3.6
	
原出处文章：https://zhuanlan.zhihu.com/p/26149301
```


原始图片             |  转换后
:-------------------------:|:-------------------------:
![before.jpg](https://raw.githubusercontent.com/enjoy-binbin/img2html/master/before.jpg)  | ![after.png](https://raw.githubusercontent.com/enjoy-binbin/img2html/master/after.png) 

### 使用方式
---


#### 代码调用

```Python
# 引包调用
from img2html.converter import Img2HTMLConverter

converter = Img2HTMLConverter()
html = converter.convert('before.jpg')

with open('display.html', 'w', encoding='utf-8') as fp:
	fp.write(html)
    
# converter.py
if __name__ == '__main__':
    converter = Img2HTMLConverter(char='閔')
    img = 'before.jpg'
    html = converter.convert(img)

    with open('display.html', 'w', encoding='utf-8') as fp:
        fp.write(html)
```


### 安装
---

`img2html` 已经上传到了 [PYPI](https://pypi.python.org/pypi/img2html)，所以最简单的安装方式就是使用 pip：

```
$ pip install img2html
```

更新：

```
$ pip install img2html --upgrade
```


当然，你也可以通过源码安装：

```
$ git clone https://github.com/xlzd/img2html.git
$ cd img2html
$ python setup.py install
```

#### 命令行
```
usage: img2html [-h] [-b #RRGGBB] [-s 4~30] [-c CHAR] [-t TITLE] [-f FONT] -i
                IN [-o OUT]

img2html : Convert image to HTML

optional arguments:
  -b #RRGGBB, --background #RRGGBB  background color (#RRGGBB format)
  -s (4~30), --size (4~30)          font size (int)
  -c CHAR, --char CHAR              characters
  -t TITLE, --title TITLE           html title
  -f FONT, --font FONT              html font
  -i IN, --in IN                    image to convert
  -o OUT, --out OUT                 output file
```
