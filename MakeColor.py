# -*- coding:utf-8 -*-

import colorsys
from random import shuffle

'''
Convert color from hsv to rgb color space.
@param hsv : hsv color tuple [h[0,359],s[0.0-1.0],v[0.0-1.0]]
@return (int) : rgb color tuple (r[0,255],g[0,255],b[0,255])
'''
def hsv2rgb(hsv):
  return tuple(i*255 for i in colorsys.hsv_to_rgb(hsv[0], hsv[1], hsv[2]))

'''
Max hue value
'''
MAX_HUE = 360

'''
Create colors divided by hue value.
@param div_n : number of colors to create
@return [(int, int, int)] : list of rgb colors
'''
def create_colors(div_n):
  colors = list()
  for n in range(div_n):
    hue = float(n/div_n)
    colors.append(hsv2rgb((hue, 1.0, 1.0)))
  return colors

'''
Randomize order when create colors
@param div_n : number of colors to create
@return [(int, int, int)] : list of rgb colors
'''
def create_random_colors(div_n):
  colors = create_colors(div_n)
  shuffle(colors)
  return colors

'''
Calculate luminance
@param rgb : list pf rgb value of the pixel
@return float : luminance
'''
def calc_luminance(rgb):
  if type(rgb): # rgb or rgba
    return 0.298912*rgb[0] + 0.586611*rgb[1] + 0.114478*rgb[2]
  else:
    return rgb # monocolor
