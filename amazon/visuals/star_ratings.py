import gc
from plotly.graph_objs._figure import Figure
import polars as pl
import plotly.express as px


def plot_histogram(lf: pl.LazyFrame, plot_name: str) -> Figure:
    lf = lf.group_by(["rating","verified_purchase"]).len()
    lf = lf.rename({"len": "n_reviews"}).collect()
    print("Plotting figure")

    fig = px.bar(
        lf,
        x="rating",
        y="n_reviews",
        color="verified_purchase",
        barmode="stack",
        category_orders={"rating": [1, 2, 3, 4, 5]},
        color_discrete_sequence=px.colors.qualitative.Set2,
        height=800,
        template="ggplot2",
        text_auto=True        
    )

    fig=fig.update_layout(
        title="Distribution of Star Ratings",
        xaxis_title="Star Rating",
        yaxis_title="Number of Reviews",
        legend_title="Verified Purchase",
        title_font_size=22,
        xaxis=dict(tickmode="linear"),
        bargap=0.0,         
        bargroupgap=0.0
    )
    print("Saving Figure")
    path = "data/processed/"
    fig.write_html(f"{path}/html/{plot_name}.html", include_plotlyjs='cdn')
    fig.write_image(f"{path}/imgs/{plot_name}.png", width=1500)
    fig.write_image(f"{path}/docs/{plot_name}.pdf", width=1500)
    return fig


def plot_histogram_deprecated(lf: pl.LazyFrame, plot_name: str) -> Figure:
    columns: list[str] = ["rating", "verified_purchase"]
    ratings: pl.DataFrame = lf.select(columns).collect()

    print("Plotting figure")
    fig: Figure = px.histogram(
        ratings,
        x="rating",
        color="verified_purchase",
        category_orders={"rating": [1, 2, 3, 4, 5]},
        color_discrete_sequence=px.colors.qualitative.Set2,
        height=800,
        template="ggplot2",
    )
    del ratings

    fig.update_layout(
        title="Distribution of Star Ratings",
        xaxis_title="Star Rating",
        yaxis_title="Number of Reviews",
        legend_title="Verified Purchase",
        title_font_size=22,
        xaxis=dict(tickmode="linear"),
    )

    print("Saving figure")
    path = "data/processed/"
    # fig.write_html(f"{path}/html/{plot_name}.html", include_plotlyjs='cdn')
    # fig.write_image(f"{path}/imgs/{plot_name}.png", width=1500)
    # fig.write_image(f"{path}/docs/{plot_name}.pdf", width=1500)

    gc.collect()
    return fig
