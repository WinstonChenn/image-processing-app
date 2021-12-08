import tkinter as tk
from .settings import MARGIN, MAXDIM, BG_COLOR, LIGHT_GREY


def clear_widgets(self):
    for widget in self.control_widgets_arr:
        widget.destroy()
    if hasattr(self, "webCamOnButton"):
        self.webCamOnButton.destroy()
    if hasattr(self, "webCamOffButton"):
        self.webCamOffButton.destroy()
    self.control_widgets_arr = []

def setup_blur_control_widgets(self):
    """ Create a SCALE that lets the user blur the image"""
    self.clear_widgets()
    self.scl_blur = tk.Scale(
        self.frame3, from_=1, to=50, orient=tk.HORIZONTAL, showvalue=1,
        command=self.blur_image, length=400, sliderlength=20, label="Blur", font="Tahoma 16",
        troughcolor=BG_COLOR, bg=BG_COLOR, fg='white', trough=LIGHT_GREY, highlightthickness=0,
    )
    self.scl_blur.place(relx=0.25, rely=0.2, relwidth=0.5, relheight=0.3)
    self.control_widgets_arr.append(self.scl_blur)

    self.web_cam_on_button_setup()
    self.blur_image()

def setup_bilateral_smooth_control_widegts(self):
    """ Create 3 SCLAEs that controls bilateral smooth's control panel"""
    self.clear_widgets()
    # self.scl_smooth_d = tk.Scale(
    #     self.frame3, from_=1, to=5, orient=tk.HORIZONTAL, showvalue=1,
    #     command=lambda d: self.bilateral_smooth_image(d=d), 
    #     length=400, sliderlength=20, label="Distance", font="Tahoma 16",
    #     troughcolor=BG_COLOR, bg=BG_COLOR, fg='white', trough="white", 
    #     highlightthickness=0,
    # )
    # self.scl_smooth_d.place(relx=0.25, rely=0.0, relwidth=0.5, relheight=0.3)
    # self.control_widgets_arr.append(self.scl_smooth_d)
    self.scl_smooth_sigma = tk.Scale(
        self.frame3, from_=1, to=50, orient=tk.HORIZONTAL, showvalue=1,
        command=lambda sigma: self.bilateral_smooth_image(sigma=sigma), 
        length=400, sliderlength=20, label="Sigma Space", font="Tahoma 16",
        troughcolor=BG_COLOR, bg=BG_COLOR, fg='white', trough="white", 
        highlightthickness=0,
    )
    self.scl_smooth_sigma.place(relx=0.25, rely=0.1, relwidth=0.5, relheight=0.3)
    self.control_widgets_arr.append(self.scl_smooth_sigma)

    self.scl_recursion_level = tk.Scale(
        self.frame3, from_=1, to=100, orient=tk.HORIZONTAL, showvalue=1,
        command=lambda level: self.bilateral_smooth_image(recursion_level=level), 
        length=400, sliderlength=20, label="Recursion Level", font="Tahoma 16",
        troughcolor=BG_COLOR, bg=BG_COLOR, fg='white', trough="white", 
        highlightthickness=0,
    )
    self.scl_recursion_level.place(relx=0.25, rely=0.5, relwidth=0.5, relheight=0.3)
    self.control_widgets_arr.append(self.scl_recursion_level)

    self.web_cam_on_button_setup()
    self.bilateral_smooth_image()

def setup_gradient_control_widgets(self):
    self.clear_widgets()
    self.edge_type_sel = tk.StringVar()
    self.edge_type_sel.set("Select")
    self.edge_type_sel.trace("w", self.edgeTypeSelCallback)
    self.sel_edge_type = tk.OptionMenu(
        self.frame3, self.edge_type_sel, *["x gradient", "y gradient", "xy gradient"]
    )
    self.sel_edge_type.config(fg="black", bg=BG_COLOR)
    self.sel_edge_type.place(relx=0.25, rely=0.2, relwidth=0.1)
    self.control_widgets_arr.append(self.sel_edge_type)

    def odd_fix(n):
        if not hasattr(self, "_past"):
            self._past = 0
        n = int(n)
        if not n % 2:
            self.scl_edge_size.set(n+1 if n > self._past else n-1)
            self._past = self.scl_edge_size.get()

    def command(n):
        odd_fix(n)
        self.sobel_edge_detection()
    self.scl_edge_size = tk.Scale(
        self.frame3, from_=1, to=31, orient=tk.HORIZONTAL, showvalue=1,
        command=command, length=400, sliderlength=20, label="Kernel Size", font="Tahoma 16",
        troughcolor=BG_COLOR, bg=BG_COLOR, fg='white', trough=LIGHT_GREY, highlightthickness=0,
    )
    self.scl_edge_size.place(relx=0.25, rely=0.4, relwidth=0.5, relheight=0.3)
    self.control_widgets_arr.append(self.scl_edge_size)

    self.web_cam_on_button_setup()
    self.sobel_edge_detection()

