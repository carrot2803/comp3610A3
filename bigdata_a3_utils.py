# uncomment the stuff below if you want to get rid of HF Symlink warning on Windows
# ====================================================================================
# import os
# os.environ['HF_HUB_DISABLE_SYMLINKS_WARNING'] = "1"
# ====================================================================================

import shutil
from pathlib import Path
import tarfile
from datasets import load_dataset, config, Dataset, DatasetDict, load_from_disk
from yaspin import yaspin
from typing import Optional, Union, List, Literal
import uuid

import warnings

warnings.filterwarnings("ignore", category=UserWarning, module="yaspin.core")

# Type alias for compression formats
CompressionFormat = Literal["gz", "bz2", "xz"]


def get_cache_directory(verbose: bool = True) -> Path:
    """
    Returns the current Hugging Face datasets cache directory as a Path object.

    Note:
    If you want to use a custom cache directory, you must set the
    HF_DATASETS_CACHE environment variable *before* importing anything from `datasets`.
    For example:

        import os
        os.environ["HF_DATASETS_CACHE"] = "C:\\your\\custom\\path"

        from datasets import load_dataset  # Import AFTER setting the env variable
    """
    cache_dir = Path(config.HF_DATASETS_CACHE)

    if verbose:
        print(f"[INFO] Current cache directory: {cache_dir}")

        print(
            "[NOTE] To use a custom cache directory, set HF_DATASETS_CACHE before importing datasets.\n"
            "Example:\n"
            "    import os\n"
            "    os.environ['HF_DATASETS_CACHE'] = 'C:\\\\your\\\\custom\\\\path'\n"
            "    from datasets import load_dataset\n"
        )

    return cache_dir


def delete_cache_directory() -> None:
    """
    Deletes the Hugging Face datasets cache directory using the path from datasets.config.
    """
    cache_path = Path(config.HF_DATASETS_CACHE)
    print(f"[INFO] Deleting Hugging Face cache at: {cache_path}")

    if cache_path.exists():
        shutil.rmtree(cache_path, ignore_errors=True)
        print("[SUCCESS] Cache directory deleted.")
    else:
        print(f"[WARNING] Cache directory does not exist: {cache_path}")


def default_cache_path() -> Path:
    """
    Returns and prints the default Hugging Face datasets cache path.
    """
    default_path = Path.home() / ".cache" / "huggingface" / "datasets"
    print(f'[INFO] Your default cache path: "{default_path}"')
    return default_path


# list of available categories
VALID_CATEGORIES = [
    "All_Beauty", "Amazon_Fashion", "Appliances", "Arts_Crafts_and_Sewing", "Automotive",
    "Baby_Products", "Beauty_and_Personal_Care", "Books", "CDs_and_Vinyl",
    "Cell_Phones_and_Accessories", "Clothing_Shoes_and_Jewelry", "Digital_Music", "Electronics",
    "Gift_Cards", "Grocery_and_Gourmet_Food", "Handmade_Products", "Health_and_Household",
    "Health_and_Personal_Care", "Home_and_Kitchen", "Industrial_and_Scientific", "Kindle_Store",
    "Magazine_Subscriptions", "Movies_and_TV", "Musical_Instruments", "Office_Products",
    "Patio_Lawn_and_Garden", "Pet_Supplies", "Software", "Sports_and_Outdoors",
    "Subscription_Boxes", "Tools_and_Home_Improvement", "Toys_and_Games", "Video_Games", "Unknown"
]


def compress_folder(folder: Path, compression_format: CompressionFormat = "gz", level: int = 6) -> Path:
    """
    Compress a folder into a tar.gz archive and delete the original folder.

    Args:
        folder: Path to the folder to compress
        compression_format: Compression format to use - "gz" (fastest), "bz2" (medium), "xz" (highest compression)
        level: Compression level (1-9, where 1 is fastest and 9 is highest compression)

    Returns:
        Path to the created archive
    """
    # validate compression level
    if not 1 <= level <= 9:
        raise ValueError(f"Compression level must be between 1 and 9, got {level}")

    # set correct file extension based on format
    if compression_format == "gz":
        ext = ".tar.gz"
        mode = f"w:gz"
    elif compression_format == "bz2":
        ext = ".tar.bz2"
        mode = f"w:bz2"
    elif compression_format == "xz":
        ext = ".tar.xz"
        mode = f"w:xz"
    else:
        raise ValueError(f"Unsupported compression format: {compression_format}")

    archive_path = folder.with_suffix(ext)

    # gzip allows us to set compression level directly
    if compression_format == "gz":
        with tarfile.open(archive_path, mode, compresslevel=level) as tar:
            tar.add(folder, arcname=folder.name)
    else:
        # For bz2 and xz, we need to handle differently
        with tarfile.open(archive_path, mode) as tar:
            tar.add(folder, arcname=folder.name)

        # Display info about compression format
        print(f"[INFO] Using {compression_format.upper()} compression (level {level}) - this may take some time...")

    # Remove the original folder after successful compression
    shutil.rmtree(folder)
    return archive_path


