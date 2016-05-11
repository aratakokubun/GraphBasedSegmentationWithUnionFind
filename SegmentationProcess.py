# -*- coding:utf-8 -*-

from abc import ABCMeta, abstractmethod
from PIL import Image
import numpy as np

from GraphBasedSegment import *
from Edge import *
from CreateResultImage import *

'''
Implementation of graph based segmentation process
'''
class SegmentationProcess:
  __metaclass__ = ABCMeta

  '''
  Initialize with empty lists.
  @param src_img : source image to process
  @param dst_img : path of an output image
  @param top_n   : color segmentations having top n area
  @param tau_k   : merging super parameter
  '''
  def __init__(self, src_img, dst_img, top_n, tau_k=4.5):
    self.img = src_img
    self.dst_img = dst_img
    self.top_n = top_n
    self.tau_k = tau_k
    # Dictionary accomodates id:Component set
    self.component_dict = dict()
    # Dictionary accomodates EdgeIdSet:Edge set
    self.edge_dict = dict()
    # Dictionary accomodates id:Root set
    self.root_dict = dict()

    # Initialize nearest neightbor pixels to search around target pixel.
    self.nn_list = list()
    self.init_nn()

  '''
  Abstract method to initialize nearest neightbor pixels to search around target pixel.
  Implement concrete method at child class.
  '''
  @abstractmethod
  def init_nn(self):
    pass

  '''
  Get or create Component if not exist, and add new root then.
  @param target_id  : target id to be fetched
  @param target_row : pixel row on creating new component
  @param target_col : pixel col on creating new component
  @return Component : component specified with the target_id
  '''
  def fetch_component(self, target_id, target_row, target_col):
    # Add component if not found
    if target_id in self.component_dict:
      return self.component_dict[target_id]
    else:
      target_component = Component(row=target_row, col=target_col, img=self.img)
      self.component_dict[target_id] = target_component
      self.root_dict[target_id] = Root(rank=1, min_dif=0, size=1)
      return target_component

  '''
  Create initailized graph components.
  '''
  def init_graph(self):
    img_row = self.img.shape[0]
    img_col = self.img.shape[1]

    # y loop
    for row in range(img_row):
      # x loop
      for col in range(img_col):
        # Issue unique id for this element
        pixel_id = create_pixel_id(self.img, row, col)

        pixel_component = self.fetch_component(target_id = pixel_id, target_row = row, target_col = col)

        # Search edges
        for dif in self.nn_list:
          target_row = row + dif[0]
          target_col = col + dif[1]
          if not (0 <= target_row < img_row and 0 <= target_col < img_col):
            continue
          # Issue unique id for this element
          target_id = create_pixel_id(self.img, target_row, target_col)

          target_component = self.fetch_component(target_id = target_id, target_row = target_row, target_col = target_col)

          # Add edge
          uf_edge_id_set = EdgeIdSet(pixel_id, target_id)
          uf_edge = Edge(pixel_component, target_component)
          self.edge_dict[uf_edge_id_set] = uf_edge

  '''
  Train the image and get graph based segmentation.
  '''
  def train(self):
    # Initialize segmentation
    self.init_graph()

    # Initialize uf graph based segment with the size of image.
    size = self.img.shape[0]*self.img.shape[1]
    union_find = UnionFind(size, self.root_dict)
    ufgbs = GraphBasedSegment(uf=union_find, tau_k=self.tau_k)

    # Sort edge by ascending order of the difference of it.
    sorted_edge = sorted(self.edge_dict.items(), key=lambda item:item[1].get_difference())
    print("edge len = {0}".format(len(sorted_edge)))

    for edge_item in sorted_edge:
      id_set = edge_item[0]
      edge = edge_item[1]
      edge_value = edge.get_difference()
      # Merge edge
      ufgbs.merge(id1=id_set.get_id1(), id2=id_set.get_id2(), edge_value=edge_value)

    # Create result image colored with top n area.
    create_colored_result(self.img, union_find, self.top_n, self.dst_img)


'''
Implementation of Segmentation Process with Grid-Graph
'''
class GridGraphSegmentation(SegmentationProcess):

  '''
  Concrete to init nearest neighbor with Grid-Graph.
  '''
  def init_nn(self):
    # Search for 4 direction (drow, dcol)
    self.nn_list = [(1, -1), (1, 0), (1, 1), (0, 1)]


'''
Implementation of Segmentation Process with Nearest-Neighbor-Graph
'''
class NearestNeightborGraphSegmentation(SegmentationProcess):

  '''
  Initialize with empty lists.
  @param src_img : source image to process
  @param dst_img : path of an output image
  @param top_n   : color segmentations having top n area
  @param nn      : nearest neighbor distance
  '''
  def __init__(self, src_img, dst_img, top_n, tau_k=4.5, nn=2):
    # Limit maximum nn to size/4
    img_row = src_img.shape[0]
    img_col = src_img.shape[1]
    self.nn = min(nn, min(img_row/4, img_col/4))

    SegmentationProcess.__init__(self, src_img, dst_img, top_n, tau_k)

  '''
  Define nearest neighbor.
  '''
  def init_nn(self):
    for row in range(0, self.nn+1):
      for col in range(self.nn, -self.nn, -1):
        # Check if the cell is in the range nn
        if sqrt(row**2+col**2) > self.nn:
          continue
        # Check if not base point
        if row == 0 and col == 0:
          continue
        self.nn_list.append((row, col))
