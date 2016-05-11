# -*- coding:utf-8 -*-

from PIL import Image
import numpy as np
from math import *
import sys

'''
Preserve pair of edge pixels between two components
'''
class Edge:

  '''
  Initialize with components.
  @note ids of comp1 and comp2 are different.
  @param comp1 : One of the interested components
  @param comp2 : One of the interested components
  '''
  def __init__(self, comp1, comp2):
    self.comp1 = comp1
    self.comp2 = comp2
    self.diff = abs(self.comp1.get_value() - self.comp2.get_value())

  '''
  Get difference value between the componennts
  @return int : difference between the components
  '''
  def get_difference(self):
    return self.diff


'''
Preserve two ids of edge components.
This class is used to edge key of dictionary.
DO NOT CHANGE IDS IN THIS OBJECT.
'''
class EdgeIdSet(object):

  '''
  Intialize with two ids.
  @param id1 : id of one component (id1 < id2)
  @param id2 : id of one component (id1 < id2)
  '''
  def __init__(self, id1, id2):
    if id1 > id2:
      self.id1 = id2
      self.id2 = id1
    else:
      self.id1 = id1
      self.id2 = id2

  def __eq__(self, other):
    return isinstance(other, self.__class__) \
            and self.id1 == other.get_id1() \
            and self.id2 == other.get_id2()

  def  __ne__(self, other):
    return not self.__eq__(other)

  def __hash__(self):
    # Use large prime number
    return self.id1 + 14365291*self.id2

  '''
  Get an id of smaller value.
  @return int : id
  '''
  def get_id1(self):
    return self.id1

  '''
  Get an id of larger value.
  @return int : id
  '''
  def get_id2(self):
    return self.id2

  '''
  Get if this id set contains the specified key id
  @param key_id : id to be searched
  @return bool : True if contains the id, else False
  '''
  def contains_id(self, key_id):
    return self.id1 == key_id or self.id2 == key_id

