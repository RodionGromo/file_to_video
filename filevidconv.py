import PIL

def readBytesToHex(file):
	byte_list = []
	for char in file.read():
		n = ord(char)
		if n > 255:
			raise ValueError(f"char {char} too large on utf-8 table")
		byte_list.append(hex(n)[2:])
	return byte_list

def byteHexToHexColor(hex_list):
	colors = []
	for i in range(0,len(hex_list),3):
		clr_list = hex_list[i:i+3]
		if len(clr_list) < 3:
			clr_list += ["00"] * (3 - len(clr_list))
		hex_color = "#" + "".join(clr_list)
		colors.append(hex_color)
