import cv2
from seam_carve import SeamCarve, Direction

from util import calc_energy

def main():
	img = cv2.imread("img/test4.jpg",cv2.IMREAD_COLOR)
	img_edit = SeamCarve(img)
	img_edit.resize(700, 450)
	cv2.imshow("Original Image", img)
	cv2.waitKey(0)
	cv2.imshow("Modified Umage", img_edit.img)
	cv2.waitKey(0)
	pass

if __name__ == "__main__":
	main()