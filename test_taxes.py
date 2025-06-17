import sys
import pytest
sys.path.append(".")
import taxes


class TestTax:
    """Test cases for the base Tax class."""
    
    def test_zero_income_fed_tax(self):
        """Test that zero income results in zero tax."""
        fed_tax = taxes.Tax(0, [0.0], [0.0], 0).calculate_tax()
        assert fed_tax == 0

    def test_basic_tax_calculation(self):
        """Test basic tax calculation with single bracket."""
        tax = taxes.Tax(50000, [float("inf")], [0.1], 0)
        assert tax.calculate_tax() == 5000.0

    def test_progressive_tax_brackets(self):
        """Test progressive tax calculation with multiple brackets."""
        # Income: 100000, brackets at 50000 and inf, rates 10% and 20%
        tax = taxes.Tax(100000, [50000, float("inf")], [0.1, 0.2], 0)
        expected = 50000 * 0.1 + 50000 * 0.2  # 5000 + 10000 = 15000
        assert tax.calculate_tax() == expected

    def test_tax_with_deductions(self):
        """Test tax calculation with deductions."""
        tax = taxes.Tax(50000, [float("inf")], [0.1], 10000)
        expected = 40000 * 0.1  # (50000 - 10000) * 0.1 = 4000
        assert tax.calculate_tax() == expected

    def test_deductions_exceed_income(self):
        """Test that deductions exceeding income result in zero taxable income."""
        tax = taxes.Tax(30000, [float("inf")], [0.1], 40000)
        assert tax.calculate_tax() == 0

    def test_negative_income_raises_error(self):
        """Test that negative income raises ValueError."""
        with pytest.raises(ValueError, match="Income cannot be negative"):
            taxes.Tax(-1000, [float("inf")], [0.1], 0)

    def test_negative_deductions_raises_error(self):
        """Test that negative deductions raise ValueError."""
        with pytest.raises(ValueError, match="Deductions cannot be negative"):
            taxes.Tax(50000, [float("inf")], [0.1], -1000)

    def test_empty_brackets_raises_error(self):
        """Test that empty brackets raise ValueError."""
        with pytest.raises(ValueError, match="Brackets and rates cannot be empty"):
            taxes.Tax(50000, [], [0.1], 0)

    def test_empty_rates_raises_error(self):
        """Test that empty rates raise ValueError."""
        with pytest.raises(ValueError, match="Brackets and rates cannot be empty"):
            taxes.Tax(50000, [float("inf")], [], 0)

    def test_mismatched_brackets_rates_raises_error(self):
        """Test that mismatched brackets and rates raise ValueError."""
        with pytest.raises(ValueError, match="Brackets and rates must have the same length"):
            taxes.Tax(50000, [10000, float("inf")], [0.1], 0)

    def test_income_exceeds_highest_bracket(self):
        """Test tax calculation when income exceeds the highest bracket."""
        tax = taxes.Tax(200000, [50000, 100000], [0.1, 0.2], 0)
        expected = 50000 * 0.1 + 50000 * 0.2 + 100000 * 0.2  # Uses last rate for excess
        assert tax.calculate_tax() == expected


class TestFederalTax:
    """Test cases for the FederalTax class."""
    
    def test_federal_tax_with_standard_deductions(self):
        """Test federal tax calculation with standard deductions and 401k."""
        fed_tax = taxes.FederalTax(100000, 20000)
        # Taxable income: 100000 - 29200 (std) - 20000 (401k) = 50800
        # Should fall in first bracket (10% up to 23200) and second bracket (12%)
        expected_tax = 23200 * 0.1 + (50800 - 23200) * 0.12
        assert fed_tax.calculate_tax() == expected_tax

    def test_federal_tax_zero_income(self):
        """Test federal tax with zero income."""
        fed_tax = taxes.FederalTax(0, 0)
        assert fed_tax.calculate_tax() == 0

    def test_federal_tax_high_income(self):
        """Test federal tax with high income across multiple brackets."""
        fed_tax = taxes.FederalTax(500000, 25000)
        assert fed_tax.calculate_tax() > 0


