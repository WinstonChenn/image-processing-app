import tkinter as tk
import numpy as np
from .settings import MARGIN, MAXDIM, BG_COLOR, LIGHT_GREY

class App():
    from .control_panel import \
        clear_widgets, \
        setup_blur_control_widgets, \
        setup_bilateral_smooth_control_widegts, \
        setup_gradient_control_widgets, \
        setup_canny_control_widgets
    from .basic_operations import \
        blur_image, \
        bilateral_smooth_image, \
        sobel_edge_detection, \
        canny_edge_detection
    from .photo import setup_photo, \
        load_local_photo, \
        save_processed_photo, \
        photo_select_button_setup, \
        photo_save_button_setup

    def __init__(self, window, window_title, image_path="img/lena.bmp"):
        self.window = window
        self.window.title(window_title)
        self.image_path = image_path
        

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

        # Create a FRAME for control panel
        self.frame3 = tk.Frame(self.window, width=self.width, height=self.height//2, bg=BG_COLOR)
        self.frame3.pack(side=tk.BOTTOM, fill=tk.BOTH)

# ##############################################################################################
# ################################   PARAMETER TOOLBAR   #######################################
# ##############################################################################################

        # Dropdown menu for selecting effects
        self.dropDownSel = tk.StringVar(self.window)
        self.dropDownSel.set("Select")
        self.dropDownSel.trace("w", self.dropDownSelCallback)
        self.dropDown = tk.OptionMenu(
            self.frame3, self.dropDownSel, *["blur", "smooth", "gradient", "edge"]
        )
        self.dropDown.config(fg="black", bg=BG_COLOR)
        self.dropDown.place(relx=0.05, rely=0.1, relwidth=0.08)
        self.control_widgets_arr = []
        self.effect_setup_funcs_dict = {
            "blur": self.setup_blur_control_widgets,
            "smooth": self.setup_bilateral_smooth_control_widegts,
            "gradient": self.setup_gradient_control_widgets,
            "edge": self.setup_canny_control_widgets,
        }

        self.photo_select_button_setup()
        self.photo_save_button_setup()

        self.window.resizable(False, False)
        self.window.mainloop()
        
##############################################################################################
#################################  CALLBACK FUNCTIONS  #######################################
##############################################################################################
    def dropDownSelCallback(self, *args):
        effect_str = self.dropDownSel.get()
        if effect_str in self.effect_setup_funcs_dict:
            self.effect_setup_funcs_dict[self.dropDownSel.get()]()
            self.setup_photo(self.image_path)

    def edgeTypeSelCallback(self, *args):
        self.edge_type_sel_str = self.edge_type_sel.get()
        self.sobel_edge_detection()
        