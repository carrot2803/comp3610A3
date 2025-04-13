import gc
import os
from datasets import load_dataset, Dataset


def create_directories(paths: list[str]) -> None:
    for path in paths:
        os.makedirs(path, exist_ok=True)


def load_amazon_dataset(category: str, type: str) -> Dataset:
    return load_dataset(
        "McAuley-Lab/Amazon-Reviews-2023",
        f"raw_{type}_{category}",
        split="full",
        trust_remote_code=True,
    )


def download_data(category: str, type: str) -> None:
    path: str = f"data/raw/{type}/{category}.parquet"
    if os.path.exists(path):
        print(f"File already exists: {path}. Skipping.")
        return

    print(f"Downloading {category} ({type})...")
    data_set: Dataset = load_amazon_dataset(category, type)
    data_set.to_parquet(path)
    del data_set
    gc.collect()
