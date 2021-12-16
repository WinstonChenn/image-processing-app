import cv2
import numpy as np
import tkinter as tk
import PIL
from sklearn.cluster import MiniBatchKMeans
from .settings import MARGIN, MAXDIM, BG_COLOR, LIGHT_GREY

def blur_image(self, k=None, image=None, return_image=False):
    if k is None:
        k = self.scl_blur.get()
    k = int(k)
    if image is None:
        image = self.resized_ori_img
    self.resized_mod_img = cv2.blur(image, (k, k))
    self.resized_mod_img_copy = self.resized_mod_img.copy()
    self.tk_mod_img = PIL.ImageTk.PhotoImage(
        image = PIL.Image.fromarray(self.resized_mod_img)
    )
    if return_image:
        return self.resized_mod_img
    else:
        self.canvas1.create_image(
            MAXDIM//2, MAXDIM//2, image=self.tk_mod_img, anchor=tk.CENTER
        )

def bilateral_smooth_image(
    self, d=5, sigma=None, recursion_level=None, image=None, return_image=False
):
    if sigma is None:
        sigma = self.scl_smooth_sigma.get()
    if recursion_level is None:
        recursion_level = self.scl_recursion_level.get()
    if image is None:
        image = self.resized_ori_img
    d, sigma, recursion_level = int(d), int(sigma), int(recursion_level)
    self.resized_mod_img = image.copy()
    for i in range(recursion_level):
        self.resized_mod_img = cv2.bilateralFilter(
            self.resized_mod_img, d, sigma, sigma
        )
    self.resized_mod_img_copy = self.resized_mod_img.copy()
    self.tk_mod_img = PIL.ImageTk.PhotoImage(
        image = PIL.Image.fromarray(self.resized_mod_img)
    )
    if return_image:
        return self.resized_mod_img
    else:
        self.canvas1.create_image(
            MAXDIM//2, MAXDIM//2, image=self.tk_mod_img, anchor=tk.CENTER
        )

def sobel_edge_detection(
    self, type=None, ksize=None, image=None, return_image=False
):
    if type is None:
        type = self.edge_type_sel.get()
    if ksize is None:
        ksize = int(self.scl_edge_size.get())
    if image is None:
        image = self.resized_ori_img
    if type == "x gradient":
        self.resized_mod_img = cv2.Sobel(
            image, cv2.CV_64F, dx=1, dy=0, ksize=ksize
        )
    elif type == "y gradient":
        self.resized_mod_img = cv2.Sobel(
            image, cv2.CV_64F, dx=0, dy=1, ksize=ksize
        )
    elif type == "xy gradient":
        self.resized_mod_img = cv2.Sobel(
            image, cv2.CV_64F, dx=1, dy=1, ksize=ksize
        )
    self.resized_mod_img_copy = self.resized_mod_img.copy()
    self.tk_mod_img = PIL.ImageTk.PhotoImage(
        image = PIL.Image.fromarray(self.resized_mod_img.astype(np.uint8))
    )
    if return_image:
        return self.resized_mod_img.astype(np.uint8)
    else:
        self.canvas1.create_image(MAXDIM//2, MAXDIM//2, image=self.tk_mod_img, anchor=tk.CENTER)


def canny_edge_detection(
    self, threshould_low=None, threshould_high=None, ksize=None,
    image=None, return_image=False
):
    if threshould_low is None:
        threshould_low = self.scl_edge_threshold_low.get()
    if threshould_high is None:
        threshould_high = self.scl_edge_threshold_high.get()
    if ksize is None:
        ksize = self.edge_ksize_sel.get()
    if image is None:
        image = self.resized_ori_img

    threshould_low, threshould_high, ksize = int(threshould_low), int(threshould_high), int(ksize)
    self.resized_mod_img = cv2.Canny(
        image, threshold1=threshould_low, threshold2=threshould_high, 
        apertureSize=ksize
    )
    self.resized_mod_img_copy = self.resized_mod_img.copy()
    self.tk_mod_img = PIL.ImageTk.PhotoImage(
        image = PIL.Image.fromarray(self.resized_mod_img)
    )
    if return_image:
        return self.resized_mod_img
    else:
        self.canvas1.create_image(
            MAXDIM//2, MAXDIM//2, image=self.tk_mod_img, anchor=tk.CENTER
        )


def quantization(
    self, n_clusters=None, type=None, image=None, return_image=False
):
    if n_clusters is None:
        n_clusters = self.scl_n_clusters.get()
    if type is None:
        type = self.quantization_type_sel.get()
    if image is None:
        image = self.resized_ori_img
    assert type in ["color", "luminance"]
    n_clusters = int(n_clusters)
    clt = MiniBatchKMeans(n_clusters = n_clusters)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2LAB)
    (h, w) = image.shape[:2]
    if type == "color":
        labels = clt.fit_predict(image.reshape((w * h, 3)))
        quant = clt.cluster_centers_.astype("uint8")[labels].reshape((h, w, 3))
    elif type == "luminance":
        labels = clt.fit_predict(image[:,:,0].reshape((w * h, 1)))
        quant = image
        quant[:, :, 0:1] = clt.cluster_centers_.astype("uint8")[labels].reshape((h, w, 1))
    quant = cv2.cvtColor(quant, cv2.COLOR_LAB2RGB)
    self.resized_mod_img = quant
    self.resized_mod_img_copy = self.resized_mod_img.copy()
    self.tk_mod_img = PIL.ImageTk.PhotoImage(
        image = PIL.Image.fromarray(self.resized_mod_img)
    )
    if return_image:
        return self.resized_mod_img
    self.canvas1.create_image(
        MAXDIM//2, MAXDIM//2, image=self.tk_mod_img, 
        anchor=tk.CENTER
    )

