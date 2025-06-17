
from __future__ import annotations

class Tax:
    """
    A simple tax calculator that supports progressive tax brackets and optional deductions.
    """

    def __init__(self, income: float, brackets: list[float], rates: list[float], deductions: float = 0.0):
        """
        Initialize the TaxCalculator class.

        Args:
            income (float): The individual's income.
            brackets (list[float]): The tax brackets (limits for each tax tier).
            rates (list[float]): The tax rates (as decimals) for each bracket.
            deductions (float, optional): The deductions to reduce taxable income. Default is 0.0.
        """
        if income < 0:
            raise ValueError("Income cannot be negative.")
        if deductions < 0:
            raise ValueError("Deductions cannot be negative.")
        if not brackets or not rates:
            raise ValueError("Brackets and rates cannot be empty.")
        if len(brackets) != len(rates):
            raise ValueError("Brackets and rates must have the same length.")

        self.income = income
        self.taxable_income = max(income - deductions, 0)  # Adjust income by deductions
        self.brackets = brackets
        self.rates = rates
        self.deductions = deductions

    def calculate_tax(self) -> float:
        """
        Calculate the total tax based on taxable income and tax brackets.

        Returns:
            float: The total tax owed.
        """
        tax = 0
        previous_bracket = 0
        for i, bracket in enumerate(self.brackets):
            # print("Bracket: ", bracket)
            if self.taxable_income > bracket:
                tax += (bracket - previous_bracket) * self.rates[i]
                previous_bracket = bracket
                # print("Rolling sum Tax: ", tax)
            else:
                tax += (self.taxable_income - previous_bracket) * self.rates[i]
                # print("Tax: ", tax)
                break
        else:
            # In case income exceeds the highest bracket
            tax += (self.taxable_income - previous_bracket) * self.rates[-1]

        return round(tax, 2)

    def print_summary(self):
        print("Tax type: ", self.__class__.__name__)
        print("Total Income: ", self.income)
        print("Deductions: ", self.deductions)
        print("Taxable Income: ", self.taxable_income)
        print("Tax Liability: ", self.calculate_tax())


class FederalTax(Tax):
    def __init__(self, income, contr401k):
        brackets = [23200, 94300, 201050, 383900, 487450, 731200, float("inf")]
        rates = [.1, .12, .22, .24, .32, .35, .37]
        std_deduction = 29200
        deductions = std_deduction + contr401k
        super().__init__(income, brackets, rates, deductions)


class StateTax(Tax):
    def __init__(self, income, contr401k, state):
        if state not in ["PA", "NY"]:
            raise ValueError("Only [['PA', 'NY']] are supported.")

        self.state = state
        brackets = []
        rates = []
        deductions = 0
        child_deduction = 1000

        if self.state == "PA":
            brackets = [float("inf")]
            rates = [0.0307]
        elif self.state == "NY":
            # Progressive tax for New York (2024 married filing jointly brackets)
            brackets = [17150, 23600, 27900, 161550, 323200, 2155350, 5000000, 25000000, float("inf")]
            rates = [0.04, 0.045, 0.0525, 0.055, .06, 0.0685, 0.0965, 0.103, 0.109]
            ny_std_deduction = 16050
            deductions = ny_std_deduction + contr401k + child_deduction

        super().__init__(income, brackets, rates, deductions)


class LocalTax(Tax):
    def __init__(self, income, state):
        if state not in ["PA", "NY"]:
            raise ValueError("Only [['PA', 'NY']] are supported.")

        self.state = state
        rates = [0.04] if self.state == "NY" else [0.01]
        brackets = [float("inf")]
        deductions = 0

        super().__init__(income, brackets, rates, deductions)


class SocialSecurityTax(Tax):
    def __init__(self, income1, income2):
        income_cap = 168600  # per person
        self.base1 = min(income1, income_cap)
        self.base2 = min(income2, income_cap)
        income = income1 + income2
        rates = [0.062]
        brackets = [float("inf")]
        super().__init__(income, brackets, rates, deductions=0)

    def calculate_tax(self) -> float:
        return (self.base1 + self.base2) * self.rates[0]


