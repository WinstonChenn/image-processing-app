import pathlib, os
import tkinter as tk
import numpy as np
import cv2
import PIL.Image
from PIL import Image, ImageTk
from .settings import MARGIN, MAXDIM, BG_COLOR, LIGHT_GREY, DROPDOWN_WIDTH

class App():
    from .control_panel import \
        clear_widgets, \
        setup_blur_control_widgets, \
        setup_bilateral_smooth_control_widegts, \
        setup_gradient_control_widgets, \
        setup_canny_control_widgets, \
        setup_quantization_widgets
    from .basic_operations import \
        blur_image, \
        bilateral_smooth_image, \
        sobel_edge_detection, \
        canny_edge_detection, \
        quantization
    from .photo import setup_photo, \
        load_local_photo, \
        save_processed_photo, \
        photo_select_button_setup, \
        photo_save_button_setup, \
        resize_photo, \
        load_photo
    from .video import web_cam_on_button_setup, \
        webCamOnButtonCallback, \
        web_cam_off_button_setup, \
        webCamOffButtOffCallback


    def __init__(self, window, window_title, default_img="lena.bmp"):
        curr_dir = pathlib.Path(__file__).parent.resolve()
        img_dir = os.path.join(curr_dir, "..", "..", "img")
        image_path = os.path.join(img_dir, default_img)
        self.window = window
        self.window.title(window_title)
        self.image_path = image_path
        self.video = False # indicate whether processing video or not
        
        # Variables storing images
        self.resized_ori_img = None # original image
        self.resized_mod_img = None # processed image
        self.resized_mod_img_copy = None # copy of processed image
        self.tk_ori_img = None # original image for TK display
        self.tk_mod_img = None # processed image for TK display
        
        # FRAME 1: Image Display
        self.frame1 = tk.Frame(self.window, width=MAXDIM*2, height=MAXDIM, bg='black')
        self.frame1.pack(fill=tk.BOTH)
        self.setup_photo(self.load_photo(image_path))

        # FRAME 3: image label
        self.frame2 = tk.Frame(self.window, width=MAXDIM*2, height=MARGIN*3, bg="white")
        self.frame2.pack(fill=tk.BOTH)
        self.label_canvas_orig = tk.Canvas(
            self.frame2, width=MAXDIM*2//2, height=MARGIN*3, bg=LIGHT_GREY
        )
        self.label_canvas_orig.pack(side=tk.LEFT)
        self.label_canvas_orig.create_text(
            MAXDIM*2//4, MARGIN*1.5, font="Tahoma 20",text="Original Photo", fill="black"
        )
        self.label_canvas_mod = tk.Canvas(
            self.frame2, width=MAXDIM*2//2, height=MARGIN*3, bg=LIGHT_GREY
        )
        self.label_canvas_mod.pack(side=tk.LEFT)
        self.label_canvas_mod.create_text(
            MAXDIM*2//4, MARGIN*1.5, font="Tahoma 20", text="Processed Photo", fill="black"
        )

        # frame 3: process control panel
        self.frame3 = tk.Frame(self.window, width=MAXDIM*2, height=MAXDIM//2, bg=BG_COLOR)
        self.frame3.pack(side=tk.BOTTOM, fill=tk.BOTH)

# ##############################################################################################
# ################################   PARAMETER TOOLBAR   #######################################
# ##############################################################################################

        # Dropdown menu for selecting effects
        self.dropDownSel = tk.StringVar(self.window)
        self.dropDownSel.set("Select")
        self.dropDownSel.trace("w", self.dropDownSelCallback)
        self.dropDown = tk.OptionMenu(
            self.frame3, self.dropDownSel, *["blur", "smooth", "gradient", "edge", "quantization"]
        )
        self.dropDown.config(fg="black", bg=BG_COLOR)
        self.dropDown.place(relx=0.05, rely=0.1, relwidth=DROPDOWN_WIDTH)
        self.control_widgets_arr = []
        self.effect_setup_funcs_dict = {
            "blur": self.setup_blur_control_widgets,
            "smooth": self.setup_bilateral_smooth_control_widegts,
            "gradient": self.setup_gradient_control_widgets,
            "edge": self.setup_canny_control_widgets,
            "quantization": self.setup_quantization_widgets
        }

        self.effect_operation_funcs_dict = {
            "blur": self.blur_image,
            "smooth": self.bilateral_smooth_image,
            "gradient": self.sobel_edge_detection,
            "edge": self.canny_edge_detection,
            "quantization": self.quantization
        }

        self.photo_select_button_setup()
        self.photo_save_button_setup()
        
        self.window.resizable(False, False)
        self.window.mainloop()
        
##############################################################################################
#################################  CALLBACK FUNCTIONS  #######################################
##############################################################################################
    def dropDownSelCallback(self, *args):
        if hasattr(self, "dropDownSel"):
            effect_str = self.dropDownSel.get()
            if effect_str in self.effect_setup_funcs_dict:
                self.effect_setup_funcs_dict[effect_str]()

    def imageUpdateCallBack(self, *args):
        if hasattr(self, "dropDownSel"):
            effect_str = self.dropDownSel.get()
            if effect_str in self.effect_operation_funcs_dict:
                self.effect_operation_funcs_dict[effect_str]()


    def edgeTypeSelCallback(self, *args):
        self.edge_type_sel_str = self.edge_type_sel.get()
        self.sobel_edge_detection()
        