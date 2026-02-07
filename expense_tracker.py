import csv
from datetime import datetime
import os
import matplotlib.pyplot as plt

FILE_NAME = "expenses.csv"

DEFAULT_CATEGORIES = [
    "Food",
    "Fuel",
    "Shopping",
    "Bills",
    "Entertainment"
]

def ensure_csv_has_header():
    # Create file + header if missing or empty
    if not os.path.exists(FILE_NAME) or os.path.getsize(FILE_NAME) == 0:
        with open(FILE_NAME, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["date", "amount", "category"])

def add_expense(amount, category):
    date = datetime.now().strftime("%Y-%m-%d")
    with open(FILE_NAME, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([date, amount, category])

def choose_category():
    print("\nChoose a category:")
    for i, cat in enumerate(DEFAULT_CATEGORIES, start=1):
        print(f"{i}. {cat}")
    print(f"{len(DEFAULT_CATEGORIES) + 1}. Other (type your own)")

    choice = input("Enter option number: ").strip()

    if not choice.isdigit():
        print("❌ Please enter a valid number.")
        return None

    choice = int(choice)

    if 1 <= choice <= len(DEFAULT_CATEGORIES):
        return DEFAULT_CATEGORIES[choice - 1]

    if choice == len(DEFAULT_CATEGORIES) + 1:
        custom = input("Enter custom category: ").strip()
        if custom == "":
            print("❌ Category cannot be empty.")
            return None
        return custom

    print("❌ Invalid option.")
    return None

def show_pie_chart(category_total):
    if not category_total:
        print("No data to plot.")
        return

    labels = list(category_total.keys())
    sizes = list(category_total.values())

    plt.figure()
    plt.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=90)
    plt.title("Expense Breakdown by Category")
    plt.axis("equal")  # makes it a perfect circle
    plt.show()

def view_expenses():
    total = 0.0
    category_total = {}

    if not os.path.exists(FILE_NAME):
        print("❌ No expense file found.")
        return

    with open(FILE_NAME, "r", newline="") as file:
        reader = csv.reader(file)
        try:
            next(reader)
        except StopIteration:
            print("❌ Expense file is empty.")
            return

        for row in reader:
            row = [x.strip() for x in row]
            if len(row) != 3 or row[0] == "":
                continue

            date, amount, category = row

            try:
                amount = float(amount)
            except ValueError:
                continue

            category = category.strip().title()

            total += amount
            category_total[category] = category_total.get(category, 0) + amount

    print("\n💰 Total Spending:", total)
    print("📊 Category-wise Breakdown:")

    for cat, amt in category_total.items():
        print(f"{cat}: {amt}")

    show_pie_chart(category_total)

def main():
    ensure_csv_has_header()

    while True:
        print("\n1. Add Expense")
        print("2. View Summary")
        print("3. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            try:
                amount = float(input("Enter amount: ").strip())
            except ValueError:
                print("❌ Please enter a valid number.")
                continue

            category = choose_category()
            if category is None:
                continue

            # Normalize category before saving too
            category = category.strip().title()

            add_expense(amount, category)
            print(f"✅ Expense added under '{category}'.")

        elif choice == "2":
            view_expenses()

        elif choice == "3":
            print("👋 Exiting...")
            break

        else:
            print("❌ Invalid choice.")

if __name__ == "__main__":
    main()
