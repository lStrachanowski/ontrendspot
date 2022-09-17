from .analytics import get_stock_from_db
import plotly.subplots as ms
import plotly.graph_objects as go
import plotly
import json
import os
from django.conf import settings


def candle_chart(stockname, period, volume, chart_type):
    df = get_stock_from_db(stockname.upper(), period)
    if volume:
        fig = ms.make_subplots(rows=2, cols=1, shared_xaxes=True,
                               vertical_spacing=0.02,  row_heights=[0.8, 0.2])
    else:
        fig = ms.make_subplots(rows=1, cols=1, shared_xaxes=True)
    fig.add_trace(go.Candlestick(x=df['day'],
                                 open=df['stock_open'],
                                 high=df['stock_high'],
                                 low=df['stock_low'],
                                 close=df['stock_close'],
                                 showlegend=False),
                  row=1,
                  col=1)
    fig.update_layout(xaxis_rangeslider_visible=False)
    if volume:
        fig.add_trace(go.Bar(x=df['day'], y=df['volume'],
                      showlegend=False, marker_color="#3d3c3c"), row=2, col=1)
        fig.update_layout(xaxis_rangeslider_visible=False)
        fig.update_xaxes(
            rangebreaks=[
                dict(bounds=["sat", "mon"]),
            ])
    fig.layout.xaxis.fixedrange = True
    fig.layout.yaxis.fixedrange = True
    fig.update_layout(
        margin=dict(l=5, r=5, t=5, b=5),
        paper_bgcolor="#FCFCFC",)
    cs = fig.data[0]
    cs.increasing.fillcolor = '#27cc02'
    cs.increasing.line.color = '#27cc02'
    cs.decreasing.fillcolor = '#ff0400'
    cs.decreasing.line.color = '#ff0400'
    if chart_type == 'image':
        fig.write_image(os.path.join(settings.BASE_DIR,
                        './stocks/static/img/'+stockname+'.svg'))
    if chart_type == 'json':
        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        return graphJSON
    if chart_type == 'fig':
        return fig


def histogram(stockname, period):
    df = get_stock_from_db(stockname.upper(), period)
    stock_changes = df['stock_close'].pct_change().round(4).dropna()*100
    fig = go.Figure(data=[go.Histogram(x= stock_changes)])
    fig.update_layout(bargap=0.2)
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON
