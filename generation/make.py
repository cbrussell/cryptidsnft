from get_components import get_background, get_tails, get_legs

def main():
    tails = get_tails()
    print(tails)
    legs = get_legs()
    print(legs)
    background = get_background()
    print(background)
    # rightarms = get_rightarm()
    # spaces = get_space()
    # stars = get_stars()
    # cockpits = get_cockpit()
    # windows = get_windows()

    for (i, (tail, leg, background)) in enumerate(zip(tails, legs, background)):

        # Star is base

        background.paste(tail, mask=tail)

        background.paste(leg, mask=leg)

        # star.paste(window, mask=window)

        # star.paste(cockpit, mask=cockpit)

        # star.paste(leftarm, mask=leftarm)

        # star.paste(rightarm, mask=rightarm)

        # star.paste(leg, mask=leg)

        # star.paste(panel, mask=panel)

        background.save(f'output/output{i:03}.png')

    return



if __name__ == "__main__":
    main()
