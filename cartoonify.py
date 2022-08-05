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
    img_path = easy,gui.fileopenbox()
    # cartoonify(img_path)
