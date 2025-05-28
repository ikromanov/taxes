# TODO: put taxes in a separate class
# class FederalTax:
#     def __init__(self, brackets, rates, deduction):
#         self.brackets = brackets
#         self.rates = rates
#         self.deduction = deduction


def calc_brackets_tax(income, brackets, rates):
    if len(brackets) != len(rates):
        print("Length of tax rates and tax brackets must match")
        return

    taxable_per_bracket = []
    tax_per_bracket = []

    for i in range(len(brackets) - 1, -1, -1):
        bracket = brackets[i]
        tax_rate = rates[i]

        taxable = max(income - bracket, 0)
        tax_for_br = round(taxable * tax_rate, 2)

        taxable_per_bracket = [taxable] + taxable_per_bracket
        tax_per_bracket = [tax_for_br] + tax_per_bracket

        income -= taxable

#       for i in range(len(tax_per_bracket)):
#           print("Taxable: {} x {}: {}".format(taxable_per_bracket[i], rates[i], tax_per_bracket[i]))

    return round(sum(tax_per_bracket))


class Tax:
    def __init__(self, income, brackets, rates):
        self.income = income
        self.brackets = brackets
        self.rates = rates

    def amount(self):
        return calc_brackets_tax(self.income, self.brackets, self.rates)


class FedTax(Tax):
    def __init__(self, income, brackets, rates, deduction, contr401k):
        super().__init__(income, brackets, rates)
        self.deduction = deduction
        self.contr401k = contr401k

    def amount(self):
        taxable_income = self.income - self.deduction - self.contr401k
        # return Tax(taxable_income, self.brackets, self.rates).amount()
        return calc_brackets_tax(taxable_income, self.brackets, self.rates)


class StateTax(Tax):
    def __init__(self, income, brackets, rates, deduction, contr401k, state):
        super().__init__(income, brackets, rates)
        self.deduction = deduction
        self.contr401k = contr401k
        self.state = state

    def amount(self):
        if self.state == "PA":
            rate = 0.031
            return round(self.income * rate, 2)
        elif self.state == "NY":
            ny_deduction = 16050
            income = self.income - self.contr401k - ny_deduction

            # print(f"Taxable income: {income}")

            # brackets = [0, 17150, 23600, 27900, 161550, 323200, 2155350, 5000000, 25000000]
            # rates = [.04, .045, .0525, 0.055, .06, .0685, .0965, .103, .0109]

            return calc_brackets_tax(income, self.brackets, self.rates)


class Tax:
    def __init__(self, income, fed_deduction, contr401k, state):
        self.income = income
        self.contr401k = contr401k
        self.fed_deduction = fed_deduction
        self.state = state

    def fed_amount(self):
        income = self.income
        # deduction = 29200
        # contr401k = 22500
        brackets = [0, 23200, 94300, 201050, 383900, 487450, 731200]
        tax_rates = [.1, .12, .22, .24, .32, .35, .37]

        income -= self.fed_deduction
        income -= self.contr401k

        print(f"Taxable income: {income}")

        tax_amount = calc_brackets_tax(income, brackets, tax_rates)

        return tax_amount



class Income:
    def __init__(self, w2_income_1, w2_income_2, other_income, contr401k, state):
        self.income1 = w2_income_1
        self.income2 = w2_income_2
        self.income = w2_income_1 + w2_income_2 + other_income
        self.contr401k = contr401k
        self.deduction = 29200
        self.state = state

    def fed_tax(self):
        return Tax(self.income, self.deduction, self.contr401k, self.state).fed_amount()

    def state_tax(self):
        return Tax(self.income, self.deduction, self.contr401k, self.state).state_amount()


    def local_tax(self):
        if self.state == "PA":
            rate = 0.01
        elif self.state == "NY":
            rate = 0.04
        return round(self.income * rate, 2)

    
    def social_sec_tax(self):
        income_cap = 168600 # per person
        rate = 0.062
        base1 = min(self.income1, income_cap)
        base2 = min(self.income2, income_cap)
        return (base1 + base2) * rate

    
    def medicare_tax(self):
        rate = 0.0145
        extra_tax_rate = 0.009
        extra_tax_threshold = 250000
        extra_tax = max(0, self.income - extra_tax_threshold) * extra_tax_rate

        return round(self.income * rate, 2) + extra_tax
    
    
    def all_taxes(self):
        return round(self.state_tax() + \
                     self.fed_tax() + \
                     self.local_tax() + \
                     self.social_sec_tax() + \
                     self.medicare_tax(), 2)
    
    
    def eff_tax_rate(self):
        return round(self.all_taxes() / self.income, 4)
    
    
    def print_summary(self):
        print("Total Income: ", self.income)

        print("Medicare taxes:", self.medicare_tax())
        print("Social Security taxes:", self.social_sec_tax())
        print("Federal taxes:", self.fed_tax())
        print("State taxes:", self.state_tax())
        print("Local taxes:", self.local_tax())

        print("Total taxes:", self.all_taxes())