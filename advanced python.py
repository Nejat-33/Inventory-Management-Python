import json
import re
from pathlib import Path

from mpmath.ctx_mp_python import return_mpc

file_path = Path("open_db.json")
current_user = None
is_logged_in = False



def save_file_of_user(data):
  file = Path("open_db.json")
  try:
    with open(file, 'w') as jsonf:
        json.dump(data, jsonf, indent=4)
  except (IOError, PermissionError) as e:
      print(f"error saving file {e}")



def save_file_of_invent(data):
    file = Path("inventory.json")
    try:
       with open(file, "w") as fi:
           json.dump(data, fi, indent=4)
    except (IOError, PermissionError) as e:
        print(f"error saving file {e}")


def save_user_product(data):
    file = Path("user_product.json")
    try:
        with open(file, "w") as fi:
            json.dump(data, fi, indent=4)
    except (IOError, PermissionError) as e:
        print(f"error saving file {e}")


def load_inv_file():
    file = Path("inventory.json")
    if not file.exists():
        return []
    try:
        with open(file, "r") as fi:
            return json.load(fi)
    except (Exception) as ex:
        print(f"Error : {ex}")
        return []


def load_file_user():
  file = Path("open_db.json")
  if not file.exists():
      return []
  try:
    with open(file, 'r') as jsonf:
        return json.load(jsonf)
  except(FileNotFoundError, json.decoder.JSONDecodeError) as e:
      print(f"error when file loaded {e}")
      return []

def user_product():
    file =Path("user_product.json")
    if not file.exists():
        return []
    try:
        with open(file, 'r') as jsonf:
            return json.load(jsonf)
    except(FileNotFoundError, json.decoder.JSONDecodeError) as e:
        print(f"error when file loaded {e}")
        return []



def is_strong_password(password):
    if len(password) < 8:
        return False
    elif not re.search("[A-Z]", password):
        return False
    elif not re.search("[a-z]", password):
        return False
    elif not re.search("[0-9]", password):
        return False
    elif not re.search("[^A-Za-z0-9]", password):
        return False
    return True

def isvalid_email(email):
    email_pattern = r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    if re.match(email_pattern, email):
        return True
    return False

def register():
    global current_user
    current_user = load_file_user()
    print("\n   -------- Create Account --------")

    while True:
      username = input("Enter your name: ")
      if username.isalnum():
        break
      print('Enter valid username')

    while True:
      email = (input("Enter your email: ")).lower()
      if any(us["email"]== email for us in current_user):
         print("user already exists")
      elif not isvalid_email(email):
         print ("enter valid email")
      else:
        break

    while True:
       password = input("Enter your password: ")
       if is_strong_password(password):
          break
       print("Enter valid password")

    data = {
        "username" : username,
        "email" : email,
        "password" : password,
        "role": "user"
    }
    current_user.append(data)
    save_file_of_user(current_user)
    return print("\nUser registered successfully")


def login():
    print("\n  -------- Login --------")
    password = input("Enter your password: ")
    email =( input("Enter your email: ")).lower()

    current_user = load_file_user()
    for user in current_user:
        if user["email"] == email:
            if user["password"] == password:
                print("Login successful!")
                if user["role"] == "admin":
                    admin_dashboard(user)
                else:
                    user_dashboard(user)
                return
            else:
                print("Invalid password")
                return
    print("User does not exist")


def view_profile(email):
   current_user = load_file_user()
   for user in current_user:
      if user["email"] == email:
          profile_card = f"""
        ------------------------------
        Username : {user.get('username')}
        Email    : {user.get('email')}
        Password : {user.get('password')}
        ------------------------------"""
          return print(profile_card)

   return print("user not found")



def delete_account(email):
    current_user = load_file_user()
    user = len(current_user)

    current_user = [user for user in current_user if user["email"] != email]
    if user > len(current_user):
        save_file_of_user(current_user)
        print(f"\nAccount with email {email} deleted successfully")
        global is_logged_in
        is_logged_in = False
    else:
        print("error deleting user")


def logout():
  global is_logged_in
  is_logged_in = False
  return print("\nlogged out successfully")


def add_product(id, name, price, quantity):
    all_product = load_inv_file()
    if  price < 0:
        return print("product price must be greater number greater than 0")
    if quantity <0 :
        return print("product quantity must be greater than o")

    product = {
        "id": id,
        "name": name,
        "price": price,
        "quantity": quantity
    }
    all_product.append(product)
    save_file_of_invent(all_product)
    return print("\nproduct added successfully")


def view_products():
    current_inv = load_inv_file()
    if len(current_inv) > 0:
        for items in current_inv:
            product_card = f"""
                   ------------------------------
                   Id : {items.get('id')}
                   Name    : {items.get('name')}
                   Price : {items.get('price')}
                   Quantity : {items.get('quantity')}
                   ------------------------------"""
            print(product_card)
    else:
        return print("Product not found")

