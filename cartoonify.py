#---------Imports
import cv2 #for image processing
import easygui #to open the filebox
import numpy as np #to store image
import imageio #to read image stored at particular path
import sys
import matplotlib.pyplot as plt
import os
import tkinter as tk
# from tkinter import filedialog
# from tkinter import *
from PIL import ImageTk, Image
#---------End of imports

### FUNCTIONS ###
def upload_img():
    ''' creates a dialog box to select image and calls the cartoonify function '''

    img_path = easygui.fileopenbox()
    cartoonify(img_path)

def cartoonify(img_path):
    ''' turns the image specified at img_path into a cartoon '''

    img = cv2.imread(img_path) # read image
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) # convert colors to RGB scale

    if img is None:
        print("Please choose appropriate image file")
        sys.exit()

    resized_img = cv2.resize(img, (960, 540))
    # plt.imshow(resized_img, cmap='gray') # display image on graph

    grayscale_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # turn image into grayscale
    resized_grayscale = cv2.resize(grayscale_img, (960, 540))
    # plt.imshow(resized_grayscale, cmap='gray') # display image on graph

    smooth_grayscale_img = cv2.medianBlur(grayscale_img, 5) # apply median blur to smoothen image
    resized_smooth_grayscale = cv2.resize(smooth_grayscale_img, (960, 540))
    # plt.imshow(resized_smooth_grayscale, cmap='gray') # display image on graph

    edges = cv2.adaptiveThreshold(smooth_grayscale_img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9) # get edges of image by applying a threshold
    resized_edges = cv2.resize(edges, (960, 540))
    # plt.imshow(resized_edges, cmap='gray') # display image on graph

    color_img = cv2.bilateralFilter(img, 9, 300, 300) # get lightened color and use bilateral filter to remove noise
    resized_color = cv2.resize(color_img, (960, 540))
    # plt.imshow(resized_color, cmap='gray') # display image on graph

    cartoon = cv2.bitwise_and(color_img, color_img, mask=edges) # use edges to mask colored image
    resized_cartoon = cv2.resize(cartoon, (960, 540))
    # plt.imshow(resized_cartoon, cmap='gray') # display image on graph

    images = [resized_img, resized_grayscale, resized_smooth_grayscale, resized_edges, resized_color, resized_cartoon]

    fig, axes = plt.subplots(3, 2, figsize=(8, 8), subplot_kw={'xticks':[], 'yticks':[]}, gridspec_kw=dict(hspace=0.1, wspace=0.1))

    # plot each transformation
    for i, ax in enumerate(axes.flat):
        ax.imshow(images[i], cmap='gray')

    plt.show()

def save(img, path):
    ''' save the cartoon image into a file '''

    directory = os.path.dirname(path)
    filename = os.path.basename(path)
    extension = ps.path.splitext(path)[1]
    save_path = os.path.join(directory, f'cartoon_{filename}{extension}')

    cv2.imwrite(save_path, cv2.cvtColor(img, cv2.COLOR_RGB2BGR)) # save img to file

    msg = f"Cartoon image saved at {save_path}"
    tk.messagebox.showinfo(title='Information', message=msg)



if __name__ == '__main__':
    upload_img()
