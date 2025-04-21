from plotly.graph_objs._figure import Figure
import polars as pl
import plotly.express as px
import numpy as np


def plot_correlation_matrix(lf: pl.LazyFrame, plot_name: str) -> Figure:
    lf: pl.LazyFrame = lf.select(["review_length", "rating"])
    corr_matrix: np.ndarray = lf.collect().corr().to_numpy()

    fig: Figure = px.imshow(
        corr_matrix,
        text_auto=True,
        color_continuous_scale=px.colors.sequential.Purpor_r,
        x=["review length", "rating"],
        y=["review length", "rating"],
    )

    del corr_matrix

    fig.update_layout(
        title="Correlation Between Review Length and Star Rating",
        title_font_size=22,
        width=800,
        height=800,
        template="ggplot2",
    )

    path = "data/processed/plots/"
    path += plot_name

    fig.write_html(f"{path}.html")
    fig.write_image(f"{path}.png", width=1500)
    fig.write_image(f"{path}.pdf", width=1500)
    return fig
