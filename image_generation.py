from PIL import Image
import plotly.express as px


def get_image_figure():
    img1 = Image.open("assets/test_tamagotchi_0003_Layer-5.png")
    img2 = Image.open("assets/test_tamagotchi_0000_Layer-7.png")
    img3 = Image.open("assets/test_tamagotchi_0001_Layer-4.png")
    img4 = Image.open("assets/test_tamagotchi_0002_Layer-6.png")

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

    return fig
