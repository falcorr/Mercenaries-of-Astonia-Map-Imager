#! /usr/bin/python
# Mercenaries of Astonia map imager by Makadon

import os
import sys
import re
try:
    from PIL import Image
except:
    try:
        from pillow import Image
    except:
        try:
            import Image
        except:
            print("Failed:")
            print("from PIL import Image")
            print("from pillow import Image")
            print("import Image")

MAP_WIDTH = 1024
MAP_HEIGHT = 1024

# Colour for missing image files
missingColour = (255, 0, 255)

imageColourOverrides = { "99999": (255, 255, 255) }
imageColourIgnore = []
imageColourCache = {}

tiles = {}
tileCounter = 0
hexCounter = 0

print("\nMercenaries of Astonia map imager")
print("by Makadon\n")

mapFile = "map.dat"
if len(sys.argv) == 2:
    try:
        if sys.argv[1][-4:] == ".dat":
            mapFile = sys.argv[1]
    except:
        print("Invalid map filename")

print("Loading map file ", end='')
sys.stdout.flush()
with open(os.getcwd() + '/' + mapFile, "rb") as file:    
    hexData = file.read().hex().lower()
sys.stdout.flush()
print("[100%]")

# Calibrate tile data length (assumes first two tiles are the same)
portion = ""
tileLength = None
for h in hexData[8:]:
    portion += str(h)
    if portion[-8:] == hexData[:8]:
        tileLength = len(portion)
        break

def getImageColour(mapHex):
    imageNumber = str(int(mapHex[2:] + mapHex[:2], 16)).zfill(5)
    
    # Ignore blank
    if imageNumber == "00000":
        return None
    # Check ignores
    if imageNumber.lstrip("0") in imageColourIgnore or imageNumber in imageColourIgnore:
        return None
    # Check overrides
    for key, value in imageColourOverrides.items():
        if key == imageNumber.lstrip("0") or key == imageNumber:
            return value
    # Check cache
    for key, value in imageColourCache.items():
        if key == imageNumber:
            return value
    
    try:
        image = Image.open(os.getcwd() + "/png/" + imageNumber + ".png")
    except:
        try:
            image = Image.open(os.getcwd() + "/bmp/" + imageNumber + ".bmp")
        except:
            return None
    
    pixels = list(image.getdata())
    averageRed = 0
    averageGreen = 0
    averageBlue = 0
    pixelCount = 0
    if image.mode == "RGBA":
        imageDimensions = image.size[0] * image.size[1]
        for channels in pixels:
            if channels[3] != 0:
                averageRed += channel[0]
                averageGreen += channel[1]
                averageBlue += channel[2]
                pixelCount += 1
        percentageTransparent = 100 / (imageDimensions / pixelCount)
        if percentageTransparent < 10:
            image.convert("RGB")
    if image.mode == "RGB":
        for channels in pixels:
            if channels != (255, 0, 255) and channels != (254, 0, 254): # pink mask
                averageRed += channels[0]
                averageGreen += channels[1]
                averageBlue += channels[2]
                pixelCount += 1
    
    imageColour = (int(averageRed / pixelCount), int(averageGreen / pixelCount), int(averageBlue / pixelCount))    
    imageColourCache[imageNumber] = imageColour
    
    return imageColour

print("Reading map file [0%]\r", end='')
sys.stdout.flush()
for h in hexData:
    try:
        tiles[tileCounter] = tiles[tileCounter] + str(h)
    except:
        tiles[tileCounter] = ""
        tiles[tileCounter] = tiles[tileCounter] + str(h)
        
    hexCounter += 1
    
    if hexCounter == tileLength:
        tileCounter += 1
        hexCounter = 0
    if tileCounter % MAP_WIDTH == 0:
        print("Reading map file [{0}%]\r".format(int(tileCounter / (MAP_WIDTH * MAP_HEIGHT) * 100)), end='')
        sys.stdout.flush()

print("\nDetermining colours [0%]\r", end='')
sys.stdout.flush()
surface = Image.new('RGB', (MAP_WIDTH, MAP_HEIGHT), 0x000000)
x = 0
y = 0
haveColourRecord = False
for key, value in tiles.items():
    sprite = value[:8]
    background = sprite[:4]
    sprite = sprite[4:]
    
    # floor tiles
    colour = getImageColour(background)
    if colour:
        surface.putpixel((y, x % MAP_WIDTH), colour)
    else:
        surface.putpixel((y, x % MAP_WIDTH), missingColour)
    # sprites
    colour = getImageColour(sprite)
    if colour:
        surface.putpixel((y, x % MAP_WIDTH), colour)
    
    x += 1
    if x % MAP_WIDTH == 0:
        y += 1
        print("Determining colours [{0}%]\r".format(int(y / MAP_WIDTH * 100)), end='')
        sys.stdout.flush()

#surface.show()
surface.save("map.png")
print("\nSaved map.png")
