import psycopg2 as p
import csv

# Connect to the database
con = p.connect(
    host="localhost", 
    dbname="phonebook", 
    user="postgres", 
    password="1", 
    port=5432
)
cur = con.cursor()

# Create the phonebook table if it doesn't exist
cur.execute("""
    CREATE TABLE IF NOT EXISTS phonebook(
        id SERIAL PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        surname VARCHAR(100) NOT NULL,
        phone VARCHAR(15) NOT NULL
    )
""")
con.commit()  # Commit the changes to the database

# Insert data from a CSV file
def insert_from_csv(filename):
    with open(filename, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        for line in csv_reader:
            cur.execute(
                "INSERT INTO phonebook (name, surname, phone) VALUES (%s, %s, %s)",
                (line[0], line[1], line[2])
            )
        con.commit()
        print(f"Data from {filename} inserted successfully.")

# Insert data manually through the console
def insert_from_console():
    name = input("Enter name: ")
    surname = input("Enter surname: ")
    phone = input("Enter phone: ")
    cur.execute(
        "INSERT INTO phonebook (name, surname, phone) VALUES (%s, %s, %s)",
        (name, surname, phone)
    )
    con.commit()
    print(f"Inserted: {name} {surname} {phone}")

# Update data (name or phone)
def update_data(name=None, phone=None, new_name=None, new_phone=None):
    if new_name:
        cur.execute("UPDATE phonebook SET name = %s WHERE name = %s", (new_name, name))
    if new_phone:
        cur.execute("UPDATE phonebook SET phone = %s WHERE phone = %s", (new_phone, phone))
    con.commit()
    print(f"Updated data for {name or phone}.")

# Query data with a filter (by name or phone)
def query_data(name=None, phone=None):
    if name:
        cur.execute("SELECT * FROM phonebook WHERE name = %s", (name,))
    elif phone:
        cur.execute("SELECT * FROM phonebook WHERE phone = %s", (phone,))
    rows = cur.fetchall()
    if rows:
        for row in rows:
            print(row)
    else:
        print("No matching records found.")

# Delete data by name or phone
def delete_data(name=None, phone=None):
    if name:
        cur.execute("DELETE FROM phonebook WHERE name = %s", (name,))
    elif phone:
        cur.execute("DELETE FROM phonebook WHERE phone = %s", (phone,))
    con.commit()
    print(f"Deleted data for {name or phone}.")

# Display and handle the main menu
def main_menu():
    while True:
        print("\n--- PhoneBook Menu ---")
        print("1. Insert data from CSV file")
        print("2. Insert data manually via console")
        print("3. Update data (name or phone)")
        print("4. Query data (by name or phone)")
        print("5. Delete data (by name or phone)")
        print("6. Exit")
        
        choice = input("Enter your choice (1-6): ")

        if choice == "1":
            filename = input("Enter the path of the CSV file: ")
            insert_from_csv(filename)
        elif choice == "2":
            insert_from_console()
        elif choice == "3":
            print("Updating data...")
            update_choice = input("Do you want to update by (1) Name or (2) Phone? Enter 1 or 2: ")
            if update_choice == "1":
                old_name = input("Enter the old name: ")
                new_name = input("Enter the new name: ")
                update_data(name=old_name, new_name=new_name)
            elif update_choice == "2":
                old_phone = input("Enter the old phone: ")
                new_phone = input("Enter the new phone: ")
                update_data(phone=old_phone, new_phone=new_phone)
        elif choice == "4":
            query_choice = input("Do you want to query by (1) Name or (2) Phone? Enter 1 or 2: ")
            if query_choice == "1":
                name = input("Enter the name to search: ")
                query_data(name=name)
            elif query_choice == "2":
                phone = input("Enter the phone to search: ")
                query_data(phone=phone)
        elif choice == "5":
            delete_choice = input("Do you want to delete by (1) Name or (2) Phone? Enter 1 or 2: ")
            if delete_choice == "1":
                name = input("Enter the name to delete: ")
                delete_data(name=name)
            elif delete_choice == "2":
                phone = input("Enter the phone to delete: ")
                delete_data(phone=phone)
        elif choice == "6":
            print("Exiting...")
            break
        else:
            print("Invalid choice, please try again.")

# Run the main menu
main_menu()

# Close the database connection
cur.close()
con.close()