def edgeTypeSelCallback(self, *args):
    self.edge_type_sel_str = self.edge_type_sel.get()
    self.sobel_edge_detection()


def setup_canny_control_widgets(self):
    self.clear_widgets()

    def command_low(n):
        low = int(self.scl_edge_threshold_low.get())
        high = int(self.scl_edge_threshold_high.get())
        if low > high:
            self.scl_edge_threshold_high.set(low)
        self.canny_edge_detection()
    def command_high(n):
        low = int(self.scl_edge_threshold_low.get())
        high = int(self.scl_edge_threshold_high.get())
        if low > high:
            self.scl_edge_threshold_low.set(high)
        self.canny_edge_detection()

    self.scl_edge_threshold_low = tk.Scale(
        self.frame3, from_=0, to=255, orient=tk.HORIZONTAL, showvalue=1,
        command=command_low, length=400, sliderlength=20, label="Low Threshold", font="Tahoma 16",
        troughcolor=BG_COLOR, bg=BG_COLOR, fg='white', trough=LIGHT_GREY, highlightthickness=0,
    )
    self.scl_edge_threshold_low.place(relx=0.25, rely=0.1, relwidth=0.5, relheight=0.3)
    self.control_widgets_arr.append(self.scl_edge_threshold_low)

    self.scl_edge_threshold_high = tk.Scale(
        self.frame3, from_=0, to=255, orient=tk.HORIZONTAL, showvalue=1,
        command=command_high, length=400, sliderlength=20, label="High Threshold", font="Tahoma 16",
        troughcolor=BG_COLOR, bg=BG_COLOR, fg='white', trough=LIGHT_GREY, highlightthickness=0,
    )
    self.scl_edge_threshold_high.place(relx=0.25, rely=0.4, relwidth=0.5, relheight=0.3)
    self.control_widgets_arr.append(self.scl_edge_threshold_high)

    self.ksize_label = tk.Label(
        self.frame3, text="Kernel Size", font="Tahoma 16", bg=BG_COLOR, fg='white'
    )
    self.ksize_label.place(relx=0.25, rely=0.7, relwidth=0.1, relheight=0.1)
    self.control_widgets_arr.append(self.ksize_label)
    self.edge_ksize_sel = tk.IntVar()
    self.edge_ksize_sel.set(3)
    self.ksize3_radiobutton = tk.Radiobutton(
        self.frame3, text="3", variable=self.edge_ksize_sel, value=3,
        command=self.canny_edge_detection, font="Tahoma 16",
        bg=BG_COLOR, fg='white', activebackground=BG_COLOR, activeforeground='white',
    )
    self.ksize3_radiobutton.place(relx=0.25, rely=0.8, relwidth=0.1)
    self.control_widgets_arr.append(self.ksize3_radiobutton)
    self.ksize5_radiobutton = tk.Radiobutton(
        self.frame3, text="5", variable=self.edge_ksize_sel, value=5,
        command=self.canny_edge_detection, font="Tahoma 16",
        bg=BG_COLOR, fg='white', activebackground=BG_COLOR, activeforeground='white',
    )
    self.ksize5_radiobutton.place(relx=0.35, rely=0.8, relwidth=0.1)
    self.control_widgets_arr.append(self.ksize5_radiobutton)
    self.ksize7_radiobutton = tk.Radiobutton(
        self.frame3, text="7", variable=self.edge_ksize_sel, value=7,
        command=self.canny_edge_detection, font="Tahoma 16",
        bg=BG_COLOR, fg='white', activebackground=BG_COLOR, activeforeground='white',
    )
    self.ksize7_radiobutton.place(relx=0.45, rely=0.8, relwidth=0.1)
    self.control_widgets_arr.append(self.ksize7_radiobutton)

    self.web_cam_on_button_setup()
    self.canny_edge_detection()


