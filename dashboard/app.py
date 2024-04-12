import pandas as pd
from faicons import icon_svg
from shiny import reactive
from shiny.express import input, render, ui
from shiny.ui import output_ui
from shinywidgets import render_plotly
import plotly.express as px
from pathlib import Path
import seaborn as sns

# Load the Seaborn tips dataset
tips = sns.load_dataset("tips")

# Title
ui.page_opts(title="Tip Determination Explorer", fillable=True)

with ui.sidebar():
    ui.input_selectize("sex", "Select Sex", choices=list(tips["sex"].unique()), selected="Male")
    ui.input_selectize("day", "Select Day", choices=list(tips["day"].unique()), selected="Sun")
    ui.input_slider("n", "Number of bins", 0, 100, 20)

    ui.h6("Github Links:")
    ui.a(
        "GitHub Source",
        href="https://github.com/Crusoe22/cintel-06-custom",
        target="_blank",
        style="color: #007bff;",
    )
    
    ui.a(
        "GitHub App",
        href="https://github.com/Crusoe22/cintel-06-custom/blob/main/dashboard/app.py",
        target="_blank",
        style="color: #007bff;",
    )

# Define a function to get data 
def get_dataframe():
    selected_sex = input.sex()
    selected_day = input.day()
    return tips[(tips["sex"] == selected_sex) & (tips["day"] == selected_day)]


# Define a function to get the tip data
@reactive.calc
def get_data():
    return get_dataframe()

with ui.layout_column_wrap(fill=False, height=75):
    with ui.value_box(showcase=icon_svg("dollar-sign")):
        "Summary of Bills Selected"

        @render.ui
        def total_bill():
            selected_day = input.day()  # Get the selected day
            selected_sex = input.sex()  # Get the selected sex
            selected_data = tips[(tips["day"] == selected_day) & (tips["sex"] == selected_sex)]  # Filter data by selected day and sex
            sum_of_bills = selected_data["total_bill"].sum()  # Calculate sum of bills
            return f"{sum_of_bills:.2f}"


with ui.layout_columns(row_heights=None, col_widths=None):
    with ui.card(full_screen=True):
        ui.card_header("Total Bill vs. Tip")

        @render_plotly
        def total_bill_vs_tip():
            fig = px.scatter(
                get_data(),
                x="total_bill",
                y="tip",
                color="sex",
                title="Total Bill vs. Tip",
            )
            fig.update_layout(
                hovermode="closest",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
            )
            return fig


    with ui.card():
        ui.card_header("Tip Distribution")

        @render_plotly
        def tip_distribution():
            return px.histogram(
                get_data(),
                x="tip",
                nbins=input.n(),
                title="Tip Distribution",
                labels={"tip": "Tip Amount"},
            )


with ui.layout_columns(height=300, col_widths=12):
    with ui.card():
        ui.card_header("Tips Data")

        @render.data_frame
        def tips_data():
            data = get_data()  # Get the tips data
            if data is not None:
                return render.DataGrid(data)  # Render the DataGrid with the tips data

ui.include_css(Path(__file__).parent / "styles.css")

@reactive.calc
def get_data():
    return get_dataframe()


with ui.hold():

    @render.ui
    def change_icon():
        icon = icon_svg("arrow-up")
        icon.add_class("text-success")
        return icon