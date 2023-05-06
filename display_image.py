import time
import sys

from rgbmatrix import RGBMatrix, RGBMatrixOptions
from PIL import Image

file_path = '../images/seraphine.png'

image = Image.open(file_path)

options = RGBMatrixOptions()
options.rows = 32
options.cols = 64
options.chain_length = 1
options.parallel = 1
options.hardware_mapping = 'adafruit-hat'

matrix = RGBMatrix(options = options)
