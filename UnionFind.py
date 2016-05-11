# -*- coding:utf-8 -*-

from GraphBasedSegment import *

'''
Implemnetation of Union Find Tree

row and col (position in the table) value means position of each pixel
The elmenet with index 0 value 0 means empty.
This element is not used for union find.

Value of table:
  Negative (>0) : nagative id value refering to Root
  Positive (<0): next parent node
'''
class UnionFind:

  '''
  Initialize table with negative id value (-root_id)
  @param size : size of the table
  @param root_dict : dictionary contains all root node
  '''
  def __init__(self, size, root_dict):
    self.table = [-root_id for root_id in range(1+size)]
    self.root_dict = root_dict

  '''
  Find the representative node id (root node) of the segmentation.
  @param id : pixel id of the interested node
  @return int : root node id
  '''
  def find(self, id):
    if self.table[id] < 0:
      # return UF root id 
      return id
    else:
      # compress the tree search root
      self.table[id] = self.find(self.table[id])
      return self.table[id]

  '''
  Get root node id.
  @param id : node id to search
  @return int : root node id
  '''
  def get_root(self, id):
    root_id = self.find(id)
    root_node_id = - self.table[root_id]
    return self.root_dict[root_node_id]

  '''
  Merge 2 unions.
  @param id1 : component id to merge
  @param id2 : component id to merge
  @param edge_value : interested edge value
  @return bool : True if merge occurred, else False
  '''
  def union(self, id1, id2, edge_value):
    # Find root nodes of the specified component
    s1 = self.find(id1)
    s2 = self.find(id2)
    if s1 != s2:
      s1_id = - self.table[s1]
      s2_id = - self.table[s2]
      r1 = self.root_dict[s1_id]
      r2 = self.root_dict[s2_id]
      r1_rank = r1.get_rank()
      r2_rank = r2.get_rank()
      # Merge samller component to another one.
      # !! Because the value is negative, more than and less than are reversed. !!
      if r1_rank == r2_rank:
        r1.update(dif_rank=1, new_min_dif=edge_value, dif_size=r2.get_size())
        self.table[s2] = s1
      elif r1_rank > r2_rank:
        r1.update(dif_rank=0, new_min_dif=edge_value, dif_size=r2.get_size())
        self.table[s2] = s1
      else:
        r1.update(dif_rank=0, new_min_dif=edge_value, dif_size=r1.get_size())
        self.table[s1] = s2
      return True
    return False

  '''
  Get root id and rank.
  @return (int, int) : root node id and size of the tree
  '''
  def subsetall(self):
    ret = []
    for i in range(len(self.table)):
      if self.table[i] < 0:
        root_id = -self.table[i]
        root = self.root_dict[root_id]
        ret.append((i, root.get_size()))
    return ret

  '''
  Get union find table.
  @return list(int) : union find table
  '''
  def get_all_union(self):
    return self.table

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
