import gc
from plotly.graph_objs._figure import Figure
import polars as pl
import plotly.express as px


def plot_histogram(lf: pl.LazyFrame, plot_name: str) -> Figure:
    lf = lf.group_by(["rating","verified_purchase"]).len()
    lf = lf.rename({"len": "number of reviews"}).collect()
    print("Plotting figure")

    fig = px.bar(
        lf,
        x="rating",
        y="number of reviews",
        color="verified_purchase",
        barmode="stack",
        category_orders={
            "rating": [1, 2, 3, 4, 5],
            "verified_purchase": [True, False]
        },
        color_discrete_sequence=px.colors.qualitative.Set2,
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

    print("Saving figure")
    path = "data/processed/"

    fig.update_layout(height=625)
    fig.write_html(f"{path}/html/{plot_name}.html", include_plotlyjs='cdn')
    fig.update_layout(height=800)
    fig.write_image(f"{path}/imgs/{plot_name}.png", width=1500)
    fig.write_image(f"{path}/docs/{plot_name}.pdf", width=1500)
    return fig


