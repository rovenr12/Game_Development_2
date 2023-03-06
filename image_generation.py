from PIL import Image
import plotly.express as px
from os import path


def get_image_figure(character_name, character_attributes, images_dict):
    if not images_dict:
        images_dict = {"body": "5_5_5_5", "eye": "5_5_5_5", "mouth": "5_5_5_5", "accessory": "5_5_5_5"}

    images = {"body": "", "eye": "", "mouth": "", "accessory": ""}

    attribute_code = [str(int(val)) for val in character_attributes.values()]
    attribute_code = "_".join(attribute_code)

    if path.exists(f"assets/body/{character_name}/{attribute_code}.png"):
        images['body'] = attribute_code
    else:
        images['body'] = images_dict['body']

    for attribute in ['eye', 'mouth', 'accessory']:
        if path.exists(f"assets/{attribute}/{attribute_code}.png"):
            images[attribute] = attribute_code
        else:
            images[attribute] = images_dict[attribute]

    img1 = Image.open(f"assets/body/{character_name}/{images['body']}.png")
    img2 = Image.open(f"assets/accessory/{images['accessory']}.png")
    img3 = Image.open(f"assets/mouth/{images['mouth']}.png")
    img4 = Image.open(f"assets/eye/{images['eye']}.png")

    img1.paste(img2, mask=img2)
    img1.paste(img3, mask=img3)
    img1.paste(img4, mask=img4)

    fig = px.imshow(img1)
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

    return fig, images
