from pathlib import Path

import cufflinks as cf
import pandas as pd
import yfinance as yf
from faicons import icon_svg
from shiny import reactive
from shiny.express import input, render, ui
from shiny.ui import output_ui
from shinywidgets import render_plotly
#from shiny.express.render import DataGrid  # Import DataGrid

from stocks import stocks

# Default to the last 6 months
end = pd.Timestamp.now()
start = end - pd.Timedelta(weeks=26)

ui.page_opts(title="Stock explorer", fillable=True)

with ui.sidebar():
    ui.input_selectize("ticker", "Select Stocks", choices=stocks, selected="AAPL")
    ui.input_date_range("dates", "Select dates", start=start, end=end)

# Define a function to get data as a pandas DataFrame
def get_dataframe():
    dates = input.dates()
    return get_ticker().history(start=dates[0], end=dates[1])

# Define a function to get a specific ticker
@reactive.calc
def get_ticker():
    return yf.Ticker(input.ticker())

# Define a function to calculate the change
@reactive.calc
def get_change():
    close = get_dataframe()["Close"]
    return close.iloc[-1] - close.iloc[-2]

# Define a function to calculate the percent change
@reactive.calc
def get_change_percent():
    close = get_dataframe()["Close"]
    change = close.iloc[-1] - close.iloc[-2]
    return change / close.iloc[-2] * 100

# Define a function to get the stock data
@reactive.calc
def get_data():
    return get_dataframe()

with ui.layout_column_wrap(fill=False):
    with ui.value_box(showcase=icon_svg("dollar-sign")):
        "Current Price"

        @render.ui
        def price():
            close = get_dataframe()["Close"]
            return f"{close.iloc[-1]:.2f}"

    with ui.value_box(showcase=output_ui("change_icon")):
        "Change"

        @render.ui
        def change():
            return f"${get_change():.2f}"

    with ui.value_box(showcase=icon_svg("percent")):
        "Percent Change"

        @render.ui
        def change_percent():
            return f"{get_change_percent():.2f}%"



with ui.layout_columns(col_widths=[9, 3]):
    with ui.card(full_screen=True):
        ui.card_header("Price history")

        @render_plotly
        def price_history():
            qf = cf.QuantFig(
                get_data(),
                name=input.ticker(),
                up_color="#44bb70",
                down_color="#040548",
                legend="top",
            )
            qf.add_sma()
            qf.add_volume(up_color="#44bb70", down_color="#040548")
            fig = qf.figure()
            fig.update_layout(
                hovermode="x unified",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
            )
            return fig

        # Add DataGrid to display the stock data
    with ui.card():
        ui.card_header("Stock Data")

        @render.data_frame
        def stock_data():
            data = get_data()  # Get the stock data
            if data is not None:
                return render.DataGrid(data)  # Render the DataGrid with the stock data


ui.include_css(Path(__file__).parent / "styles.css")


@reactive.calc
def get_ticker():
    return yf.Ticker(input.ticker())


@reactive.calc
def get_data():
    dates = input.dates()
    return get_ticker().history(start=dates[0], end=dates[1])


@reactive.calc
def get_change():
    close = get_data()["Close"]
    return close.iloc[-1] - close.iloc[-2]


@reactive.calc
def get_change_percent():
    close = get_data()["Close"]
    change = close.iloc[-1] - close.iloc[-2]
    return change / close.iloc[-2] * 100


with ui.hold():

    @render.ui
    def change_icon():
        change = get_change()
        icon = icon_svg("arrow-up" if change >= 0 else "arrow-down")
        icon.add_class(f"text-{('success' if change >= 0 else 'danger')}")
        return icon