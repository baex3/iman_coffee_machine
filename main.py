'''
Written by Odera Eneugwu -
This python code simulates the functionality of a basic coffee vending machine
'''

from art import logo
from constants import MENU, resources

# print the coffe machine logo
print(logo)
report = {}


def load_coffee_machine() -> dict:
    '''initialize coffee machine's resources and stats'''
    report = resources
    report["Money"] = 0.0
    return resources


def accept_coin(coin: str):
    '''This method returns the total value of each coinage'''
    value = None
    while value is None:
        try:
            value = int(input(f"How many {coin}?: "))
        except ValueError:
            print("Please enter a valid integer.")
    if coin == "quarters":
        return value * 0.25
    elif coin == "dimes":
        return value * 0.10
    elif coin == "nickels":
        return value * 0.05
    elif coin == "pennies":
        return value * 0.01
    else:
        print("We don't accept this currency. Please come back with valid currency.")


def finished_resources(remaining_resource: dict, order: str) -> dict:
    '''This method returns the dictionary of finished resources'''
    final_checks = {}
    water_check = remaining_resource["water"] - MENU[order]["ingredients"]["water"]
    if water_check < 0:
        final_checks["water"] = water_check
    coffee_check = remaining_resource["coffee"] - MENU[order]["ingredients"]["coffee"]
    if coffee_check < 0:
        final_checks["coffee"] = coffee_check
    if order != "espresso":
        milk_check = remaining_resource["milk"] - MENU[order]["ingredients"]["milk"]
        if milk_check < 0:
            final_checks["milk"] = milk_check
    return final_checks


def update_report(remaining_resource: dict, order: str) -> dict:
    '''Update the report once an order is successfully placed'''
    remaining_resource["water"] -= MENU[order]["ingredients"]["water"]
    if order != "espresso":
        remaining_resource["milk"] -= MENU[order]["ingredients"]["milk"]
    remaining_resource["coffee"] -= MENU[order]["ingredients"]["coffee"]
    remaining_resource["Money"] += MENU[order]["cost"]

    return remaining_resource


def enough_resources(remaining_resource: dict, order: str) -> bool:
    '''check if there are enough of every ingredient'''
    water_check = remaining_resource["water"] - MENU[order]["ingredients"]["water"]
    coffee_check = remaining_resource["coffee"] - MENU[order]["ingredients"]["coffee"]
    if order != "espresso":
        milk_check = remaining_resource["milk"] - MENU[order]["ingredients"]["milk"]

    if order != "espresso":
        return water_check >= 0 and coffee_check >= 0 and milk_check >= 0
    else:
        return water_check >= 0 and coffee_check >= 0


def coffee_machine():
    command = ""
    global report
    # Add current money as well
    while command not in ["espresso", "latte", "cappuccino", "report", "off"]:
        try:
            command = input("What would you like? (espresso/latte/cappuccino): ")
        except ValueError:
            print("Sorry, this is an invalid input. Please select an order, or if you are an admin, enter 'report' or 'off'.")
    if command == "off":
        exit()
    elif command in ["espresso", "latte", "cappuccino"]:
        if enough_resources(current_resources, command):
            print(f"The price of this drink is ${MENU[command]['cost']}. Please insert sufficient funds\n")
            quarter_tot = accept_coin("quarters")
            dime_tot = accept_coin("dimes")
            nickel_tot = accept_coin("nickels")
            pennies_tot = accept_coin("pennies")
            total_tendered = quarter_tot + dime_tot + nickel_tot + pennies_tot
            if total_tendered >= MENU[command]["cost"]:
                if total_tendered > MENU[command]["cost"]:
                    change = format(total_tendered - MENU[command]["cost"], '.2f')
                    report = update_report(current_resources, command)
                    print(f"Here is ${change} in change.")
                    print(f"Here is your {command} ☕ Enjoy! ")
                    coffee_machine()
                else:
                    print(f"Here is your {command} ☕ Enjoy! ")
                    report = update_report(current_resources, command)
                    coffee_machine()
            else:
                print("Sorry that's not enough money. Money refunded.")
                coffee_machine()
        else:
            finished_ingredients = finished_resources(current_resources, command)
            print(f"Sorry, there is not enough {' and '.join(finished_ingredients)}")
            coffee_machine()
    elif command == "report":
        print(f"Water: {report['water']}ml")
        print(f"Milk: {report['milk']}ml")
        print(f"Coffee: {report['coffee']}g")
        print(f"Money: ${report['Money']}")
        coffee_machine()
    else:
        print("Command not recognized. Please enter a valid command\n")
        coffee_machine()


# Load the starting resources and initial report into variables
current_resources = load_coffee_machine()
report = load_coffee_machine()
coffee_machine()