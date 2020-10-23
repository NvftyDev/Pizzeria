# Adminstrator Log In
# Username = admin
# Password = admin


# Imports
import os
import time
import random
import socket
import pickle
import datetime
import sys

# Client and server transmission
# HEADER_LENGTH = 10
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Sockets
client.connect(('127.0.0.1', 8080)) # Declare IP and PORT

print("\nConnection to Server established...\nTime:"+ time.ctime() + "\nWelcome to SPAM v2!") # SPAM v2 opening message
now = datetime.datetime.now() # Get current date and time.
tday = now.strftime("%A") # Extract the day

day_dict = { # Assign corresponding day numbers to respective names.
    "Monday" : 1,
    "Tuesday" : 2,
    "Wednesday" : 3,
    "Thursday" : 4,
    "Friday" : 5,
    "Saturday" : 6,
    "Sunday" : 7
}


while True:  
    view = input("\n[1] Enter 1 to view today's menu. \n[2] Enter 2 to view another day's menu.\n> ")
    if view == "1":
        print("\nLoading today's menu...")
        today = day_dict[tday] # Get the integer form of the day.
        msg_to_server = today # Request today's menu.
        break
    elif view == "2":
        while True:
            print("\n[1] Monday's Menu \n[2] Tuesday's Menu \n[3] Wednesday's Menu \n[4] Thursday's Menu \n[5] Friday's Menu \n[6] Saturday's Menu\n[7] Sunday's Menu \n[8] SP Anniversary \n[9] New Years Special \n[10] Jolly Christmas")
            try:
                requested = int(input("\nHere are all the menu available. Enter the corresponding number to view.\n> "))
                if requested > 10 or requested < 1:
                    print("Error Enter only numbers from 1 - 10.")
                    continue
                else:
                    msg_to_server = requested # Request other day's menu.
                    break
            except ValueError:
                print("Error. Enter only numbers from 1 - 10.")
                continue          
        break
    else:
        print("Error. Enter only numbers 1 and 2.")
        continue


messageTS = repr(msg_to_server).encode('utf-8') # Encoding to bytes.
client.send(messageTS) # Sending bytes to server.

messageTC = client.recv(4096) # Receiving the menu from server.
# print(messageTC)
d = pickle.loads(messageTC) # Loading the menu from pickle.

# Menu Items
menu = d
# print(type(d)) # Dict
print("\nLoading selected menu...")
print(*d, sep="\n")


print("============================\nWelcome to SPAM Pizzeria:\n============================")  # Opening Message
pizzalogo = open("pizzalogo.txt", "r")
diagram = pizzalogo.read()
pizzalogo.close()
print(diagram) # Print out the diagram.

# Coupon Codes
cpcodes = [  # list
    "TGIF",
    "WeekendFun",
    "NEW15"
]


def adminlogon():  # Key to enter the admin mode.
    crosspass = False  # To exit out of the loop, shall the admin decides to enter the normal mode.
    while True:
        try:
            adminlogin = int(input("\n(1) View Customer Log In Details\n(2) Reset Customer Password\n(3) View Admin Logs\n(4) Edit Menu\n(5) Normal Mode\n> "))
            if adminlogin == 1:  # View Customer Log In Details - View customers' username and password.
                while True:
                    searchfor = input("Enter target customer's username: (Enter 0 to exit) ")
                    searchforfile = searchfor + ".txt"  # [ie.] joe.txt
                    if searchfor == "0":
                        adminlogon()  # Back to the start
                        break
                    try:
                        dump = open(searchforfile, "r+")  # Open targeted user's data file (Read Only)
                        print(dump.read())  # Print targeted user's data file
                        break
                    except FileNotFoundError:  # Error when the file is non existent.
                        print("Error. Customer not found, try again.")
            elif adminlogin == 2:  # Reset Customer Password - In case customers forget their passwords.
                while True:
                    searchfor = input("Enter target customer's username: (Enter 0 to exit) ")
                    searchforfile = searchfor + ".txt"
                    if searchfor == "0":
                        adminlogon()
                        break
                    try:
                        dump = open(searchforfile, "w+")  # Same as earlier, this time with Write only, as there will be over writing to change password.
                        print(dump.read())
                        usernamereset = input("Enter new username: ")
                        passwdreset = input("Enter new password: ")
                        dump.write(usernamereset + passwdreset)
                        break
                    except FileNotFoundError:
                        print("Error. Customer not found, try again.")
            elif adminlogin == 3:  # View Admin Logs - To keep track with Admin Activity in the Admin Mode for security purposes.
                viewlog = open("adminlog.txt", "r")  # Read only, as no one should tamper with the Admin Log.
                print(viewlog.read())
                viewlog.close()
                break
            elif adminlogin == 4:  # Back to normal mode.
                crosspass = True
                break
            else:
                print("Error. Enter numbers 1 - 5 only.")
        except ValueError:
            print("Error. Enter numbers 1 - 5 only.")
        if crosspass == True:
            break


