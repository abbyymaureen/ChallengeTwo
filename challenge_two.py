"""
@filename challenge_two.py
@author abbybrown
@date 02/05/24

    A coding challenge that allows the user to look up Montana county info based on city name.
    If the city is not in the database, the user can add it.
"""
import csv

FILE_NAME = "MontanaCounties.csv"


def file_to_dictionary(filename):
    my_dict = {}
    try:
        with open(filename, 'r') as file:
            # skip the first line of column headers
            next(file)
            for line in file:
                data = line.strip().split(',')
                values = int(data[2]), data[0]
                key = data[1]
                my_dict[key] = values

        return my_dict

    except FileNotFoundError:
        print(f"I'm sorry, {filename} does not exist.")

    except ValueError:
        print(f"I'm sorry, the key in your new dictionary had an improper numeric entry.")


def find_county(my_dict, num):
    for plate, (county_name, _) in my_dict.items():
        if num == plate:
            return county_name
    return None


def find_county_two(my_dict, num):
    for town, (plate, county) in my_dict.items():
        if num == plate:
            return county
    return None


def write_to_csv(filename, city, county, plate):
    try:
        with open(filename, 'a', newline='') as file:  # Open the file in append mode
            writer = csv.writer(file)
            writer.writerow([county, city, plate])
        print(f"Updated information has been written to {filename} successfully.")
    except Exception as e:
        print(f"An error occurred while writing to {filename}: {e}")


def do_the_search(my_dict, city):
    # Clean the input city name
    city = city.strip().title()  # Remove leading/trailing whitespaces and capitalize the city name

    for town, values in my_dict.items():
        # Extract the city portion from the key
        town_city = town.split('-')[0].strip().title()

        # We found the city in our database
        if city == town_city:
            county, plate = values
            print(f"{town_city} is in {county} County with license plate number {plate}.")
            return
    # We didn't find the city, so add it
    print(f"We don't have '{city}' in our database yet!")
    try:
        while True:  # Loop until a valid plate number is entered
            try:
                plate = int(input("Enter the license plate for the city's county (or any string to quit): "))
                if 1 <= plate <= 56:
                    county = find_county_two(my_dict, plate)
                    if county:
                        print("The following information has been added to the database:")
                        print(f"City: {city}\nCounty: {county}\nLicense Plate Number: {plate}")
                        my_dict[city] = (county, plate)
                        write_to_csv(FILE_NAME, city, county, plate)
                        break  # Exit the loop if a valid plate number is entered
                    else:
                        print("County information not found for the entered license plate.")
                else:
                    print("License numbers should range between 1 and 56. Please try again.")
            except ValueError:
                print("You successfully cancelled adding the city!")
                break
    except ValueError:
        print("You did not enter a number. Please try again.")


if __name__ == "__main__":
    running = True
    counties = file_to_dictionary(FILE_NAME)
    print(counties)
    while running:
        print("\n* * * City Search * * * ")
        user_input = str(input("Please enter a city for lookup or any number to quit > "))

        if user_input.isdigit():
            print("Thank you for using our program! Goodbye!")
            break

        do_the_search(counties, user_input)
