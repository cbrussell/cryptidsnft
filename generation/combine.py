import os
import numpy as np
from datetime import datetime
from numpy.core.multiarray import array
from PIL import Image, ImageFont, ImageDraw
from background import get_gradient, get_gradient_3d
from dna import Frames
from time import sleep

def combine_attributes(frames: Frames, prefix: str):
    # random frame color backhround
    # R = random.randint(0,255)
    # G = random.randint(0,255)
    # B = random.randint(0,255)
    R = np.random.randint(0, 256)
    G = np.random.randint(0, 256)
    B = np.random.randint(0, 256)

    R1 = np.random.randint(0, 256)
    G1 = np.random.randint(0, 256)
    B1 = np.random.randint(0, 256)
    
    array = get_gradient_3d(1100, 1100, (R1, G1, B1), (R, G, B), (True, False, False))
    # array = get_gradient()

    dir_path = os.path.dirname(os.path.realpath(__file__))
    # use this for metadatabackground
    # for (n, background) in enumerate(frames.background_frames):
    # print("Generating frames...")

    for n in range(0,1): #0,72

        # use this is background color
        # frame = Image.open(background) # background of data

        # frame = Image.new('RGB', (1100, 1100), (R, G, B)) # random solid
    
        # 4 way gradient
        # frame = Image.fromarray(np.uint8(array))

        frame = Image.open(frames.background_frame[0])

        # frame = Image.new('RGB', (1100, 1100), (255, 255, 255)) # white bg

        if frames.tail_frames:
            print(frames.tail_frames[n])
            tail = Image.open(frames.tail_frames[n])
            frame.paste(tail, mask=tail)

        if frames.leftbackleg_frames:
            leftbackleg = Image.open(frames.leftbackleg_frames[n])
            frame.paste(leftbackleg, mask=leftbackleg)

        if frames.leftfrontleg_frames[n]:
            leftfrontleg = Image.open(frames.leftfrontleg_frames[n])
            frame.paste(leftfrontleg, mask=leftfrontleg)

        if frames.back_frames:
            back = Image.open(frames.back_frames[n])
            frame.paste(back, mask=back)
       
        if frames.torsobase_frames:
            torsobase = Image.open(frames.torsobase_frames[n])
            frame.paste(torsobase, mask=torsobase)

        if frames.torsoaccent_frames:
            torsoaccent = Image.open(frames.torsoaccent_frames[n])
            frame.paste(torsoaccent, mask=torsoaccent)

        if frames.torsopattern_frames:
            torsopattern = Image.open(frames.torsopattern_frames[n])
            frame.paste(torsopattern, mask=torsopattern)

        if frames.neckbase_frames:
            neckbase = Image.open(frames.neckbase_frames[n])
            frame.paste(neckbase, mask=neckbase)
        
        if frames.neckaccent_frames:
            neckaccent = Image.open(frames.neckaccent_frames[n])
            frame.paste(neckaccent, mask=neckaccent)

        if frames.neckpattern_frames:
            neckpattern = Image.open(frames.neckpattern_frames[n])
            frame.paste(neckpattern, mask=neckpattern)
        
        if frames.neckshadow_frames:
            neckshadow = Image.open(frames.neckshadow_frames[n])
            frame.paste(neckshadow, mask=neckshadow)

        if frames.fur_frames:
            fur = Image.open(frames.fur_frames[n])
            frame.paste(fur, mask=fur)

        if frames.rightbackleg_frames:
            rightbackleg = Image.open(frames.rightbackleg_frames[n])
            frame.paste(rightbackleg, mask=rightbackleg)
        
        if frames.rightfrontleg_frames:
            rightfrontleg = Image.open(frames.rightfrontleg_frames[n])
            frame.paste(rightfrontleg, mask=rightfrontleg)

        if frames.ears_frames:
            ears = Image.open(frames.ears_frames[n])
            frame.paste(ears, mask=ears)

        if frames.headbase_frames:
            headbase = Image.open(frames.headbase_frames[n])
            frame.paste(headbase, mask=headbase)
        
        if frames.headaccent_frames:
            headaccent = Image.open(frames.headaccent_frames[n])
            frame.paste(headaccent, mask=headaccent)

        if frames.headpattern_frames:
            headpattern = Image.open(frames.headpattern_frames[n])
            frame.paste(headpattern, mask=headpattern)

        if frames.mouth_frames:
            mouth = Image.open(frames.mouth_frames[n])
            frame.paste(mouth, mask=mouth)

        if frames.horns_frames:
            horns = Image.open(frames.horns_frames[n])
            frame.paste(horns, mask=horns)
        
        if frames.eyes_frames:
            eyes = Image.open(frames.eyes_frames[n])
            frame.paste(eyes, mask=eyes)

        print("Almost there...")

        # watermark settings
        # find texts with "find {/System,}/Library/Fonts -name *ttf"
        ######

        # Width, Height = frame.size 
        # drawn = ImageDraw.Draw(frame) 
        # text = "test mint"
        # font = ImageFont.truetype("Arial Black", 138)
        # textwidth, textheight = drawn.textsize(text, font)
        # margin = 5
        # x = Width - textwidth
        # y = Height - textheight
        # drawn.text(((x/2), (y/2)), text, font=font) 

        #####


        frame.save(f"{dir_path}/output/raw/{prefix}/{prefix}_{n:03}.png")

        if n == 0:
        #     time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            frame.save(f"{dir_path}/output/stills/{prefix}.png")
        #     frame = Image.fromarray(np.uint8(array)).save(f"{dir_path}/output/bg/{prefix}_bg_{time}_{R1}_{G1}_{B1}_{R}_{G}_{G}.png", "PNG")

    