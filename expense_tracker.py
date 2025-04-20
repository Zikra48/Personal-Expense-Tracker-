



import json
from datetime import datetime

class Transaction:
    def __init__(self, amount, category, trans_type, date=None):
        self.amount = amount
        self.category = category
        self.trans_type = trans_type  # 'income' or 'expense'
        self.date = date if date else datetime.now().strftime('%Y-%m-%d')

    def to_dict(self):
        return self.__dict__

class ExpenseTracker:
    def __init__(self):
        self.transactions = []

    def add_transaction(self, amount, category, trans_type):
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
            print(f"{t.date} | {t.trans_type.upper()} | {t.category} | ${t.amount}")
        print(f"\nCurrent Balance: ${self.get_balance():.2f}")

# Example Usage
if __name__ == "__main__":
    tracker = ExpenseTracker()
    tracker.load_from_file()

    while True:
        print("\n1. Add Income")
        print("2. Add Expense")
        print("3. Show Summary")
        print("4. Save & Exit")

        choice = input("Choose an option: ")

        if choice == '1':
            amount = float(input("Enter amount: "))
            category = input("Enter category: ")
            tracker.add_transaction(amount, category, 'income')

        elif choice == '2':
            amount = float(input("Enter amount: "))
            category = input("Enter category: ")
            tracker.add_transaction(amount, category, 'expense')

        elif choice == '3':
            tracker.show_summary()

        elif choice == '4':
            tracker.save_to_file()
            print("Data saved. Goodbye!")
            break

        else:
            print("Invalid choice. Try again.")

