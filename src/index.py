import os
import threading
import webview
import tkinter as tk
import subprocess
import base64

from time import time
from tkinter import simpledialog, Tk, Label, Button, Radiobutton, IntVar
from PIL import Image
from io import BytesIO

class Api:
    def __init__(self):
        self.EDS_ROM = None
    def fullscreen(self):
        webview.windows[0].toggle_fullscreen()

    def save_content(self, content):
        filename = webview.windows[0].create_file_dialog(webview.SAVE_DIALOG)
        if not filename:
            return

        with open(filename, 'w') as f:
            f.write(content)
    def select_graphics(self, graphics_choice, index):
        self.graphics_choice = graphics_choice
        with open(self.EDS_ROM[0], 'rb+') as EDS_ROM:
            if graphics_choice == 'Cards':
                EDS_ROM.seek(0x5E047)
                card_graphics_starting_offset = str(EDS_ROM.read(1).hex())
                EDS_ROM.seek(-2, 1)
                card_graphics_starting_offset = card_graphics_starting_offset + str(EDS_ROM.read(1).hex())
                EDS_ROM.seek(-2, 1)
                card_graphics_starting_offset = card_graphics_starting_offset + str(EDS_ROM.read(1).hex())
                EDS_ROM.seek(-2, 1)
                card_graphics_starting_offset = card_graphics_starting_offset + str(EDS_ROM.read(1).hex())
                EDS_ROM.seek(0x5E043)
                card_palettes_starting_offset = str(EDS_ROM.read(1).hex())
                EDS_ROM.seek(-2, 1)
                card_palettes_starting_offset = card_palettes_starting_offset + str(EDS_ROM.read(1).hex())
                EDS_ROM.seek(-2, 1)
                card_palettes_starting_offset = card_palettes_starting_offset + str(EDS_ROM.read(1).hex())
                EDS_ROM.seek(-2, 1)
                card_palettes_starting_offset = card_palettes_starting_offset + str(EDS_ROM.read(1).hex())
                EDS_ROM.seek(int('0x' + card_graphics_starting_offset, 16) - 0x08000000 + 0x10E0 * index)
                card_graphic = EDS_ROM.read(0x10E0)
                EDS_ROM.seek(int('0x' + card_palettes_starting_offset, 16) - 0x08000000 + 0x80 * index)
                card_palette = EDS_ROM.read(0x80)
                pixels = [0] * 0x1680
                def decode(paramArrayOfbyte: bytearray, paramInt1: int):
                    b1 = 0
                    for b2 in range(720):
                        i1 = paramArrayOfbyte[paramInt1] & 0xFF
                        paramInt1 += 1
                        n = paramArrayOfbyte[paramInt1] & 0xFF
                        paramInt1 += 1
                        m = paramArrayOfbyte[paramInt1] & 0xFF
                        paramInt1 += 1
                        k = paramArrayOfbyte[paramInt1] & 0xFF
                        paramInt1 += 1
                        j = paramArrayOfbyte[paramInt1] & 0xFF
                        paramInt1 += 1
                        i = paramArrayOfbyte[paramInt1] & 0xFF
                        paramInt1 += 1
                        pixels[b1] = i >> 2 & 0x3F
                        b1 += 1
                        pixels[b1] = (i & 0x3) << 4 | j >> 4 & 0xF
                        b1 += 1
                        pixels[b1] = (j & 0xF) << 2 | k >> 6 & 0x3
                        b1 += 1
                        pixels[b1] = k & 0x3F
                        b1 += 1
                        pixels[b1] = m >> 2 & 0x3F
                        b1 += 1
                        pixels[b1] = (m & 0x3) << 4 | n >> 4 & 0xF
                        b1 += 1
                        pixels[b1] = (n & 0xF) << 2 | i1 >> 6 & 0x3
                        b1 += 1
                        pixels[b1] = i1 & 0x3F
                        b1 += 1
                    return pixels
                card_graphic = decode(card_graphic, 0)
                output = open('output.8bpp', 'wb')
                output.write(bytes(card_graphic))
                output = open('output.gbapal', 'wb')
                output.write(bytes(card_palette))
                output.close()
                subprocess.call(['gbagfx.exe', 'output.8bpp', 'output.png', '-palette', 'output.gbapal', '-mwidth', '9'])
                card_graphic = Image.open('output.png')
                sub_image = card_graphic.crop(box=(0,0,8,80)).transpose(Image.FLIP_LEFT_RIGHT)
                card_graphic.paste(sub_image, box=(0,0))
                sub_image = card_graphic.crop(box=(8,0,16,80)).transpose(Image.FLIP_LEFT_RIGHT)
                card_graphic.paste(sub_image, box=(8,0))
                sub_image = card_graphic.crop(box=(16,0,24,80)).transpose(Image.FLIP_LEFT_RIGHT)
                card_graphic.paste(sub_image, box=(16,0))
                sub_image = card_graphic.crop(box=(24,0,32,80)).transpose(Image.FLIP_LEFT_RIGHT)
                card_graphic.paste(sub_image, box=(24,0))
                sub_image = card_graphic.crop(box=(32,0,40,80)).transpose(Image.FLIP_LEFT_RIGHT)
                card_graphic.paste(sub_image, box=(32,0))
                sub_image = card_graphic.crop(box=(40,0,48,80)).transpose(Image.FLIP_LEFT_RIGHT)
                card_graphic.paste(sub_image, box=(40,0))
                sub_image = card_graphic.crop(box=(48,0,56,80)).transpose(Image.FLIP_LEFT_RIGHT)
                card_graphic.paste(sub_image, box=(48,0))
                sub_image = card_graphic.crop(box=(56,0,64,80)).transpose(Image.FLIP_LEFT_RIGHT)
                card_graphic.paste(sub_image, box=(56,0))
                sub_image = card_graphic.crop(box=(64,0,72,80)).transpose(Image.FLIP_LEFT_RIGHT)
                card_graphic.paste(sub_image, box=(64,0))
                card_graphic.save('output.png')
                
                # Read the output.png file and convert it to base64
                with open('output.png', 'rb') as img_file:
                    img_data = img_file.read()
                    img_base64 = base64.b64encode(img_data).decode('utf-8')
                
                return f"data:image/png;base64,{img_base64}"
    def open_file_dialog(self):
        file_types = ('GBA ROM Files (*.gba)', 'All files (*.*)')

        self.EDS_ROM = window.create_file_dialog(
            webview.OPEN_DIALOG, allow_multiple=True, file_types=file_types
        )
        return self.EDS_ROM
    def ls(self):
        return os.listdir('.')


