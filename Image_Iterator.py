'''This program was written for the Brownian motion experiment at the
University of Toronto. It was designed for the purpose of tracking a single
spot through a sequence of frames and then displaying, saving or plotting this
information. This program is distributed with the hope that it might be found
useful, but with no warranty, not even the implied warranty of usefulness for
a specific purpose. This file contains the main elements of the program,
intended for use with the supporting Tools file.

Author: Donald J Woodbury, University of Toronto'''

import sys
sys.path.append("/usr/local/lib/python2.7/site-packages")

from Tkinter import *
from tkSimpleDialog import askstring
from tkFileDialog import asksaveasfilename, askopenfilename
from PIL import Image, ImageSequence, ImageDraw, ImageOps, ImageTk
from numpy import average
import os
import os.path

class ImageIterator:
    def __init__(self, filename = None):
        '''Prompts the user to select an image sequence file and creates the
        Tkinter window with bindings, scrollbars and images.'''

        self.root = Tk()
        self.root.title('ImageIterator')

        self.filename = filename

        #Opening the Image Sequence
        if self.Open_im_seq() == -1:
            self.Close_window()
            return None
        
        #Parameters
        self.im_size = self.im_seq[0].size

        #Results

        self.frames = []
        
        #Building the Tkinter window
        self.Draw_canvas()
        self.Draw_sliders()

        #bindings
        self.Bindings()

        self.root.mainloop()

    def Draw_canvas(self):
        '''Creates the Tkinter window and populates it with the images from
        the user selected image sequence file.'''
        
        frame = Frame(self.root)
        frame.pack()
        
        self.label = Label(frame, text="GPE Simulation", anchor = 'n')
        self.label.pack()
        
        self.canvas = Canvas(frame, width=self.im_size[0], height=self.im_size[1])
        self.canvas.pack()

        self.tkimg = ImageTk.PhotoImage(self.im_seq[0].convert('RGB'), master = self.root)

        self.im_id = self.canvas.create_image(0,0,image=self.tkimg,anchor="nw")

    def Open_im_seq(self):
        '''Opens the sequence of images used for analysis. When called, this
        function will open a file selection dialog in which the user may either
        select a Tiff/Gif animation file, or the first image in a sequence of
        images named as "ImagenameFramenumber.jpg"'''

        if self.filename == None:
            self.filename = askopenfilename(master = self.root,
                                       filetypes = [('All Files',\
                                                     ('*.png', '*.tif', '*.gif')),
                                                    ('PNG','*.png'),
                                                    ('Tiff','*.tif'), \
                                                    ('GIF','*.gif')],\
                                       title="Open...")

        if len(self.filename) == 0:
            return -1

        self.im_seq = []

        directory, im_name = os.path.split(self.filename)
        im_num = int(''.join(s for s in im_name if s.isdigit()))
        im_name = ''.join(s for s in im_name if not s.isdigit())[:-4]
        
        while os.path.isfile(directory+'/'+im_name+str(im_num)+'.png'):
            image = Image.open(directory+'/'+im_name+str(im_num)+'.png')
            self.im_seq.append(image)
            im_num+=1
    #_________________Sliders__________________#

    def Draw_sliders(self):
        '''Defines the Sliders in the Tkinter window'''
        self.frame_number = IntVar()
        self.frame_number.set(0)
        self.frame_slider = Scale(self.root, command = self.Update_frame, \
                                  label="Frame Number:", \
                                  variable = self.frame_number,\
                                  length=self.im_size[0], orient=HORIZONTAL, \
                                  from_= 0, to=len(self.im_seq)-1)
        self.frame_slider.pack()

    def Update_frame(self, event):
        '''Updates the frame displayed when the frame_slider is moved. If
        no analysis has been performed, the raw images will be displayed.
        After the analysis, the spot location will be displayed.'''
        self.frame_num = min(self.frame_number.get(), len(self.im_seq)-1)
        self.tkimg.paste(self.im_seq[self.frame_num])

    #______________Event Bindings_______________#
    
    def Bindings(self):
        '''Defines the bindings in the tkinter window.'''
        self.root.protocol("WM_DELETE_WINDOW", self.Close_window)

    def Close_window(self):
        '''Closes the Tkinter window.'''
        self.root.destroy()

if "__main__" == __name__:

    track = ImageIterator()
