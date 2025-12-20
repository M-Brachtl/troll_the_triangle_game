def grid_from_image(filename):
    corrupt_pixels = []
    # get brightness of pixels (28x28)
    vzory = {
        (0,0,0): 0, # black - empty
        (255,255,255): 1, # white - wall
        (255,0,0): 2, # red - perma wall
        (0,255,0): 3, # green - spawn
        (0,0,255): 4, # blue - exit
        (255,255,0): 5, # yellow - entrance
        (0,255,255): 6, # cyan - loot
    }
    def get_color_code(image):
        color_codes = []
        for y in range(28):
            for x in range(28):
                r, g, b = image.getpixel((x, y))
                color_codes.append((r, g, b))
                if (r, g, b) not in vzory.keys():
                    corrupt_pixels.append((x, y, (r, g, b)))
        if corrupt_pixels:
            raise ValueError(f"Corrupt pixels found in level image '{filename}': {corrupt_pixels}")
        return color_codes
    # Example usage with PIL
    from PIL import Image
    image = Image.open(filename)
    color_codes = get_color_code(image)
    color_codes = [vzory[color] for color in color_codes]
    reshaped_values = [color_codes[i:i+28] for i in range(0, len(color_codes), 28)]
    return reshaped_values

if __name__ == "__main__":
    filename = "levels/test2.lvl.png"
    grid = grid_from_image(filename)
    for row in grid:
        print(row)