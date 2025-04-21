from plotly.graph_objs._figure import Figure
import polars as pl
import plotly.express as px


def plot_histogram(lf: pl.LazyFrame, plot_name: str) -> Figure:
    columns: list[str] = ["rating", "verified_purchase"]
    ratings: pl.DataFrame = lf.select(columns).collect()

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

    path = "data/processed/plots/"
    path += plot_name

    fig.write_html(f"{path}.html")
    fig.write_image(f"{path}.png", width=1500)
    fig.write_image(f"{path}.pdf", width=1500)
    return fig
