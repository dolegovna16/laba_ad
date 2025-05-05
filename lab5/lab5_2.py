import dash
from dash import dcc, html, Input, Output, State
import numpy as np
from scipy.signal import butter, filtfilt
import plotly.graph_objs as go

t = np.linspace(0, 1, 500)
fs = 500
noise_data = np.zeros_like(t)
noise_generated = False

def smart_rangeslider(id, min_val, max_val, step, value):
    return html.Div([
        html.Label(id),
        dcc.RangeSlider(
            id=id,
            min=min_val,
            max=max_val,
            step=step,
            value=value,
            marks={
                str(min_val): str(min_val),
                str(max_val): str(max_val)
            },
            tooltip={"placement": "top", "always_visible": True}
        )
    ])

def smart_slider(id, min_val, max_val, step, value):
    return html.Div([
        html.Label(id),
        dcc.Slider(
            id=id,
            min=min_val,
            max=max_val,
            step=step,
            value=value,
            marks={
                str(min_val): str(min_val),
                str(max_val): str(max_val)
            },
            tooltip={"placement": "top", "always_visible": True}
        )
    ])

app = dash.Dash(__name__)
app.title = "lab 5"

app.layout = html.Div([
    dcc.Graph(id='signal-graph'),

    html.Div([
        smart_slider('amp', 0.1, 5, 0.1, 1.0),
        smart_slider('freq', 1, 10, 0.1, 3),
        smart_slider('phase', 0, 2*np.pi, 0.1, 0),

        smart_slider('noise-mean', -2, 2, 0.1, 0),
        smart_slider('noise-cov', 0, 1, 0.01, 0.2),

        smart_rangeslider('cutoff', 1, 50, 0.5, [5, 30]),

        html.Br(),
        dcc.Checklist(
            options=[
                {'label': ' Show Noise', 'value': 'noise'},
                {'label': ' Show Filter', 'value': 'filter'}
            ],
            value=['noise', 'filter'],
            id='options',
            labelStyle={'display': 'block'}
        ),
        html.Br(),
        html.Button('Reset Noise', id='reset-noise', n_clicks=0)
    ], style={'width': '40%', 'display': 'inline-block', 'verticalAlign': 'top'})
], style={'padding': '30px'})


@app.callback(
    Output('signal-graph', 'figure'),
    Input('amp', 'value'),
    Input('freq', 'value'),
    Input('phase', 'value'),
    Input('noise-mean', 'value'),
    Input('noise-cov', 'value'),
    Input('cutoff', 'value'),
    Input('options', 'value'),
    Input('reset-noise', 'n_clicks'),
    prevent_initial_call=False
)
def update_graph(A, f, phi, noise_mean, noise_cov, cutoff_range, options, reset_clicks):
    global noise_data, noise_generated, t

    y = A * np.sin(2 * np.pi * f * t + phi)

    ctx = dash.callback_context #Він містить інформацію хто викликав функцію які Input змінилися
    #воно містить рядки а-ля amp.value, тому знизу витягаємо лише id елемента
    triggered_props = [trg['prop_id'].split('.')[0] for trg in ctx.triggered] if ctx.triggered else []

    if (not noise_generated or 'reset-noise' in triggered_props or
            'noise-mean' in triggered_props or 'noise-cov' in triggered_props):
        noise_data = np.random.normal(noise_mean, noise_cov, size=t.shape)
        noise_generated = True

    y_noise = y + noise_data

    # Band-pass фільтрація
    low, high = cutoff_range
    b, a = butter(N=4, Wn=[low / (fs / 2), high / (fs / 2)], btype='band')
    y_filtered = filtfilt(b, a, y_noise)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=t, y=y, mode='lines', name='Signal', line=dict(dash='dash', color='blue')))
    if 'noise' in options:
        fig.add_trace(go.Scatter(x=t, y=y_noise, mode='lines', name='Signal + Noise', line=dict(color='pink')))
    if 'filter' in options:
        fig.add_trace(go.Scatter(x=t, y=y_filtered, mode='lines', name='Filtered (Band)', line=dict(color='purple')))

    fig.update_layout(title="Signal With Filtering", height=500, margin=dict(l=50, r=10, t=40, b=40))
    return fig


if __name__ == '__main__':
    app.run(debug=True)
