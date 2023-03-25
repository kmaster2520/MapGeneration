import yaml
from PIL import Image


def generate_modules(name, *, config=None):
    if config is None:
        config = 'config'

    with open(f"assets/{name}/{config}.yaml") as fin:
        try:
            module_config = yaml.safe_load(fin)
        except yaml.YAMLError as exc:
            raise exc

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

    return module_list


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
        "t": "b",
        "b": "t",
        "l": "r",
        "r": "l"
    }
}