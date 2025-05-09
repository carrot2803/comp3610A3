import gc
from plotly.graph_objs._figure import Figure
import polars as pl
import plotly.express as px
import numpy as np


def plot_correlation_matrix(lf: pl.LazyFrame, plot_name: str) -> Figure:
    lf: pl.LazyFrame = lf.select(["review_length", "rating"])
    corr_matrix: np.ndarray = lf.collect().corr().to_numpy()
    print("Plotting Figure")
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
        width=600,
        height=600,
        template="ggplot2",
    )

    path = "data/processed/"
    print("Saving Figure")
    fig.write_html(f"{path}/html/{plot_name}.html", include_plotlyjs='cdn')
    fig.update_layout(width=800, height=800)
    fig.write_image(f"{path}/imgs/{plot_name}.png", width=1500)
    fig.write_image(f"{path}/docs/{plot_name}.pdf", width=1500)

    gc.collect()
    return fig
