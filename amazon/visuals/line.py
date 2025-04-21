from plotly.graph_objs._figure import Figure
import polars as pl
import plotly.express as px


def plot_line(lf: pl.LazyFrame, plot_name: str) -> Figure:
    lf: pl.LazyFrame = lf.select(["rating", "year"]).group_by("year")
    lf = lf.agg(pl.mean("rating")).sort("year")
    ratings_by_year: pl.DataFrame = lf.collect()

    fig: Figure = px.line(
        ratings_by_year,
        x="year",
        y="rating",
        markers=True,
        height=800,
        template="ggplot2",
    )

    fig.update_layout(
        title="Average Star Rating Per Year",
        title_font_size=22,
        xaxis_title="Year",
        yaxis_title="Average Rating",
    )

    x_min: float = ratings_by_year["year"].min() - 0.2
    x_max: float = ratings_by_year["year"].max() + 0.2
    del ratings_by_year

    fig.update_xaxes(range=[x_min, x_max], dtick=1)
    fig.update_yaxes(tickformat=".3f")

    path = "data/processed/plots/"
    path += plot_name

    fig.write_html(f"{path}.html")
    fig.write_image(f"{path}.png", width=1500)
    fig.write_image(f"{path}.pdf", width=1500)
    return fig


def price_rating(lf: pl.LazyFrame, plot_name: str) -> Figure:
    expr: pl.Expr = pl.col("price").str.contains(r"^\d+.?\d*$")
    lf: pl.LazyFrame = lf.filter(expr).select(["rating", "price"])
    lf = lf.cast(pl.Float64).group_by("rating").agg(pl.mean("price"))

    price_by_rating: pl.DataFrame = lf.sort("rating").collect()

    fig: Figure = px.line(
        price_by_rating,
        x="rating",
        y="price",
        markers=True,
        height=800,
        template="ggplot2",
    )

    del price_by_rating

    fig.update_layout(
        title="Average Price Per Rating",
        title_font_size=22,
        xaxis_title="Rating",
        yaxis_title="Average Price",
    )

    fig.update_xaxes(range=[0.5, 5.5], dtick=1)
    fig.update_yaxes(tickformat="$.2f")

    path = "data/processed/plots/"
    path += plot_name

    fig.write_html(f"{path}.html")
    fig.write_image(f"{path}.png", width=1500)
    fig.write_image(f"{path}.pdf", width=1500)
    return fig

