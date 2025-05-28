import sys
sys.path.append(".")
import taxes

def test_zero_income_fed_tax():
    fed_tax = taxes.Tax(0,0,0, "PA").fed_amount()
    assert fed_tax == 0

def test_zero_income_state_tax():
    tax = taxes.Tax(0,0,0, "PA").state_amount()
    assert tax == 0

