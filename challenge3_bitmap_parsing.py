# -*- coding: utf-8 -*-
"""
Created on Thu Nov 23 17:37:59 2017

@author: cbothore
"""
# https://fr.wikipedia.org/wiki/Windows_bitmap

# A first method to parse a BMP file
# It is a binary file
# Import a module to convert bytes from binary files 
# to H (unsigned short, 2 bytes), I (unsigned int, 4 bytes)
import struct

input_filename="population-density-map.bmp"

bmp = open(input_filename, 'rb') # open a binary file
print('-- First part of the header, information about the file (14 bytes)')
print('Type:', bmp.read(2).decode())
print('Size: %s' % struct.unpack('I', bmp.read(4)))
print('Reserved 1: %s' % struct.unpack('H', bmp.read(2)))
print('Reserved 2: %s' % struct.unpack('H', bmp.read(2)))
offset=struct.unpack('I', bmp.read(4))
print('Image start after Offset: %s' % offset)

print('-- Second part of the header, DIB header, bitmap information header (varying size)')
print('The size of this DIB Header Size: %s' % struct.unpack('I', bmp.read(4)))
print('Width: %s' % struct.unpack('I', bmp.read(4)))
print('Height: %s' % struct.unpack('I', bmp.read(4)))
print('Colour Planes: %s' % struct.unpack('H', bmp.read(2)))
pixel_size=struct.unpack('H', bmp.read(2))
print('Bits per Pixel: %s' % pixel_size)
print('Compression Method: %s' % struct.unpack('I', bmp.read(4)))
print('Raw Image Size: %s' % struct.unpack('I', bmp.read(4)))
print('Horizontal Resolution: %s' % struct.unpack('I', bmp.read(4)))
print('Vertical Resolution: %s' % struct.unpack('I', bmp.read(4)))
print('Number of Colours: %s' % struct.unpack('I', bmp.read(4)))
print('Important Colours: %s' % struct.unpack('I', bmp.read(4)))

# At this step, we have read 14+40 bytes
# As offset[0] = 54, from now, we will read the BMP content
# You have to read each pixel now, and do what you have to do
# First pixel is bottom-left, and last one top-right
# .........
bmp.close()


# Another method to parse a BMP image
# To manipulate imageIf you want to work with image data in Python, 
# numpy is the best way to store and manipulate arrays of pixels. 
# You can use the Python Imaging Library (PIL) to read and write data 
# to standard file formats.

# Use PIL module to read file
# http://pillow.readthedocs.io/en/latest/
from PIL import Image
import numpy as np
import networkx as nx
im = Image.open(input_filename)

# This modules gives useful informations
width=im.size[0]
heigth=im.size[1]
colors = im.getcolors(width*heigth)
print('Nb of different colors: %d' % len(colors))
# To plot an histogram
from matplotlib import pyplot as plt
def hexencode(rgb):
    r=rgb[0]
    g=rgb[1]
    b=rgb[2]
    return '#%02x%02x%02x' % (r,g,b)

#for idx, c in enumerate(colors):
#    plt.bar(idx, c[0], color=hexencode(c[1]))

#plt.show()
# We have 32 different colors in this image
# We can see that we have "only" 91189 black pixels able to stop zombies 
# but we have a large majority of dark ones slowing their progression

# With the image im, let's generate a numpy array to manipulate pixels
p = np.array(im) 

print(p.shape)
# a result (3510, 4830, 3) means (rows, columns, color channels)
# where 3510 is the height and 4830 the width

# to get the Red value of pixel on row 3 and column 59
p[3,59][0]

# How to get the coordinates of the green and red pixels where 
# (0,0) is top-left and (width-1, height-1) is bottom-right
# In numpy array, notice that the first dimension is the height, 
# and the second dimension is the width. That is because, for a numpy array, 
# the first axis represents rows (our classical coord y), 
# and the second represents columns (our classical x).

# First method
# Here is a double loop (careful, O(n²) complexity) to parse the pixels from
# (0,0) top-left and (heigth-1, width-1) is bottom-right
#    for x in range(width):
        # p[y,x] is the coord (x,y), x the colum, and y the line
        # As an exemple, we search for the green and red pixels
        # p[y,x] is an array with 3 values
        # We test if there is a complete match between the 3 values 
        # from both arrays p[y,x] and np.array([0,255,0])
        # to detect green pixels
        #if (p[y,x] == np.array([0,255,0])).all():
          #  print("Coordinates (x,y) of the green pixel: (%s,%s)" % (str(x),str(y)))
            # Coordinates (x,y) of the green pixel: (4426,2108)
        #if (p[y,x] == np.array([255,0,0])).all():
            #print("Coordinates (x,y) of the red pixel: (%s,%s)" % (str(x),str(y)))
            # Coordinates (x,y) of the red pixel: (669,1306)

