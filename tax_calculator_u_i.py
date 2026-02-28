import tkinter as tk
from tkinter import ttk, messagebox
import taxes


class TaxCalculatorUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Tax Calculator")
        self.root.geometry("1200x900")  # Much larger window
        self.root.resizable(True, True)
        
        # Configure style
        style = ttk.Style()
        style.theme_use('clam')
        
        self.create_widgets()
        
    def create_widgets(self):
        # Create a main paned window for better layout control
        main_paned = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        main_paned.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left frame for inputs
        left_frame = ttk.Frame(main_paned, padding="10")
        main_paned.add(left_frame, weight=1)
        
        # Right frame for results
        right_frame = ttk.Frame(main_paned, padding="10")
        main_paned.add(right_frame, weight=2)  # Give more space to results
        
        # Title for left side
        title_label = ttk.Label(left_frame, text="Tax Calculator", font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Input section
        input_frame = ttk.LabelFrame(left_frame, text="Income Information", padding="10")
        input_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        input_frame.columnconfigure(1, weight=1)
        
        # Income fields
        ttk.Label(input_frame, text="Person 1 Income ($):").grid(row=0, column=0, sticky=tk.W, pady=3)
        self.income1_var = tk.StringVar(value="100000")
        ttk.Entry(input_frame, textvariable=self.income1_var, width=20).grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5, pady=3)
        
        ttk.Label(input_frame, text="Person 2 Income ($):").grid(row=1, column=0, sticky=tk.W, pady=3)
        self.income2_var = tk.StringVar(value="80000")
        ttk.Entry(input_frame, textvariable=self.income2_var, width=20).grid(row=1, column=1, sticky=(tk.W, tk.E), padx=5, pady=3)
        
        ttk.Label(input_frame, text="Other Income ($):").grid(row=2, column=0, sticky=tk.W, pady=3)
        self.other_income_var = tk.StringVar(value="5000")
        ttk.Entry(input_frame, textvariable=self.other_income_var, width=20).grid(row=2, column=1, sticky=(tk.W, tk.E), padx=5, pady=3)
        
        ttk.Label(input_frame, text="Person 1 401k ($):").grid(row=3, column=0, sticky=tk.W, pady=3)
        self.contrib401k1_var = tk.StringVar(value="20000")
        ttk.Entry(input_frame, textvariable=self.contrib401k1_var, width=20).grid(row=3, column=1, sticky=(tk.W, tk.E), padx=5, pady=3)
        
        ttk.Label(input_frame, text="Person 2 401k ($):").grid(row=4, column=0, sticky=tk.W, pady=3)
        self.contrib401k2_var = tk.StringVar(value="15000")
        ttk.Entry(input_frame, textvariable=self.contrib401k2_var, width=20).grid(row=4, column=1, sticky=(tk.W, tk.E), padx=5, pady=3)
        
        ttk.Label(input_frame, text="State:").grid(row=5, column=0, sticky=tk.W, pady=3)
        self.state_var = tk.StringVar(value="PA")
        state_combo = ttk.Combobox(input_frame, textvariable=self.state_var, values=["PA", "NY"], 
                                  state="readonly", width=17)
        state_combo.grid(row=5, column=1, sticky=tk.W, padx=5, pady=3)
        
        # Optional: Already paid taxes section
        paid_frame = ttk.LabelFrame(left_frame, text="Taxes Already Paid (Optional)", padding="10")
        paid_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        paid_frame.columnconfigure(1, weight=1)
        
        ttk.Label(paid_frame, text="Federal Tax Paid ($):").grid(row=0, column=0, sticky=tk.W, pady=3)
        self.fed_paid_var = tk.StringVar(value="0")
        ttk.Entry(paid_frame, textvariable=self.fed_paid_var, width=20).grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5, pady=3)
        
        ttk.Label(paid_frame, text="State Tax Paid ($):").grid(row=1, column=0, sticky=tk.W, pady=3)
        self.state_paid_var = tk.StringVar(value="0")
        ttk.Entry(paid_frame, textvariable=self.state_paid_var, width=20).grid(row=1, column=1, sticky=(tk.W, tk.E), padx=5, pady=3)
        
        ttk.Label(paid_frame, text="Local Tax Paid ($):").grid(row=2, column=0, sticky=tk.W, pady=3)
        self.local_paid_var = tk.StringVar(value="0")
        ttk.Entry(paid_frame, textvariable=self.local_paid_var, width=20).grid(row=2, column=1, sticky=(tk.W, tk.E), padx=5, pady=3)
        
        ttk.Label(paid_frame, text="Social Security Paid ($):").grid(row=3, column=0, sticky=tk.W, pady=3)
        self.ss_paid_var = tk.StringVar(value="0")
        ttk.Entry(paid_frame, textvariable=self.ss_paid_var, width=20).grid(row=3, column=1, sticky=(tk.W, tk.E), padx=5, pady=3)
        
        ttk.Label(paid_frame, text="Medicare Tax Paid ($):").grid(row=4, column=0, sticky=tk.W, pady=3)
        self.medicare_paid_var = tk.StringVar(value="0")
        ttk.Entry(paid_frame, textvariable=self.medicare_paid_var, width=20).grid(row=4, column=1, sticky=(tk.W, tk.E), padx=5, pady=3)
        
        # Button frame
        button_frame = ttk.Frame(left_frame)
        button_frame.grid(row=3, column=0, columnspan=2, pady=20)
        
        # Calculate button
        calc_button = ttk.Button(button_frame, text="Calculate Taxes", command=self.calculate_taxes)
        calc_button.grid(row=0, column=0, padx=5)
        
        # Clear button
        clear_button = ttk.Button(button_frame, text="Clear All", command=self.clear_all)
        clear_button.grid(row=0, column=1, padx=5)
        
        # Results section (RIGHT SIDE)
        results_title = ttk.Label(right_frame, text="Tax Calculation Results", font=('Arial', 14, 'bold'))
        results_title.pack(pady=(0, 10))
        
        # Results text widget with scrollbar
        text_frame = ttk.Frame(right_frame)
        text_frame.pack(fill=tk.BOTH, expand=True)
        
        self.results_text = tk.Text(text_frame, font=('Courier', 10), 
                                   wrap=tk.NONE, state=tk.NORMAL)
        
        # Scrollbars
        scrollbar_y = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=self.results_text.yview)
        scrollbar_x = ttk.Scrollbar(text_frame, orient=tk.HORIZONTAL, command=self.results_text.xview)
        
        self.results_text.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
        
        # Pack text widget and scrollbars
        self.results_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Add initial placeholder text
        self.results_text.insert(tk.END, "Enter your income information on the left and click 'Calculate Taxes' to see your detailed tax report here.\n\nThis calculator supports:\n• Federal taxes\n• State taxes (PA and NY)\n• Local taxes\n• Social Security taxes\n• Medicare taxes\n• Effective tax rate calculations\n• Tax owed/refund estimates")
        self.results_text.config(state=tk.DISABLED)
        
    def get_float_value(self, var):
        """Safely convert string to float, return 0 if invalid."""
        try:
            value = var.get().replace(',', '').replace('$', '').strip()
            return float(value) if value else 0.0
        except ValueError:
            return 0.0
    
    def calculate_taxes(self):
        """Calculate taxes and display results."""
        try:
            # Get input values
            income1 = self.get_float_value(self.income1_var)
            income2 = self.get_float_value(self.income2_var)
            other_income = self.get_float_value(self.other_income_var)
            contrib401k1 = self.get_float_value(self.contrib401k1_var)
            contrib401k2 = self.get_float_value(self.contrib401k2_var)
            state = self.state_var.get()
            
            # Get already paid taxes
            fed_paid = self.get_float_value(self.fed_paid_var)
            state_paid = self.get_float_value(self.state_paid_var)
            local_paid = self.get_float_value(self.local_paid_var)
            ss_paid = self.get_float_value(self.ss_paid_var)
            medicare_paid = self.get_float_value(self.medicare_paid_var)
            
            # Create budget object
            budget = taxes.Budget(
                income1, income2, other_income, contrib401k1, contrib401k2, state,
                fed_paid, state_paid, local_paid, ss_paid, medicare_paid
            )
            
            # Clear previous results
            self.results_text.config(state=tk.NORMAL)
            self.results_text.delete(1.0, tk.END)
            
            # Generate detailed report
            report = self.generate_tax_report(budget)
            
            # Display results
            self.results_text.insert(tk.END, report)
            self.results_text.config(state=tk.DISABLED)
            
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while calculating taxes:\n{str(e)}")
    
    def generate_tax_report(self, budget):
        """Generate a detailed tax report."""
        report = []
        report.append("=" * 70)
        report.append("                    TAX CALCULATION REPORT")
        report.append("=" * 70)
        report.append("")
        
        # Income Summary
        report.append("INCOME SUMMARY:")
        report.append("-" * 50)
        report.append(f"Person 1 Income:              ${budget.income1:,.2f}")
        report.append(f"Person 2 Income:              ${budget.income2:,.2f}")
        report.append(f"Other Income:                 ${budget.other_income:,.2f}")
        report.append(f"Total Income:                 ${budget.total_income:,.2f}")
        report.append("")
        
        # Deductions
        report.append("DEDUCTIONS:")
        report.append("-" * 50)
        report.append(f"Person 1 401k Contribution:   ${budget.contr401k1:,.2f}")
        report.append(f"Person 2 401k Contribution:   ${budget.contr401k2:,.2f}")
        report.append(f"Total 401k Contributions:     ${budget.contr401k1 + budget.contr401k2:,.2f}")
        report.append("")
        
        # Tax Calculations
        report.append("TAX CALCULATIONS:")
        report.append("-" * 50)
        federal_tax = budget.federal_tax()
        state_tax = budget.state_tax()
        local_tax = budget.local_tax()
        ss_tax = budget.social_sec_tax()
        medicare_tax = budget.medicare_tax()
        total_tax = budget.total_tax()
        
        report.append(f"Federal Tax:                  ${federal_tax:,.2f}")
        report.append(f"{budget.state} State Tax:                  ${state_tax:,.2f}")
        report.append(f"Local Tax (PA):               ${local_tax:,.2f}")
        report.append(f"Social Security Tax:          ${ss_tax:,.2f}")
        report.append(f"Medicare Tax:                 ${medicare_tax:,.2f}")
        report.append(f"Total Tax Liability:          ${total_tax:,.2f}")
        report.append("")
        
        # Effective tax rate
        eff_rate = budget.eff_tax_rate()
        report.append(f"Effective Tax Rate:           {eff_rate}%")
        report.append("")
        
        # Taxes already paid
        if any([budget.fed_tax_paid, budget.state_tax_paid, budget.local_tax_paid, 
                budget.social_sec_tax_paid, budget.medicare_tax_paid]):
            report.append("TAXES ALREADY PAID:")
            report.append("-" * 50)
            report.append(f"Federal Tax Paid:             ${budget.fed_tax_paid:,.2f}")
            report.append(f"State Tax Paid:               ${budget.state_tax_paid:,.2f}")
            report.append(f"Local Tax Paid:               ${budget.local_tax_paid:,.2f}")
            report.append(f"Social Security Tax Paid:     ${budget.social_sec_tax_paid:,.2f}")
            report.append(f"Medicare Tax Paid:            ${budget.medicare_tax_paid:,.2f}")
            total_paid = (budget.fed_tax_paid + budget.state_tax_paid + budget.local_tax_paid + 
                         budget.social_sec_tax_paid + budget.medicare_tax_paid)
            report.append(f"Total Taxes Paid:             ${total_paid:,.2f}")
            report.append("")
            
            # Amount owed or refund
            report.append("AMOUNT OWED/REFUND:")
            report.append("-" * 50)
            fed_owed = budget.federal_tax_owed()
            state_owed = budget.state_tax_owed()
            local_owed = budget.local_tax_owed()
            
            report.append(f"Federal Tax Owed:             ${fed_owed:,.2f}")
            report.append(f"State Tax Owed:               ${state_owed:,.2f}")
            report.append(f"Local Tax Owed:               ${local_owed:,.2f}")
            
            total_owed = fed_owed + state_owed + local_owed
            report.append(f"Total Amount Owed:            ${total_owed:,.2f}")
            report.append("")
            
            if total_owed < 0:
                report.append("🎉 REFUND EXPECTED!")
                report.append(f"*** You may be due a refund of ${abs(total_owed):,.2f} ***")
            elif total_owed > 0:
                report.append("💰 AMOUNT OWED:")
                report.append(f"*** You owe ${total_owed:,.2f} in taxes ***")
            else:
                report.append("✅ TAXES FULLY PAID:")
                report.append("*** Your tax liability is fully paid ***")
        
        report.append("")
        report.append("=" * 70)
        report.append("Note: This is an estimate. Please consult a tax professional")
        report.append("for official tax advice.")
        report.append("=" * 70)
        
        return "\n".join(report)
    
    def clear_all(self):
        """Clear all input fields and results."""
        # Clear input fields
        self.income1_var.set("0")
        self.income2_var.set("0")
        self.other_income_var.set("0")
        self.contrib401k1_var.set("0")
        self.contrib401k2_var.set("0")
        self.state_var.set("PA")
        
        # Clear already paid fields
        self.fed_paid_var.set("0")
        self.state_paid_var.set("0")
        self.local_paid_var.set("0")
        self.ss_paid_var.set("0")
        self.medicare_paid_var.set("0")
        
        # Clear results
        self.results_text.config(state=tk.NORMAL)
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END, "Enter your income information on the left and click 'Calculate Taxes' to see your detailed tax report here.")
        self.results_text.config(state=tk.DISABLED)


def main():
    root = tk.Tk()
    app = TaxCalculatorUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()