def process_dataset(dataset_type: str, category: str, base_save_path: Path, compress: bool, compression_format: CompressionFormat = "gz", compression_level: int = 6) -> str:
    """
    Download and save a specific dataset type for a category.

    Args:
        dataset_type: Type of dataset ("review" or "meta")
        category: Category name
        base_save_path: Base path to save datasets
        compress: Whether to compress the dataset after downloading
        compression_format: Format to use for compression ("gz", "bz2", or "xz")
        compression_level: Compression level (1-9, where 9 is highest compression)
    """
    folder_name = f"raw_{dataset_type}_{category}"
    dataset_path = base_save_path / folder_name

    # check for existing files with any of the possible extensions
    compressed_paths = [
        dataset_path.with_suffix(".tar.gz"),
        dataset_path.with_suffix(".tar.bz2"),
        dataset_path.with_suffix(".tar.xz")
    ]

    # skip if already exists in any format
    if dataset_path.exists() or any(path.exists() for path in compressed_paths):
        return f"[SKIP] {folder_name} already exists"

    # download and save
    dataset = load_dataset(
        "McAuley-Lab/Amazon-Reviews-2023",
        f"raw_{dataset_type}_{category}",
        trust_remote_code=True
    )
    dataset_path.mkdir(parents=True, exist_ok=True)
    dataset.save_to_disk(str(dataset_path))

    # compress if requested
    if compress:
        compress_folder(dataset_path, compression_format=compression_format, level=compression_level)
        return f"[DONE] {folder_name} downloaded and compressed with {compression_format.upper()} level {compression_level}"

    return f"[DONE] {folder_name} downloaded"


def download_all_amazon_reviews(base_save_path: Union[str, Path], categories: Optional[List[str]] = None, compress: bool = False, compression_format: CompressionFormat = "gz", compression_level: int = 6) -> None:
    """
    Download Amazon review datasets for specified categories.

    Args:
        base_save_path: Directory to save the datasets
        categories: List of categories to download (defaults to all)
        compress: Whether to compress each dataset after downloading
        compression_format: Format to use for compression ("gz", "bz2", or "xz")
            - "gz": Fastest compression, moderate file size (default)
            - "bz2": Medium compression speed, smaller file size
            - "xz": Slowest compression, smallest file size
        compression_level: Compression level (1-9)
            - 1: Fastest compression, largest file size
            - 9: Slowest compression, smallest file size
            - Default is 6 for a balance of speed and size

    Raises:
        ValueError: If invalid categories are specified or if paths overlap
    """
    # validate categories
    if categories is None:
        categories = VALID_CATEGORIES
    else:
        invalid = set(categories) - set(VALID_CATEGORIES)
        if invalid:
            raise ValueError(f"Invalid categories: {invalid}")

    # validate compression options
    if not 1 <= compression_level <= 9:
        raise ValueError(f"Compression level must be between 1 and 9, got {compression_level}")

    if compression_format not in ["gz", "bz2", "xz"]:
        raise ValueError(f"Unsupported compression format: {compression_format}. Use 'gz', 'bz2', or 'xz'")

    hf_datasets_cache = get_cache_directory(verbose=False)
    base_save_path = Path(base_save_path).resolve()
    cache_path = Path(hf_datasets_cache).expanduser().resolve()

    # check for path overlap
    if (base_save_path == cache_path or
            base_save_path in cache_path.parents or
            cache_path in base_save_path.parents):
        raise ValueError("❌ base_save_path and HF_DATASETS_CACHE must be separate and non-overlapping.")

    # create base dir if it doesn't exist
    base_save_path.mkdir(parents=True, exist_ok=True)

    # process each category
    successful = []
    failed = []

    # print compression info if compressing
    if compress:
        print(f"[INFO] Using {compression_format.upper()} compression at level {compression_level}")
        print(
            f"[INFO] Compression speed: {'Fast' if compression_level < 4 else 'Medium' if compression_level < 7 else 'Slow'}")
        print(
            f"[INFO] Compression ratio: {'Low' if compression_level < 4 else 'Medium' if compression_level < 7 else 'High'}")

    for category in categories:
        with yaspin(text=f"Processing {category}") as spinner:
            try:
                # review dataset
                review_result = process_dataset(
                    "review",
                    category,
                    base_save_path,
                    compress,
                    compression_format,
                    compression_level
                )
                spinner.write(review_result)

                # meta dataset
                meta_result = process_dataset(
                    "meta",
                    category,
                    base_save_path,
                    compress,
                    compression_format,
                    compression_level
                )
                spinner.write(meta_result)

                spinner.ok("✅")
                successful.append(category)
            except Exception as e:
                spinner.fail("💥")
                spinner.write(f"Failed to process category '{category}': {str(e)}")
                failed.append((category, str(e)))
            finally:
                # clean up cache after each category
                if cache_path.exists():
                    shutil.rmtree(cache_path, ignore_errors=True)

    # print summary
    print(f"\n🎉 Download summary:")
    print(f"  - Successfully processed: {len(successful)}/{len(categories)} categories")
    if failed:
        print(f"  - Failed: {len(failed)}/{len(categories)} categories")
        for category, error in failed:
            print(f"    - {category}: {error}")


