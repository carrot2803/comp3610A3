import polars as pl
import plotly.express as px
from plotly.graph_objs import Figure


def plot_helpful_votes(lf: pl.LazyFrame, plot_name: str) -> Figure:
    columns: list[str] = ["helpful_vote", "rating"]
    helpful_votes: pl.DataFrame = lf.select(columns).collect()

    fig: Figure = px.violin(
        helpful_votes,
        x="rating",
        y="helpful_vote",
        height=800,
        category_orders={"rating": [1, 2, 3, 4, 5]},
        color="rating",
        color_discrete_sequence=px.colors.qualitative.Prism,
        template="ggplot2",
    )

    del helpful_votes

    fig.update_layout(
        title="Distribution of Helpful Votes Across Star Ratings",
        xaxis_title="Star Rating",
        yaxis_title="Helpful Votes",
    )

    path: str = "data/processed/"

    fig.write_html(f"{path}/html/{plot_name}.html")
    fig.write_image(f"{path}/imgs/{plot_name}.png", width=1500)
    fig.write_image(f"{path}/docs/{plot_name}.pdf", width=1500)
    return fig
