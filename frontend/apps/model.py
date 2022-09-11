import streamlit as st
import datetime
import pandas as pd
from calc.py_bollingerbands import BollingerBands
from calc.py_macd import MACD
from calc.py_rsi import RSIIndicator
from diagram.plot_candlestick import get_candlestick_plot
import plotly.graph_objects as go
import requests

def app():

    option = st.sidebar.selectbox('Select one symbol', ( 'ADANIPORTS', 'ASIANPAINT',"AXISBANK",'BAJFINANCE','TATASTEEL','WIPRO','YESBANK'))
    # need to add list of stock names

    today = datetime.date.today()
    before = today - datetime.timedelta(days=700)
    interval = st.sidebar.selectbox('Select interval', (1,3, 5,30,60,"1W",'1D','1M'))
    start_date = st.sidebar.date_input('Start date', before)
    end_date = st.sidebar.date_input('End date', today)
    if start_date < end_date:
        st.sidebar.success('Start date: `%s`\n\nEnd date:`%s`' % (start_date, end_date))
    else:
        st.sidebar.error('Error: End date must fall after start date.')

    days_to_plot = st.sidebar.slider(
        'Days to Plot', 
        min_value = 1,
        max_value = 300,
        value = 120,
    )
    ma1 = st.sidebar.number_input(
        'Moving Average #1 Length',
        value = 10,
        min_value = 1,
        max_value = 120,
        step = 1,    
    )
    ma2 = st.sidebar.number_input(
        'Moving Average #2 Length',
        value = 20,
        min_value = 1,
        max_value = 120,
        step = 1,    
    )
    # https://technical-analysis-library-in-python.readthedocs.io/en/latest/ta.html#momentum-indicators

    data = {
        "symbol": option,
        "interval": interval,
        "start_date": str(start_date),
        "end_date": str(end_date)
        }
    print(data)
    res = requests.post(f"http://localhost:8080/historic_data", json=data)
    
    if res.status_code == 200:
        df = pd.DataFrame(res.json())
    else:
        raise ValueError
    # indicator_bb = BollingerBands(df['Close'])

    # bb = df
    # bb['bb_h'] = indicator_bb.bollinger_hband()
    # bb['bb_l'] = indicator_bb.bollinger_lband()
    # bb = bb[['Close','bb_h','bb_l']]

    # macd = MACD(df['Close']).macd()

    # rsi = RSIIndicator(df['Close']).rsi()

    #st.write('Stock Bollinger Bands')

    # st.line_chart(bb)

    # progress_bar = st.progress(0)

    # https://share.streamlit.io/daniellewisdl/streamlit-cheat-sheet/app.py

    # st.write('Stock Moving Average Convergence Divergence (MACD)')
    # st.area_chart(macd)

    # st.write('Stock RSI ')
    # st.line_chart(rsi)

    # figure = go.Figure(data=[go.Candlestick(
    #     x=df.index,
    #     low=df['Low'],
    #     high=df['High'],
    #     close=df['Close'],
    #     open=df['Open'],
    #     increasing_line_color='green',
    #     decreasing_line_color='red',
    # )])
    # st.plotly_chart(figure)

    df[f'{ma1}_ma'] = df['Close'].rolling(ma1).mean()
    df[f'{ma2}_ma'] = df['Close'].rolling(ma2).mean()
    df = df[-days_to_plot:]

    # Display the plotly chart on the dashboard
    
    st.plotly_chart(
        get_candlestick_plot(df, ma1, ma2, option),
        use_container_width = True,
    )

    st.write('Recent data ')
    st.dataframe(df.tail(10))




    