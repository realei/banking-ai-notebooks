"""Banking AI Notebooks - Financial calculation utilities."""

from .financial_engine import FinancialEngine, engine
from .utils import is_kaggle, is_colab, get_environment, setup_environment

__all__ = [
    "FinancialEngine",
    "engine",
    "is_kaggle",
    "is_colab",
    "get_environment",
    "setup_environment",
]
__version__ = "0.1.0"
