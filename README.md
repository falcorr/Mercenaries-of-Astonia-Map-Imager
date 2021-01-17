# Mercenaries of Astonia Map Imager
Creates a minimap image from the server's map file. Unless the map format has been heavily altered, will work with maps from post-v2 servers. 

## Requires
- Python 3
- Pillow

## Usage
`MoAmapimager [filename.dat]`

Expects map.dat in the same directory. Looks for image files in /png, /bmp, with a preference for png. 

Can define images to be ignored or have their colours overridden.

## Future

- Add missing map features
- Specify layers to draw
- Specify mask colours
