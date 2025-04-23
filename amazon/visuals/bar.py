from plotly.graph_objs._figure import Figure
import polars as pl
import plotly.express as px
import gc

def plot_categories_bar(lf: pl.LazyFrame, plot_name: str) -> Figure:
    lf: pl.LazyFrame = lf.with_columns(
        pl.col("main_category").fill_null(pl.col("main_category")).alias("category")
    )
    lf = lf.group_by("category").agg(pl.len()).sort("len", descending=True).head(10)
    top_categories: pl.DataFrame = lf.collect()
    print("Plotting Figure")
    fig: Figure = px.bar(
        top_categories,
        x="len",
        y="category",
        height=800,
        color="category",
        color_discrete_sequence=px.colors.qualitative.Prism,
        orientation="h",
        template="ggplot2",
    )

    del top_categories

    fig.update_layout(
        title_font_size=22,
        title="Top 10 Categories",
        xaxis_title="Category",
        yaxis_title="Total Review Count",
    )

    path = "data/processed/"
    print("Saving Figure")
    fig.write_html(f"{path}/html/{plot_name}.html", include_plotlyjs='cdn')
    fig.write_image(f"{path}/imgs/{plot_name}.png", width=1500)
    fig.write_image(f"{path}/docs/{plot_name}.pdf", width=1500)

    gc.collect()
    return fig


def plot_brands_bar(lf: pl.LazyFrame, plot_name: str) -> Figure:
    lf: pl.LazyFrame = lf.filter(~(pl.col("brand") == "Unknown"))
    lf = lf.group_by("brand").agg(pl.len())
    lf = lf.sort("len", descending=True).head(10)

    top_brands: pl.DataFrame = lf.collect()
    print("Plotting Figure")
    fig: Figure = px.bar(
        top_brands,
        y="len",
        x="brand",
        height=800,
        color="brand",
        color_discrete_sequence=px.colors.qualitative.Prism,
        template="ggplot2",
    )

    del top_brands

    fig.update_layout(
        title_font_size=22,
        title="Top 10 Brands",
        xaxis_title="Brand",
        yaxis_title="Total Review Count",
    )

    path = "data/processed/"
    print("Saving Figure")
    fig.write_html(f"{path}/html/{plot_name}.html", include_plotlyjs='cdn')
    fig.write_image(f"{path}/imgs/{plot_name}.png", width=1500)
    fig.write_image(f"{path}/docs/{plot_name}.pdf", width=1500)
    gc.collect()
    return fig
