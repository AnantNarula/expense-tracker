import json
import os
import argparse

DATA_FILE = "data.json"

def load_expenses():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_expenses(expenses):
    with open(DATA_FILE, "w") as f:
        json.dump(expenses, f, indent=2)

def add_expense(amount, category, description):
    expenses = load_expenses()
    expense = {
        "id": len(expenses) + 1,
        "amount": amount,
        "category": category,
        "description": description
    }
    expenses.append(expense)
    save_expenses(expenses)
    print(f"Added: ${amount} | {category} | {description}")

def list_expenses():
    expenses = load_expenses()
    if not expenses:
        print("No expenses yet.")
        return
    print(f"\n{'ID':<5} {'Amount':<10} {'Category':<15} {'Description'}")
    print("-" * 45)
    for e in expenses:
        print(f"{e['id']:<5} ${e['amount']:<9} {e['category']:<15} {e['description']}")

def delete_expense(expense_id):
    expenses = load_expenses()
    original_count = len(expenses)
    expenses = [e for e in expenses if e["id"] != expense_id]
    if len(expenses) == original_count:
        print(f"No expense found with ID {expense_id}")
        return
    save_expenses(expenses)
    print(f"Deleted expense ID {expense_id}")

def summary():
    expenses = load_expenses()
    if not expenses:
        print("No expenses yet.")
        return
    totals = {}
    for e in expenses:
        category = e["category"]
        totals[category] = totals.get(category, 0) + e["amount"]
    total = sum(totals.values())
    print(f"\n{'Category':<15} {'Total'}")
    print("-" * 25)
    for category, amount in sorted(totals.items()):
        print(f"{category:<15} ${amount}")
    print("-" * 25)
    print(f"{'TOTAL':<15} ${total}")

def main():
    parser = argparse.ArgumentParser(description="CLI Expense Tracker")
    subparsers = parser.add_subparsers(dest="command")

    add_parser = subparsers.add_parser("add", help="Add an expense")
    add_parser.add_argument("--amount", type=float, required=True)
    add_parser.add_argument("--category", type=str, required=True)
    add_parser.add_argument("--description", type=str, required=True)

    subparsers.add_parser("list", help="List all expenses")
    subparsers.add_parser("summary", help="Show category summary")

    delete_parser = subparsers.add_parser("delete", help="Delete an expense")
    delete_parser.add_argument("--id", type=int, required=True)

    args = parser.parse_args()

    if args.command == "add":
        add_expense(args.amount, args.category, args.description)
    elif args.command == "list":
        list_expenses()
    elif args.command == "summary":
        summary()
    elif args.command == "delete":
        delete_expense(args.id)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()