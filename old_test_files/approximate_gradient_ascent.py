
import numpy as np
import matplotlib.pyplot as plt



def calculate_gradient_ascent(p,degree,D):

	x = D[:,0]
	y = D[:,1]
        z = D[:,2]

	## calculate polynomial

	w = np.polyfit(x, y ,z , degree)
	f = np.poly1d(w)
	print f


	# calculate new x's and y's

	#y_new = f(x)
	#gradient = (y_new[1]- y_new[0]) / (x[1]-x[0])  
	#step_size = 2

	#plt.plot(x,y,'o', x, y_new)
	#plt.plot(x, y,'bo')
	#plt.show()

	return #p + gradient  * step_size

degree =5
p = 0.5

D =  np.array([(0.1, 0.1,0.1), (0.2, 0.3,0.1), (0.3, 0.4,0.1), (0.5, 0.5,0.1),(0.2, 0.27,0.1)])

calculate_gradient_ascent(p,degree,D)