def update_products_name(id, data):
    current_inv = load_inv_file()
    for items in current_inv:
        if items["id"] == id:
            items["name"] = data
            save_file_of_invent(current_inv)
            return print("\nproduct name updated successfully")

def update_products_price(id, data):
    current_inv = load_inv_file()
    for ite in current_inv:
        if ite["id"] == id:
            ite["price"] = data
            save_file_of_invent(current_inv)
            return print("\nproduct price updated successfully")

def update_product_quantity(id, data):
    current_inv = load_inv_file()
    for it in current_inv:
        if it["id"] == id:
            it["quantity"] = data
            save_file_of_invent(current_inv)
            return print("\nproduct quantity updated successfully")

def delete_product(id):
    current_inv = load_inv_file()
    current = len(current_inv)

    current_inv = [ite for ite in current_inv if ite["id"] != id]
    if len(current_inv) < current:
        save_file_of_invent(current_inv)
        print("\ndelete product successfully")


def show_specific_product(id):
    current_inv = load_inv_file()

    for target in current_inv:
       if target["id"] == id:
         product_card = f"""
                      ------------------------------
                      Id : {target.get('id')}
                      Name    : {target.get('name')}
                      Price : {target.get('price')}
                      Quantity : {target.get('quantity')}
                      ------------------------------"""
         print(product_card)
    else:
      return print("product not found")



def manage_inventory():
    while True:
        print("""
                       ------- Inventory Management-------
                           1. Add Product
                           2. View Products
                           3. Update Products
                           4. Delete Products
                           5. Show Specific Products
                           6. Exit
                       -------------------------------""")


        choice = input("Choice: ")
        try:
         if choice == "1":
            pid = int(input("Enter product id: "))
            name = input("Enter product name: ")
            price = int(input("Enter product price: "))
            quantity = int(input("Enter product quantity: "))
            add_product(pid, name,price, quantity)
         elif choice == "2":
            view_products()
         elif choice == "3":
          while True:
            print("""
                     ------- Update Products -------
                         1. Update Product Name
                         2. Update Product Price
                         3. Update Product Quantity
                         4. Back
                     -------------------------------""")
            choice2 = input("choice: ")

            if choice2 == "1":
                proid = int(input("enter product id: "))
                proname = input("enter product name: ")
                update_products_name(proid, proname)
            elif choice2 == "2":
                proid = int(input("enter product id: "))
                proname = int(input("enter product price: "))
                update_products_price(proid, proname)
            elif choice2 == "3":
                id = int(input("enter product id: "))
                pro = int(input("enter product quantity: "))
                update_product_quantity(id, pro)
            elif choice2 == "4":
                break
         elif choice == "4":
            ch = int(input(" Enter id: "))
            delete_product(ch)
         elif choice == "5":
            ch = int(input("Enter id: "))
            show_specific_product(ch)
         elif choice == "6":
            break
        except ValueError as ex:
            print("please enter number only")


def view_all_user():
    current_user = load_file_user()
    if len(current_user) > 0:
        for user in current_user:
            product_card = f"""
                            ------------------------------
                            Name    : {user.get('username')}
                            Email : {user.get('email')}
                            Role : {user.get('role')} \n
                            ------------------------------"""
            print(product_card)

def delete_any_user(email):
    current_user = load_file_user()
    current = len(current_user)

    for user in current_user:
        if user["email"] == email and user["role"] != "admin":
          updated_file = [user for user in current_user if user["email"] != email]
          if len(updated_file) < current:
            save_file_of_user(updated_file)
            print(f"\nAccount with email {email} deleted successfully")
        else:
            return print("user not found or this user can not be deleted")


def admin_dashboard(user):
    while True:
        print("""
                    ------- Admin Dashboard-------
                        1. View Profile
                        2. Manage Inventory
                        3. View All Users
                        4. Delete Any User
                        5. Logout
                    -------------------------------""")

        choice = input("Choice: ")

        if choice == "1":
            view_profile(user["email"])
        elif choice == "2":
            manage_inventory()
        elif choice == "3":
            view_all_user()
        elif choice == "4":
            cho = input("enter email of user to be deleted: ")
            delete_any_user(cho)
        elif choice == "5":
            logout()
            break


def search_using_id(id):
    current_inv = load_inv_file()
    for item in current_inv:
        if item["id"] == id:
            product_card = f"""
                                  ------------------------------
                                  Id : {item.get('id')}
                                  Name    : {item.get('name')}
                                  Price : {item.get('price')}
                                  Quantity : {item.get('quantity')} \n
                                  ------------------------------"""
            print(product_card)

def search_using_name(name):
    current_inv = load_inv_file()
    for it in current_inv:
        if it["name"].lower() == name:
            product_card = f"""
                                  ------------------------------
                                  Id : {it.get('id')}
                                  Name    : {it.get('name')}
                                  Price : {it.get('price')}
                                  Quantity : {it.get('quantity')} \n
                                  ------------------------------"""
            print(product_card)

