import cv2, os
import tkinter as tk
from tkinter import filedialog
import PIL.Image, PIL.ImageTk
import numpy as np

# global variables
MARGIN = 10  # px
MAXDIM = 500
BG_COLOR = "#48484A"
LIGHT_GREY = "#ECECEC"

class App():
    def __init__(self, window, window_title, image_path="img/lena.bmp"):
        self.window = window
        self.window.title(window_title)
        

        # Get the image dimensions (OpenCV stores image data as NumPy ndarray)
        self.height, self.width, no_channels = MAXDIM, MAXDIM*2, 0#self.cv_img.shape
        
        ''' Image Display Related Code'''
        # Create a FRAME that can fit the images
        self.frame1 = tk.Frame(self.window, width=self.width, height=self.height, bg='black')
        self.frame1.pack(fill=tk.BOTH)
        self.setup_photo(image_path)

        # Create FRAME for label
        self.frame2 = tk.Frame(self.window, width=self.width, height=MARGIN*3, bg="white")
        self.frame2.pack(fill=tk.BOTH)
        self.label_canvas_orig = tk.Canvas(
            self.frame2, width=self.width//2, height=MARGIN*3, bg=LIGHT_GREY
        )
        self.label_canvas_orig.pack(side=tk.LEFT)
        self.label_canvas_orig.create_text(
            self.width//4, MARGIN*1.5, font="Tahoma 20",text="Original Photo", fill="black"
        )
        self.label_canvas_mod = tk.Canvas(
            self.frame2, width=self.width//2, height=MARGIN*3, bg=LIGHT_GREY
        )
        self.label_canvas_mod.pack(side=tk.LEFT)
        self.label_canvas_mod.create_text(
            self.width//4, MARGIN*1.5, font="Tahoma 20", text="Processed Photo", fill="black"
        )

