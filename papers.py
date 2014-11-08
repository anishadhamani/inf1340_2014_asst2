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

    input_info = json.load(open(input_file))
    watchlist = json.load(open(watchlist_file))
    countries = json.load(open(countries_file))

    priority_list = ["Quarantine", "Reject", "Secondary", "Accept"]

    for entry in range(len(input_info)):
        result = ["Accept", valid_entry_record(input_info[entry]), test_returning_home(input_info[entry]),
                  test_watchlist(input_info[entry], watchlist), test_quarantine(input_info[entry], countries)]
        print(result)
        # removing None values from the list
        result = [item for item in result if item is not None]
    return result


def valid_entry_record(input_data):
    """
    Checks whether the required information of an entry record is complete or incomplete
    :param input_data: dictionary with information about travellers
    :return: List of strings, Reject if record is not complete
    """
    if not valid_passport_format(input_data["passport"]) or not valid_date_format(input_data["birth_date"]):
        return "Reject"
    if (input_data["first_name"] or input_data["last_name"] or input_data["home"] or input_data["from"] or
            input_data["entry_reason"]) == "":
            return "Reject"


def test_returning_home(input_data):
    """
    Checks whether the traveller is "returning" and home country is "KAN"
    :param input_data: dictionary with information about travellers
    :return: List of strings, Accept if home country is "KAN"
    """
    if input_data["entry_reason"] == "returning" and input_data["home"]["country"] == "KAN":
            return "Accept"


def test_watchlist(input_data, watch_list):
    """
    Checks whether the traveller's name or passport number is on the watchlist
    :param input_data: dictionary with information about travellers
    :param watch_list: list; watchlist provided by Ministry
    :return: List of strings, Secondary if on the watchlist
    """
    for entry in watch_list:
        if (entry["first_name"] == input_data["first_name"] and entry["last_name"] == input_data["last_name"]) or \
                entry["passport"] == input_data["passport"]:
            return "Secondary"


def test_quarantine(input_data, country_list):
    """
    Checks whether the traveller is coming from or via a country that has a medical advisory
    :param input_data: dictionary with information about travellers
    :param country_list: dictionary with list of countries that has medical advisory details provided by Ministry
    :return: List of strings, Quarantine if medical advisory
    """
    if "from" in input_data.keys():
            country_from = input_data["from"]["country"]
            if country_from in country_list and country_list[country_from]["medical_advisory"]:
                return "Quarantine"
    elif "via" in input_data.keys():
            country_from = input_data["via"]["country"]
            if country_from in country_list and country_list[country_from]["medical_advisory"]:
                return "Quarantine"


def valid_visa(input_data):
    """
    Checks whether a visa is valid i.e. less than 2 years old
    :param input_data: dictionary with information about travellers
    :return: Boolean; True if visa is valid, False otherwise
    """
    if "visa" in input_data.keys():
        visa_date = datetime.datetime.strptime(input_data["visa"]["date"], '%Y-%m%d')
        today_date = datetime.datetime.today()
        if visa_date < today_date:
            if (today_date - visa_date).days < 730:
                return True
            else:
                return False
        else:
            print("Invalid date")
            raise ValueError


def test_visitor_visa(input_data, country_list):
    """
    Checks whether the traveller's home country needs a visitor visa if entry reason is visit
    :param input_data: dictionary with information about travellers
    :param country_list: dictionary with list of countries that has visitor visa details provided by Ministry
    :return: List of strings; Reject if visitor visa required and not valid visa
    """
    if input_data["entry_reason"] == "visit" and input_data["home"]["country"] in country_list.keys() and \
       country_list[input_data["home"]["country"]]["visitor_visa_required"] == "1":
        if valid_visa(input_data) is False:
            return "Reject"


def test_transit_visa(input_data, country_list):
    """
    Checks whether the traveller's home country needs a transit visa if entry reason is transit
    :param input_data: dictionary with information about travellers
    :param country_list: dictionary with list of countries that has transit visa details provided by Ministry
    :return: List of strings; Reject if transit visa required and not valid visa
    """
    if input_data["entry_reason"] == "transit" and input_data["home"]["country"] in country_list.keys() and \
       country_list[input_data["home"]["country"]]["transit_visa_required"] == "1":
        if valid_visa(input_data) is False:
            return "Reject"


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
