import cv2
import enum
import numpy as np
from util import calc_energy

class Direction(enum.Enum):
	VERTICAL = 0
	HORIZONTAL = 1

class SeamCarve:
	def __init__(self, img):
		self.img = img.copy()
		self.energy_map = calc_energy(img)
		self.rows, self.cols, _ = self.img.shape

	def __find_opt_seam(self, direction):

		if direction == Direction.HORIZONTAL:
			self.energy_map = np.transpose(self.energy_map)
			self.rows = len(self.energy_map)
			self.cols = len(self.energy_map[0])

		seam = []

		M = self.energy_map.copy()

		for i in range(0, self.rows):
			if i == 0:
				continue
			for j in range(0, self.cols):
				if j == 0:
					M[i][j] += min((M[i - 1][j], M[i - 1][j + 1]))
				elif j == self.cols - 1:
					M[i][j] += min((M[i - 1][j - 1], M[i - 1][j]))
				else:
					M[i][j] += min((M[i - 1][j - 1],M[i - 1][j], M[i - 1][j + 1]))

		current_point = np.min(M[-1])
		current_index = np.where(M[-1] == current_point)[0][0]
		seam.append([self.rows - 1, current_index])
		for i in range(self.rows - 2, -1, -1):
			
			index_mapping = {
				M[i][current_index]: current_index,
			}

			if current_index == 0:	
				index_mapping[M[i][current_index + 1]] = current_index + 1
				current_point = min((M[i][current_index], M[i][current_index + 1]))
			elif current_index == self.cols - 1:
				index_mapping[M[i][current_index - 1]] = current_index - 1
				current_point = min((M[i][current_index - 1], M[i][current_index]))
			else:
				index_mapping[M[i][current_index + 1]] = current_index + 1
				index_mapping[M[i][current_index - 1]] = current_index - 1
				current_point = min((M[i][current_index - 1],M[i][current_index], M[i][current_index + 1]))

			current_index = index_mapping[current_point]
			seam.append([i, current_index])

		if direction == Direction.HORIZONTAL:
			for entry in seam:
				entry[0],entry[1] = entry[1],entry[0]
			self.energy_map = np.transpose(self.energy_map)
			self.rows, self.cols, _ = self.img.shape

		for seam_item in seam:
			self.img[seam_item[0],seam_item[1]] = (0,0,255)

		return seam

	def __remove_seam(self, seam, direction):
		if direction == Direction.HORIZONTAL:
			for point in seam:
				for i in range(point[0], self.rows - 1):
					self.img[i, point[1]] = self.img[i + 1, point[1]]
			self.img = self.img[0:self.rows - 1, 0:self.cols]
		else:
			for point in seam:
				for j in range(point[1], self.cols - 1):
					self.img[point[0], j] = self.img[point[0], j + 1]
			self.img = self.img[0:self.rows, 0:self.cols - 1]

		self.rows, self.cols, _ = self.img.shape
		self.energy_map = calc_energy(self.img)

	def __insert_seam(self, seam, direction):
		if direction == Direction.VERTICAL:
			new_img = np.zeros((self.rows,self.cols + 1,3), np.uint8)
			
			for row in range(0, self.rows):
				offset = 0
				for col in range(0, self.cols):
					if col + offset >= self.cols: 
						break
					new_img[row,col + offset] = self.img[row,col].copy()
					if [row, col] in seam:
						new_img[row, col + 1] = self.img[row,col].copy()
						offset = 1
		else:
			new_img = new_img = np.zeros((self.rows + 1,self.cols,3), np.uint8)

			for col in range(0, self.cols):
				offset = 0
				for row in range(0, self.rows):
					if row + offset >= self.rows:
						break
					new_img[row + offset,col] = self.img[row,col].copy()
					if [row, col] in seam:
						new_img[row + 1,col] = self.img[row,col].copy()
						offset = 1

		self.img = new_img.copy()
		self.rows, self.cols, _ = new_img.shape
		self.energy_map = calc_energy(new_img)

	def resize(self, width, height):
		
		if width > self.cols:
			print("Starting vertical insertion...")
			diff = width - self.cols
			print(diff)
			ref_img = SeamCarve(self.img)
			for i in range (0, diff):
				# back up the original information
				opt_seam = ref_img.__find_opt_seam(Direction.VERTICAL)
				self.__insert_seam(opt_seam,Direction.VERTICAL)
				ref_img.__remove_seam(opt_seam,Direction.VERTICAL)
				print(f"Added {i} seams")

		elif width < self.cols:
			print("Starting vertical carving...")
			diff = self.cols - width
			print(diff)
			for i in range(0, diff):
				opt_seam = self.__find_opt_seam(Direction.VERTICAL)
				self.__remove_seam(opt_seam, Direction.VERTICAL)
				print(f"Carved {i} seams")

		if height > self.rows:
			print("Starting horizontal insertion...")
			diff = height - self.rows
			print(diff)
			ref_img = SeamCarve(self.img)
			for i in range (0, diff):
				# back up the original information
				opt_seam = ref_img.__find_opt_seam(Direction.HORIZONTAL)
				self.__insert_seam(opt_seam,Direction.HORIZONTAL)
				ref_img.__remove_seam(opt_seam,Direction.HORIZONTAL)
				print(f"Added {i} seams")

		elif height < self.rows:
			print("Starting horizontal carving...")
			diff = self.rows - height
			print(diff)
			for i in range(0, diff):
				opt_seam = self.__find_opt_seam(Direction.HORIZONTAL)
				self.__remove_seam(opt_seam, Direction.HORIZONTAL)
				print(f"Carved {i} seams")
			pass


	def remove_object(self, mask):
		pass


	