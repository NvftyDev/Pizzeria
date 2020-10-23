import socket
import pickle
import time
import sys

# Advanced Features:
"""
1. Improved visuals for the program, including validation for server-client interaction.
Server closes when client force shuts down.

2. Ability to view other day's menu.

3. Ability to send the full transaction receipt after the user finished check out, to the server.

"""
try:
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server.bind(('127.0.0.1', 8080)) # Declare IP and PORT.
    server.listen(5) # Limits number of clients at one time.


    print("Server started at [" + time.ctime() + "]\nListening...") # Opening message
    while True:
        clientsocket, address = server.accept()
        print(f"Connection from {address} has been established!") # Shows client incoming connection.
            
        menu = clientsocket.recv(4096) # Receiving client's request for a menu.
        decoded = str(menu, 'utf-8') # Decoding
        if len(decoded) > 0: 
            print("Message received successfully.") # Affirms integrity of message.
        else:
            print("Critical Error.") # Placeholder for else. This should not happen
        # print(decoded)
        decoded = int(decoded)

        list = [  # Nested dictionary in a list. Contains all the menus available.
        { # Monday's Menu
        "1  Hawaiian Pizza:            $ 10.00" : 10.00,
        "2  Cheesy Pizza:              $  9.50" :  9.50,
        "3  Soup of the day:           $  6.00" :  6.00,
        "4  Salted Fries:              $  4.00" :  4.00,
        "5  Ice Cream:                 $  3.50" :  3.50
        },
        {  # Tuesday's Menu
        "1  Meat Lover Pizza:          $ 15.50" : 15.50,
        "2  Vegetable Lover Pizza:     $ 12.00" : 12.00,
        "3  Soup of the day:           $  6.00" :  6.00,
        "4  Tuesday Wings:             $  9.00" :  9.00,
        "5  Eclairs:                   $  5.50" :  5.50
        }, 
        {  # Wedneday's Menu
        "1  Seafood Lover Pizza:       $ 16.50" : 16.50,
        "2  Pepperoni Pizza:           $ 14.00" : 14.00,
        "3  Soup of the day:           $  6.00" :  6.00,
        "4  Popcorn Chicken:           $  7.00" :  7.00,
        "5  Donuts:                    $  4.50" :  4.50
        }, 
        {  # Thursday's Menu
        "1  Hawaiian Pizza:            $ 13.50" : 13.50,
        "2  Pepperoni Pizza:           $ 14.00" : 14.00,
        "3  Soup of the day:           $  6.00" :  6.00,
        "4  Cheese Fries:              $  5.00" :  5.00,
        "5  Milkshakes:                $  2.50" :  2.50
        }, 
        {  # Friday's Menu
        "1  Seafood Lover Pizza:       $ 16.50" : 16.50,
        "2  Meat Lover Pizza:          $ 15.00" : 15.00,
        "3  Soup of the day:           $  6.00" : 6.00,
        "4  Spicy Drumlets:            $  9.00" : 9.00,
        "5  Assorted Fruits:           $  1.50" : 1.50
        }, 
        {  # Saturday's Menu
        "1  Vegetable Lover Pizza:     $ 12.00" : 12.00,
        "2  Cheesy Pizza:              $  9.50" :  9.50,
        "3  Soup of the day:           $  6.00" :  6.00,
        "4  Fish and Chips             $ 10.00" : 10.00,
        "5  Assorted Cakes:            $  4.50" :  4.50
        }, 
        {  # Sunday's Menu
        "1  Tropical Pizza:            $ 12.50" : 12.50,
        "2  Mushroom Delight Pizza:    $ 12.00" : 12.00,
        "3  Soup of the day:           $  6.00" :  6.00,
        "4  Fried Chicken:             $  6.00" :  6.00,
        "5  Lava Cake:                 $  4.50" :  4.50
        }, 
        {  # SP Anniversary
        "1  So Possible Pizza:         $ 13.00" : 13.00,
        "2  Founders Pizza:            $ 13.00" : 13.00,
        "3  Clam Chowder Soup:         $  6.50" :  6.50,
        "4  Honey Roasted Wings:       $  8.00" :  8.00,
        "5  Champagne:                 $  2.50" :  2.50
        }, 
        {  # New Years Special
        "1  Prosperity Pizza:          $ 11.50" : 11.50,
        "2  Fortune Pizza:             $ 12.00" : 12.00,
        "3  Pumpkin Soup               $  5.50" :  5.50,
        "4  Prosperity Toss:           $ 18.80" : 18.80,
        "5  Mandarin Oranges:          $  3.50" :  3.50
        }, 
        {  # Jolly Christmas
        "1  Christmas Pizza:           $ 15.00" : 15.00,
        "2  Santa's Snack:             $  9.00" :  9.00,
        "3  Cauliflower soup:          $  7.00" :  7.00,
        "4  Roasted Turkey:            $ 25.00" : 25.00,
        "5  Sweet Christmas Treats:    $  1.00" :  1.00
        }] # End of list

        msg_to_client = (list[decoded-1]) # Prepare menu to be sent to client with the request from client earlier.

        messageTC = pickle.dumps(msg_to_client) # Pickling of the menu dictionary.
        # print(messageTC)

        clientsocket.send(messageTC) # Sending menu to client...
    
        receiptTS = clientsocket.recv(4096) # Receiving receipt from client after checkout
        # print(messageTC)
        r = pickle.loads(receiptTS) # Loading the receipt with pickle.
        print("\n==============================\n Transaction Recorded \n==============================\n")
        print(*r, sep="\n") # Print the receipt on server.
        if len(r) == 0:
            print("Critical Error. Server terminated the transmission.\nError: Received no data from client.") # Placeholder for else. This should not happen.
            exit()
        else:
            print("\n==============================\n  Transaction Closed  \n==============================\n")
            print("\nConnection to Client closed...\nTime:"+ time.ctime()) # Shows time of disconnection.
            exit() # Disconnection
except pickle.UnpicklingError: # Server disconnects when client abruptly disconnects.
    print("\nConnection abruptly closed by client. Program exited.")
    print("Connection to Client closed...\nTime:"+ time.ctime()) # Shows time of disconnection.
    sys.exit() # Disconnection