# -*- coding:utf-8 -*-

from PIL import Image
import numpy as np

import MakeColor as mcolor
from GraphBasedSegment import *

'''
Make monocolor segmented image with top n area segment.
@param img  : source image
@param uf   : union find (result)
@param n    : colorize top n are segment
@param name : result image file name
'''
def create_monocolor_result(img, uf, n, name):
  # image size
  row = img.shape[0]
  col = img.shape[1]

  segmented_image = np.zeros((row, col), dtype=np.uint8)
  uf_subset = uf.subsetall()
  # n can not be over size of mc_dict
  n = min(n, len(uf_subset))
  # Get top n of sorted subset 
  sorted_uf_subset = sorted(uf_subset, key=lambda x:x[1], reverse=True)[:n]
  # Create n sets of colors and root ids
  colors = [(i+1)*255/n for i in range(n)]
  id_color_dict = dict()
  for subset, color in zip(sorted_uf_subset, colors):
    id_color_dict[subset[0]] = color
    print("Size : {0}, color : {1}".format(subset[1], color))

  # Get all table
  uf_table = uf.get_all_union()

  # Apply a color to each component
  for uf_id, value in enumerate(uf_table):
    # Empty element
    if uf_id == 0:
      continue

    elem = get_elem_from_pixe_id(img, uf_id)

    uf_id = uf.find(uf_id)
    if uf_id in id_color_dict:
      color = id_color_dict[uf_id]
      segmented_image[elem[0], elem[1]] = color

  img_raw = Image.fromarray(segmented_image, 'L')
  img_raw.save(name)

'''
Make rgb color segmented image with top n area segment.
@param img  : source image
@param uf   : union find (result)
@param n    : colorize top n are segment
@param name : result image file name
'''
def create_colored_result(img, uf, n, name):
  # image size
  row = img.shape[0]
  col = img.shape[1]

  segmented_image = np.zeros((row, col, 3), dtype=np.uint8)
  uf_subset = uf.subsetall()
  # n can not be over size of mc_dict
  n = min(n, len(uf_subset))
  # Get top n of sorted subset 
  sorted_uf_subset = sorted(uf_subset, key=lambda x:x[1], reverse=True)[:n]
  # Create n sets of colors and root ids
  colors = mcolor.create_random_colors(n)
  id_color_dict = dict()
  for subset, color in zip(sorted_uf_subset, colors):
    id_color_dict[subset[0]] = color
    print("Size : {0}, color : {1}".format(subset[1], color))

  # Get all table
  uf_table = uf.get_all_union()
  # Apply a color to each component
  for uf_id, value in enumerate(uf_table):
    # Empty element
    if uf_id == 0:
      continue

    elem = get_elem_from_pixe_id(img, uf_id)

    uf_id = uf.find(uf_id)
    if uf_id in id_color_dict:
      color = id_color_dict[uf_id]
      segmented_image[elem[0], elem[1], 0] = color[0]
      segmented_image[elem[0], elem[1], 1] = color[1]
      segmented_image[elem[0], elem[1], 2] = color[2]

  img_raw = Image.fromarray(segmented_image)
  img_raw.save(name)