def check_stock(id, quantity):
    current_inv = load_inv_file()
    for item in current_inv:
        if item["id"] == id and item["quantity"] > quantity:
             return True
    return False


def update_quantity(pid, quantity):
    current_inv = load_inv_file()
    for item in current_inv:
        if item["id"] == pid and item["quantity"] < quantity:
            item["quantity"] -= quantity
            save_file_of_invent(current_inv)
            return True
    return False


def buy_product(email):
    view_products()
    all_products = load_inv_file()
    all_user_orders = user_product()  # Load the orders file

    try:
        choice = int(input("Enter Product ID: "))
        buy_qty = int(input("Enter Quantity: "))
    except ValueError:
        print("Please enter numbers only.")
        return

    product = next((p for p in all_products if p["id"] == choice), None)

    if not product:
        print("Product ID not found.")
        return

    if product["quantity"] < buy_qty:
        print(f"Not enough stock! (Available: {product['quantity']})")
        return

    user_entry = next((u for u in all_user_orders if u["user"] == email), None)

    order_item = {
        "id": product["id"],
        "name": product["name"],
        "price": product["price"],
        "quantity": buy_qty
    }

    if user_entry:
        existing_item = next((i for i in user_entry["data"] if i["id"] == choice), None)
        if existing_item:
            existing_item["quantity"] += buy_qty
        else:
            user_entry["data"].append(order_item)
    else:
        all_user_orders.append({
            "user": email,
            "data": [order_item]
        })

    save_user_product(all_user_orders)
    update_quantity(choice, buy_qty)
    print(f"\nSuccessfully ordered {buy_qty}x {product['name']}!")

def order_products(email):
    products = user_product()
    if len(products) > 0:
      for item in products:
        if item["user"] == email:
            for item in item["data"]:
                product =  f"""
                                  ------------------------------
                                  Id : {item.get('id')}
                                  Name    : {item.get('name')}
                                  Price : {item.get('price')}
                                  Quantity : {item.get('quantity')} \n
                                  ------------------------------"""
                print(product)
    else:
        return print("there is no product")



def user_dashboard(user):
    while True:
        print("""
                    ------- User Dashboard-------
                        1. View Profile
                        2. View Products
                        3. Search products
                        4. Buy Products
                        5. Order products
                        6. Exits
                    -------------------------------""")

        cho = input("Enter choice: ")
        if cho == "1":
            view_profile(user["email"])
        if cho == "2":
            view_products()
        elif cho == "3":
          while True:
            print("""
                  ------- Search Products -------
                        1. Search by id
                        2. Search by name
                        3. Back
                  -------------------------------""")

            c = input("\nEnter choice: ")
            try:
              if c == "1":
                u_id = int(input("Enter id: "))
                search_using_id(u_id)
              elif c == "2":
                name = input("Enter name: ")
                search_using_name(name.lower())
              elif c == "3":
                break
            except ValueError:
                print("Please enter numbers only.")
        elif cho == "4":
            buy_product(user["email"])
        elif cho == "5":
            order_products(user["email"])
        elif cho == "6":
            break



def change_username(email, updatedvalue):
    current_user = load_file_user()
    for user in current_user:
        if user["email"] == email:
            user["username"] = updatedvalue
            save_file_of_user(current_user)


def change_email(email, updatedvalue):
    current_user = load_file_user()
    for user in current_user:
        if user["email"] == email:
            user["email"] = updatedvalue
            save_file_of_user(current_user)

def change_password(email, updatedvalue):
    current_user = load_file_user()
    for user in current_user:
        if user["email"] == email:
            is_valid = is_strong_password(updatedvalue)
            if is_valid:
              user["password"] = updatedvalue
              save_file_of_user(current_user)
            else:
              return print("invalid password")



def updateprofile(email):
  current_email = email
  while True:
    print("""
                     ------- Update Profile -------
                           1. Change Username
                           2. Change Email
                           3. Change Password
                           4. Back
                     -------------------------------""")
    userinput = int(input("enter your choice: "))
    if userinput == 1:
        newusername = input("enter the new username: ")
        change_username(email, newusername)
        print("\nuser successfully changed username")
    elif userinput == 2:
        newemail = input("enter the new email: ")
        change_email(current_email, newemail.lower())
        current_email = newemail
        print("\nuser successfully changed email")
    elif userinput == 3:
        newpassword = input("enter the new password: ")
        change_password(email, newpassword)
        print("\nuser successfully changed password")
    elif userinput == 4:
       break

while True:
 print("""
        ------- Welcome to our user management system -------
                        1. Register
                        2. Login
                        3. Exit
        -----------------------------------------------------""")
 userinput = (input("Enter your choice: "))
 match(userinput):
     case "1":
         register()
     case "2":
         login()
     case "3":
         break