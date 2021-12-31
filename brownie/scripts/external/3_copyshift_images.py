from collections import deque
import os
from pathlib import Path 
import fnmatch
import shutil

# Renames image directory based on community generated shift-value
shift_amount = 229183

# Determine image paths
image_path = Path(__file__).resolve().parents[2] / "assets/images/"
new_path = Path(__file__).resolve().parents[2] / "assets/shifted_images/"

print(image_path)

# Make list of images
image_list = fnmatch.filter(os.listdir(image_path), '*.png')

# Size of image list
image_count = len(image_list)

# Sort image list
image_list = sorted(image_list, key=lambda x: int(os.path.splitext(x)[0]))

# Rotate list using deque
test_list = deque(image_list)
test_list.rotate(shift_amount)
shifted_list = list(test_list)

# Output
print(f"\nOriginal list is: {image_list}\n")
print(f"\nShifted list is: {shifted_list}\n")

# Replace original files for new name (changing folders)
for i in range(image_count):


    new_name = Path(new_path / shifted_list[i]) #file
    original_name = Path(image_path / image_list[i]) #location

    shutil.copy(original_name, new_name)
    
    # original_name.rename(new_name)

