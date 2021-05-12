# Content Aware Resizing Homework Report

张敏胜 2018080102

## Environment

- OS: Windows 10 64 Bit
- Programming Stack: Python 3.9.0
- Dependencies: OpenCV2, numpy, scipy

## Implementation

### Energy Function Calculation

The energy function calculation is calculated by the formula :

![image-20210418151318982](C:\Users\Richard\AppData\Roaming\Typora\typora-user-images\image-20210418151318982.png)

Which is implemented using the convolution of their differentation matrices.

### Seam finding

The seam finding is implemented using a naive method, wherein after the energy map of the entire image is calculated, the M value for each pixel is calculated using the following formula:

 ![image-20210418151846840](C:\Users\Richard\AppData\Roaming\Typora\typora-user-images\image-20210418151846840.png) 

After finding all the M-values for each pixel, the program performs a "greedy" backtrack to determine the optimal seam to process, it checks for the next shortest energy-level seam in the enerygy map, adding that coordinate to a seam array containing the pixel-coordinates of the seam. This algorithm has a straightforward implementation but very large time complexity.

### Seam carving

The seam carving process is relatively straightforward, the program simply remove the pixels indicated within the seam array from the image, resulting in a size-reduced image.

### Seam insertion

The seam insertion is implemented by using another instance of the image to determine which seams to be removed. Since the inserted seams have to be different each time, another instance (I will call it the reference image) of the image was used to allow the program to find different optimum seams. Upon each insertion of a seam , a seam is removed in the reference image to avoid redudancy.

### Object removal

The general idea of the objecft removal algorithm is the removal of specific seams and putting back the size onto the original size afterwards. The way to direct the seam removal algorithm to removing specific parts of the image is by setting its pixel energy map into the negative of it's own energy map. This energy map will then be used to perform the normal seam removal.

## Results

### Seam Carving

| ![](D:\Documents\School\Spring2021\数字图像处理\作业\hw3\ContentAwareResizing_python\img\test4.jpg) | ![](D:\Documents\School\Spring2021\数字图像处理\作业\hw3\res1.PNG) | ![image-20210418161146153](C:\Users\Richard\AppData\Roaming\Typora\typora-user-images\image-20210418161146153.png) |
| ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ |
| The original image                                           | Image after horizontal and vertical seam carving (aspect ratio change) | Image after horizontal and vertical seam insertion (aspect ratio change) |