def load_compressed_dataset(compressed_path: Union[str, Path], extract_dir: Optional[Union[str, Path]] = None, cleanup_after_load: bool = True) -> Union[Dataset, DatasetDict]:
    """
    Load a dataset from a compressed archive (tar.gz, tar.bz2, or tar.xz).

    Args:
        compressed_path: Path to the compressed dataset file
        extract_dir: Directory to extract files to (defaults to a temporary directory)
        cleanup_after_load: Whether to delete the extracted files after loading
                           (only applies to auto-generated temp directories)

    Returns:
        The loaded dataset (Dataset or DatasetDict)

    Raises:
        ValueError: If the file doesn't exist or isn't a supported compressed file
    """
    compressed_path = Path(compressed_path)

    if not compressed_path.exists():
        raise ValueError(f"File not found: {compressed_path}")

    # check file extension
    valid_extensions = [".tar.gz", ".tar.bz2", ".tar.xz"]
    is_valid = False

    for ext in valid_extensions:
        if compressed_path.name.endswith(ext):
            is_valid = True
            break

    if not is_valid:
        raise ValueError(f"Expected a compressed tar file (.tar.gz, .tar.bz2, or .tar.xz), got: {compressed_path}")

    # get the expected directory name (remove the extension)
    dir_name = compressed_path.name
    for ext in valid_extensions:
        if dir_name.endswith(ext):
            dir_name = dir_name[:-len(ext)]
            break

    # create extraction directory
    is_temp_dir = extract_dir is None
    if is_temp_dir:
        extract_dir = compressed_path.parent / f"temp_{uuid.uuid4().hex}"
    else:
        extract_dir = Path(extract_dir)

    extract_dir.mkdir(parents=True, exist_ok=True)

    try:
        # extract archive
        print(f"Extracting {compressed_path} to {extract_dir}...")
        with tarfile.open(compressed_path, "r:*") as tar:
            tar.extractall(path=extract_dir)

        # dataset should be in a subdirectory matching the original directory name
        dataset_dir = extract_dir / dir_name

        if not dataset_dir.exists():
            # try to find any directory
            extracted_folders = [f for f in extract_dir.iterdir() if f.is_dir()]
            if not extracted_folders:
                raise ValueError(f"No folders found in extracted archive: {compressed_path}")
            dataset_dir = extracted_folders[0]
            print(f"Using extracted directory: {dataset_dir}")

        # load dataset
        print(f"Loading dataset from {dataset_dir}...")
        dataset = load_from_disk(str(dataset_dir))

        return dataset

    finally:
        # clean up only if it's a temporary directory we created AND cleanup is requested
        if cleanup_after_load and is_temp_dir and extract_dir.exists():
            print(f"Cleaning up temporary directory: {extract_dir}")
            shutil.rmtree(extract_dir)