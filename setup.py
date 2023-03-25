import yaml
from PIL import Image, ImageTk
import tkinter as tk


def load_yaml(name, *, config=None):
    with open(f"assets/{name}/{config}.yaml") as fin:
        try:
            module_config = yaml.safe_load(fin)
            return module_config
        except yaml.YAMLError as exc:
            raise exc


def generate_modules(name, *, config=None):
    if config is None:
        config = 'config'

    module_config = load_yaml(name, config=config)

    tile_w = module_config["tile"]["width"]
    tile_h = module_config["tile"]["height"]

    module_list = []
    with Image.open(f"assets/{name}/tiles.png") as image:
        for module_name, module_info in module_config["modules"].items():
            r, c = module_info["imageCoords"]
            box = ((c-1)*tile_w, (r-1)*tile_h, c*tile_w, r*tile_h)
            tile_image = image.crop(box)

            for rotation in module_info["rotations"] + [0]:
                m = dict()
                m["name"] = f"{module_name}_{rotation}"
                m["image"] = tile_image.rotate(rotation)
                m["connections"] = dict()
                for base, rotated in rotation_map[rotation].items():
                    m["connections"][rotated] = module_info["connections"][base]

                module_list.append(m)

    return module_list, tile_w, tile_h


def display_grid(grid, module_list, tile_w, tile_h):
    # Create a Tkinter window and canvas
    shape = grid.shape

    root = tk.Tk()
    canvas = tk.Canvas(root, width=shape[1] * tile_w, height=(shape[0] + 3) * tile_h)
    canvas.pack()

    images = []
    for r in range(shape[0]):
        for c in range(shape[1]):
            if grid[r, c] < 0:
                continue
            image = module_list[grid[r, c]]["image"]
            image_tk = ImageTk.PhotoImage(image)
            images.append(image_tk)
            canvas.create_image(tile_w * c, tile_h * r, image=images[-1], anchor='nw')

    for i, module in enumerate(module_list):
        image = module_list[i]["image"]
        image_tk = ImageTk.PhotoImage(image)
        images.append(image_tk)
        canvas.create_image(tile_w * i, tile_h * (r + 2), image=images[-1], anchor='nw')

    # Start the Tkinter event loop
    root.mainloop()



# key = base module, value = rotated module
rotation_map = {
    0: {
        "t": "t",
        "b": "b",
        "l": "l",
        "r": "r"
    },
    90: {
        "t": "l",
        "b": "r",
        "l": "b",
        "r": "t"
    },
    180: {
        "t": "b",
        "b": "t",
        "l": "r",
        "r": "l"
    },
    270: {
        "t": "r",
        "b": "l",
        "l": "t",
        "r": "b"
    }
}