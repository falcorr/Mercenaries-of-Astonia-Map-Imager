# Mercenaries of Astonia Map Imager
Creates an image of the entire minimap from the server's map and items files. Unless the map format has been heavily altered, will work with maps from post-v2 servers (e.g. Aranock).

Can toggle layers, ignore and override images, retrieve location info, and search item names and descriptions by word.

![Mercenaries of Astonia](https://i.imgur.com/NxkAlBq.png)

## Requires
- Python 3.6+ (tested with 3.8.5)
- [Pillow](https://pillow.readthedocs.io/) 8.0+ (tested with 8.1.0)

## Usage
`python MoA-map-imager.py [-map map.dat] [-items item.dat] [-location x,y]`

No arguments for console. Use arguments for automation. Supplying map and / or items arguments will save `map.png`

Expects data files in the same directory. Looks for image files in /png, /bmp, with a preference for png.

## Examples

`python MoA-map-imager.py -m newmap.dat`

`python MoA-map-imager.py -map map_copy.dat -items item_copy.dat`

`python MoA-map-imager.py -l 512,492`

`python MoA-map-imager.py` + 

`help`

`display map`

`display 1915`

`override 1915 255,0,255`

`override 1915`

`ignore`

`map map_copy.dat`

`location 512,492`

`location 434-554,528`

`location 493,-541`

`search red`

## Potential future

- draw characters
- draw carried items
- define mask colours (apart from alpha transparency, currently only recognises 255, 0, 255 and the peculiar, occasional 254, 0, 254)
- define map width and height (currently only v2's 1024x1024)
- define missing image colour (currently a pink 255, 0, 255)
- define start and stop points for map drawing
- descriptions of background and foreground images
- item whitelist
- define overrides for specific regions
- define length between tile, item, and character entries and various offsets in data files (for non-v2 formats)
- extended search
- cursor with coordinates over map display
- filter tiles and items by flags
- access packed images
- create copies of data files with only the minimum information utilised
- lots of optimisation
