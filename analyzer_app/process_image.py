import tifffile as tiff
import numpy as np
import matplotlib.pyplot as plt

def process_image(filepath):
    image = tiff.imread(filepath)
    labels = tiff.imread
    