import dash_bootstrap_components as dbc
from dash import Dash, html, dcc, Input, Output, State
import dash_daq as daq
import image_generation

app = Dash(external_stylesheets=[dbc.themes.FLATLY], title='Senti-tamagotchi')

character_card = html.Div(dbc.Card([
    dbc.CardHeader(html.H4("Character", className='m-0 fw-bold text-center text-primary'),
                   class_name='py-3'),
    dbc.CardBody([dcc.Graph(figure=image_generation.get_image_figure(),
                            id='character_image',
                            config={'staticPlot': True}
                            ),
                  dbc.Select(options=['Dominik'], value='Dominik', id='character_name')], style={'height': '550px'})
]), className='my-2 shadow')

# Angry or Pleased,  Board or Excited, Sick or Healthy, Scary or Relaxed
angry_gauge = daq.Gauge(id='angry_pleased', label="Angry vs Pleased", value=5)
board_gauge = daq.Gauge(id='board_excited', label="Board vs Excited", value=5)
sick_gauge = daq.Gauge(id='sick_healthy', label="Sick vs Healthy", value=5)
scary_gauge = daq.Gauge(id='scary_relaxed', label="Scary vs Relaxed", value=5)

attributes_card = html.Div(dbc.Card([
    dbc.CardHeader(html.H4("Attributes", className='m-0 fw-bold text-center text-primary'), class_name='py-3'),
    dbc.CardBody(dbc.Container([dbc.Row([dbc.Col(angry_gauge), dbc.Col(board_gauge)]),
                                dbc.Row([dbc.Col(sick_gauge), dbc.Col(scary_gauge)])]), style={'height': '550px'}),
    dcc.Store(id='attributes')
]), className='my-2 shadow')

app.layout = dbc.Container([
    dbc.Row([dbc.Col(character_card, lg=4, md=12),
             dbc.Col(attributes_card, lg=8, md=12)], class_name='g-3 mb-4 px-3'),
    dbc.Row("Question & Answer", class_name='g-3 mb-4 px-3'),
    dbc.Row([dbc.Col("Collections", lg=8, md=12), dbc.Col("Generation", lg=4, md=12)], class_name='g-3 mb-4 px-3')
], style={"overflow-x": "hidden", "min-height": "100vh"}, class_name='bg-light')

if __name__ == "__main__":
    app.run(debug=True)
