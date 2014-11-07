#!/usr/bin/env python3

""" Computer-based immigration office for Kanadia """

__author__ = 'Susan Sim'
__email__ = "ses@drsusansim.org"

__copyright__ = "2014 Susan Sim"
__license__ = "MIT License"

__status__ = "Prototype"

# imports one per line
import re
import datetime
import json


def decide(input_file, watchlist_file, countries_file):
    """
    Decides whether a traveller's entry into Kanadia should be accepted

    :param input_file: The name of a JSON formatted file that contains cases to decide
    :param watchlist_file: The name of a JSON formatted file that contains names and passport numbers on a watchlist
    :param countries_file: The name of a JSON formatted file that contains country data, such as whether
        an entry or transit visa is required, and whether there is currently a medical advisory
    :return: List of strings. Possible values of strings are: "Accept", "Reject", "Secondary", and "Quarantine"
    """
    try:
        with open("example_entries.json", "r") as file_reader:
            input_file = json.loads(file_reader.read())
            print(input_file)

        with open("watchlist.json", "r") as file_reader:
            watchlist_file = json.loads(file_reader.read())
            print(watchlist_file)

        with open("countries.json", "r") as file_reader:
            countries_file = json.loads(file_reader.read())
            print(countries_file)
    except FileNotFoundError:
        raise FileNotFoundError("File not found")

    return ["Reject"]


def valid_entry_record(input_data):
    """
    Checks whether the required information of an entry record is complete or incomplete
    :param input_data: dictionary with information about travellers
    :return: Boolean; True if record is complete, False otherwise
    """
    for entry in input_data.values():
        if not valid_passport_format(input_data["passport"]):
            return ["Reject"]
        if not valid_date_format(input_data["birth_date"]):
            return ["Reject"]
        if (input_data["first_name"]) is None or (input_data["last_name"]) is None or (input_data["home"]) is None or \
                (input_data["from"]) is None or (input_data["entry_reason"]) is None:
            return ["Reject"]


def test_returning_home(input_data):
    """
    Checks whether the traveller is "returning" and home country is "KAN"
    :param input_data: dictionary with information about travellers
    :return: List of strings, Accept if home country is "KAN", None otherwise
    """
    for entry in input_data:
        if entry["entry_reason"] == "returning" and entry["home"]["country"] == "KAN":
            return ["Accept"]
        else:
            return None


def test_watchlist(input_data, watch_list):
    """
    Checks whether the traveller's name or passport number is on the watchlist
    :param input_data: dictionary with information about travellers
    :param watch_list: watchlist provided by Ministry
    :return: List of strings, Secondary if on the watchlist, None otherwise
    """

    for entry in watch_list:
        if (entry["first_name"] == input_data["first_name"] and entry["last_name"] == input_data["last_name"]) or \
                entry["passport"] == input_data["passport"]:
            return ["Secondary"]
        else:
            return None


def test_quarantine(input_data, country_list):
    """
    Checks whether the traveller is coming from or via a country that has a medical advisory
    :param input_data: dictionary with information about travellers
    :param country_list: list of countries with medical advisory provided by Ministry
    :return: List of strings, Quarantine if medical advisory, None otherwise
    """
    for entry in country_list:
        if (entry["from"]["country"] or entry["via"]["country"]) in country_list and country_list["medical_advisory"]:
            return ["Quarantine"]
        else:
            return None


def valid_visa(input_data):
    """
    Checks whether a visa is valid i.e. less than 2 years old
    :param input_data: dictionary with information about travellers
    :return: Boolean; True if visa is valid, False otherwise
    """
    if "visa" in input_data.keys():
        visa_date = datetime.datetime.strptime(input_data["visa"]["date"], '%Y-%m%d')
        today_date = datetime.datetime.today()
        if (today_date - visa_date).year < 2:
            return True
        else:
            return False


def valid_passport_format(passport_number):
    """
    Checks whether a passport number is five sets of five alpha-number characters separated by dashes
    :param passport_number: alpha-numeric string
    :return: Boolean; True if the format is valid, False otherwise
    """
    passport_format = re.compile('.{5}-.{5}-.{5}-.{5}-.{5}')

    if passport_format.match(passport_number):
        return True
    else:
        return False


def valid_date_format(date_string):
    """
    Checks whether a date has the format YYYY-mm-dd in numbers
    :param date_string: date to be checked
    :return: Boolean True if the format is valid, False otherwise
    """
    try:
        datetime.datetime.strptime(date_string, '%Y-%m-%d')
        return True
    except ValueError:
        return False
