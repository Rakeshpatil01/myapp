from turtle import width
import pandas as pd
import plotly.io as pio
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from .plot_trend_line import find_grad_intercept
from calc.py_bollingerbands import BollingerBands
from calc.py_rsi import RSIIndicator
import plotly.express as px


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
    # Using the trend-line algorithm, deduce the gradient and intercept terms of
    # the straight lines
    m_res, c_res = find_grad_intercept(
        'resistance',
        df.index.values,
        df.High.values,
    )
    m_supp, c_supp = find_grad_intercept(
        'support',
        df.index.values,
        df.Low.values,
    )

    fig.add_trace(
        go.Scatter(
            x=df['Date'],
            y=m_res*df.index + c_res,
            name='Resistance line'
        )
    )

    fig.add_trace(
        go.Scatter(
            x=df['Date'],
            y=m_supp*df.index + c_supp,
            name='Support line'
        )
    )

    indicator_bb = BollingerBands(df['Close'])

    bb = df
    bb['bb_h'] = indicator_bb.bollinger_hband()
    bb['bb_l'] = indicator_bb.bollinger_lband()
    bb = bb[['Close', 'bb_h', 'bb_l']]

    fig.add_trace(
        go.Line(x=df['Date'], y=df[f'bb_h'], name=f'upperBBand'),
        row=1,
        col=1,
    )
    fig.add_trace(
        go.Line(x=df['Date'], y=df[f'bb_l'], name=f'lowerBBand'),
        row=1,
        col=1,
    )

    df["rsi"] = RSIIndicator(df['Close']).rsi()
    fig.add_trace(
        go.Line(x=df['Date'], y=df['rsi'], name=f'RSI'),
        row=2,
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
