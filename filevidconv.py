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