def ask_multiple_choice_question(prompt, options):
    root = Tk()
    if prompt:
        Label(root, text=prompt).pack()
    v = IntVar()
    for i, option in enumerate(options):
        Radiobutton(root, text=option, variable=v, value=i).pack(anchor="w")
    Button(text="Submit", command=root.destroy).pack()
    root.mainloop()
    return options[v.get()]


def gba_color_to_rgb(color):
    """Converts a 15-bit GBA color value to RGB."""
    r = (color & 0x1F) << 3
    g = ((color >> 5) & 0x1F) << 3
    b = ((color >> 10) & 0x1F) << 3
    return r, g, b


def convert_palette(f, output_format="rgb"):
    """Converts a GBA palette file to RGB or hex values."""
    palette = []
    while True:
        color_bytes = f.read(2)
        if not color_bytes:
            break
        color = int.from_bytes(color_bytes, byteorder="little")
        if output_format == "rgb":
            palette.append(gba_color_to_rgb(color))
        else:
            palette.append(f"#{color:04X}")
    return palette






def get_entrypoint():
    def exists(path):
        return os.path.exists(os.path.join(os.path.dirname(__file__), path))

    if exists('../gui/index.html'): # unfrozen development
        return '../gui/index.html'

    if exists('../Resources/gui/index.html'): # frozen py2app
        return '../Resources/gui/index.html'

    if exists('./gui/index.html'):
        return './gui/index.html'

    raise Exception('No index.html found')


def set_interval(interval):
    def decorator(function):
        def wrapper(*args, **kwargs):
            stopped = threading.Event()

            def loop(): # executed in another thread
                while not stopped.wait(interval): # until stopped
                    function(*args, **kwargs)

            t = threading.Thread(target=loop)
            t.daemon = True # stop if the program exits
            t.start()
            return stopped
        return wrapper
    return decorator



entry = get_entrypoint()

@set_interval(1)
def update_ticker():
    if len(webview.windows) > 0:
        webview.windows[0].evaluate_js('window.pywebview.state.setTicker("%d")' % time())


if __name__ == '__main__':
    window = webview.create_window('Open EDS ROM', entry, js_api=Api())
    webview.start(window, debug=True)