def cartoonization(
    self, n_clusters=None, sigma_base=None, sigma_step=None, 
    image=None, return_image=False
):
    if n_clusters is None:
        n_clusters = self.scl_n_clusters.get()
    if sigma_base is None:
        sigma_base = self.scl_base_sigma.get()
    if sigma_step is None:
        sigma_step = self.scl_sigma_step.get()
    if image is None:
        image = self.resized_ori_img
    n_clusters, sigma_base, sigma_step = int(n_clusters), int (sigma_base), int (sigma_step)

    # Bilateral Filtering
    n_recurssion = 30
    d = 5
    sigma = 20
    smoothed = image.copy()
    for i in range(n_recurssion):
        smoothed = cv2.bilateralFilter(
            smoothed, d, sigma, sigma
        )
    
    # Luminance Quantization
    clt = MiniBatchKMeans(n_clusters = n_clusters)
    smoothed_cpy = smoothed.copy()
    (h, w) = smoothed_cpy.shape[:2]
    labels = clt.fit_predict(smoothed_cpy[:,:,:].reshape((w * h, 3)))
    quant = smoothed_cpy
    quant[:, :, :] = clt.cluster_centers_.astype("uint8")[labels].reshape((h, w, 3))
    # quant = cv2.cvtColor(quant, cv2.COLOR_LAB2RGB)

    # DoG Edge Detection
    low_sigma_img = cv2.GaussianBlur(smoothed,[sigma_base]*2,0)
    high_sigma_img = cv2.GaussianBlur(smoothed,[sigma_base+sigma_step]*2,0)
    dog = cv2.cvtColor(
        np.maximum(0, low_sigma_img - high_sigma_img), 
        cv2.COLOR_BGR2GRAY
    )
    dog_invert = 255 - dog
    dog_invert = np.dstack([dog_invert] * 3)

    # Combine qunatization and edge detection
    cartoon = np.minimum(quant, dog_invert)
    self.resized_mod_img = cartoon
    self.resized_mod_img_copy = self.resized_mod_img.copy()
    self.tk_mod_img = PIL.ImageTk.PhotoImage(
        image = PIL.Image.fromarray(self.resized_mod_img)
    )
    if return_image:
        return self.resized_mod_img
    self.canvas1.create_image(
        MAXDIM//2, MAXDIM//2, image=self.tk_mod_img,
        anchor=tk.CENTER
    )