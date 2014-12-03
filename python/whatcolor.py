from PIL import Image as img
import urllib, cStringIO
import yaml


camlist = open("camlist.yaml")

cams = camlist.read()

print yaml.load(cams)

print cams


URL = "http://www.met.sjsu.edu/cam_directory/webcam3/latest.jpg";

file = cStringIO.StringIO(urllib.urlopen(URL).read())
im = img.open(file)
# im = img.open("sjsky.jpg")
size = im.size
im = im.crop((0,40,size[0],size[1]/3))
# im.show()
# im = im.quantize(1).convert("RGB")


# im.show()

print(im.getpixel((3,3)))