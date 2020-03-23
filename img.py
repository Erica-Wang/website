import os
import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt
from google_images_download import google_images_download
loc = 'toronto'

#search for skyline

query = loc+' skyline'

response = google_images_download.googleimagesdownload()

config = {
	"keywords":query,
	"format": "jpg",
	"limit":5,
	"size": ">1024*768",
	"output_directory": "skylines/"
}
#absolute_image_paths = response.download(config)

#image processing
countMax = -1
finalEdges = []
direc = 'skylines/'+query+'/'
directory = os.fsencode(direc)

for file in os.listdir(directory):
	filename = os.fsdecode(file)
	print(filename)
	img = cv.imread(direc+filename,0)
	edges = cv.Canny(img,100,200,True)

	mx = -1
	rw = -1

	index = 0
	for row in edges:
		counter = 0
		for col in row:
			if (col==255):
				counter+=1
		if (mx==-1 or counter>mx):
			mx = counter
			rw = index
		index+=1

	edges = edges[:rw]
	print(counter/len(edges))
	if(countMax==-1 or countMax<counter/len(edges)):
		countMax = counter/len(edges)
		finalEdges = edges

	'''
	rangeVals = 6
	targetVals = 3

	upperBound = []
	numCol = len(edges[0])

	for c in range(2,numCol-3):
		#find upper bound of buildings in each colomn
		done = 0
		counter = 0
		for check in range(0,rangeVals):
			if(edges[check][c]==255):
				counter+=1
		for r in range(0,len(edges)-rangeVals-1):
			if(done==0):
				if(counter==targetVals):
					for i in range(0,6):
						if(edges[r+i][c]==255):
							upperBound.append(r+i)
							break
					done = 1
				if(edges[r][c]==255):
					counter-=1
				if(edges[r+4][c]==255):
					counter+=1
		if(done==0):
			upperBound.append(len(edges)-1);

	threshhold = 200
	for i in range(0,len(upperBound)):
		diff = 0
		if(i>0):
			diff+=abs(upperBound[i]-upperBound[i-1])
		if(i<len(upperBound)-1):
			diff+=abs(upperBound[i]-upperBound[i+1])
		if(diff>threshhold):
			upperBound[i]=(upperBound[i-1]+upperBound[i+1])/2

		if(upperBound[i]>rw):
			upperBound[i]=rw

	print(upperBound)

	plt.plot(upperBound)
	plt.gca().invert_yaxis()
	plt.title('Original')
	'''

plt.subplot(2,2,2),plt.imshow(finalEdges,cmap = 'gray')
plt.xticks([]), plt.yticks([])

plt.show()