def guesstheday():
    print("Today's day is " + tday)
    if tday == "Friday":
        print("\nTGIF! Weekend is near and here is our Friday coupon code: " + cpcodes [0] + "\nUse code at checkout for a 15per cent storewide discount!")
    elif tday == "Saturday" or "Sunday":
        print("Enjoy your weekend coupon code here: " + cpcodes[1] + "\nUse code at checkout for a 15per cent storewide discount!")
    else:
        print("Constantly check back on weekends for a special gift!")


while True:
    while True:
        try:
            login = int(input("[Sign In]\n(1) Log In with existing account\n(2) Create an account\n(3) Continue as Guest\n> "))  # Sign In Message
            if login > 3 or login < 1:
                login = int("a")
            else:
                break
        except ValueError:
            print("Error. Enter only 1 - 3.") 
    if login == 1:
        wronglogin = True
        while wronglogin == True:
            userlogin = input("Enter your username: ")
            userpasswd = input("Enter your password: ")
            if userlogin == "admin":
                print("==Adminstrator Access== ")
                localtime = time.asctime(time.localtime(time.time()))  # Captures current time of log in
                print("Time of Log In :", localtime)

                logoncount = open("adminlogcount.txt", "r")  # Read-only (Reading counter from the file)
                counter = int(logoncount.read())
                counter += 1  # Counter + 1 every time admin logs in, to keep track of admin activity.
                logoncount.close()
                logoncount = open("adminlogcount.txt", "w")  # Write-only (Writing counter into the file)
                logoncount.write(str(counter))
                logoncount.close()
                viewadminlog = open("adminlog.txt", "a")  # Append-only, no over write (to store logs)
                viewadminlog.write("Entry " + str(counter) + "\nTime of Log In:\n" + str(localtime) + "\n\n")
                viewadminlog.close()
                adminlogon()
            try:
                filename = str(userlogin) + ".txt"
                datafile = open(filename, "r")
                found = False
                for line in datafile:
                    if userlogin in line and userpasswd in line:  # If it is a returning user, it will show successful log in.
                        found = True
                        print("Login Successful. Welcome back, " + userlogin + ".")
                        useronline = userlogin
                        wronglogin = False
                        break
                    else:
                        print("Error. Invalid account credentials. (Hint: Ensure you have the right password!)")  # Wrong password will result in a loop.
                        wronglogin = True
            except FileNotFoundError:
                print("Error. You do not have an account created.")
                useronline = "Guest"
                print("[Auto] Continued as Guest.")  # By Default, when the program doesn't detect an account, it will continue as guest.
                wronglogin = False
    elif login == 2:
        while True:
            createuser = input("Enter your desired username: ")
            createpasswd = input("Enter your password: ")
            confirmpasswd = input("Enter your password again: ")  # To avoid mistyping the password, a verification is needed.
            if createpasswd != confirmpasswd:
                print("Your passwords do not match.")  # User will be prompted to restart the process shall the verification fails.
            else:
                newuserfile = createuser + ".txt"
                f = open(newuserfile, "a+")  # User File being created. From now on, the file is permanent and the user is now a returning customer.
                f.write(createuser)
                f.write(createpasswd)
                useronline = createuser
                print("Welcome " + createuser + "! Use code NEW15 for your first 15per cent off at checkout.")  # Welcome message, with a welcome gift of 15% off coupon code.
                break
    elif login == 3:
        useronline = "Guest"
        break
    else:
        print("Error. Enter only 1 - 3.")
    break