class MedicareTax(Tax):
    def __init__(self, income):
        rates = [0.0145]
        brackets = [float("inf")]
        self.extra_tax_rate = 0.009
        self.extra_tax_threshold = 250000
        super().__init__(income, brackets, rates, deductions=0)

    def calculate_tax(self) -> float:
        extra_tax = max(0.0, self.income - self.extra_tax_threshold) * self.extra_tax_rate
        return round(self.income * self.rates[0] + extra_tax, 2)


class Budget:
    def __init__(self, income1, income2, other_income, contr401k1, contr401k2, state,
                 fed_tax_paid=0, state_tax_paid=0, local_tax_paid=0, social_sec_tax_paid=0, medicare_tax_paid=0):
        self.income1 = income1
        self.income2 = income2
        self.other_income = other_income
        self.total_income = income1 + income2 + other_income
        self.contr401k1 = contr401k1
        self.contr401k2 = contr401k2
        self.state = state

        self.fed_tax_paid = fed_tax_paid
        self.state_tax_paid = state_tax_paid
        self.local_tax_paid = local_tax_paid
        self.social_sec_tax_paid = social_sec_tax_paid
        self.medicare_tax_paid = medicare_tax_paid

    def federal_tax(self):
        return FederalTax(self.total_income, self.contr401k1 + self.contr401k2).calculate_tax()

    def state_tax(self):
        return StateTax(self.total_income, self.contr401k1 + self.contr401k2, self.state).calculate_tax()

    def local_tax(self):
        # return LocalTax(self.total_income, self.state).calculate_tax()
        return LocalTax(self.total_income, "PA").calculate_tax()

    def social_sec_tax(self):
        return SocialSecurityTax(self.income1, self.income2).calculate_tax()

    def medicare_tax(self):
        return MedicareTax(self.total_income).calculate_tax()

    def total_tax(self):
        return self.federal_tax() + self.state_tax() + self.local_tax() + self.social_sec_tax() + self.medicare_tax()

    def federal_tax_owed(self):
        return (self.federal_tax() - self.fed_tax_paid) + \
            (self.social_sec_tax() - self.social_sec_tax_paid) + \
            (self.medicare_tax() - self.medicare_tax_paid)

    def state_tax_owed(self):
        return self.state_tax() - self.state_tax_paid

    def local_tax_owed(self):
        return self.local_tax() - self.local_tax_paid

    def eff_tax_rate(self):
        if self.total_income == 0:
            return 0.0
        return round(self.total_tax() / self.total_income * 100, 2)

    def print_summary(self):
        print("Total Income:", self.total_income)
        print(f"Federal Tax owed (incl. Medicare & SS): {self.federal_tax_owed()}",)
        print(f"{self.state.upper()} State Tax owed: {self.state_tax()} - {self.state_tax_paid} = {self.state_tax_owed()}",)
        print(f"PA Local Tax owed: {self.local_tax()} - {self.local_tax_paid} = {self.local_tax_owed()}",)
        print(f"Total Tax Liability: {self.total_tax()}")
        print(f"Effective Tax Rate: {self.eff_tax_rate()}%")


if __name__ == "__main__":
    ivan_w2 = 292060.68
    olga_w2 = 325953.54
    other_income = 2178 + 2807 + 2477

    ivan_401k = 23000
    olga_401k = 23000

    state = "NY"

    # paid = (63603 + 10453 + 5859 + 26450 + 3028) + (62267 + 10453 + 5063 + 18993)

    fed_paid = 63603 + 62267
    ss_paid = 10453 + 10453
    medicare_paid = 5859 + 5063
    ny_state_paid = 26450 + 18993
    local_paid = 3028

    budget = Budget(ivan_w2, olga_w2, other_income, ivan_401k, olga_401k, state,
                    fed_paid, ny_state_paid, local_paid, ss_paid, medicare_paid)

    budget.print_summary()

    income = ivan_w2 + olga_w2 + other_income
    contr401k = ivan_401k + olga_401k
    fed_tax = FederalTax(income, contr401k)
    state_tax = StateTax(income, contr401k, "NY")
    local_tax = LocalTax(income, "NY")
    social_sec_tax = SocialSecurityTax(ivan_w2, olga_w2)
    medicare_tax = MedicareTax(income)

    fed_tax.print_summary()
    print("===========")
    state_tax.print_summary()
    print("===========")
    local_tax.print_summary()
    print("===========")
    social_sec_tax.print_summary()
    print("===========")
    medicare_tax.print_summary()