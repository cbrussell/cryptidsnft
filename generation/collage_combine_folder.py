import os
from PIL import Image
import fnmatch
from pathlib import Path
from matplotlib import image, scale 
from prime_factor import gridSize


def main():
    dir_path = os.path.dirname(os.path.realpath(__file__))

    still_path = Path(__file__).resolve().parents[1] / "generation/output/stills/"

    still_list = fnmatch.filter(os.listdir(still_path), '*.png')


    still_count = len(still_list)

    grid = [] #[x,y]

    print(grid)

    grid = gridSize(still_count)

    print(grid)

    image = Image.open(f"{dir_path}/output/stills/1.png")

    width, height = image.size

    frame = Image.new('RGB', (width*grid[0], height*grid[1]))# random solid

    frame_count = 1
    for x in range(grid[0]):
        for y in range(grid[1]):
            still = Image.open(f"{dir_path}/output/stills/{frame_count}.png")
            frame.paste(still, box=(height * x, height * y))
            print(f"Pasted frame #{frame_count}! Only {still_count - frame_count} more frames left to go!")
            frame_count += 1

    # ***************     scale      ***************     

    basewidth = 7500
    resize_scale = float(basewidth)/float(width*grid[0])
    frame = frame.resize((basewidth, int(float(height*grid[1]) * resize_scale)))

    # ***************     scale      ***************

    print("Saving collage...")
    frame.save(f"{dir_path}/output/collage_still/full_collage_{grid[0]}_x_{grid[1]}.png", format="png")  
    print(f'Completed Collage!')

if __name__ == "__main__":
    main()
