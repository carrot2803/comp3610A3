import gc
import polars as pl
import plotly.express as px
from plotly.graph_objs import Figure
import numpy as np
from nltk.sentiment.vader import SentimentIntensityAnalyzer


def analysis(reviews: pl.Series) -> pl.Series:
    analyzer = SentimentIntensityAnalyzer()

    def scale_sentiment(review: str) -> float:
        # normalize polarity score from [-1, 1] to [1, 5]
        polarity: dict[str, float] = analyzer.polarity_scores(review)
        compound_score: float = polarity["compound"]
        return round(1 + (compound_score + 1) * 2)

    return reviews.map_elements(scale_sentiment, pl.Float64)


def get_sentiment(lf: pl.LazyFrame, cache: bool = False) -> pl.DataFrame:
    path: str = "data/processed/rating_cache.parquet"
    if cache == True:
        return pl.read_parquet(path)
    expr: pl.Expr = pl.col("text").map_batches(analysis).alias("sentiment_rating")
    lf = lf.select(["rating", expr]).collect()
    lf.write_parquet(path)
    return lf


def plot_sentiment(lf: pl.LazyFrame, plot_name: str, cache: bool = False) -> Figure:
    bin: np.ndarray = np.arange(1, 6)
    sentiment_df: pl.DataFrame = get_sentiment(lf, cache)
    print("Plotting Figure")
    fig: Figure = px.box(
        sentiment_df,
        x="rating",
        y="sentiment_rating",
        color="rating",
        color_discrete_sequence=px.colors.qualitative.Prism,
        category_orders={"rating": bin},
        template="ggplot2",
    )

    print("Saving Figure")
    fig.update_layout(
        title=f"Discrepancy Between User Rating and Review Sentiment (Purchase Sample={len(sentiment_df)})",
        xaxis_title="Star Rating (1-5)",
        yaxis_title="Sentiment",
    )
    del sentiment_df
    path = "data/processed/"

    fig.update_layout(height=625)
    fig.write_html(f"{path}/html/{plot_name}.html", include_plotlyjs='cdn')
    fig.update_layout(height=800)
    fig.write_image(f"{path}/imgs/{plot_name}.png", width=1500)
    fig.write_image(f"{path}/docs/{plot_name}.pdf", width=1500)
    
    gc.collect()
    return fig


def plot_verified_purchase(lf: pl.LazyFrame, plot_name: str) -> Figure:
    columns: list[str] = ["verified_purchase", "rating"]
    verified_purchase: pl.DataFrame = lf.select(columns).collect()
    print("Plotting Figure")
    fig: Figure = px.box(
        verified_purchase,
        x="verified_purchase",
        y="rating",
        category_orders={"rating": [1, 2, 3, 4, 5]},
        color="verified_purchase",
        color_discrete_sequence=px.colors.qualitative.Prism,
        template="ggplot2",
    )


    fig.update_layout(
        title=f"Distribution of Star Ratings Across Verified (Purchase Sample={len(verified_purchase)})",
        xaxis_title="Verified Purchase",
        yaxis_title="Star Rating",
    )
    del verified_purchase

    path: str = "data/processed/"
    print("Saving Figure")

    fig.update_layout(height=625)
    fig.write_html(f"{path}/html/{plot_name}.html", include_plotlyjs='cdn')
    fig.update_layout(height=800)
    fig.write_image(f"{path}/imgs/{plot_name}.png", width=1500)
    fig.write_image(f"{path}/docs/{plot_name}.pdf", width=1500)

    gc.collect()
    return fig