# ##############################################################################################
# ################################   PARAMETER TOOLBAR   #######################################
# ##############################################################################################

        # Create a FRAME that can fit the features
        self.canvas3 = tk.Frame(self.window, width=self.width, height=self.height//2, bg=BG_COLOR)
        self.canvas3.pack(side=tk.BOTTOM, fill=tk.BOTH)

        # Dropdown menu for selecting effects
        self.dropDownSel = tk.StringVar(self.window)
        self.dropDownSel.set("Select")
        self.dropDownSel.trace("w", self.dropDownSelCallback)
        self.dropDown = tk.OptionMenu(
            self.canvas3, self.dropDownSel, *["blur", "smooth"]
        )
        self.dropDown.config(fg="black", bg=BG_COLOR)
        self.dropDown.place(relx=0.05, rely=0.1, relwidth=0.08)
        self.control_widgets_arr = []
        self.effect_setup_funcs_dict = {
            "blur": self.setup_blur_control_widgets,
            "smooth": self.setup_bilateral_smooth_control_widegts
        }

        # Button for selecting photo to process
        self.photoSelButton = tk.Button(
            self.canvas3, text="Select Photo", 
            command=self.load_local_photo, font="Tahoma 13", 
            highlightbackground=BG_COLOR, 
            fg='black', activeforeground="grey",
        )
        self.photoSelButton.place(
            relx=0.047, rely=0.25, relwidth=0.085, relheight=0.11
        )

        # Button for saving processed photo
        self.photoSaveButton = tk.Button(
            self.canvas3, text="Save Photo",
            command=self.save_processed_photo, font="Tahoma 13",
            highlightbackground=BG_COLOR,
            fg='black', activeforeground="grey",
        )
        self.photoSaveButton.place(
            relx=0.047, rely=0.4, relwidth=0.085, relheight=0.11
        )

        self.window.resizable(False, False)
        self.window.mainloop()

    def clear_widgets(self):
        for widget in self.control_widgets_arr:
            widget.destroy()

    def setup_photo(self, image_path, reload=False):
        # Load an image using OpenCV
        assert os.path.isfile(image_path), f"Image: {image_path} not found!"
        self.cv_img = cv2.cvtColor(cv2.imread(image_path), cv2.COLOR_BGR2RGB)
        self.photo = np.zeros(self.cv_img.shape, dtype=np.uint8)
        self.NEWcv_img = self.cv_img.copy()  # for recursive processing
        self.NEWcv_img_modify = self.photo
        # Use PIL (Pillow) to convert the NumPy ndarray to a PhotoImage
        self.photoOG = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(self.cv_img))
        self.photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(self.photo))

        if not reload:
            # Create a CANVAS for original image
            self.canvas0 = tk.Canvas(self.frame1, width=MAXDIM, height=MAXDIM, bg=BG_COLOR)
            self.canvas0.pack(side=tk.LEFT)
            
            # Create a CANVAS for changing image
            self.canvas1 = tk.Canvas(self.frame1, width=MAXDIM, height=MAXDIM, bg=BG_COLOR)
            self.canvas1.pack(side=tk.LEFT)
        
        
        # Add a PhotoImage to the Canvas (original)
        self.canvas0.create_image(MAXDIM//2, MAXDIM//2, image=self.photoOG)
        
        # Add a PhotoImage to the Canvas (changing effects)
        self.canvas1.create_image(MAXDIM//2, MAXDIM//2, image=self.photo, anchor=tk.CENTER)

        if reload:
            self.dropDownSelCallback()
    
    def setup_blur_control_widgets(self):
        """ Create a SCALE that lets the user blur the image"""
        self.clear_widgets()
        self.scl_blur = tk.Scale(
            self.canvas3, from_=1, to=50, orient=tk.HORIZONTAL, showvalue=1,
            command=self.blur_image, length=400, sliderlength=20, label="Blur", font="Tahoma 16",
            troughcolor=BG_COLOR, bg=BG_COLOR, fg='white', trough=LIGHT_GREY, highlightthickness=0,
        )
        self.scl_blur.place(relx=0.25, rely=0.2, relwidth=0.5, relheight=0.3)
        self.control_widgets_arr.append(self.scl_blur)

        self.blur_image(1)

    def setup_bilateral_smooth_control_widegts(self):
        """ Create 3 SCLAEs that controls bilateral smooth's control panel"""
        self.clear_widgets()
        self.scl_smooth_d = tk.Scale(
            self.canvas3, from_=1, to=5, orient=tk.HORIZONTAL, showvalue=1,
            command=lambda d: self.bilateral_smooth_image(d=d), 
            length=400, sliderlength=20, label="Distance", font="Tahoma 16",
            troughcolor=BG_COLOR, bg=BG_COLOR, fg='white', trough="white", 
            highlightthickness=0,
        )
        self.scl_smooth_d.place(relx=0.25, rely=0.0, relwidth=0.5, relheight=0.3)
        self.scl_smooth_sigmaColor = tk.Scale(
            self.canvas3, from_=1, to=300, orient=tk.HORIZONTAL, showvalue=1,
            command=lambda sigmaColor: self.bilateral_smooth_image(sigmaColor=sigmaColor), 
            length=400, sliderlength=20, label="Sigma Color", font="Tahoma 16",
            troughcolor=BG_COLOR, bg=BG_COLOR, fg='white', trough="white", 
            highlightthickness=0,
        )
        self.scl_smooth_sigmaColor.place(relx=0.25, rely=0.3, relwidth=0.5, relheight=0.3)
        self.control_widgets_arr.append(self.scl_smooth_d)
        self.control_widgets_arr.append(self.scl_smooth_sigmaColor)
        self.scl_smooth_sigmaSpace = tk.Scale(
            self.canvas3, from_=1, to=300, orient=tk.HORIZONTAL, showvalue=1,
            command=lambda sigmaSpace: self.bilateral_smooth_image(sigmaSpace=sigmaSpace), 
            length=400, sliderlength=20, label="Sigma Space", font="Tahoma 16",
            troughcolor=BG_COLOR, bg=BG_COLOR, fg='white', trough="white", 
            highlightthickness=0,
        )
        self.scl_smooth_sigmaSpace.place(relx=0.25, rely=0.6, relwidth=0.5, relheight=0.3)
        self.control_widgets_arr.append(self.scl_smooth_sigmaSpace)

        self.bilateral_smooth_image()
        
##############################################################################################
#################################  CALLBACK FUNCTIONS  #######################################
##############################################################################################
    def dropDownSelCallback(self, *args):
        effect_str = self.dropDownSel.get()
        if effect_str in self.effect_setup_funcs_dict:
            self.effect_setup_funcs_dict[self.dropDownSel.get()]()
    
    def load_local_photo(self):
        file_url = tk.filedialog.askopenfilename(
            initialdir = "/", title = "Select file",
            filetypes = (("image files",("*.jpg", "*.png")),("all files","*.*"))
        )
        self.setup_photo(file_url, reload=True)

    def save_processed_photo(self):
        filename = tk.filedialog.asksaveasfile(
            mode='w', defaultextension=".jpg"
        )
        if not filename:
            return
        try:
            self.NEWcv_img_modify.save(filename)
        except:
            PIL.Image.fromarray(self.NEWcv_img_modify).save(filename)
        
    # Callback for the "Blur" Scale 
    def blur_image(self, k):
        k = int(k)
        self.NEWcv_img_modify = cv2.blur(self.NEWcv_img, (k, k))
        self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(self.NEWcv_img_modify))
        self.canvas1.create_image(MAXDIM//2, MAXDIM//2, image=self.photo, anchor=tk.CENTER)

    def bilateral_smooth_image(self, d=None, sigmaColor=None, sigmaSpace=None):
        if d is None:
            d = self.scl_smooth_d.get()
        if sigmaColor is None:
            sigmaColor = self.scl_smooth_sigmaColor.get()
        if sigmaSpace is None:
            sigmaSpace = self.scl_smooth_sigmaSpace.get()
        d, sigmaColor, sigmaSpace = int(d), int(sigmaColor), int(sigmaSpace)
        self.NEWcv_img_modify = cv2.bilateralFilter(self.NEWcv_img, d, sigmaColor, sigmaSpace)
        self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(self.NEWcv_img_modify))
        self.canvas1.create_image(MAXDIM//2, MAXDIM//2, image=self.photo, anchor=tk.CENTER)
        
    def blur_image(self, k):
        k = int(k)
        self.NEWcv_img_modify = cv2.blur(self.NEWcv_img, (k, k))
        self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(self.NEWcv_img_modify))
        self.canvas1.create_image(MAXDIM//2, MAXDIM//2, image=self.photo, anchor=tk.CENTER)

        

##############################################################################################
# Create a window and pass it to the Application object
App(tk.Tk(), "EE 440 Image Processing GUI")