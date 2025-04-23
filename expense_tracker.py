



import json
from datetime import datetime
from collections import defaultdict
import matplotlib.pyplot as plt



class Transaction:
    def __init__(self, amount, category, trans_type, date=None):
        self.amount = float(amount)
        self.category = category.strip().title()
        self.trans_type = trans_type  # 'income' or 'expense'
        self.date = date if date else datetime.now().strftime('%Y-%m-%d')

    def to_dict(self):
        return self.__dict__

class Budget:
    def __init__(self, limits=None):
        self.limits = limits if limits else {}  # e.g., {'Food': 300, 'Transport': 100}

class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.transactions = []
        self.budget = Budget()

    def add_transaction(self, amount, category, trans_type):
        if trans_type not in ['income', 'expense']:
            raise ValueError("Transaction type must be 'income' or 'expense'")
        trans = Transaction(amount, category, trans_type)
        self.transactions.append(trans)

    def get_balance(self):
        income = sum(t.amount for t in self.transactions if t.trans_type == 'income')
        expenses = sum(t.amount for t in self.transactions if t.trans_type == 'expense')
        return income - expenses

    def save_to_file(self, filename="data.json"):
        with open(filename, "w") as f:
            json.dump([t.to_dict() for t in self.transactions], f, indent=4)

    def load_from_file(self, filename="data.json"):
        try:
            with open(filename, "r") as f:
                data = json.load(f)
                self.transactions = [Transaction(**d) for d in data]
        except FileNotFoundError:
            print("No saved data found.")

    def show_summary(self):
        print("\n--- Transaction Summary ---")
        for t in self.transactions:
            print(f"{t.date} | {t.trans_type.upper()} | {t.category} | ${t.amount:.2f}")
        print(f"\nCurrent Balance: ${self.get_balance():.2f}")

    def plot_expense_breakdown(self):
        cat_totals = defaultdict(float)
        for t in self.transactions:
            if t.trans_type == 'expense':
                cat_totals[t.category] += t.amount
        if cat_totals:
            labels = list(cat_totals.keys())
            sizes = list(cat_totals.values())
            plt.pie(sizes, labels=labels, autopct='%1.1f%%')
            plt.title("Expense Breakdown")
            plt.show()
        else:
            print("No expenses to plot.")

    def generate_monthly_advice(self):
        this_month = defaultdict(float)
        last_month = defaultdict(float)
        now = datetime.now()
        for t in self.transactions:
            date_obj = datetime.strptime(t.date, "%Y-%m-%d")
            if date_obj.year == now.year:
                if date_obj.month == now.month:
                    this_month[t.category] += t.amount
                elif date_obj.month == now.month - 1:
                    last_month[t.category] += t.amount

        print("\n--- Monthly Advice ---")
        for cat in this_month:
            if cat in last_month:
                change = (this_month[cat] - last_month[cat]) / last_month[cat] * 100
                if change > 20:
                    print(f"You spent {change:.1f}% more on {cat} this month!")
                elif change < -20:
                    print(f"Good job! You spent {abs(change):.1f}% less on {cat} this month.")


# --- CLI Interaction ---

if __name__ == "__main__":
    user = User("John Doe", "john@example.com")
    user.load_from_file()

    print("👋 Welcome to your Personal Expense Tracker!")
    
    while True:
        print("\n🔘 What would you like to do?")
        print("1️⃣  Add Income")
        print("2️⃣  Add Expense")
        print("3️⃣  Show Summary")
        print("4️⃣  Show Expense Chart")
        print("5️⃣  Get Monthly Advice")
        print("6️⃣  Save & Exit")

        choice = input("👉 Enter your choice (1-6): ").strip()

        if choice in ['1', '2']:
            trans_type = 'income' if choice == '1' else 'expense'
            print(f"\n💸 Adding a new {trans_type.capitalize()}...")

            try:
                amount = float(input("➡️  Enter amount: "))
                category = input("➡️  Enter category (e.g., Food, Rent, Transport): ").strip()
                user.add_transaction(amount, category, trans_type)
                print(f"✅ {trans_type.capitalize()} of ${amount:.2f} added under '{category.title()}'.")
            except ValueError:
                print("❌ Invalid amount. Please enter a number.")

        elif choice == '3':
            print("\n📊 Generating summary...")
            user.show_summary()

        elif choice == '4':
            print("\n🧁 Preparing your expense breakdown chart...")
            user.plot_expense_breakdown()

        elif choice == '5':
            print("\n📅 Analyzing monthly spending patterns...")
            user.generate_monthly_advice()

        elif choice == '6':
            user.save_to_file()
            print("\n💾 All data saved successfully.")
            print("👋 Goodbye and keep tracking your expenses smartly!")
            break

        else:
            print("❌ Invalid choice. Please enter a number from 1 to 6.")