class TestStateTax:
    """Test cases for the StateTax class."""
    
    def test_zero_income_state_tax(self):
        """Test that zero income results in zero state tax."""
        tax = taxes.StateTax(0, 0, "PA")
        assert tax.calculate_tax() == 0

    def test_pa_state_tax(self):
        """Test Pennsylvania flat tax calculation."""
        tax = taxes.StateTax(100000, 0, "PA")
        expected = 100000 * 0.0307
        assert tax.calculate_tax() == expected

    def test_ny_state_tax(self):
        """Test New York progressive tax calculation."""
        tax = taxes.StateTax(50000, 10000, "NY")
        # Taxable income: 50000 - 16050 (std) - 10000 (401k) - 1000 (child) = 22950
        # First bracket: 17150 * 0.04 = 686
        # Second bracket: (22950 - 17150) * 0.045 = 261
        expected = 17150 * 0.04 + (22950 - 17150) * 0.045
        assert abs(tax.calculate_tax() - expected) < 0.01

    def test_unsupported_state_raises_error(self):
        """Test that unsupported state raises ValueError."""
        with pytest.raises(ValueError, match="Only.*are supported"):
            taxes.StateTax(50000, 0, "CA")


class TestLocalTax:
    """Test cases for the LocalTax class."""
    
    def test_pa_local_tax(self):
        """Test Pennsylvania local tax calculation."""
        tax = taxes.LocalTax(100000, "PA")
        expected = 100000 * 0.01
        assert tax.calculate_tax() == expected

    def test_ny_local_tax(self):
        """Test New York local tax calculation."""
        tax = taxes.LocalTax(100000, "NY")
        expected = 100000 * 0.04
        assert tax.calculate_tax() == expected

    def test_unsupported_state_local_tax_raises_error(self):
        """Test that unsupported state raises ValueError for local tax."""
        with pytest.raises(ValueError, match="Only.*are supported"):
            taxes.LocalTax(50000, "TX")


class TestSocialSecurityTax:
    """Test cases for the SocialSecurityTax class."""
    
    def test_social_security_under_cap(self):
        """Test Social Security tax calculation under income cap."""
        ss_tax = taxes.SocialSecurityTax(50000, 60000)
        expected = (50000 + 60000) * 0.062
        assert ss_tax.calculate_tax() == expected

    def test_social_security_over_cap(self):
        """Test Social Security tax calculation with income over cap."""
        ss_tax = taxes.SocialSecurityTax(200000, 180000)
        cap = 168600
        expected = (cap + cap) * 0.062  # Both incomes capped
        assert ss_tax.calculate_tax() == expected

    def test_social_security_mixed_cap(self):
        """Test Social Security tax with one income over cap, one under."""
        ss_tax = taxes.SocialSecurityTax(100000, 200000)
        cap = 168600
        expected = (100000 + cap) * 0.062
        assert ss_tax.calculate_tax() == expected

    def test_social_security_zero_income(self):
        """Test Social Security tax with zero income."""
        ss_tax = taxes.SocialSecurityTax(0, 0)
        assert ss_tax.calculate_tax() == 0


class TestMedicareTax:
    """Test cases for the MedicareTax class."""
    
    def test_medicare_under_threshold(self):
        """Test Medicare tax calculation under additional tax threshold."""
        medicare_tax = taxes.MedicareTax(200000)
        expected = 200000 * 0.0145
        assert medicare_tax.calculate_tax() == expected

    def test_medicare_over_threshold(self):
        """Test Medicare tax calculation over additional tax threshold."""
        medicare_tax = taxes.MedicareTax(300000)
        base_tax = 300000 * 0.0145
        additional_tax = (300000 - 250000) * 0.009
        expected = round(base_tax + additional_tax, 2)
        assert medicare_tax.calculate_tax() == expected

    def test_medicare_at_threshold(self):
        """Test Medicare tax calculation exactly at threshold."""
        medicare_tax = taxes.MedicareTax(250000)
        expected = 250000 * 0.0145
        assert medicare_tax.calculate_tax() == expected

    def test_medicare_zero_income(self):
        """Test Medicare tax with zero income."""
        medicare_tax = taxes.MedicareTax(0)
        assert medicare_tax.calculate_tax() == 0


