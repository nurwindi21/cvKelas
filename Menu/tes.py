import datetime

# Sample menu dictionary with item numbers as keys
menu = {
    "1": ("Burger", 8.5),
    "2": ("Pizza", 12),
    "3": ("Pasta", 10),
    "4": ("Salad", 7),
    "5": ("Soup", 6),
    "6": ("Coke", 2),
    "7": ("Water", 1.5),
    "8": ("Juice", 3)
}

def validate_date_time(date_input):
    try:
        valid_date_time = datetime.datetime.strptime(date_input, "%d/%m/%Y %H:%M")
        return True
    except ValueError:
        return False

def take_reservation():
    print("Welcome to my restaurant")
    name = input("Enter name: ")
    phone = input("Enter phone number: ")

    while True:
        date_time = input("Enter reservation date and time (dd/mm/yyyy hh:mm): ")
        if validate_date_time(date_time):
            break
        else:
            print("Invalid date and time format. Please try again.")

    num_people = input("Enter the number of people: ")

    print("\nReservation details:")
    print(f"Name: {name}")
    print(f"Phone number: {phone}")
    print(f"Date and time: {date_time}")
    print(f"Number of people: {num_people}")

    while True:
        confirm = input("Is this information correct? (yes/no): ")
        if confirm.lower() == "yes":
            return name, phone, date_time, num_people
        elif confirm.lower() == "no":
            print("Please re-enter your reservation details.")
            return take_reservation()
        else:
            print("Invalid response, please type 'yes' or 'no'.")

def display_menu():
    print("Menu:")
    for item_number, (item_name, price) in menu.items():
        print(f"{item_number}. {item_name} - ${price}")
    return menu

def take_order():
    food_order = []
    drink_order = []

    order_input = input("Enter the number of the item you want to order, separated by commas: ")
    order_items = [item.strip() for item in order_input.split(",") if item.strip().isdigit()]
    for item in order_items:
        if item in menu:
            item_name, _ = menu[item]
            if int(item) <= 5:
                food_order.append(item_name)
            else:
                drink_order.append(item_name)
        else:
            print(f"Item number {item} is not on the menu. Please enter valid item numbers.")

    return food_order, drink_order

def confirm_reservation(name, phone, date, num_people, food_order, drink_order):
    print("\n--- Reservation Summary ---")
    print(f"Name: {name}")
    print(f"Phone: {phone}")
    print(f"Date & Time: {date}")
    print(f"Number of people: {num_people}")
    if food_order or drink_order:
        print(f"Ordered Food: {', '.join(food_order)}")
        print(f"Ordered Drinks: {', '.join(drink_order)}")
    else:
        print("No food or drinks ordered.")
    print("\nThank you for your reservation and order!")

def main():
    name, phone, date_time, num_people = take_reservation()

    while True:
        order_time = input("Would you like to order now or at the restaurant? (Type 'now' to order, 'later' to order at the restaurant): ").lower()
        if order_time == "now":
            display_menu()
            food_order, drink_order = take_order()
            break
        elif order_time == "later":
            food_order, drink_order = [], []
            break
        else:
            print("Please type 'now' or 'later'.")

    confirm_reservation(name, phone, date_time, num_people, food_order, drink_order)

main()
