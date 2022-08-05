#---------Imports
import cv2 #for image processing
import easygui #to open the filebox
import sys
import matplotlib.pyplot as plt
import os
import tkinter as tk
from tkinter import messagebox
#---------End of imports

### CLASSES ###
class Image:
    original_img_path = ''
    cartoon_path = ''
    cartoon_image = None

### FUNCTIONS ###
def upload_img(img_object):
    ''' creates a dialog box to select image and calls the cartoonify function'''

    img_path = easygui.fileopenbox()
    img_object.original_img_path = img_path

    cartoonify(img_object)

def cartoonify(img_object):
    ''' turns the image specified at img_path into a cartoon;
        returns the cartoon image '''

    img = cv2.imread(img_object.original_img_path) # read image
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
    img_object.cartoon_image = resized_cartoon

def save_img(img_object):
    ''' save the cartoon image into a file '''

    if img_object.cartoon_image is not None:
        directory = os.path.dirname(img_object.original_img_path)
        filename = os.path.basename(img_object.original_img_path)
        save_path = os.path.join(directory, f'cartoon_{filename}')
        img_object.cartoon_path = save_path # save new path to image objet

        cv2.imwrite(save_path, cv2.cvtColor(img_object.cartoon_image, cv2.COLOR_RGB2BGR)) # save img to file

        msg = f"Cartoon image saved at {save_path}"
        tk.messagebox.showinfo(title='Information', message=msg)
    else:
        tk.messagebox.showinfo(title='Information', message="No image uploaded")

### MAIN FLOW ###
if __name__ == '__main__':
    img = Image() # create new image object

    # create tkinter window
    root = tk.Tk()
    root.geometry('400x400')
    root.title('Cartoonify an Image!')
    root.configure(background='white')
    label = tk.Label(root, background='#CDCDCD', font=('calibri', 20, 'bold'))

    # upload image button
    upload = tk.Button(root, text='Cartoonify an image', command=lambda: upload_img(img), padx=10, pady=5)
    upload.configure(background='#364156', foreground='white', font=('calibri', 10, 'bold'))
    upload.pack(side=tk.TOP, pady=50)

    # save image button
    save = tk.Button(root, text="Save cartoon image", command=lambda: save_img(img), padx=30, pady=5)
    save.configure(background='#364156', foreground='white', font=('calibri', 10, 'bold'))
    save.pack(side=tk.BOTTOM, pady=50)

    # run tkinter GUI
    root.mainloop()
