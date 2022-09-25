from .analytics import get_stock_from_db, bollinger_bands, rsi, mean_volume, stock_changes
import plotly.subplots as ms
import plotly.graph_objects as go
import plotly
import json
import os
from django.conf import settings
import talib
import numpy


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
    stock_changes_data = stock_changes(stockname, period)
    fig = go.Figure(data=[go.Histogram(x= stock_changes_data)])
    fig.update_layout(bargap=0.2)
    fig.update_layout(
    margin=dict(
        l=35,
        r=35,
        b=25,
        t=25,
        pad=2
        )
    )
    fig.update_layout(plot_bgcolor="white")
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON

def rolling_mean_charts(stockname, period):
    df = get_stock_from_db(stockname.upper(), period)
    df = df.set_index(df['day'])
    fig = ms.make_subplots(rows=1, cols=1)
    rolling_mean_15 = df.rolling(15).mean().round(4).dropna()
    rolling_mean_30 = df.rolling(30).mean().round(4).dropna()
    rolling_mean_45 = df.rolling(45).mean().round(4).dropna()
    fig.add_trace(go.Scatter(x = rolling_mean_15.index, y = rolling_mean_15['stock_close'],line_shape='spline',name='SMA 15'),row=1, col=1)
    fig.add_trace(go.Scatter(x = rolling_mean_30.index, y = rolling_mean_30['stock_close'],line_shape='spline',name='SMA 30'),row=1, col=1 )
    fig.add_trace(go.Scatter(x = rolling_mean_45.index, y = rolling_mean_45['stock_close'],line_shape='spline', name='SMA 45'),row=1, col=1 )
    fig.update_layout(plot_bgcolor="white")
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON

def rsi_chart(stockname, period):
    df = rsi(stockname, period)
    fig = ms.make_subplots(rows=1, cols=1)
    fig.add_trace(go.Scatter(x = df.index, y = df ,line_shape='spline',name='RSI'),row=1, col=1)
    fig.update_layout(plot_bgcolor="white")
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON

def bollinger_bands_chart(stockname,period):
    df = bollinger_bands(stockname, period)
    fig = ms.make_subplots(rows=1, cols=1)
    fig.add_trace(go.Scatter(x = df.index, y = df['upper'] ,line_shape='spline',name='UPPER', line_color='#a0a0b8'),row=1, col=1)
    fig.add_trace(go.Scatter(x = df.index, y = df['middle'] ,line_shape='spline',name='MIDDLE', line_color='#a0a0b8'),row=1, col=1 )
    fig.add_trace(go.Scatter(x = df.index, y = df['lower'] ,line_shape='spline', name='LOWER', line_color='#a0a0b8'),row=1, col=1 )
    fig.add_trace(go.Scatter(x = df.index, y = df['stock_close'] ,line_shape='spline', name='PRICE', line_color='#0d0006'),row=1, col=1 )
    fig.update_layout(plot_bgcolor="white")
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON


def mean_volume_chart(stockname,period):
    df = mean_volume(stockname,period)
    fig = ms.make_subplots(rows=1, cols=1)
    fig.add_trace(go.Scatter(x = df['day'], y = df['rolling_volume'] ,line_shape='spline',name='UPPER', line_color='#a0a0b8'),row=1, col=1)
    fig.update_layout(plot_bgcolor="white")
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON