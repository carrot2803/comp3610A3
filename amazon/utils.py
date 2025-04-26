import gc
import os
from pathlib import Path
import shutil
from datasets import load_dataset, Dataset, config


def load_amazon_dataset(category: str, type: str, ram: bool = False) -> Dataset:
    return load_dataset(
        "McAuley-Lab/Amazon-Reviews-2023",
        f"raw_{type}_{category}",
        split="full",
        trust_remote_code=True,
        keep_in_memory=ram,
    )


def download_data(category: str, type: str, ram: bool = False) -> None:
    path: str = f"data/raw/{type}/{category}.parquet"
    if os.path.exists(path):
        print(f"File already exists: {path}. Skipping.")
        return

    print(f"Downloading {category} ({type})...")
    data_set: Dataset = load_amazon_dataset(category, type, ram)
    data_set.to_parquet(path)
    del data_set
    cache_path = Path(config.HF_DATASETS_CACHE)
    shutil.rmtree(cache_path, ignore_errors=True)
    gc.collect()


def create_directories(paths: list[str]) -> None:
    for path in paths:
        os.makedirs(path, exist_ok=True)


def get_cache_directory() -> None:
    print(Path(config.HF_DATASETS_CACHE))
