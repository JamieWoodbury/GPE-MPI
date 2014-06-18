from numpy import *
from pylab import *
import sys
sys.path.append("/usr/local/lib/python2.7/site-packages")
from PIL import *
from scipy.misc import fromimage, toimage
from mpl_toolkits.mplot3d import Axes3D
import Image_Iterator

def restore_from_file(dim, t_size, x_size = 1, y_size = 1, z_size = 1):
	'''Returns "dim" dimensional array from the file psi.txt. y_size and z_size
	only need to be specified in the case where dim is 2 or 3'''

	psi = fromfile("psi.bin", 'float64')
	if dim == 1:
		psi = reshape(psi, (t_size, x_size), "C")
	if dim == 2:
		psi = reshape(psi, (t_size, x_size, y_size), "C")
	if dim == 3:
		psi = reshape(psi, (t_size, x_size, y_size, z_size), "C")

	return psi

def shrink_array(data, red_x_size, red_y_size, red_z_size):
    '''Reduces the size of the 3D array "data" to one of size 
    (red_x_size, red_y_size, red_z_size)'''

    return data.reshape(red_x_size, data.shape[0]/red_x_size, \
    				red_y_size, data.shape[1]/red_y_size, \
    				red_z_size, data.shape[2]/red_z_size)\
    				.sum(axis=1).sum(axis=2).sum(axis=3)

def reduce_dim(psi, dim):
	'''Reduces the dimension of the 3D array "psi" down to the target dimension
	"dim" by summing over the third, or the second and third dimensions'''

	if dim == 3:
		return psi
	if dim == 2:
		return psi.sum(axis=2)
	if dim == 1:
		return psi.sum(axis=1).sum(axis=2)

def create_image(array, display = False, save = False, file_name = None):
    '''Creates and optionally displays and saves an image given the 2D input array'''
    
    im_data = array.astype(integer)
    im_data = im_data.astype(float32)

    imag = toimage(im_data, mode = 'L')

    if display:
        print 'Displaying...'
        imag.show()

    if save:
        print 'Saving...'
        imag.save(file_name+'.tif')

    return imag

def plot_3D(psi, x_size, y_size, dx, iteration, save = 0):
	"Creates a #d contour plot given the 2D array psi"

	fig = figure()
	ax = fig.add_subplot(111, projection='3d')

	x = linspace(-x_size*dx/2, x_size*dx/2, x_size)
	y = linspace(-y_size*dx/2, y_size*dx/2, y_size)

	X, Y = meshgrid(x, y)

	ax.plot_surface(X, Y, psi, rstride=1, cstride=1, cmap=cm.coolwarm, \
		linewidth=0, antialiased=False)

	if save:
		fig.savefig("3D_Plots/GPE_Plot_"+str(iteration)+".png")

def plot_widths():
	'''Creates a plot of the x, y, and z widths of the condensate given the file
	widths.txt'''

	widths = loadtxt("widths.txt")
	t, xsizes, ysizes, zsizes = array(zip(*widths))

	plot(t, xsizes)
	plot(t, ysizes)
	plot(t, zsizes)

	title("Plotting the change in Condensate size over time")
	xlabel("Time")
	ylabel("Condensate Width")

	legend(('X size', 'Y size', 'Z size'))

	show()

def plot_error():
	'''Creates a plot of the x, y, and z widths of the condensate given the file
	widths.txt'''

	data = loadtxt("error.txt")
	t, error = array(zip(*data))

	plot(t, error)

	title("Plotting the convergence to the SHO limit")
	xlabel("Time")
	ylabel("Error")

	show()


if __name__ == "__main__":

	#_______Setting some constants_______#

	#Properties of the incoming array
	dim = 2
	x_size = 64
	y_size = 64
	z_size = 64

	#Spacial and Temporal scaling values
	dx = 0.125
	t_size = 500

	#Toggling functionality within the program

	width_plotting = 0
	error_plotting = 0
	display_psi = 1

	draw_3D_plot = 0
	create_2D_image = 0

	display_3D_Plots = 1

	#________Plotting________#

	if width_plotting:
		plot_widths()

	if error_plotting:
		plot_error()

	if display_psi:

		psi = restore_from_file(dim, t_size, x_size, y_size, z_size)

		for i in xrange(0, t_size):
			if dim == 1:
				pass
			if dim == 2:
				if create_2D_image:
					create_image(psi[i], display = 1) #, save = 1, file_name = "Test_%d" % t)
				if draw_3D_plot:
					plot_3D(psi[i], x_size, y_size, dx, i, save = 1)
					print "Plotting %d..." %i
			if dim == 3:
				pass
		
		if display_3D_Plots:
			Image_Iterator.ImageIterator()


