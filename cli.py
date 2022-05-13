import ast
import json
import os
import shutil
import sys
from configparser import ConfigParser

from crypt import generate_key, load_key, encrypt_data, decrypt_data
from database import save_data, load_data
from gui import start_gui


def clear_screen():
    """
    Clear all text from the terminal
    """
    command = "clear"
    if os.name in ("nt", "dos"):  # If Machine is running on Windows, use cls
        command = "cls"
    os.system(command)


def init_settings():
    """
    Load settings from the config.ini file
    """
    config = ConfigParser()
    config.read("config.ini")

    key_location = config["File locations"]["key_location"]
    data_location = config["File locations"]["data_location"]
    loaded_settings = {"key_location": key_location, "data_location": data_location}
    return loaded_settings


def print_menu(menu_name, options):
    clear_screen()
    print("-" * (18 + len(menu_name)))
    print(f"Password Protect: {menu_name}")
    print("-" * (18 + len(menu_name)))
    list_index = 0
    for index in options:
        list_index += 1
        print(str(list_index) + ". " + index)
    while True:
        response = input("Please choose one: ")  # TODO: add ability to add default option "Please choose one [1]: "
        if response.isdecimal():
            break
    return options[int(response) - 1]


def get_data(old_saved_data):
    """
    Get information for new credentials entry
    """
    print("What is the name of the website?")
    website = input("> ")
    print("What is your email or username?")
    username = input("> ")
    print("What is your password?")
    password = input("> ")
    old_saved_data[website] = {"Username": username, "Password": password}
    return old_saved_data


def settings_menu():
    """
    Start the settings menu
    """
    clear_screen()
    print(
        """
------------------------------
Password Protect: Settings
------------------------------

Some Settings Description

1. Key location
2. Data location
3. Save and go back
"""
    )
    config = ConfigParser()
    config.read("config.ini")
    while True:

        response = input("> ")
        if response == "1":
            old_key_location = config.get("File locations", "key_location")
            print("Where would you like to save key files in the future?")
            print("Current location: " + old_key_location)
            while True:
                new_key_location = input("> ")
                if old_key_location == new_key_location:
                    print("Please enter a different location")
                    break
            shutil.move(old_key_location, new_key_location)
            config["File locations"]["key_location"] = new_key_location

        elif response == "2":
            old_data_location = config.get("File locations", "data_location")
            print("Where would you like to save data files in the future?")
            print("Current location: " + old_data_location)
            while True:
                new_data_location = input("> ")
                if old_data_location == new_data_location:
                    print("Please enter a different location")
                    break
            shutil.move(old_data_location, new_data_location)
            config["File locations"]["data_location"] = new_data_location
        elif response == "3":
            with open("config.ini", "w") as configfile:  # save
                config.write(configfile)
            config.write(sys.stdout)
            break


def edit_saved_data(saved_data):
    """
    Edit the saved credentials entry
    """
    print("Edit preexisting credentials")
    saved_data = ast.literal_eval(saved_data)
    index = 1
    keys_list = list(saved_data.keys())
    for i in keys_list:
        print(str(index) + ". " + i)
    selected_key = keys_list[int(input("What? ")) - 1]
    print(
        "Please enter the new data seperated by commas. (For example: nEwWeb$ite,NeW eM@l,NeWpAAssW0rd"
    )
    response = input("> ")
    response = response.split(",")
    saved_data[response[0]] = saved_data[selected_key]
    del saved_data[selected_key]
    return saved_data


def start_cli():
    """
    Start the command line interface
    """
    data = {}
    settings = init_settings()

    while True:
        print("Have you already created key and data files? (Y/n)")
        response = input("> ").lower()
        if response.startswith("y") or response == "":
            key = load_key(settings["key_location"])
            loaded_data = bytes(load_data(), "ascii")
            data = decrypt_data(loaded_data, key)
            break
        elif response.startswith("n"):
            generate_key()
            key = load_key(settings["key_location"])
            break

    while True:
        response = print_menu(menu_name="Main Menu",
                              options=["View saved credentials", "Add new credentials", "Edit preexisting credentials",
                                       "Save changes", "Change settings", "Start graphical interface", "Quit"])
        if response == "View saved credentials":
            if not data:
                print("No saved credentials!")
                continue
            # new_data = ast.literal_eval(data)
            new_data = data
            for i in new_data:
                print(
                    i
                    + ": Username: "
                    + new_data[i]["Username"]
                    + ", Password: "
                    + new_data[i]["Password"]
                )
        elif response == "Add new credentials":
            data = get_data(data)
        elif response == "Edit preexisting credentials":
            edit_saved_data(data)
        elif response == "Save changes":
            encrypted_data = encrypt_data(json.dumps(data), key)
            save_data(encrypted_data)
        elif response == "Change settings":
            settings_menu()
        elif response == "Start graphical interface":
            print("Starting graphical interface")
            start_gui()
        elif response == "Quit":
            clear_screen()
            sys.exit()
        else:
            clear_screen()
            sys.exit()
