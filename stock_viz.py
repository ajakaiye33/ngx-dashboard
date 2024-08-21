"""
Created on Tue Jun 17 00:59:25 2021
@author: Hedgar Ajakaiye
"""

import streamlit as st
import matplotlib
import plotly.express as px
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import warnings
warnings.filterwarnings("ignore")

from stock_view.data_prep import load_equities_data, get_insider_symbols
from stock_view.data_prep import filter_top_gainers, filter_top_losers
from stock_view.data_prep import ngx_50_index, ngx_30_index, ngx_pension_index
from stock_view.data_prep import dividend_tracker_data
from stock_view.data_prep import latest_news

# from stock_view.data_prep import current_p50, current_p30, current_pens
# from stock_view.data_prep import yesterday_p50, yesterday_p30, yesterday_pens

# import streamlit.components.v1 as components


matplotlib.use("agg")


# st.set_page_config(
#     page_icon=":chart_with_upwards_trend:",
#     layout="wide",
#     initial_sidebar_state="collapsed",
# )


# st.markdown("<style> body {color: white;}</style>", unsafe_allow_html=True)
# st.markdown(
#     "<h1 style='text-align: center; margin-top: 15px;'>Stock Market Live Dashboard</h1>",  # noqa
#     unsafe_allow_html=True,
# )
# st.markdown(
#     "<style> .css-18c15ts {padding-top: 1rem; margin-top:-75px;} </style>",
#     unsafe_allow_html=True,
# )

