# -*- coding:utf-8 -*-

from PIL import Image
import numpy as np

from UnionFind import *
from MakeColor import *

'''
Create id of the specified pixel in the source image
@param img : numpy array source image
@param row : row of the pixel
@param col : column of the pixel
@return int : id
'''
def create_pixel_id(img, row, col):
  return row*img.shape[1] + col + 1

'''
Get list index id from pixel id.
@param pixel_id : pixel id of the source image
@return int : index
'''
def get_index_from_pixel_id(pixel_id):
  return pixel_id-1

'''
Get pixel element from pixel id of the source image
@param img : numpy array source image
@param pixel_id : pixel id of the source image
@return (int, int) : (row, col)
'''
def get_elem_from_pixe_id(img, pixel_id):
  index = get_index_from_pixel_id(pixel_id)
  row = int(index / img.shape[1])
  col = index % img.shape[1]
  return (row, col)

'''
tau k image segmentation parameter
'''
tau_k = 4.5

'''
Merge two components.
@param id1 : component id to merge
@param id2 : component id to merge
@param edge_value : difference value of intertested edge
@param uf : union find object
@return bool : TRUE if merging two components, else FALSE
'''
def merge(id1, id2, edge_value, uf):
  root_node1 = uf.get_root(id1)
  root_node2 = uf.get_root(id2)
  if edge_value < mint(root_node1, root_node2):
    uf.union(id1=id1, id2=id2, edge_value=edge_value)

'''
Calculate the minimum internal difference between two components.
@param id1 : One of two components to calculate minimum internal difference of boundary
@param id2 : One of two components to calculate minimum internal difference of boundary
@param mcl : Merged Component List
@return float : minimum internal difference between two components
'''
def mint(r1, r2):
  return min(r1.get_min_dif()+tau(r1), r2.get_min_dif()+tau(r2))

'''
Calculate threashold based on the size of the component.
@param mc : merged component to calculate the threashold
@return float : threashold based on the size of the component
'''
def tau(root):
  return float(tau_k / root.get_size())