# Function to show Today's Menu
def DisplayTodayMenu():
    print(*d, sep="\n") # Print the menu received by server.


# Function to show Search Menu
def DisplaySearchMenu():
    matches = []
    searchFor = str(input("Enter the food item you are searching for: "))
    matches.append(searchFor)
    lower_matches = [a.lower() for a in matches]
    lower_menu = [b.lower() for b in menu]
    matching = [s for s in lower_menu if any(xs in s for xs in lower_matches)] # Finding a match to search the menu.
    if matching == []:
        print("None found.")
    print(*matching, sep="\n") # Print matching results.


cart = []  # Define cart as list in general for multiple function use.
count = []  # Tracks the order S/N for price tabulation.


# Function "Add to Cart"
def AddToCart():
    while True:
        try:
            userchoice = int(input("Enter the dish number you would like to order, or 0 to stop. "))
            # Since the list index starts with 0, we will need to -1 from the user's input
            # to accurately display the user's selected menu item.
            if userchoice == 0:
                start()
                break
            elif userchoice < 0 or userchoice > 5:
                print("Error. Please only enter between 1 - 5, or 0 to exit. ")
            else:
                cart.append(list(d)[userchoice - 1])
                count.append(userchoice)
        except ValueError:
            print("Error. Please only enter between 1 - 5, or 0 to exit. ")


def ViewCart():
    print("\n-=View your Cart=-\n")
    print(*cart, sep="\n")
    if len(cart) == 0:
        print("Reminder! Your cart is empty.")  # Alert the user when the cart is empty.
    checkoutcheck = False
    while checkoutcheck == False:
        check = int(input("Enter 1 to checkout, 2 to edit cart, 3 to exit: "))
        if check == 1:
            checkout()
            checkoutcheck = True
        elif check == 2:
            print(*cart, sep="\n")
            print("")
            while True:
                try:
                    split = int(input("Enter 1 to add an item, 2 to remove an item, 3 to exit. "))
                    if split == 1:
                        new = int(input("Enter the dish number you would like to order: "))
                        if 0 < new < 6:
                            cart.append(list(d)[new - 1])  # Add users' desired dish to cart.
                            count.append(new)  # Tracks menu item and store it in a list. (for checkout function)
                            print(list(d)[new - 1] + " added successfully.")  # Confirm Message
                            print("")
                            print(*cart, sep="\n")  # Show changes applied
                        else:
                            print("Error. Enter only numbers between 1 - 3.")
                    if split == 2:
                        change = int(input("Enter the dish number you would like to remove from the cart: "))
                        if 0 < change < 6:
                            cart.remove(list(d)[change - 1])  # Remove users' desired dish from cart.
                            count.remove(change)
                            print(list(d)[change - 1] + " removed successfully.")  # Confirm Message
                            print("")
                            print(*cart, sep="\n")  # Show changes applied
                            if len(cart) == 0:
                                print("Cart Empty. Do not attempt to remove anymore items.")  # Alert the user to not remove any more items when the cart it empty.
                        else:
                            print("Error. Enter only numbers between 1 - 3.")
                    if split == 3:
                        start()
                        break
                except ValueError:
                    print("ERROR: \n(i) Enter only numbers between 1 - 3.\n(ii) Do not attempt to remove anymore items "
                          "from the cart if it is empty.")  # Error when ValueError occur or the user had tried removing items from an empty cart.
            checkoutcheck = True
        elif check == 3:
            start()
            checkoutcheck = True
        else:
            print("Enter numbers 1 - 3 only.")


