import gc
import polars as pl
import plotly.express as px
from plotly.graph_objs import Figure


def plot_helpful_votes(lf: pl.LazyFrame, plot_name: str) -> Figure:
    columns: list[str] = ["helpful_vote", "rating"]
    df: pl.DataFrame = lf.select(columns).collect()
    print("Plotting Figure")
    fig: Figure = px.violin(
        df,
        x="rating",
        y="helpful_vote",
        height=800,
        category_orders={"rating": [1, 2, 3, 4, 5]},
        color="rating",
        color_discrete_sequence=px.colors.qualitative.Prism,
        template="ggplot2",
    )


    fig.update_layout(
        title=f"Distribution of Helpful Votes Across Star Ratings (Purchase Sample={len(df)})",
        xaxis_title="Star Rating",
        yaxis_title="Helpful Votes",
    )
    del df

    path: str = "data/processed/"
    print("Saving Figure")
    fig.write_html(f"{path}/html/{plot_name}.html", include_plotlyjs='cdn')
    fig.write_image(f"{path}/imgs/{plot_name}.png", width=1500)
    fig.write_image(f"{path}/docs/{plot_name}.pdf", width=1500)

    gc.collect()
    return fig
    