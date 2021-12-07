import cv2
import tkinter as tk
import numpy as np
import PIL.Image
import PIL.ImageTk
from .settings import MARGIN, MAXDIM, BG_COLOR, LIGHT_GREY, DROPDOWN_WIDTH
    
def web_cam_on_button_setup(self):
    self.webCamOnButton = tk.Button(
        self.frame3, text="Web Cam On", 
        command=self.webCamOnButtonCallback, font="Tahoma 13",
        highlightbackground=BG_COLOR,
        fg='black', activeforeground="grey",
    )
    self.webCamOnButton.place(relx=0.85, rely=0.1, relwidth=DROPDOWN_WIDTH)

def web_cam_off_button_setup(self):
    self.webCamOffButton = tk.Button(
        self.frame3, text="Web Cam Off", 
        command=self.webCamOffButtOffCallback, font="Tahoma 13",
        highlightbackground=BG_COLOR,
        fg='black', activeforeground="grey",
    )
    self.webCamOffButton.place(relx=0.85, rely=0.1, relwidth=DROPDOWN_WIDTH)

def webCamOnButtonCallback(self):
    self.video = True
    self.cap= cv2.VideoCapture(0)
    self.web_cam_off_button_setup()
    # Disable regular control panel
    for widget in self.control_widgets_arr:
        try:
            widget.configure(state="disabled")
        except:
            breakpoint()
        
    def show_frames(setup=True):
        if not self.video and hasattr(self, "canvas0_solve"):
            self.canvas0.after_cancel(self.canvas0_solve)
        else:
            img = cv2.cvtColor(self.cap.read()[1],cv2.COLOR_BGR2RGB)
            self.setup_photo(img, setup_mod=setup)
            # Repeat after an interval to capture continiously
            self.canvas0_solve = self.canvas0.after(20, lambda: show_frames(setup=False))
    show_frames()
    self.webCamOnButton.destroy()

def webCamOffButtOffCallback(self):
    self.video = False
    self.cap.release()
    # self.canvas0.destroy()
    # self.canvas1.destroy()
    self.setup_photo(self.load_photo(self.image_path))
    self.webCamOffButton.destroy()
    # enbable regular control panel
    for widget in self.control_widgets_arr:
        widget.configure(state="normal")
    self.web_cam_on_button_setup()

