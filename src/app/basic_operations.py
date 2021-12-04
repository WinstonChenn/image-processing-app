import cv2
import numpy as np
import tkinter as tk
import PIL
from sklearn.cluster import MiniBatchKMeans
from .settings import MARGIN, MAXDIM, BG_COLOR, LIGHT_GREY
def blur_image(self, k):
    k = int(k)
    self.NEWcv_img_modify = cv2.blur(self.NEWcv_img, (k, k))
    self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(self.NEWcv_img_modify))
    self.canvas1.create_image(MAXDIM//2, MAXDIM//2, image=self.photo, anchor=tk.CENTER)

def bilateral_smooth_image(self, d=5, sigma=None, recursion_level=None):
    # if d is None:
    #     d = self.scl_smooth_.get()
    if sigma is None:
        sigma = self.scl_smooth_sigma.get()
    if recursion_level is None:
        recursion_level = self.scl_recursion_level.get()

    d, sigma, recursion_level = int(d), int(sigma), int(recursion_level)

    self.NEWcv_img = self.cv_img.copy()
    for i in range(recursion_level):
        self.NEWcv_img = cv2.bilateralFilter(self.NEWcv_img, d, sigma, sigma)
    self.NEWcv_img_modify = self.NEWcv_img
    self.photo = PIL.ImageTk.PhotoImage(PIL.Image.fromarray(self.NEWcv_img_modify))
    self.canvas1.create_image(
        MAXDIM//2, MAXDIM//2, image=self.photo, anchor=tk.CENTER
    )

def sobel_edge_detection(self, type=None, ksize=None):
    if type is None:
        type = self.edge_type_sel.get()
    if ksize is None:
        ksize = self.scl_edge_size.get()
    if type == "x gradient":
        self.NEWcv_img_modify = cv2.Sobel(self.NEWcv_img, cv2.CV_64F, dx=1, dy=0, ksize=ksize)
    elif type == "y gradient":
        self.NEWcv_img_modify = cv2.Sobel(self.NEWcv_img, cv2.CV_64F, dx=0, dy=1, ksize=ksize)
    elif type == "xy gradient":
        self.NEWcv_img_modify = cv2.Sobel(self.NEWcv_img, cv2.CV_64F, dx=1, dy=1, ksize=ksize)
    self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(self.NEWcv_img_modify.astype(np.uint8)))
    self.canvas1.create_image(MAXDIM//2, MAXDIM//2, image=self.photo, anchor=tk.CENTER)


def canny_edge_detection(self, threshould_low=None, threshould_high=None, ksize=None):
    if threshould_low is None:
        threshould_low = self.scl_edge_threshold_low.get()
    if threshould_high is None:
        threshould_high = self.scl_edge_threshold_high.get()
    if ksize is None:
        ksize = self.edge_ksize_sel.get()
    threshould_low, threshould_high, ksize = int(threshould_low), int(threshould_high), int(ksize)
    self.NEWcv_img_modify = cv2.Canny(
        self.NEWcv_img, threshold1=threshould_low, threshold2=threshould_high, 
        apertureSize=ksize
    )
    self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(self.NEWcv_img_modify))
    self.canvas1.create_image(MAXDIM//2, MAXDIM//2, image=self.photo, anchor=tk.CENTER)


def quantization(self, n_clusters=None):
    if n_clusters is None:
        n_clusters = self.scl_n_clusters.get()
    n_clusters = int(n_clusters)
    image = cv2.cvtColor(self.NEWcv_img, cv2.COLOR_RGB2LAB)
    (h, w) = image.shape[:2]
    image = image.reshape((h*w, 3))
    clt = MiniBatchKMeans(n_clusters = n_clusters)
    labels = clt.fit_predict(image)
    quant = clt.cluster_centers_.astype("uint8")[labels]
    quant = quant.reshape((h, w, 3))
    self.NEWcv_img_modify = cv2.cvtColor(quant, cv2.COLOR_LAB2RGB)
    self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(self.NEWcv_img_modify))
    self.canvas1.create_image(MAXDIM//2, MAXDIM//2, image=self.photo, anchor=tk.CENTER)
