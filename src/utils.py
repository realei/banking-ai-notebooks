"""Utility functions for environment detection and path handling.

This module provides utilities to detect whether code is running
on Kaggle or locally, and handles path differences accordingly.
"""

import os
import sys
from pathlib import Path


def is_kaggle() -> bool:
    """Detect if running in Kaggle environment.

    Returns:
        True if running on Kaggle, False otherwise.
    """
    return "KAGGLE_KERNEL_RUN_TYPE" in os.environ


def is_colab() -> bool:
    """Detect if running in Google Colab environment.

    Returns:
        True if running on Colab, False otherwise.
    """
    return "COLAB_GPU" in os.environ or "google.colab" in sys.modules


def get_environment() -> str:
    """Get the current execution environment name.

    Returns:
        One of: 'kaggle', 'colab', 'local'
    """
    if is_kaggle():
        return "kaggle"
    elif is_colab():
        return "colab"
    else:
        return "local"


def get_data_path(filename: str = "") -> Path:
    """Get the appropriate data path based on environment.

    Args:
        filename: Optional filename to append to the data path.

    Returns:
        Path object pointing to the data directory or file.

    Examples:
        >>> get_data_path()
        Path('/kaggle/input')  # on Kaggle
        Path('data')           # locally

        >>> get_data_path('loans.csv')
        Path('/kaggle/input/loans.csv')  # on Kaggle
        Path('data/loans.csv')           # locally
    """
    if is_kaggle():
        base = Path("/kaggle/input")
    elif is_colab():
        base = Path("/content/drive/MyDrive/data")
    else:
        # Local: relative to project root
        base = Path(__file__).parent.parent / "data"

    return base / filename if filename else base


def get_output_path(filename: str = "") -> Path:
    """Get the appropriate output path based on environment.

    Args:
        filename: Optional filename to append to the output path.

    Returns:
        Path object pointing to the output directory or file.
    """
    if is_kaggle():
        base = Path("/kaggle/working")
    elif is_colab():
        base = Path("/content")
    else:
        base = Path(__file__).parent.parent / "output"

    # Create directory if it doesn't exist (for local)
    if not is_kaggle() and not is_colab():
        base.mkdir(parents=True, exist_ok=True)

    return base / filename if filename else base


def setup_environment():
    """Setup the environment for notebook execution.

    This function:
    1. Prints the detected environment
    2. Adds the src directory to Python path (for local development)
    3. Returns environment info dict

    Returns:
        Dictionary with environment information.

    Example usage in notebook:
        >>> from src.utils import setup_environment
        >>> env = setup_environment()
        Environment: local
        >>> env['name']
        'local'
    """
    env_name = get_environment()
    print(f"Environment: {env_name}")

    # For local development, ensure src is in path
    if env_name == "local":
        src_path = Path(__file__).parent
        if str(src_path) not in sys.path:
            sys.path.insert(0, str(src_path.parent))

    return {
        "name": env_name,
        "is_kaggle": is_kaggle(),
        "is_colab": is_colab(),
        "data_path": get_data_path(),
        "output_path": get_output_path(),
    }


# Convenience: print environment on import if running interactively
if __name__ == "__main__":
    env = setup_environment()
    print(f"Data path: {env['data_path']}")
    print(f"Output path: {env['output_path']}")
