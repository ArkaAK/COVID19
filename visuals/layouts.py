import plotly.graph_objects as go
import base64

with open("data/india.png", "rb") as image_file:
    encoded_string = base64.b64encode(image_file.read()).decode()
    #add the prefix that plotly will want when using the string as source
    encoded_image = "data:image/png;base64," + encoded_string

    map_layout = dict( autosize=False,
                      margin={"r": 0, "t": 0, "l": 0, "b": 0},
                      height=560, width=595,
                      paper_bgcolor="rgb(247, 247, 245)",

                      images = [dict(
                          source= encoded_image,
                          xref= "x",
                          yref= "y",
                          x=-1,
                          y= 4,
                          sizex= 7,
                          sizey= 7,
                          opacity= 1,
                          visible = True,
                          layer= "below")],

                      geo=go.layout.Geo(
                          center={"lat": 22, "lon": 82.5},
                          resolution=110,
                          scope='asia',
                          showframe=False,
                          showcoastlines=True,
                          fitbounds="locations",
                          landcolor="rgba(247, 247, 245,0)",
                          oceancolor="rgba(247, 247, 245,0)",
                          bgcolor="rgba(247, 247, 240,0)",
                          framecolor="rgba(247, 247, 245,0)",
                          countrycolor="rgba(247, 247, 245,0)",
                          coastlinecolor="rgba(247, 247, 245,0)",
                          projection_type='mercator',
                          lonaxis_range=[-4.0, 26.0],
                          lataxis_range=[-10.5, 20.0],
                          domain=dict(x=[0, 1], y=[0, 1])))


def get_bar_layout(city):
    layout = dict(
        title=dict(
            text='SEIR Model for {0}'.format(city),
            font=dict(family="Open Sans, sans-serif", size=15, color="#515151"),
        ),
        paper_bgcolor="rgb(247, 247, 245)",
        plot_bgcolor="rgb(247, 247, 245)",
        updatemenus=list([
            dict(active=1,
                 buttons=list([
                     dict(label='Log Scale',
                          method='update',
                          args=[{'visible': [True, True]},
                                {'title': 'Log scale',
                                 'yaxis': {'type': 'log'}}]),
                     dict(label='Linear Scale',
                          method='update',
                          args=[{'visible': [True, True]},
                                {'title': 'Linear scale',
                                 'yaxis': {'type': 'linear'}}])
                 ]),
                 )
        ]),
        legend=dict(
            x=-0.265,
            y=-0.1,
            traceorder="reverse",
            font=dict(
                family="sans-serif",
                size=12,
                color="black"
            ),
            bgcolor="rgb(247, 247, 245)",
            bordercolor="rgb(247, 247, 245)",
            borderwidth=2
        ),
        # barmode='stack',
        width=900,
        height=400,
        font=dict(family="Open Sans, sans-serif", size=13),
        hovermode="all",
        xaxis=dict(title="Days",rangemode="nonnegative"), yaxis=dict(title="Records"),rangemode="nonnegative",autorange = False,rangeslider=dict(visible = True))
    return layout
