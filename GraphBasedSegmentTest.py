# -*- coding:utf-8 -*-

'''
Sample program of graph based segmentation algorithm with Union Find
'''

# Import required packages
from PIL import Image
import numpy as np

from SegmentationProcess import *

# Load image via PIL.
src_file = 'images/sample12.jpg'
# src_file = 'images/texture.png'
img = np.array(Image.open(src_file))
# Specify destination output file.
dst = 'result/gbs_ret.png'
# Specify coloring2segmentations each of which has top n area. 
top_n = 20
# Specify tau_k parameter optinally.
tau_k = 150

# Print image information
print("file : {0}, shape:{1}".format(src_file, img.shape))

# Initialize SegmentationProcess.
ggs = GridGraphSegmentation(img, dst, top_n, tau_k)
# Traing the image and output a image file.
ggs.train()

'''
# Initialize SegmentationProcess.
nn = 2
nngs = NearestNeightborGraphSegmentation(img, dst, top_n, tau_k, nn)
# Traing the image and output a image file.
nngs.train()
'''