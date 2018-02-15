import os
import glob
from PIL import Image

print("Building File List")
imagelist = glob.glob("*.jpg")
imagelist.extend(glob.glob("*.png"))
imagelist.extend(glob.glob("*.gif"))


def thum(infile):

  print(infile)

  im = Image.open(infile).convert('RGB')

  # convert to thumbnail image
  im.thumbnail((300, 300), Image.ANTIALIAS)

  # prefix thumbnail file with T_
  im.save("T_" + infile, "JPEG")
  print("Thumb saved")

  # delete converted file
  os.remove(infile)
  print("File Zapped!")

# get all the jpg files from the current folder
for infile in imagelist:

  # open RGB
  if infile.find("T_") < 0:
    thum(infile)
