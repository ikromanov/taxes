import sys
sys.path.append(".")
import taxes

def test_zero_income_fed_tax():
    fed_tax = taxes.Tax(0,[0.0], [0.0], 0).calculate_tax()
    assert fed_tax == 0

def test_zero_income_state_tax():
    tax = taxes.StateTax(0,0,"PA").calculate_tax()
    assert tax == 0

test_zero_income_fed_tax()
test_zero_income_state_tax()