class TestBudget:
    """Test cases for the Budget class."""
    
    def test_basic_budget_creation(self):
        """Test basic budget creation and total income calculation."""
        budget = taxes.Budget(100000, 80000, 5000, 20000, 15000, "PA")
        assert budget.total_income == 185000
        assert budget.contr401k1 == 20000
        assert budget.contr401k2 == 15000

    def test_budget_federal_tax(self):
        """Test budget federal tax calculation."""
        budget = taxes.Budget(100000, 80000, 5000, 20000, 15000, "PA")
        fed_tax = budget.federal_tax()
        assert fed_tax > 0
        assert isinstance(fed_tax, float)

    def test_budget_state_tax_pa(self):
        """Test budget PA state tax calculation."""
        budget = taxes.Budget(100000, 80000, 5000, 20000, 15000, "PA")
        state_tax = budget.state_tax()
        expected = 185000 * 0.0307
        assert state_tax == expected

    def test_budget_state_tax_ny(self):
        """Test budget NY state tax calculation."""
        budget = taxes.Budget(100000, 80000, 5000, 20000, 15000, "NY")
        state_tax = budget.state_tax()
        assert state_tax > 0
        assert isinstance(state_tax, float)

    def test_budget_local_tax(self):
        """Test budget local tax calculation (always PA)."""
        budget = taxes.Budget(100000, 80000, 5000, 20000, 15000, "NY")
        local_tax = budget.local_tax()
        expected = 185000 * 0.01  # Always PA rate
        assert local_tax == expected

    def test_budget_social_security_tax(self):
        """Test budget Social Security tax calculation."""
        budget = taxes.Budget(100000, 80000, 5000, 20000, 15000, "PA")
        ss_tax = budget.social_sec_tax()
        expected = (100000 + 80000) * 0.062
        assert ss_tax == expected

    def test_budget_medicare_tax(self):
        """Test budget Medicare tax calculation."""
        budget = taxes.Budget(100000, 80000, 5000, 20000, 15000, "PA")
        medicare_tax = budget.medicare_tax()
        expected = 185000 * 0.0145
        assert medicare_tax == expected

    def test_budget_total_tax(self):
        """Test budget total tax calculation."""
        budget = taxes.Budget(100000, 80000, 5000, 20000, 15000, "PA")
        total = budget.total_tax()
        individual_sum = (budget.federal_tax() + budget.state_tax() + 
                         budget.local_tax() + budget.social_sec_tax() + 
                         budget.medicare_tax())
        assert total == individual_sum

    def test_budget_effective_tax_rate(self):
        """Test budget effective tax rate calculation."""
        budget = taxes.Budget(100000, 80000, 5000, 20000, 15000, "PA")
        eff_rate = budget.eff_tax_rate()
        expected = round(budget.total_tax() / budget.total_income * 100, 2)
        assert eff_rate == expected
        assert 0 <= eff_rate <= 100

    def test_budget_tax_owed_calculations(self):
        """Test budget tax owed calculations with payments."""
        budget = taxes.Budget(100000, 80000, 5000, 20000, 15000, "PA",
                             fed_tax_paid=15000, state_tax_paid=5000, 
                             local_tax_paid=1000, social_sec_tax_paid=8000, 
                             medicare_tax_paid=2000)
        
        fed_owed = budget.federal_tax_owed()
        state_owed = budget.state_tax_owed()
        local_owed = budget.local_tax_owed()
        
        assert isinstance(fed_owed, float)
        assert isinstance(state_owed, float)
        assert isinstance(local_owed, float)

    def test_budget_zero_income(self):
        """Test budget with zero income."""
        budget = taxes.Budget(0, 0, 0, 0, 0, "PA")
        assert budget.total_income == 0
        assert budget.total_tax() == 0
        assert budget.eff_tax_rate() == 0  # This might cause division by zero, should be handled


# Run the existing tests for backward compatibility
def test_zero_income_fed_tax():
    fed_tax = taxes.Tax(0, [0.0], [0.0], 0).calculate_tax()
    assert fed_tax == 0


def test_zero_income_state_tax():
    tax = taxes.StateTax(0, 0, "PA").calculate_tax()
    assert tax == 0


if __name__ == "__main__":
    pytest.main([__file__])