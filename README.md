# All sizes icon generator

> tips: broken English below ;)

## Introduction

一个用于生成全尺寸icon的python包。

在Windows系统中，应用程序所使用的icon需要是全尺寸的。也即一个同时包含16x, 32x, 64x, 128x, 256x图像的icon文件。而asicon_generator就可以完成这样的icon的生成。

asicon_generator不需要安装任何python的第三方包，它直接生成符合icon文件规范的二进制数据并进行存储来实现（为此我啃了2天的书 XD ）。

---

A python package which can generate all-size icon.

In Windows OS, application's icon must be all-sized, which contains 16x, 32x, 64x, 128x and 256x bitmap images in one single file. And, **asicon_generator** can generate icon file like that.

**asicon_generator** does not need any third party package. It directly generates and stores binary data that conforms to icon file specification(and I went through the information for two days :( ).

## Usage

下载`asicon_generator.py`并拷贝到你的项目根目录或者一个空目录，然后：

Download files and copy `asicon_generator.py` to your project root, or a empty folder.

Then.

```python
asi = ASIcon('./icon.png')
asi.save('./test.ico')
```

在这个例子中，我们有一张名为icon.png的图片。它必须是一个正方形，否则会报错——毕竟icon都是正方形的嘛。

然后ASIcon类会完成icon二进制数据的生成，接下来只需要调用save方法指定保存的路径即可。

In this example, we have an image named `icon.png`. It must be square size, or the program will raise an error.

Then the ASIcon Object will complete the generation of icon binary data. Then, you just need to call the save method to specify the path to save.