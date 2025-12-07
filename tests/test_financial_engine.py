"""Tests for the FinancialEngine class."""

import pytest
import numpy as np
from src.financial_engine import FinancialEngine


@pytest.fixture
def engine():
    """Create a FinancialEngine instance for testing."""
    return FinancialEngine()


class TestPayment:
    """Tests for the payment() method."""

    def test_basic_payment(self, engine):
        """Test basic monthly payment calculation."""
        # $50,000 at 5% for 36 months
        payment = engine.payment(principal=50000, rate=0.05, periods=36)
        # Expected: approximately $1498.88
        assert abs(payment - 1498.88) < 0.01

    def test_zero_rate_payment(self, engine):
        """Test payment with zero interest rate."""
        payment = engine.payment(principal=12000, rate=0, periods=12)
        assert payment == 1000.0

    def test_mortgage_payment(self, engine):
        """Test typical mortgage payment."""
        # $300,000 at 6.5% for 30 years
        payment = engine.payment(principal=300000, rate=0.065, periods=360)
        # Expected: approximately $1896.20
        assert abs(payment - 1896.20) < 0.01


class TestMaxPrincipal:
    """Tests for the max_principal() method."""

    def test_basic_max_principal(self, engine):
        """Test maximum principal calculation."""
        # Can afford $500/month at 5% for 60 months
        max_loan = engine.max_principal(payment=500, rate=0.05, periods=60)
        # Expected: approximately $26,485
        assert abs(max_loan - 26485) < 1

    def test_zero_rate_max_principal(self, engine):
        """Test max principal with zero interest rate."""
        max_loan = engine.max_principal(payment=1000, rate=0, periods=12)
        assert max_loan == 12000.0

    def test_roundtrip_payment_principal(self, engine):
        """Test that payment and max_principal are inverse operations."""
        principal = 50000
        rate = 0.06
        periods = 48

        payment = engine.payment(principal, rate, periods)
        recovered_principal = engine.max_principal(payment, rate, periods)

        assert abs(principal - recovered_principal) < 0.01


class TestInterestPrincipalPayment:
    """Tests for interest_payment() and principal_payment() methods."""

    def test_first_payment_breakdown(self, engine):
        """Test that first payment = interest + principal."""
        principal = 25000
        rate = 0.059
        periods = 60

        payment = engine.payment(principal, rate, periods)
        first_interest = engine.interest_payment(principal, rate, 1, periods)
        first_principal = engine.principal_payment(principal, rate, 1, periods)

        assert abs(payment - (first_interest + first_principal)) < 0.01

    def test_last_payment_breakdown(self, engine):
        """Test that last payment = interest + principal."""
        principal = 25000
        rate = 0.059
        periods = 60

        payment = engine.payment(principal, rate, periods)
        last_interest = engine.interest_payment(principal, rate, periods, periods)
        last_principal = engine.principal_payment(principal, rate, periods, periods)

        assert abs(payment - (last_interest + last_principal)) < 0.01

    def test_interest_decreases_over_time(self, engine):
        """Test that interest portion decreases over loan term."""
        principal = 50000
        rate = 0.07
        periods = 60

        first_interest = engine.interest_payment(principal, rate, 1, periods)
        last_interest = engine.interest_payment(principal, rate, periods, periods)

        assert first_interest > last_interest

    def test_principal_increases_over_time(self, engine):
        """Test that principal portion increases over loan term."""
        principal = 50000
        rate = 0.07
        periods = 60

        first_principal = engine.principal_payment(principal, rate, 1, periods)
        last_principal = engine.principal_payment(principal, rate, periods, periods)

        assert last_principal > first_principal


class TestRemainingBalance:
    """Tests for the remaining_balance() method."""

    def test_initial_balance(self, engine):
        """Test balance at period 0 equals principal."""
        principal = 50000
        balance = engine.remaining_balance(principal, 0.05, 0, 36)
        assert balance == principal

    def test_final_balance(self, engine):
        """Test balance at final period is zero."""
        principal = 50000
        rate = 0.05
        periods = 36

        balance = engine.remaining_balance(principal, rate, periods, periods)
        assert abs(balance) < 0.01

    def test_balance_decreases(self, engine):
        """Test that balance decreases over time."""
        principal = 50000
        rate = 0.05
        periods = 36

        balance_10 = engine.remaining_balance(principal, rate, 10, periods)
        balance_20 = engine.remaining_balance(principal, rate, 20, periods)

        assert balance_10 > balance_20


class TestAmortizationTable:
    """Tests for the amortization_table() method."""

    def test_table_shape(self, engine):
        """Test that table has correct shape."""
        table = engine.amortization_table(50000, 0.05, 36)

        assert len(table) == 36
        assert list(table.columns) == ["month", "payment", "principal", "interest", "balance"]

    def test_table_final_balance_zero(self, engine):
        """Test that final balance is zero."""
        table = engine.amortization_table(50000, 0.05, 36)
        assert table.iloc[-1]["balance"] == 0

    def test_table_payments_sum(self, engine):
        """Test that principal payments sum to original principal."""
        principal = 50000
        table = engine.amortization_table(principal, 0.05, 36)
        total_principal = table["principal"].sum()

        assert abs(total_principal - principal) < 0.01

    def test_zero_rate_table(self, engine):
        """Test amortization table with zero interest."""
        principal = 12000
        periods = 12
        table = engine.amortization_table(principal, 0, periods)

        assert len(table) == periods
        assert all(table["interest"] == 0)
        assert all(table["payment"] == 1000)
        assert table.iloc[-1]["balance"] == 0


class TestEdgeCases:
    """Tests for edge cases and error handling."""

    def test_very_high_rate(self, engine):
        """Test with very high interest rate."""
        payment = engine.payment(10000, 0.24, 12)  # 24% APR
        assert payment > 0
        assert not np.isnan(payment)

    def test_very_long_term(self, engine):
        """Test with very long loan term (40 years)."""
        payment = engine.payment(500000, 0.05, 480)
        assert payment > 0
        assert not np.isnan(payment)

    def test_small_principal(self, engine):
        """Test with small principal amount."""
        payment = engine.payment(100, 0.05, 12)
        assert payment > 0
        assert abs(payment - 8.56) < 0.01
