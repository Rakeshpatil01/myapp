from turtle import width
import pandas as pd
import plotly.io as pio
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def get_candlestick_plot(
        df: pd.DataFrame,
        ma1: int,
        ma2: int,
        ticker: str
):
    '''
    Create the candlestick chart with two moving avgs + a plot of the volume
    Parameters
    ----------
    df : pd.DataFrame
        The price dataframe
    ma1 : int
        The length of the first moving average (days)
    ma2 : int
        The length of the second moving average (days)
    ticker : str
        The ticker we are plotting (for the title).
    '''

    fig = make_subplots(
        rows=2,
        cols=1,
        shared_xaxes=True,
        vertical_spacing=0.1,
        subplot_titles=(f'{ticker} Stock Price', 'Volume Chart'),
        row_width=[0.3, 0.7]
    )

    fig.add_trace(
        go.Candlestick(
            x=df['Date'],
            open=df['Open'],
            high=df['High'],
            low=df['Low'],
            close=df['Close'],
            name='Candlestick chart'
        ),
        row=1,
        col=1,
    )

    fig.add_trace(
        go.Line(x=df['Date'], y=df[f'{ma1}_ma'], name=f'{ma1} SMA'),
        row=1,
        col=1,
    )

    fig.add_trace(
        go.Line(x=df['Date'], y=df[f'{ma2}_ma'], name=f'{ma2} SMA'),
        row=1,
        col=1,
    )

    # fig.add_trace(
    #     go.Bar(x = df['Date'], y = df['Volume'], name = 'Volume'),
    #     row = 2,
    #     col = 1,
    # )

    fig['layout']['xaxis2']['title'] = 'Date'
    fig['layout']['yaxis']['title'] = 'Price'
    fig['layout']['yaxis2']['title'] = 'Volume'

    fig.update_xaxes(
        rangebreaks=[{'bounds': ['sat', 'mon']}],
        rangeslider_visible=False,
    )
    fig.update_layout(title_text="CandleStick", margin={
                      "r": 0, "t": 0, "l": 0, "b": 0}, height=800, width=2000)
    return fig
