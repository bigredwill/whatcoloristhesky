from PIL import Image as img
from PIL import ImageDraw as imgDraw
import urllib, cStringIO, yaml, tweepy, time, sys


secrets = open("secrets.yaml")
secrets = yaml.load(secrets.read())
#enter the corresponding information from your Twitter application:
CONSUMER_KEY = secrets['consumer_key']
CONSUMER_SECRET = secrets['consumer_secret']
ACCESS_KEY = secrets['access_key']
ACCESS_SECRET = secrets['access_secret']
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)


camlist = open("camlist.yaml")

cams = yaml.load(camlist.read())



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
    im = img.open(file)

    size = im.size
    im = im.crop((left,top,right,bottom))
    im = im.quantize(1).convert("RGB")
    print(im.getpixel((3,3)))

    minh = min(minh,right - left)
    width += right - left
    imgs.append(im)

  #put images in to one image
  i = 0
  blank_image = img.new("RGB", (width,200))
  for x in imgs:
    blank_image.paste(x,(i,0))
    i += x.size[0]

  blank_image.save("blank.jpg")

  #finally, get color of the sky
  blank_image = blank_image.quantize(1).convert("RGB")
  color = "rgb"+ str(blank_image.getpixel((3,3)))

  # Construct tweet
  tweet = "The color of the sky in San Jose right now is " + color
  # Create Color Square
  blank_image = img.new("RGB", (400,400))
  colorSquare = img.new("RGB", (400,400))
  draw = imgDraw.Draw(colorSquare)
  draw.rectangle([0,0,401,401],fill=color)
  del draw
  # to-do: don't save image
  colorSquare.save("color.jpg")
  # Tweet!
  api.update_with_media("color.jpg", status=tweet)

grabColor()