# Here is a more efficient method to get the location of the green and red pixels
mask = np.all(p == (0, 255, 0), axis=-1)
z = np.transpose(np.where(mask))
print("Coordinates (x,y) of the green pixel: (%d,%d)" % (z[0][1],z[0][0]))
mask = np.all(p == (255, 0, 0), axis=-1)
z = np.transpose(np.where(mask))
print("Coordinates (x,y) of the red pixel: (%d,%d)" % (z[0][1],z[0][0]))


# Now we have the source and the target positions of our zombies
# we could convert our RGB image into greyscale image to manipulate
# only 1 value for the color and deduce more easily the density of
# population


grayim = im.convert("L")

#grayim.show() #Show gray img
colors = grayim.getcolors(width*heigth)
print('Nb of different colors: %d' % len(colors))
# With the image im, let's generate a numpy array to manipulate pixels
p = np.array(grayim) 
# plot the histogram. We still have a lot of dark colors. Just to check ;-)
#plt.hist(p.ravel())
density = p/255.0
#plot point
plt.imshow(density)
plt.plot(4426,2108,'r*')
plt.plot(669,1306,'r*')
plt.axis('off')
plt.show()

# from gray colors to density

# plot the histogram. We still have a lot of dark colors. Just to check ;-)
#plt.hist(density.ravel())

density = p/255.0
a=np.amin(density)


#plt.hist(density.ravel())
#plt.show()
#print(p)


#networkx graph



def imageToAdjacency(heigth,width):
    V = heigth*width
    adj_matrix = []
 # vertex numbering starts from 0
    for i in range(V):
    	temp = []
    	for j in range(V):
            temp.append(0)
            adj_matrix.append(temp)
 # print the adjacency matrix
    return adj_matrix
#print(imageToAdjacency(100,100))
#from sklearn.feature_extraction import image
#A=image.img_to_graph(p)
#G=nx.from_numpy_matrix(A)
#print(p)
#http://love-python.blogspot.fr/2008/04/adjacency-matrix-graph-in-python.html
#G = nx.Graph([('A','B'),('C','D'),('B','C'),('D','E')])
#path = nx.shortest_path(G, 'A', 'E')

# We can use the gray 2D array density to create our graph
# Gray colors density[y,x] range now from 0 (black) to 1 (white)
# density[0,0] is top-left pixel density
# and density[heigth-1,width-1] is bottom-right pixel
#for g in p:
#	print(p)
#for pixelcoordinate, pixeldensity in np.ndenumerate(p):
    #    x, y= pixelcoordinate
      #  density= p[x, y]
        #print(density)

#for y in range(heigth):
    #for x in range(width):
    #	densityp= density[y, x]
    #	if (densityp < 0.2 ):
    	#	density[y,x]=0

from skimage.graph import route_through_array

def zombies_walk(arrayofweight,startpoint,endpoint):
	arrayofweight=1./(arrayofweight) #because we want max of weight
	zombies_route=route_through_array(arrayofweight, startpoint,endpoint,fully_connected=True,geometric=True)
	#  
	""" we use skimage.graph.MCP class

	A class for finding the minimum weighted path through a given n-d weight array. (that's why
 	we normalize arrayofweight=1./arrayofweight to have most weighted path)
	it returns a List of n-d index tuples defining the path from start to end and the sum of weight
	see more on http://scikit-image.org/docs/dev/api/skimage.graph.html#skimage.graph.route_through_array
	."""
	return zombies_route #return list of pixel route

def draw_walk(imageFile,zombiesWalkList,rgbcolor):
	img= Image.open(imageFile)
	pixelArray = img.load() #create pixel Map
	for i in zombiesWalkList[0]:
		pixelArray[i[1],i[0]] = rgbcolor # change pixel color
	img.show()

a=zombies_walk(density,[1306,669],[2108,4426])
	
draw_walk("population-density-map.bmp",a,(255,0,0,255))



def allpixeliter(image):
	allpixels={}
	for pixelcoordinate, pixeldensity in np.ndenumerate(image):
		allpixels[pixelcoordinate]=pixeldensity
	return allpixels