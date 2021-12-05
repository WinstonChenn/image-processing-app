import os
import cv2
import PIL.ImageTk
import numpy as np
import tkinter.filedialog
import tkinter as tk
from .settings import MARGIN, MAXDIM, BG_COLOR, LIGHT_GREY


def photo_select_button_setup(self):
    self.photoSelButton = tk.Button(
        self.frame3, text="Select Photo", 
        command=self.load_local_photo, font="Tahoma 13", 
        highlightbackground=BG_COLOR, 
        fg='black', activeforeground="grey",
    )
    self.photoSelButton.place(
        relx=0.047, rely=0.25, relwidth=0.085, relheight=0.11
    )

def photo_save_button_setup(self):
    self.photoSaveButton = tk.Button(
        self.frame3, text="Save Photo",
        command=self.save_processed_photo, font="Tahoma 13",
        highlightbackground=BG_COLOR,
        fg='black', activeforeground="grey",
    )
    self.photoSaveButton.place(
        relx=0.047, rely=0.4, relwidth=0.085, relheight=0.11
    )

def resize_photo(self, ori_photo):
    w, h, d  = ori_photo.shape
    if w > MAXDIM or h > MAXDIM:
        w_ratio = w/MAXDIM
        h_ratio = h/MAXDIM
        max_ratio = max(w_ratio, h_ratio)
        resized_photo = cv2.resize(
            ori_photo, (int(h/max_ratio), int(w/max_ratio))
        )
    else:
        resized_photo = ori_photo
    return resized_photo

def setup_photo(self, image_path, reload=False):
    if not reload:
        if hasattr(self, "canvas0"):
            self.canvas0.destroy()
        if hasattr(self, "canvas1"):
            self.canvas1.destroy()
    # Load an image using OpenCV
    assert os.path.isfile(image_path), f"Image: {image_path} not found!"
    self.ori_img = cv2.cvtColor(cv2.imread(image_path), cv2.COLOR_BGR2RGB)
    self.resized_ori_img = self.resize_photo(self.ori_img)
    self.resized_mod_img = np.zeros(
        self.resized_ori_img.shape, dtype=np.uint8
    )
    self.resized_mod_img_copy = self.resized_mod_img.copy()  # for recursive processing
    self.tk_ori_img = PIL.ImageTk.PhotoImage(
        image=PIL.Image.fromarray(self.resized_ori_img)
    )
    self.tk_mod_img = PIL.ImageTk.PhotoImage(
        image=PIL.Image.fromarray(self.resized_mod_img)
    )

    if not reload:
        # Create a CANVAS for original image
        self.canvas0 = tk.Canvas(self.frame1, width=MAXDIM, height=MAXDIM, bg=BG_COLOR)
        self.canvas0.pack(side=tk.LEFT)
        
        # Create a CANVAS for changing image
        self.canvas1 = tk.Canvas(self.frame1, width=MAXDIM, height=MAXDIM, bg=BG_COLOR)
        self.canvas1.pack(side=tk.LEFT)
    self.canvas0.create_image(
        MAXDIM//2, MAXDIM//2, image=self.tk_ori_img, anchor=tk.CENTER
    )
    self.canvas1.create_image(
        MAXDIM//2, MAXDIM//2, image=self.tk_mod_img, anchor=tk.CENTER
    )

    if reload:
        self.dropDownSelCallback()

def load_local_photo(self):
    file_url = tk.filedialog.askopenfilename(
        initialdir = "/", title = "Select file",
        filetypes = (("image files",("*.jpg", "*.png")),("all files","*.*"))
    )
    if os.path.isfile(file_url):
        self.image_path = file_url
        self.setup_photo(file_url, reload=True)

def save_processed_photo(self):
    filename = tk.filedialog.asksaveasfile(
        mode='w', defaultextension=".jpg"
    )
    image = self.effect_operation_funcs_dict[self.dropDownSel.get()](
        image=self.ori_img, return_image=True
    )
    pil_image = PIL.Image.fromarray(image)
    if filename:
        pil_image.save(filename)