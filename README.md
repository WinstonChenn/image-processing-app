# A Simple Classical Image Processing App
![imgageprocessing](https://raw.githubusercontent.com/WinstonChenn/image-processing-app/main/README_images/gui.png?token=AL6M65AP7YS3AQSQE3UUYTTBYFXCY)

##  Introduction
This project implements a simple image processing graphic user interface (GUI) that performs wide varieties of classical image processing (blur, smooth, edge detection, quantization, etc.) Users will be able to select different test images from image libaray or uploading their local images to perform desired image processing effect. Users can also download processed image to local or apply selected effect on their webcam to produce desired realtime image processing effect.

## How to run this App?
### 1. Install requirements
- Install [Anaconda](https://docs.anaconda.com/anaconda/install/index.html)
- Install [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
### 2. Clone this github repository
```
git clone https://github.com/WinstonChenn/image-processing-app.git
```
### 3. Create and activate virtual environment using Anaconda
```
cd image-processing-app
conda env create --name [ENV-NAME] -f environment.yml
conda activate [ENV-NAME]
```
### 3. Run the app
```
python src/main.py
```

## Implementation Details
**Graphic User Interface (GUI)** <br/>
The GUI of this image process app is entirely built with [Python](https://www.python.org/) and [Tkinter](https://docs.python.org/3/library/tkinter.html). The Python codes responsible for creating this GUI layout can be found in `src/app/__init__.py` and `src/app/control_panel.py` The GUI can be roughly separated into three sections. 
1. The display section <br/>
The display section is located in top part of the image processing app GUI. It is responsible for displaying the original image and processed images. This section provids a direct comparison between original and processed images, which allows users to easily see the result of applied filter. 
![display example](https://raw.githubusercontent.com/WinstonChenn/image-processing-app/main/README_images/display.png?token=AL6M65FWMPPTR6JR2DBZB63BYFW6Q)

2. Primary control panel <br/>
THe primary control panel locates at the lower left corner of the GUI. It is designed to provide users with high-level image processing app functionalities, such as selecting different photos, choosing different image processing effects, and saving processed photos. <br/>
![primary control example](https://raw.githubusercontent.com/WinstonChenn/image-processing-app/main/README_images/primary_control.png?token=AL6M65A77ZJ6GVT7UEYSBCLBYFXG6)
3. Secondary control panel <br/>
The secondary control panel locates at the lower right corner of the GUI. It provides functionalities specific to the image processing effects that users selected from the primary control panel. This panel provides various wigets that allows user to manipulate the parameters of the image processing filter that they are applying. Therefore different image processing effects will result in different wigets layout. <br/>
Additionally, I also provides the "Web Cam On" button that allows user to apply the selected filter with current parameter to a real-time video stream from their webcam. <br/> 
![secondary control example](https://raw.githubusercontent.com/WinstonChenn/image-processing-app/main/README_images/secondary_control.png?token=AL6M65HV26O4ETU7ZGUSVNDBYFXLA)

**Image Processing Effects** <br/>
Currently 6 image processing effects are implemented. 5 of them are classical image processing filters and 1 one them is a composite image filter that generates cartoon effect. The Python codes for implementing these filters are located in `src/app/filter_operations.py`
1. Classical image filters <br/>
Currently I implemented the following classical image filters: gaussian blur, bilateral filter, sobel gradient fiter, canny edge detection filter, quantization filter. The core algorithms of each filter are implemented by OpenCV and most of the scripts in `src/app/filter_operations.py` invovles connecting OpenCV's filter API with GUI's parameter control widgets.
2. Cartoon effect filter <br/>
The cartoon effect filter is a composite filter composed of bilateral filter, luminance qunatization filter, difference of gaussian(DoG) edge detection filter. The detail of how to combining these filters is summarized in the instruction below:
    1. Applying recursive bilateral filters to generate smoothed images
    2. Applying luminance quantization on smoothed images to generate quantized images
    3. Applying DoG edge detection filter on smoothed images to generate edge images
    3. Negate the edge images
        - the edges will have dark values in the negated image (to simulate trace).
    4. Combining qunatized image with negated edges using "Min" function
        - Min function preserves the edge pixels, which tend to have near 0 values.
## Results Discussion

## Learning Results & Feature Work

## References
