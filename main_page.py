import random

import dash_bootstrap_components as dbc
from dash import Dash, html, dcc, Input, Output, State
import dash_daq as daq
import image_generation

app = Dash(external_stylesheets=[dbc.themes.FLATLY], title='Senti-tamagotchi')

####################################
# Character Panel
####################################
character_card = html.Div(dbc.Card([
    dbc.CardHeader(html.H4("Character", className='m-0 fw-bold text-center text-primary'),
                   class_name='py-3'),
    dbc.CardBody([dcc.Graph(id='character_image',
                            config={'staticPlot': True}
                            ),
                  dbc.Select(options=['Dominik', 'Peyman', 'Judy', 'Nirit'], value='Dominik', id='character_name')],
                 style={'height': '570px'}),
    dcc.Store("images_dict")
]), className='my-2 shadow')

####################################
# Attribute Panel
####################################
angry_gauge = daq.Gauge(id='angry_pleased', label="Angry vs Pleased", value=5)
board_gauge = daq.Gauge(id='board_excited', label="Board vs Excited", value=5)
sick_gauge = daq.Gauge(id='sick_healthy', label="Sick vs Healthy", value=5)
scary_gauge = daq.Gauge(id='scary_relaxed', label="Scary vs Relaxed", value=5)

attributes_card = html.Div(dbc.Card([
    dbc.CardHeader(html.H4("Attributes", className='m-0 fw-bold text-center text-primary'), class_name='py-3'),
    dbc.CardBody(dbc.Container([dbc.Row([dbc.Col(angry_gauge), dbc.Col(board_gauge)]),
                                dbc.Row([dbc.Col(sick_gauge), dbc.Col(scary_gauge)])]),
                 style={'height': '570px', 'overflow-y': 'auto'}),
    dcc.Store(data={"angry_pleased": 5, 'board_excited': 5, 'sick_healthy': 5, 'scary_relaxed': 5}, id='attributes')
]), className='my-2 shadow')

####################################
# Question & Answer Panel
####################################
question_character = html.Span("Character: ", className='m-0 fw-bold text-primary fs-3', id='question_character')
question_span = html.Span("question", className='m-0 text-primary fs-3', id='question')

question_div = html.Div([question_character, question_span], className='text-center')

prompt = html.Div(
    [dbc.Textarea(className="mb-3", placeholder="Your answer", rows=5, size='lg', style={"resize": "none"},
                  id='prompt'),
     dbc.Button("Send", size="lg", class_name='d-grid col-6 mx-auto', id='prompt_button')])

question_answer_card = html.Div(dbc.Card([
    dbc.CardBody(dbc.Container([dbc.Row(question_div, class_name='h-50 align-items-center'),
                                dbc.Row(html.Hr()),
                                dbc.Row(prompt, class_name='h-50')], class_name='h-100'),
                 style={'height': '550px'}, ),
    dcc.Store(id='question_parameters')
]), className='my-2 shadow')

####################################
# Collections_Panel
####################################
collections_card = html.Div(dbc.Card([
    dbc.CardHeader(html.H4("Collections", className='m-0 fw-bold text-center text-primary'), class_name='py-3'),
    dbc.CardBody([dbc.Tabs([dbc.Tab(label='All', tab_id='all'),
                            dbc.Tab(label='Body', tab_id='body'),
                            dbc.Tab(label='Eye', tab_id='eye'),
                            dbc.Tab(label='Mouth', tab_id='mouth'),
                            dbc.Tab(label='Accessory', tab_id='accessory')], id='collection_tabs', active_tab='all'),
                  html.Div(id='collection_div')],
                 style={'height': '700px', 'overflow-y': 'auto'}),
    dcc.Store(data={"body": [], "eye": [], "mouth": [], "accessory": []}, id='collections')
]), className='my-2 shadow')

