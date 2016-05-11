# Abstruct
Implemnetation of Graph Based Segmentation Algorithm.
Refer a paper below.

http://cs.brown.edu/~pff/papers/seg-ijcv.pdf

# Usage
Refer a file GraphBasedSegmentTest.py
1. Import Image(PIL), numpy, SegmentationProcess.
	- from PIL import Image
	- import numpy as np
	- import SegmentationProcess as sp

2. Load an image with PIL.
	- img = np.array(Image.open('pathOfImage.png'))

3. Init SegmentationProcessClass (GridGraph or NearestNeighborGraph)
	- ggs = GridGraphSegmentation(src_img, dst_img, top_n)
	- nngs = NearestNeighborSegmentation(src_img, dst_img, top_n, nn)

4. Call a "train" method to get a processed image.
	- ggs.train()
	- nngs.train()

# Precautions
1. Recommend the pixel size is under 10000 (100 by 100).
	This program takes much time (About 3minutes with size 10000, 12minutes with size 20000 with grid-graph method).

2. NearestNeighbor takes far more time than Grid Graph.
	Grid Graph method considers 8 Nearest pixel as edge. NearestNeighbor considers pixels the distance of which is less than n.

3. Parameter top n controls how many merged components are to be colored.
	Merged Components to be colored are selected with the descending order of number of cells contained in the component.

4. Parameter nn controls the distance in which pixels are considered to be edges.
	Cosidering the cell (r, c) and nn, cells (rr, cc) which meet the condition sqrt((r-rr)^2+(c-cc)^2) < nn are considered to be edges of the cell.

5. (Optional) You can specify segmentation tau parameter.
	import GraphBasedSegment
	GraphBasaedSegment.tau_k = <Specify parameter>