def checkout():
    while True:
        out = False
        coupon = str(input("Enter your available coupon codes (if any). Enter if you do not have a code [Case Sensitive]:"))  # User allowed to apply their coupon code here.
        eligibility = False
        if coupon in cpcodes:
            eligibility = True  # If user's coupon code is found and valid, break from loop expected.
            break
        elif coupon == "":
            break
        else:
            test = False
            while test == False:
                try:
                    errorcode = int(input("Invalid Coupon Codes. Enter 1 to re-try, 2 to exit. "))  # Loop to retreive the rectified code or exit.
                    if errorcode == 1:
                        test = True
                    elif errorcode == 2:
                        test = True
                        out = True
                        break
                    else:
                        print("Error. Enter only numbers 1 and 2.")
                except ValueError:
                    print("Error. Enter only numbers 1 and 2.")
        if out == True:
            break
    i = 0  # Counter
    totalprice = 0 # Starts at 0.
    receipt = [] # Define as list for later use.
    while True:
        try:
            # totalprice += d[count[i]].keys()
            price_list = list(d.values())
            totalprice += price_list[count[i]-1]
            i += 1
        except IndexError:
            break
    if useronline == "admin":
        discounted = totalprice * 0.7  # Admin's exclusive 30% staff discount
        print("Due to your Adminstrator Status, a 30 per cent discount is activated.")
        print("\n==============================\n Order Summary \n==============================\n")
        print(*cart, sep="\n")
        print("-30% (Code Activated)")
        print("\n==============================\nPlease pay $ {:0.2f}".format(discounted) + "\n==============================\n")
        print("Thank you " + useronline + ", for patronising SPAM Pizzeria!\n")
        receipt = cart # Adding the items the user had ordered into the list.
        receipt.append(useronline + " has paid $ {:0.2f}".format(discounted)) # Adding the total sum paid into the list.
    elif eligibility == True:
        discounted = totalprice * 0.85  # Activated Coupon Codes
        print("Discount Code Activated. Enjoy!")
        print("\n==============================\n Order Summary \n==============================\n")
        print(*cart, sep="\n")
        print("-15% (Code Activated)")
        print("\n==============================\nPlease pay $ {:0.2f}".format(discounted) + "\n==============================\n")
        print("Thank you " + useronline + ", for patronising SPAM Pizzeria!\n")
        receipt = cart # Adding the items the user had ordered into the list.
        receipt.append(useronline + " has paid $ {:0.2f}".format(discounted))# Adding the total sum paid into the list.
    else:
        # No Coupon Codes - All Menu Items are charged at their usual price.
        print("\n==============================\n Order Summary \n==============================\n")
        print(*cart, sep="\n")
        print("\n==============================\nPlease pay $ {:0.2f}".format(totalprice) + "\n==============================\n")
        print("Thank you " + useronline + ", for patronising SPAM Pizzeria!\n")
        receipt = cart # Adding the items the user had ordered into the list.
        receipt.append(useronline + " has paid $ {:0.2f}".format(totalprice)) # Adding the total sum paid into the list.

    # Client to send the receipt to server.
    receiptTS = pickle.dumps(receipt)
    client.send(receiptTS)


def start():  # Start
    # Loop
    while True:  # Invoke a constant loop until a break
        print("\nA gateway to everything SPAM Pizzeria\n(1) Order\n(2) Search Menu\n(3) Display "
              "Cart\n(4) Check Out\n")
        selection = input("Please input your choice of action (Enter 0 to exit the program.): ")  # Request for user's choice
        print("If you have selected a menu previously. The same menu can be called again under choice (1).")
        try:
            selection = int(selection)
            if selection == 1:
                print("(1) Order Selected.")  # Call in function to display menu
                print("Retrieving menu selected earlier...")
                DisplayTodayMenu()
                AddToCart()
                break
            elif selection == 2:
                print("(2) Search Menu Selected.")  # Call in function to bring up search menu
                DisplaySearchMenu()
                AddToCart()
                break
            elif selection == 3:
                print("(3) Display Cart Selected.")  # Call in function to display cart
                ViewCart()
                break
            elif selection == 4:
                print("(4) Check Out Selected.")  # Call in function to check out
                checkout()
                break
            elif selection == 0:
                print("\nProgram exited at user input 0.")
                shutDownNotice = "true"
                ForceShutDown = shutDownNotice.encode('utf-8')
                client.send(ForceShutDown)
                exit()
            else:
                print("Invalid Input. Please select only from 1 - 4. Try again.")
        except ValueError:
            print("ERROR: You must enter a number. Try again.")


start()
# End Of Code