####################################
# Customisation
####################################
customisation_card = html.Div(dbc.Card([
    dbc.CardHeader(html.H4("Customisation", className='m-0 fw-bold text-center text-primary'), class_name='py-3'),
    dbc.CardBody([dcc.Graph(id='customised_image', config={'staticPlot': True}),
                  dbc.Label("Body"), dcc.Slider(min=0, max=0, value=0, id='custom_body'),
                  dbc.Label("Eye"), dcc.Slider(min=0, max=0, value=0, id='custom_eye'),
                  dbc.Label("Mouth"), dcc.Slider(min=0, max=0, value=0, id='custom_mouth'),
                  dbc.Label("Accessory"), dcc.Slider(min=0, max=0, value=0, id='custom_accessory')],
                 style={'height': '700px', 'overflow-y': 'auto'}),
]), className='my-2 shadow')

app.layout = dbc.Container([
    dbc.Row([dbc.Col(character_card, lg=4, md=12),
             dbc.Col(attributes_card, lg=8, md=12)], class_name='g-3 mb-4 px-3'),
    dbc.Row(question_answer_card, class_name='g-3 mb-4 px-3'),
    dbc.Row([dbc.Col(collections_card, lg=8, md=12), dbc.Col(customisation_card, lg=4, md=12)],
            class_name='g-3 mb-4 px-3')
], style={"overflow-x": "hidden", "min-height": "100vh"}, class_name='bg-light')


@app.callback(
    Output("question_character", "children"),
    Output("question", "children"),
    Output("question_parameters", "data"),
    Input("attributes", "data"),
    Input("character_name", "value")
)
def get_new_question(attributes, character_name):
    return f"{character_name}: ", f"new_question {random.random()}", {"angry_pleased": 0.5, 'board_excited': 0.1,
                                                                      'sick_healthy': -0.4,
                                                                      'scary_relaxed': 0.2}


@app.callback(
    Output("attributes", "data"),
    Input("prompt_button", "n_clicks"),
    State("prompt", "value"),
    State("question_parameters", "data"),
    State("attributes", "data")
)
def update_attributes(n, text, weights, attributes):
    if not n:
        return attributes

    score = 0.8
    for attribute, value in attributes.items():
        attributes[attribute] += weights[attribute] * score

    return attributes


@app.callback(
    Output("angry_pleased", "value"),
    Output("board_excited", "value"),
    Output("sick_healthy", "value"),
    Output("scary_relaxed", "value"),
    Input("attributes", "data")
)
def update_gauges(attributes):
    return attributes["angry_pleased"], attributes["board_excited"], attributes["sick_healthy"], attributes[
        "scary_relaxed"]


@app.callback(
    Output("character_image", "figure"),
    Output("images_dict", "data"),
    Input("attributes", "data"),
    Input("character_name", "value"),
    State("images_dict", "data")
)
def update_image(attributes, character_name, image_dict):
    fig, new_images_dict = image_generation.get_image_figure(character_name.lower(), attributes, image_dict)
    return fig, new_images_dict


@app.callback(
    Output("collections", "data"),
    Input("images_dict", "data"),
    State("collections", "data")
)
def update_collections(images_dict, collections):
    for collection, data in collections.items():
        if images_dict[collection] not in data:
            collections[collection].append(images_dict[collection])
    return collections


@app.callback(
    Output("collection_div", "children"),
    Input("collection_tabs", "active_tab"),
    Input("collections", "data"),
    Input("character_name", "value")
)
def update_collections(at, collections, character_name):
    images = []

    if at == 'all' or at == 'body':
        images_list = collections['body']
        for image in images_list:
            images.append(dbc.Col(html.Img(src=f'assets/body/{character_name.lower()}/{image}.png',
                                           style={'width': '128px', 'height': '128px'}), className="m-2"))

    for attribute in ['eye', 'mouth', 'accessory']:
        if at == 'all' or at == attribute:
            images_list = collections[attribute]
            for image in images_list:
                images.append(dbc.Col(html.Img(src=f'assets/{attribute}/{image}.png',
                                               style={'width': '128px', 'height': '128px'}), className="m-2"))

    return dbc.Row(images, class_name='row-cols-auto g-1')


if __name__ == "__main__":
    app.run(debug=True)
