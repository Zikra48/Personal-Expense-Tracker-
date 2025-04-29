import json
from datetime import datetime
from collections import defaultdict
import matplotlib.pyplot as plt


class Transaction:
    def __init__(self, amount, category, trans_type, date=None):
        self.amount = float(amount)
        self.category = category.strip().title()
        self.trans_type = trans_type
        self.date = date if date else datetime.now().strftime('%Y-%m-%d')

    def to_dict(self):
        return self.__dict__


class Budget:
    def __init__(self, limits=None):
        self.limits = limits if limits else {}

    def set_limit(self, category, amount):
        self.limits[category.title()] = float(amount)

    def get_limit(self, category):
        return self.limits.get(category.title(), None)


class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.transactions = []
        self.budget = Budget()

    def add_transaction(self, amount, category, trans_type):
        category = category.title()
        trans = Transaction(amount, category, trans_type)
        self.transactions.append(trans)

        if trans_type == 'expense':
            total_spent = sum(t.amount for t in self.transactions if t.category == category and t.trans_type == 'expense')
            limit = self.budget.get_limit(category)
            if limit and total_spent > limit:
                print(f"⚠️ Budget Alert: You've exceeded the budget for {category} (${total_spent:.2f} > ${limit:.2f})")

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
        print(f"{'Date':<12} {'Type':<10} {'Category':<15} {'Amount':>10}")
        print("-" * 50)
        for t in self.transactions:
            print(f"{t.date:<12} {t.trans_type.upper():<10} {t.category:<15} ${t.amount:>9.2f}")
        print("-" * 50)
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
        now = datetime.now()
        for t in self.transactions:
            date_obj = datetime.strptime(t.date, "%Y-%m-%d")
            if date_obj.year == now.year and date_obj.month == now.month:
                this_month[t.category] += t.amount

        print("\n--- Monthly Advice ---")
        for cat, amount in this_month.items():
            limit = self.budget.get_limit(cat)
            if limit:
                if amount > limit:
                    print(f"⚠️ You spent ${amount:.2f} on {cat}, exceeding your ${limit:.2f} budget.")
                else:
                    print(f"✅ Good job staying within the {cat} budget (${amount:.2f}/${limit:.2f}).")

    def search_transactions(self, keyword):
        print(f"\n🔍 Search Results for '{keyword}':")
        matches = [t for t in self.transactions if keyword.lower() in t.category.lower()]
        if matches:
            print(f"{'Date':<12} {'Type':<10} {'Category':<15} {'Amount':>10}")
            print("-" * 50)
            for t in matches:
                print(f"{t.date:<12} {t.trans_type.upper():<10} {t.category:<15} ${t.amount:>9.2f}")
        else:
            print("No matching transactions found.")

    def set_budget_interactive(self):
        print("\n📊 Set Budget Limits")
        while True:
            category = input("➡️  Enter category name (or 'done' to finish): ").strip()
            if category.lower() == 'done':
                break
            try:
                limit = float(input(f"💰 Enter budget limit for {category.title()}: "))
                self.budget.set_limit(category, limit)
                print(f"✅ Budget limit of ${limit:.2f} set for {category.title()}.")
            except ValueError:
                print("❌ Invalid amount. Please enter a number.")


# --- CLI Interface ---

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
        print("6️⃣  Set Budget Limits")
        print("7️⃣  Search Transactions")
        print("8️⃣  Save & Exit")

        choice = input("👉 Enter your choice (1-8): ").strip()

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
            user.show_summary()

        elif choice == '4':
            user.plot_expense_breakdown()

        elif choice == '5':
            user.generate_monthly_advice()

        elif choice == '6':
            user.set_budget_interactive()

        elif choice == '7':
            keyword = input("🔎 Enter category or keyword to search: ")
            user.search_transactions(keyword)

        elif choice == '8':
            user.save_to_file()
            print("\n💾 All data saved successfully.")
            print("👋 Goodbye and keep tracking your expenses smartly!")
            break

        else:
            print("❌ Invalid choice. Please enter a number from 1 to 8.")
