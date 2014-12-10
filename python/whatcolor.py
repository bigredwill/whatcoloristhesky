#!
from PIL import Image as img
from PIL import ImageDraw as imgDraw
import urllib, cStringIO, yaml, tweepy, time, sys

import webcolors

lastColorFile = open("/home/pi/whatcoloristhesky/python/lastColor.txt", "r")
lastColor = lastColorFile.read().split('\n')
print lastColor


secrets = open("/home/pi/whatcoloristhesky/python/secrets.yaml")
secrets = yaml.load(secrets.read())
#enter the corresponding information from your Twitter application:
CONSUMER_KEY = secrets['consumer_key']
CONSUMER_SECRET = secrets['consumer_secret']
ACCESS_KEY = secrets['access_key']
ACCESS_SECRET = secrets['access_secret']
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)


# camlist = open("cam2.yaml")
camlist = open("/home/pi/whatcoloristhesky/python/camlist.yaml")

cams = yaml.load(camlist.read())

# credit to fraxel, http://stackoverflow.com/a/9694246
def closest_colour(requested_colour):
  min_colours = {}
  for key, name in webcolors.css3_hex_to_names.items():
      r_c, g_c, b_c = webcolors.hex_to_rgb(key)
      rd = (r_c - requested_colour[0]) ** 2
      gd = (g_c - requested_colour[1]) ** 2
      bd = (b_c - requested_colour[2]) ** 2
      min_colours[(rd + gd + bd)] = name
  return min_colours[min(min_colours.keys())]

def get_colour_name(requested_colour):
  try:
    closest_name = actual_name = webcolors.rgb_to_name(requested_colour)
  except ValueError:
    closest_name = closest_colour(requested_colour)
    actual_name = None
    return closest_name

def grabColor():
  # get size of all images so they fit into the blank_image
  width = 0
  minh = float("inf")
  imgs = []

  #get size of images, crop them
  for x in cams:


    left = x['left']
    right = x['right']
    bottom = x['bottom']
    top = x['top']
    name = x['name']
    URL = x['url']

    file = cStringIO.StringIO(urllib.urlopen(URL).read())
    try:
      im = img.open(file)
      size = im.size
      im = im.crop((left,top,right,bottom))
      im = im.quantize(3).convert("RGB")
      print(im.getpixel((3,3)))

      im.save(str(name) + ".jpg")

      minh = min(minh,right - left)
      width += right - left
      imgs.append(im)
    except IOError:
      print "image down" + str(IOError)


    

  #put images in to one image
  i = 0
  blank_image = img.new("RGB", (width,200))
  for x in imgs:
    blank_image.paste(x,(i,0))
    i += x.size[0]

  blank_image.save("/home/pi/whatcoloristhesky/python/blank.jpg")

  #finally, get color of the sky
  blank_image = blank_image.quantize(1).convert("RGB")
  onecolor = blank_image.getpixel((3,3))
  #get name of closest color
  closest_name = get_colour_name(onecolor)
  hexCode = webcolors.rgb_to_hex(onecolor)


  sameColor = false

  for i in lastColor
    if str(closest_name)==lastColor:
      sameColor = true

  if sameColor == true:
    print "lastColor is the same " + str(closest_name)
  else:
    
    # Construct tweet
    tweet = "Looks like a " + str(closest_name) + " sky right now.\nhex: " + str(hexCode) + "\nrgb: " + str(onecolor) 
    # Create Color Square
    width = 1024
    height = 512
    colorSquare = img.new("RGB", (width,height))
    draw = imgDraw.Draw(colorSquare)
    draw.rectangle([0,0,width,height],fill=hexCode)
    del draw
    # to-do: don't save image
    colorSquare.save("/home/pi/whatcoloristhesky/python/color.jpg")
    # Tweet!
    print tweet
    didUpdate = True
    try:
      api.update_with_media("/home/pi/whatcoloristhesky/python/color.jpg", status=tweet)
    except Exception, e:
      didUpdate = False
      
    if didUpdate == True:
      lastColorFile = open("/home/pi/whatcoloristhesky/python/prevcolors.txt", "r+")
      colors = lastColorFile.read().split('\n')
      colors.append(str(closest_name))
      colors.remove(colors[0])
      skip = 0
      toAppend = ""
      for i in colors
        if skip == 0:
          print "skip"
        else:
          skip++
          toAppend += str(i)
          if skip != len(colors):
            toAppend += "\n"  
      lastColorFile.write(toAppend)

grabColor()

