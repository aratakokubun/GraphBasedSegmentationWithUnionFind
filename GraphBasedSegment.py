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
'''
class GraphBasedSegment:

  '''
  Initialize Segment
  @param uf : Union Find object
  @param tau_k : merge segmentation parameter
  '''
  def __init__(self, uf, tau_k):
    self.uf = uf
    self.tau_k = tau_k

  '''
  Merge two components.
  @param id1 : component id to merge
  @param id2 : component id to merge
  @param edge_value : difference value of intertested edge
  @return bool : TRUE if merging two components, else FALSE
  '''
  def merge(self, id1, id2, edge_value):
    root_node1 = self.uf.get_root(id1)
    root_node2 = self.uf.get_root(id2)
    if edge_value < self.mint(root_node1, root_node2):
      self.uf.union(id1=id1, id2=id2, edge_value=edge_value)

  '''
  Calculate the minimum internal difference between two components.
  @param id1 : One of two components to calculate minimum internal difference of boundary
  @param id2 : One of two components to calculate minimum internal difference of boundary
  @param mcl : Merged Component List
  @return float : minimum internal difference between two components
  '''
  def mint(self, r1, r2):
    return min(r1.get_min_dif()+self.tau(r1), r2.get_min_dif()+self.tau(r2))

  '''
  Calculate threashold based on the size of the component.
  @param mc : merged component to calculate the threashold
  @return float : threashold based on the size of the component
  '''
  def tau(self, root):
    return float(self.tau_k / root.get_size())

'''
Preserve pixel, rgba and value
'''
class Component:

  '''
  Constructer for the pixel object
  @param row : row coordinate of the pixel
  @param col : col coordinate of the pixel
  @param img : numpy array of image
  '''
  def __init__(self, row, col, img):
    self.elem = (row, col)
    self.rgba = img[row][col]
    self.value = calc_luminance(self.rgba)

  '''
  Get pixel row, col element.
  @return (int, int) : row, col
  '''
  def get_elem(self):
    return self.elem

  '''
  Get pixel color value.
  @return (int, ...) : r or rgb or rgba color
  '''
  def get_rgba(self):
    return self.rgba

  '''
  Get value of the pixel. (for example, luminance)
  @return value of the pixel
  '''
  def get_value(self):
    return self.value

'''
Root node of Union Find Tree which cotains below.
1. Rank of the tree (depth of the tree)
2. Minimum edge value in merged edges.
'''
class Root:

  '''
  Initialize with deafult values.
  @param rank : rank of the tree
  @param min_dif : minimum edge contained in the tree (merged)
  @param size : size of the tree
  '''
  def __init__(self, rank, min_dif, size):
    self.rank = rank
    self.min_dif = min_dif
    self.size = size

  '''
  Get rank value.
  @return int : rank
  '''
  def get_rank(self):
    return self.rank

  '''
  Get minimum difference value.
  @return int : minimum difference value
  '''
  def get_min_dif(self):
    return self.min_dif

  '''
  Get tree size.
  @return int : tree size
  '''
  def get_size(self):
    return self.size

  '''
  Update root node.
  @param dif_rank : difference between old rank and new rank
  @param new_min_dif  : new minimum dif value
  @param dif_size : difference bewteen old size and new size
  '''
  def update(self, dif_rank, new_min_dif, dif_size):
    self.rank += dif_rank
    self.min_dif = new_min_dif
    self.size += dif_size
