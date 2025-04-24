import polars as pl
from sklearn.metrics import accuracy_score, f1_score, recall_score
from sklearn.metrics import confusion_matrix, precision_score, roc_auc_score
import polars as pl
import numpy as np
import plotly.express as px
from plotly.graph_objs._figure import Figure


def get_metrics(y_true: np.ndarray, y_pred: np.ndarray, model_name: str) -> dict:
    tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()
    return {
        "Model": model_name,
        "Accuracy": accuracy_score(y_true, y_pred),
        "Precision": precision_score(y_true, y_pred, zero_division=1),
        "Recall": recall_score(y_true, y_pred),
        "F1 Score": f1_score(y_true, y_pred),
        "True Negative": tn,
        "False Positive": fp,
        "False Negative": fn,
        "True Positive": tp,
    }

def plot_confusion_matrix(result: pl.DataFrame) -> Figure:
    row = result.row(0)
    tn: int = result.select("True Negative").item()
    fp: int = result.select("False Positive").item()
    fn: int = result.select("False Negative").item()
    tp: int = result.select("True Positive").item()
    model_name: str = result.select("Model").item()

    conf_matrix: list[list[int]] = [[tp, fn], [fp, tn]]
    labels: list[str] = ["Positive", "Negative"]

    fig: Figure = px.imshow(
        conf_matrix,
        x=[f"Pred: {l}" for l in labels],
        y=[f"True: {l}" for l in labels],
        color_continuous_scale="Blues",
        text_auto=True,
        labels={"color": "Count"},
        title=f"Confusion Matrix: {model_name}",
        height=700,
        width=700,
    )

    fig.update_layout(
        xaxis_title="Predicted Label",
        yaxis_title="True Label"
    )

    path = "data/processed"
    fig.write_html(f"{path}/html/linear_regression.html", include_plotlyjs='cdn')
    fig.write_image(f"{path}/imgs/linear_regression.png", width=1500)
    fig.write_image(f"{path}/docs/linear_regression.pdf", width=1500)

    return fig
