from PIL import Image
import plotly.express as px
from os import path


def generate_images(character_name, images_dict):
    img1 = Image.open(f"assets/body/{character_name}/{images_dict['body']}.png")
    img2 = Image.open(f"assets/accessory/{images_dict['accessory']}.png")
    img3 = Image.open(f"assets/mouth/{images_dict['mouth']}.png")
    img4 = Image.open(f"assets/eye/{images_dict['eye']}.png")

    img1.paste(img2, mask=img2)
    img1.paste(img3, mask=img3)
    img1.paste(img4, mask=img4)

    return img1


def generate_image_fig(image):
    fig = px.imshow(image)
    fig.update_layout(plot_bgcolor='white',
                      paper_bgcolor='white',
                      margin=dict(t=0, b=0, l=0, r=0),
                      xaxis=dict(
                          showgrid=False,
                          showticklabels=False,
                          linewidth=0
                      ),
                      yaxis=dict(
                          showgrid=False,
                          showticklabels=False,
                          linewidth=0
                      ),
                      hovermode=False)
    return fig


def get_code_idx(number):
    if number < 4:
        return 0
    elif number < 7:
        return 1
    else:
        return 2


def get_image_figure_by_attributes(character_name, character_attributes, images_dict):
    if not images_dict:
        images_dict = {"body": "1_1_1_1", "eye": "1_1_1_1", "mouth": "1_1_1_1", "accessory": "1_1_1_1"}

    new_images_dict = {"body": "", "eye": "", "mouth": "", "accessory": ""}

    attribute_code = [str(get_code_idx(int(val))) for val in character_attributes.values()]
    attribute_code = "_".join(attribute_code)

    print(attribute_code)

    if path.exists(f"assets/body/{character_name}/{attribute_code}.png"):
        new_images_dict['body'] = attribute_code
    else:
        new_images_dict['body'] = images_dict['body']

    for attribute in ['eye', 'mouth', 'accessory']:
        if path.exists(f"assets/{attribute}/{attribute_code}.png"):
            new_images_dict[attribute] = attribute_code
        else:
            new_images_dict[attribute] = images_dict[attribute]

    image = generate_images(character_name, new_images_dict)
    fig = generate_image_fig(image)

    return fig, new_images_dict


def get_image_figure_by_image_dict(character_name, images_dict):
    character_name = character_name.lower()
    image = generate_images(character_name, images_dict)
    fig = generate_image_fig(image)

    return fig