# st.markdown(
#     """ <style>
# # MainMenu {visibility: hidden;}
# footer {visibility: hidden;}
# </style> """,
#     unsafe_allow_html=True,
# )
#Page configuration
st.set_page_config(
    page_title="Stock Market Dashboard",
    page_icon=":chart_with_upwards_trend:",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Custom CSS for styling
st.markdown("""
    <style>
    /* General Body Styling */
    body {
        color: #f0f0f0;
        background-color: #0e1117;
        font-family: 'Roboto', sans-serif;
    }

    /* Header Styling */
    .css-18c15ts {
        padding-top: 1rem;
        margin-top: -60px;
        color: #61dafb;
        font-size: 2rem;
        font-weight: bold;
        text-align: center;
    }

    /* Sidebar Styling */
    .css-1lcbmhc {
        background-color: #0e1117;
    }

    /* Hiding Streamlit Footer and Main Menu */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* Customizing Buttons */
    .stButton>button {
        color: #fff;
        background-color: #007bff;
        border: none;
        border-radius: 8px;
        font-size: 16px;
        padding: 0.5rem 1rem;
    }

    .stButton>button:hover {
        background-color: #0056b3;
    }

    /* Make the content responsive */
    @media (max-width: 767px) {
        .css-18c15ts {
            font-size: 1.5rem;
            margin-top: -30px;
        }
    }

    @media (min-width: 768px) and (max-width: 1023px) {
        .css-18c15ts {
            font-size: 1.75rem;
            margin-top: -45px;
        }
    }
    .css-1d391kg {
        overflow-x: auto;
    }
    .css-12c6pdh {
        max-width: 100% !important;
    }
    </style>
""", unsafe_allow_html=True)
# Title
st.markdown(
    """
    <h1 style='text-align: center; margin-top: 10px;'>Stock Market Live Dashboard</h1>
    <div style='text-align: center; font-size: 16px; margin-top: 10px; color: #61dafb;'>
        <strong>Opens:</strong> Mon-Friday 10:00 - 2.30 WAT<br>
        <span style='color: #ff6f61;'>Data is delayed by at least 10 minutes</span>
    </div>
    <div style='margin-top: 100px;'></div>
    """,
    unsafe_allow_html=True
)


data2 = get_insider_symbols()
st.set_option("deprecation.showPyplotGlobalUse", False)


def wrd_viz(stringy):
    try:
        wrdcld = WordCloud(width=1400, height=1000).generate(
            ",".join(symbol for symbol in stringy)
        )
        plt.figure(figsize=[20, 20])
        plt.axis("off")
        plt.imshow(wrdcld, interpolation="bilinear")
        plt.show()
    except Exception as e:
        st.text(f"Ooops! ... Refresh browser now {e}")


data = load_equities_data()

try:
    selling = data[(data["Change"] < 0) & (data["PercChange"] < 0)]
    # selling
    betting = data[(data["Volume"] > 0) & (data["PercChange"] > 0)]
except KeyError:
    st.text("Market Information still recalibrating...")
# top gainers


# treemap and worldclod
try:
    treemap_cont, wod_cld_cont = st.columns((7, 4))
    with treemap_cont:
        with st.container():
            st.markdown(
        """
        <div style='text-align: center; 
                    font-size: 14px; 
                    font-weight: bold; 
                    color: #4A90E2; 
                    margin-bottom: 5px;
                    padding: 5px; 
                    border: 1px solid #4A90E2; 
                    border-radius: 5px;'>
            Current Market Temperature
        </div>
        """,
        unsafe_allow_html=True
    )
            fig = px.treemap(
                data,
                path=["Sector", "Symbol"],
                values="Volume",
                width=500,
                height=500,
                color=data["PercChange"],
                color_continuous_scale=[(0, "red"), (1, "green")],
                #title="Current Temperature of The Market",
            )
            fig.update_layout(margin=dict(t=50, l=25, r=25, b=25))
            st.plotly_chart(fig, use_container_width=True)
        # wod_cld_cont.text(" ")
        # wod_cld_cont.text(" ")
        # wod_cld_cont.text(" ")
        # wod_cld_cont.text(" ")
        # wod_cld_cont.text(" ")
        # wod_cld_cont.text(" ")

    with wod_cld_cont:
        with st.container():
       #st.text("Director Dealings In the Past Months")
            st.markdown(
        """
        <div style='text-align: center; 
                    font-size: 16px; 
                    font-weight: bold; 
                    color: #4A90E2; 
                    margin-bottom: 5px;
                    padding: 10px; 
                    border: 1px solid #4A90E2; 
                    border-radius: 5px;'>
            Director Dealings In the Past Months
        </div>
        """,
        unsafe_allow_html=True
    )
            
            st.pyplot(wrd_viz(data2))

    sell, hot, value = st.columns([5, 6, 4])
    with sell:
        with st.container():
            st.markdown(
        """
        <div style='text-align: center; 
                    font-size: 16px; 
                    font-weight: bold; 
                    color: #4A90E2; 
                    margin-bottom: 5px;
                    padding: 10px; 
                    border: 1px solid #4A90E2; 
                    border-radius: 5px;'>
            Stocks Under Pressure
        </div>
        """,
        unsafe_allow_html=True
    )
            fix = px.bar(
                selling,
                x="Symbol",
                y="PercChange",
                #title="Stocks Being Dumped",
                color="Symbol",
                width=500,
                height=500,
                labels={"Symbol": "stocks", "PercChange": "%Change"},
            )
            st.plotly_chart(fix)
    with hot:
        with st.container():
            st.markdown(
        """
        <div style='text-align: center; 
                    font-size: 16px; 
                    font-weight: bold; 
                    color: #4A90E2; 
                    margin-bottom: 5px;
                    padding: 10px; 
                    border: 1px solid #4A90E2; 
                    border-radius: 5px;'>
            Current Investors Favourites
        </div>
        """,
        unsafe_allow_html=True
    )

            fog = px.bar(
                betting,
                x="Symbol",
                y="Change",
                #title="Stocks on the Run",
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
        with st.container():
            st.markdown(
        """
        <div style='text-align: center; 
                    font-size: 16px; 
                    font-weight: bold; 
                    color: #4A90E2; 
                    margin-bottom: 5px;
                    padding: 10px; 
                    border: 1px solid #4A90E2; 
                    border-radius: 5px;'>
            Money Flows
        </div>
        """,
        unsafe_allow_html=True
    )
            
            monei = px.bar(
                data,
                x="Symbol",
                y="Value",
                hover_name="Company2",
                width=500,
                height=500,
                #title="Where The Money's at (N-Naira)",
                color="Symbol",
                labels={"Symbol": "Stocks", "Value": "Naira"},
            )
            st.plotly_chart(monei)

except Exception:  # noqa
    st.text(
        "Ooops! ... Sorry, Can't retrieve data right now, try later"
        "/Refresh browser. Meanwhile see historical performance below"
    )
# show losers and gainers


# market stats

try:
    mkt_stat1, mkt_stat2, mkt_stat3 = st.columns([5, 6, 4])
    with mkt_stat1:
        with st.container():
            st.markdown(
        """
        <div style='text-align: center; 
                    font-size: 16px; 
                    font-weight: bold; 
                    color: #4A90E2; 
                    margin-bottom: 5px;
                    padding: 10px; 
                    border: 1px solid #4A90E2; 
                    border-radius: 5px;'>
            Most Traded By Volume
        </div>
        """,
        unsafe_allow_html=True
    )
            fin = px.sunburst(
                data,
                path=["Sector", "Symbol"],
                values="Volume",
                #title="Most Traded by Volume",
                width=500,
                height=500,
            )
            st.plotly_chart(fin)
    with mkt_stat2:
        with st.container():
            st.markdown(
        """
        <div style='text-align: center; 
                    font-size: 16px; 
                    font-weight: bold; 
                    color: #4A90E2; 
                    margin-bottom: 5px;
                    padding: 10px; 
                    border: 1px solid #4A90E2; 
                    border-radius: 5px;'>
            Most Traded by Value
        </div>
        """,
        unsafe_allow_html=True
    )
            cons = px.sunburst(
                data,
                path=["Sector", "Symbol"],
                values="Value",
                #title="Most Traded by Value",
                width=500,
                height=500,
            )
            st.plotly_chart(cons)

    with mkt_stat3:
        with st.container():
            st.markdown(
        """
        <div style='text-align: center; 
                    font-size: 16px; 
                    font-weight: bold; 
                    color: #4A90E2; 
                    margin-bottom: 5px;
                    padding: 10px; 
                    border: 1px solid #4A90E2; 
                    border-radius: 5px;'>
            Most Traded by Deals
        </div>
        """,
        unsafe_allow_html=True
    )
            deals = px.sunburst(
                data,
                path=["Sector", "Symbol"],
                values="Trades",
                #title="Most Traded by Deals",
                width=500,
                height=500,
            )
            st.plotly_chart(deals)

except Exception:  # noqa
    st.text("Ooops! ... Sorry, Can't retrieve data at the moment, try later")
# indecies


try:
    ngx50_current_prix_i = ngx_50_index()
    ngx50_current_prix = ngx50_current_prix_i.iloc[-1, 1]
    ngx30_current_prix_i = ngx_30_index()
    ngx30_current_prix = ngx30_current_prix_i.iloc[-1, 1]
    ngxpension_current_prix_i = ngx_pension_index()
    ngxpension_current_prix = ngxpension_current_prix_i.iloc[-1, 1]
    ngx50_prev_prix = ngx50_current_prix_i.iloc[-2, 1]
    ngx30_prev_prix = ngx30_current_prix_i.iloc[-2, 1]
    ngxpension_priv_prix = ngxpension_current_prix_i.iloc[-2, 1]

    diff_50 = round(
        ((ngx50_current_prix - ngx50_prev_prix) / ngx50_current_prix) * 100, 2
    )
    diff_30 = round(
        ((ngx30_current_prix - ngx30_prev_prix) / ngx30_current_prix) * 100, 2
    )
    diff_pens = round(
        ((ngxpension_current_prix - ngxpension_priv_prix) / ngxpension_current_prix)
        * 100,
        2,
    )

    ngx50_metric, ngx30_metric, ngxpens_metric = st.columns(3)
    with st.container():
        ngx50_metric.metric(
            label="All Share Index(ASI)", value=ngx50_current_prix, delta=f"{diff_50}%"
        )
    with st.container():
        ngx30_metric.metric(
            label="NGX30 Index", value=ngx30_current_prix, delta=f"{diff_30}%"
        )
    with st.container():
        ngxpens_metric.metric(
            label="NGX PENSION Index", value=ngxpension_current_prix, delta=f"{diff_pens}%"
        )
except Exception:
    st.text("Sorry, Can't retrieve data at the moment, try later")


def viz_index():
    try:
        ngx_50 = ngx_50_index()
        ngx_30 = ngx_30_index()
        ngx_pension = ngx_pension_index()

        fifty, thirty, pens = st.columns(3)
        with fifty:
            with st.container():
                fig1 = px.line(ngx_50, x="date", y="prices", title="All Share Index")
                st.plotly_chart(fig1)
        with thirty:
            with st.container():
                fig2 = px.line(ngx_30, x="date", y="prices", title="NGX 30 Index")
                st.plotly_chart(fig2)
        with pens:
            with st.container():
                fig3 = px.line(ngx_pension, x="date", y="prices", title="NGX PENSION Index")
                st.plotly_chart(fig3)
    except Exception:
        st.text("Sorry, Can't retrieve data at the moment")


viz_index()


getnew_link = latest_news()
try:
    #st.subheader("Latest News")
    st.markdown(
    """
    <div style='text-align: center; 
                font-size: 24px; 
                font-weight: bold; 
                color: #4A90E2; 
                margin-bottom: 20px;
                padding: 10px; 
                border: 2px solid #4A90E2; 
                border-radius: 5px;'>
        Latest News
    </div>
    """,
    unsafe_allow_html=True
)
    for i in getnew_link:
        st.markdown(f"{i['title']}, [Read More]({i['url']})-{i['date']}")
except Exception:
    st.text("Sorry news site not responding")


# dividend tracker datarame
div_data = dividend_tracker_data()
try:
    #st.subheader("Dividend Tracker")
    st.markdown(
    """
    <div style='text-align: center; 
                font-size: 24px; 
                font-weight: bold; 
                color: #4A90E2; 
                margin-bottom: 20px;
                padding: 10px; 
                border: 2px solid #4A90E2; 
                border-radius: 5px;'>
        Dividend Tracker
    </div>
    """,
    unsafe_allow_html=True
)
    st.dataframe(div_data, use_container_width=True)
except Exception:
    st.text("Ooops... Sorry can't retrieve data at the moment, try later")

# top gainers and losers  columns

top_g = filter_top_gainers(data)
top_l = filter_top_losers(data)


try:

    col1, col2 = st.columns([3, 3])
    with col1:
        #st.subheader("Todays Top Gainers")
        st.markdown(
    """
    <div style='text-align: center; 
                font-size: 24px; 
                font-weight: bold; 
                color: #4A90E2; 
                margin-bottom: 20px;
                padding: 10px; 
                border: 2px solid #4A90E2; 
                border-radius: 5px;'>
        Todays Top Gainers
    </div>
    """,
    unsafe_allow_html=True
)
        st.dataframe(top_g, use_container_width=True)
    with col2:
        #st.subheader("Todays Top Losers")
        st.markdown(
    """
    <div style='text-align: center; 
                font-size: 24px; 
                font-weight: bold; 
                color: #4A90E2; 
                margin-bottom: 20px;
                padding: 10px; 
                border: 2px solid #4A90E2; 
                border-radius: 5px;'>
        Todays Top Losers
    </div>
    """,
    unsafe_allow_html=True
)
        st.dataframe(top_l, use_container_width=True)
except Exception:
    st.text("Ooops!... Sorry can't retrieve data at the moment,try later!")
