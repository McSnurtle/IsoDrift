# Surface.py / Renderer in vanilla python - Mc_Snurtle
# imports

from PIL import Image, ImageTk
import tkinter as tk
import time


class Renderer:
	
	def __init__(self, width, height, colorspace: str):
		self.width, self.height = width, height
		self.screen = Image.new(colorspace, (self.width, self.height), 'black')

		self.root = tk.Tk()
		self.canvas = tk.Canvas(self.root, width=self.width, height=self.height)
		self.canvas.pack()
		self.running = True

	def clear(self):
		self.canvas.delete(tk.ALL)

	def draw_rect(self, x, y, width, height, color):
		x1, y1, x2, y2 = x, y, x + width, y + height
		self.canvas.create_rectangle(x1, y1, x2, y2, fill=color)

	def load_image(self, path: str):
		return Image.open(path)

	def rotate_image(self, image: str, angle: float):
		pil_image = Image.open(image)
		rotated_image = pil_image.rotate(angle, expand=True)
		return ImageTk.PhotoImage(rotated_image)

	def scale_image(self, image: str, scale: tuple):
		pil_image = Image.open(image)
		scaled_image = pil_image.resize(scale, Image.ANTIALIAS)
		return ImageTk.PhotoImage(scaled_image)

	def draw_image(self, image, position: tuple) -> None:
		self.screen.paste(image, position)

	def update(self):
		self.root.update_idletasks()
		self.root.update()


	class Clock:

		def __init__(self):
			self.start_time = time.time()
			self.last_time = self.start_time

		def tick(self, fps: int = 60):
			current_time = time.time()
			elapsed_time = current_time - self.last_time
			target_delay = 1.0 / fps - elapsed_time

			if target_delay > 0:
				time.sleep(target_delay)
			self.last_time = current_time

		def get_time(self):
			return time.time() - self.start_time

		def get_fps(self):
			return 1.0 / (time.time() - self.last_time)

		def restart(self):
			self.start_time = time.time()
			self.last_time = self.start_time