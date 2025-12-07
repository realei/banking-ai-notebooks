# banking-ai-notebooks

A comprehensive collection of Python notebooks teaching financial calculations using `numpy_financial`. From basic time value of money to advanced investment analysis, with real-world examples and professional visualizations.

## Notebooks

| # | Title | Topics | Key Functions |
|---|-------|--------|---------------|
| 01 | [Numpy Financial Fundamentals](notebooks/01-numpy-financial-fundamentals.ipynb) | Loan calculations, Amortization, Financial Planning Tools | `pmt`, `pv`, `ipmt`, `ppmt` |

## Features

- **Bilingual Content**: English and Chinese explanations
- **Professional Visualizations**: matplotlib charts for clear insights
- **SOLID Design**: Clean, maintainable `FinancialEngine` class
- **Performance Optimized**: Vectorized operations for speed
- **Real-world Examples**: Practical loan and affordability scenarios
- **Dual Environment**: Works in both VS Code and Kaggle

## Project Structure

```
banking-ai-notebooks/
├── notebooks/              # Jupyter notebooks (for Kaggle)
│   └── 01-numpy-financial-fundamentals.ipynb
├── src/                    # Reusable Python modules
│   ├── __init__.py
│   ├── financial_engine.py # Core financial calculations
│   └── utils.py            # Environment detection utilities
├── tests/                  # Unit tests
│   └── test_financial_engine.py
├── pyproject.toml          # Project configuration (uv/pip)
├── requirements.txt        # Kaggle-compatible dependencies
└── README.md
```

## Development Setup

### Prerequisites

- Python 3.10+
- [uv](https://github.com/astral-sh/uv) (recommended) or pip

### Using uv (Recommended)

```bash
# Install uv if you haven't
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone the repository
git clone https://github.com/realei/banking-ai-notebooks.git
cd banking-ai-notebooks

# Create virtual environment and install dependencies
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -e ".[dev]"

# Install Jupyter kernel
python -m ipykernel install --user --name=banking-ai --display-name="Banking AI"
```

### Using pip

```bash
# Clone the repository
git clone https://github.com/realei/banking-ai-notebooks.git
cd banking-ai-notebooks

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -e ".[dev]"

# Install Jupyter kernel
python -m ipykernel install --user --name=banking-ai --display-name="Banking AI"
```

### Running Notebooks in VS Code

1. Open the project in VS Code
2. Install the "Jupyter" extension if not already installed
3. Open any notebook in `notebooks/`
4. Select the "Banking AI" kernel (or your .venv Python)
5. Run all cells

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src

# Run specific test file
pytest tests/test_financial_engine.py -v
```

## Kaggle Integration

The notebooks are designed to work seamlessly on Kaggle:

1. **Upload to Kaggle**: Go to [kaggle.com/code](https://www.kaggle.com/code) → "New Notebook"
2. **Upload File**: Upload the notebook from `notebooks/`
3. **Run**: The notebook automatically detects the Kaggle environment and installs dependencies

### Environment Detection

The notebooks automatically detect the environment:

```python
# Runs automatically at the start of each notebook
IS_KAGGLE = "KAGGLE_KERNEL_RUN_TYPE" in os.environ
IS_COLAB = "COLAB_GPU" in os.environ
ENV_NAME = "kaggle" if IS_KAGGLE else ("colab" if IS_COLAB else "local")
```

## Financial Planning Tools

The notebooks include ready-to-use financial planning tools:

| Tool | Purpose |
|------|---------|
| 🏠 Home Buying Planner | Calculate affordable home price based on income |
| 🚗 Car Loan Comparison | Compare different loan terms and total costs |
| 💰 Early Payoff Calculator | See savings from extra monthly payments |
| 🎯 Savings Goal Calculator | Plan monthly savings to reach financial goals |
| 📊 Loan Dashboard | Comprehensive loan visualization |

## Using the FinancialEngine

```python
from src.financial_engine import engine

# Calculate monthly payment
payment = engine.payment(principal=50000, rate=0.05, periods=36)
print(f"Monthly payment: ${payment:,.2f}")  # $1,498.88

# Calculate max loan for a given payment
max_loan = engine.max_principal(payment=500, rate=0.06, periods=60)
print(f"Max loan: ${max_loan:,.2f}")  # $25,862.78

# Generate amortization schedule
schedule = engine.amortization_table(principal=50000, rate=0.05, periods=36)
print(schedule.head())
```

## Related Projects

- [personal-loan-advisor-agent](https://github.com/realei/personal-loan-advisor-agent) - AI-powered loan advisor using the FinancialEngine

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

MIT
