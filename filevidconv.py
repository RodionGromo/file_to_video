import io, math
from PIL import Image, ImageColor

def readBytesToHex(file: io.TextIOWrapper):
	byte_list = []
	for char in file.read():
		n = ord(char)
		if n > 255:
			raise ValueError(f"char {char} too large on utf-8 table")
		hex_str = hex(n)[2:]
		hex_str = "0" + hex_str if len(hex_str) == 1 else hex_str
		byte_list.append(hex_str)
	return byte_list

def byteHexToHexColor(hex_list: list):
	colors = []
	for i in range(0,len(hex_list),3):
		clr_list = hex_list[i:i+3]
		if len(clr_list) < 3:
			clr_list += ["00"] * (3 - len(clr_list))
		hex_color = "#" + "".join(clr_list)
		colors.append(hex_color)
	return colors

def colorsToSingleImage(colors: list, imagesize: tuple=None):
	if imagesize is None:
		imagesize = [math.isqrt(len(colors)) + 1] * 2
	elif (imagesize[0] * imagesize[1]) < len(colors):
		raise ValueError("Image size too small to fit data in")
	image = Image.new("RGB", imagesize)
	try:
		for y in range(image.size[1]):
			for x in range(image.size[0]):
				image.putpixel((x,y), ImageColor.getrgb(colors[y * imagesize[0] + x]))
	except IndexError:
		return image
	return image

def file2img(filename, imagesize: tuple=None):
	return colorsToSingleImage(byteHexToHexColor(readBytesToHex(open(filename,"r"))), imagesize)

def file2gif(filename, videosize: tuple, frameDurationMS=24, output_filename='output.gif'):
	colors = byteHexToHexColor(readBytesToHex(open(filename, "r")))
	frameCount = int(len(colors) / (videosize[0] * videosize[1])) + 1
	image_list = [Image.new("RGB", videosize) for i in range(frameCount if frameCount > 0 else 1)]
	current_il_index = 0
	while len(colors) > 0:
		image = image_list[current_il_index]
		try:
			for y in range(image.size[1]):
				for x in range(image.size[0]):
					image.putpixel((x,y), ImageColor.getrgb(colors[0]))
					del colors[0]
		except IndexError:
			break
		current_il_index += 1
	image_list[0].save(output_filename, save_all=True, append_images=image_list[1:], duration=frameDurationMS)
	return True

def rgb2hex(rgb):
	return (hex(rgb[0])[2:], hex(rgb[1])[2:], hex(rgb[2])[2:])

def isEmptyPixel(obj):
	return obj == ("0","0","0")

def imageToHex(filename):
	colors = []
	img = Image.open(filename)
	for y in range(img.size[1]):
		for x in range(img.size[0]):
			color = list(rgb2hex(img.getpixel((x,y))))
			color = [i for i in color if i != "0"]
			if not isEmptyPixel(color):
				colors += list(color)
	return colors

def gifFrameToHex(frame):
	img = frame.convert("RGB")
	colors = []
	for y in range(img.size[1]):
		for x in range(img.size[0]):
			color = list(rgb2hex(img.getpixel((x,y))))
			color = [i for i in color if i != "0"]
			if not isEmptyPixel(color):
				colors += list(color)
	return colors

def colorsToText(colors: list, output_filename: str="output.txt"):
	text = "".join([chr(int(i, 16)) for i in colors]).replace(r"\x00", "")
	return text

def image2textfile(filename: str, output_filename: str="output.txt"):
	with open(output_filename,"w") as file:
		file.write(colorsToText(imageToHex(filename)))

def gif2textfile(filename: str, output_filename: str="output.txt"):
	text = ""
	gif = Image.open(filename)
	for i in range(gif.n_frames):
		gif.seek(i)
		text += colorsToText(gifFrameToHex(gif))
	return text