def setup_quantization_widgets(self):
    self.clear_widgets()
    self.scl_n_clusters = tk.Scale(
        self.frame3, from_=2, to=16, orient=tk.HORIZONTAL, showvalue=2,
        command=self.quantization, length=400, sliderlength=20, 
        label="Number of Clusters", font="Tahoma 16", troughcolor=BG_COLOR, 
        bg=BG_COLOR, fg='white', trough=LIGHT_GREY, highlightthickness=0,
    )
    self.scl_n_clusters.place(relx=0.25, rely=0.1, relwidth=0.5, relheight=0.3)
    self.control_widgets_arr.append(self.scl_n_clusters)

    self.quantization_type = tk.Label(
        self.frame3, text="Quantization Type", font="Tahoma 16", bg=BG_COLOR, fg='white'
    )
    self.quantization_type.place(relx=0.25, rely=0.5, relwidth=0.15, relheight=0.1)
    self.control_widgets_arr.append(self.quantization_type)
    self.quantization_type_sel = tk.StringVar()
    self.quantization_type_sel.set("color")
    self.quantization_type_color_radiobutton = tk.Radiobutton(
        self.frame3, text="Color", variable=self.quantization_type_sel, value="color",
        command=self.quantization, font="Tahoma 16",
        bg=BG_COLOR, fg='white', activebackground=BG_COLOR, activeforeground='white',
    )
    self.quantization_type_color_radiobutton.place(relx=0.25, rely=0.65, relwidth=0.1)
    self.control_widgets_arr.append(self.quantization_type_color_radiobutton)
    self.quantization_type_luminance_radiobutton = tk.Radiobutton(
        self.frame3, text="Luminance", variable=self.quantization_type_sel, value="luminance",
        command=self.quantization, font="Tahoma 16",
        bg=BG_COLOR, fg='white', activebackground=BG_COLOR, activeforeground='white',
    )
    self.quantization_type_luminance_radiobutton.place(relx=0.35, rely=0.65, relwidth=0.1)
    self.control_widgets_arr.append(self.quantization_type_luminance_radiobutton)

    self.web_cam_on_button_setup()

    self.quantization()

def setup_cartoonization_widget(self):
    self.clear_widgets()
    self.scl_n_clusters = tk.Scale(
        self.frame3, from_=2, to=25, orient=tk.HORIZONTAL, showvalue=2,
        command=self.cartoonization, length=400, sliderlength=20,
        label="Colofulness", font="Tahoma 16", troughcolor=BG_COLOR,
        bg=BG_COLOR, fg='white', trough=LIGHT_GREY, highlightthickness=0,
    )
    self.scl_n_clusters.place(relx=0.25, rely=0.05, relwidth=0.5, relheight=0.3)
    self.control_widgets_arr.append(self.scl_n_clusters)

    def odd_fix(n):
        if not hasattr(self, "_past_odd"):
            self._past_odd = 0
        n = int(n)
        if not n % 2:
            self.scl_base_sigma.set(n+1 if n > self._past_odd else n-1)
            self._past_odd = self.scl_base_sigma.get()

    def odd_command(n):
        odd_fix(n)
        self.cartoonization()

    def even_fix(n):
        if not hasattr(self, "_past_even"):
            self._past_even = 0
        n = int(n)
        if n % 2:
            self.scl_sigma_step.set(n+1 if n > self._past_even else n-1)
            self._past_even = self.scl_sigma_step.get()
    
    def even_command(n):
        even_fix(n)
        self.cartoonization()

    self.scl_base_sigma = tk.Scale(
        self.frame3, from_=3, to=51, orient=tk.HORIZONTAL, showvalue=2,
        command=odd_command, length=400, sliderlength=20,
        label="Blurriness", font="Tahoma 16", troughcolor=BG_COLOR,
        bg=BG_COLOR, fg='white', trough=LIGHT_GREY, highlightthickness=0,
    )
    self.scl_base_sigma.place(relx=0.25, rely=0.35, relwidth=0.5, relheight=0.3)
    self.control_widgets_arr.append(self.scl_base_sigma)

    self.scl_sigma_step = tk.Scale(
        self.frame3, from_=2, to=50, orient=tk.HORIZONTAL, showvalue=2,
        command=even_command, length=400, sliderlength=20,
        label="Paint Brush Thickness", font="Tahoma 16", troughcolor=BG_COLOR,
        bg=BG_COLOR, fg='white', trough=LIGHT_GREY, highlightthickness=0,
    )
    self.scl_sigma_step.place(relx=0.25, rely=0.65, relwidth=0.5, relheight=0.3)
    self.control_widgets_arr.append(self.scl_sigma_step)

    self.web_cam_on_button_setup()
    self.cartoonization()

