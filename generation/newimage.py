from PIL import Image

def newImg():
    
    img = Image.new('RGB', (1100, 1100), (255, 100, 25))
    # img.putpixel((30,60), (155,155,55))
    img.save('sqr.png')

    return img

wallpaper = newImg()
wallpaper.show()