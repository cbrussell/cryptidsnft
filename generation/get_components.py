from PIL import Image
import os

dir_path = os.path.dirname(os.path.realpath(__file__))

def get_tails():
    images = []
    for i in range(1, 73):
        f = Image.open(f'{dir_path}/RENDERS/1_Tails/Brush/Tails_Brush_RED_{i:03}.png') #.convert('RGBA')
        images.append(f)
    return images

def get_legs():
    images = []
    for i in range(1, 73):
        f = Image.open(f'{dir_path}/RENDERS/2_LeftBackLeg/Eagle/leftBackLeg_Eagle_RED_{i:03}.png') #.convert('RGBA')
        images.append(f)
    return images

def get_background():
    images = []
    for i in range(1, 73):
        f = Image.open(f'{dir_path}/RENDERS/0_Background/Background_White.png') #.convert('RGBA')
        images.append(f)
    return images

if __name__ == "__main__":
   get_tails()
   get_legs()
   get_background()