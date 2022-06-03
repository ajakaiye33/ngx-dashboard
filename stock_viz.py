"""
Created on Tue Jun 17 00:59:25 2021
@author: Hedgar Ajkz
"""

import streamlit as st
import matplotlib
import plotly.express as px
import matplotlib.pyplot as plt
from wordcloud import WordCloud

from stock_view.data_prep import data_load, insider_data
from stock_view.data_prep import top_gainers, top_losers

# import streamlit.components.v1 as components


matplotlib.use("agg")


st.set_page_config(
    page_icon=":chart_with_upwards_trend:",
    layout="wide",
    initial_sidebar_state="collapsed",
)


st.markdown("<style> body {color: white;}</style>", unsafe_allow_html=True)
st.markdown(
    "<h1 style='text-align: center; margin-top: 15px;'>Stock Market Live Dashboard</h1>",  # noqa
    unsafe_allow_html=True,
)
st.markdown(
    "<style> .css-18c15ts {padding-top: 1rem; margin-top:-75px;} </style>",
    unsafe_allow_html=True,
)

st.markdown(
    """ <style>
# MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style> """,
    unsafe_allow_html=True,
)


# st.title("NSE Live Dashboard")
st.text(
    "Opens: Mon-Friday 10:00 - 2.30 WAT,"
    "Data is delayed by at least 10 minutes"  # noqa
)

data2 = insider_data()
st.set_option("deprecation.showPyplotGlobalUse", False)


def wrd_viz(stringy):
    try:
        wrdcld = WordCloud(width=1400, height=1000).generate(
            ",".join(symbol for symbol in stringy)
        )
        plt.figure(figsize=[20, 20])
        plt.axis("off")
        plt.imshow(wrdcld, interpolation="bilinear")
        # plt.show()
    except Exception as e:  # noqa
        st.text("Ooops! ... Refresh browser now")


data = data_load()


selling = data[(data["Change"] < 0) & (data["PercChange"] < 0)]
# selling
betting = data[(data["Volume"] > 0) & (data["PercChange"] > 0)]
# top gainers


# treemap and worldclod
try:
    treemap_cont, wod_cld_cont = st.columns((7, 4))
    with treemap_cont:
        fig = px.treemap(
            data,
            path=["Sector", "Symbol"],
            values="Volume",
            width=500,
            height=500,
            color=data["PercChange"],
            color_continuous_scale="BuGn",
            title="Current Temperature of The Market",
        )
        fig.update_layout(margin=dict(t=50, l=25, r=25, b=25))
        st.plotly_chart(fig, use_container_width=True)
    wod_cld_cont.text(" ")
    wod_cld_cont.text(" ")
    wod_cld_cont.text(" ")
    wod_cld_cont.text(" ")
    wod_cld_cont.text(" ")
    wod_cld_cont.text(" ")

    with wod_cld_cont:
        st.text("Director Dealings In the Past Months")
        st.pyplot(wrd_viz(data2))

    sell, hot, value = st.columns([5, 6, 4])
    with sell:
        fix = px.bar(
            selling,
            x="Symbol",
            y="PercChange",
            title="Stocks Being Dumped",
            color="Symbol",
            width=500,
            height=500,
            labels={"Symbol": "stocks", "PercChange": "%Change"},
        )
        st.plotly_chart(fix)
    with hot:
        fog = px.bar(
            betting,
            x="Symbol",
            y="Change",
            title="Stocks on the Run",
            color="PercChange",
            width=500,
            height=500,
            labels={
                "Symbol": "stocks",
                "Change": "Gains-Naira",
                "PercChange": "%change",
            },
        )
        st.plotly_chart(fog)
    with value:
        monei = px.bar(
            data,
            x="Symbol",
            y="Value",
            hover_name="Company2",
            width=500,
            height=500,
            title="Where The Money's at (N-Naira)",
            color="Symbol",
            labels={"Symbol": "Stocks", "Value": "Naira"},
        )
        st.plotly_chart(monei)

except Exception as e:  # noqa
    st.text(
        "Ooops! ... Sorry, Can't retrieve data right now, try later"
        "/Refresh browser. Meanwhile see historical performance below"
    )
# show losers and gainers


# market stats

try:
    mkt_stat1, mkt_stat2, mkt_stat3 = st.columns([5, 6, 4])
    with mkt_stat1:
        fin = px.sunburst(
            data,
            path=["Sector", "Symbol"],
            values="Volume",
            title="Most Traded by Volume",
            width=500,
            height=500,
        )
        st.plotly_chart(fin)
    with mkt_stat2:
        cons = px.sunburst(
            data,
            path=["Sector", "Symbol"],
            values="Value",
            title="Most Traded by Value",
            width=500,
            height=500,
        )
        st.plotly_chart(cons)

    with mkt_stat3:
        deals = px.sunburst(
            data,
            path=["Sector", "Symbol"],
            values="Trades",
            title="Most Traded by Deals",
            width=500,
            height=500,
        )
        st.plotly_chart(deals)

except Exception as e:  # noqa
    st.text(
        "Ooops! ... Sorry, Can't retrieve data right now, try later"
        "/Refresh browser.Meanwhile see historical performance below"
    )
# top gainers and losers  columns

top_g = top_gainers(data)
top_l = top_losers(data)

col1, col2 = st.columns(2)
with col1:
    st.subheader("Todays Top Gainers")
    st.write(top_g)
with col2:
    st.subheader("Todays Top Losers")
    st.write(top_l)
