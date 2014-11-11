#!/usr/bin/env python3

""" Module to test papers.py  """

__author__ = 'Anisha Dhamani and Magdalene Schifferer'

__status__ = "Prototype"

# imports one per line
import pytest
from papers import decide


def test_basic():
    # test for valid test cases
    # test for returning citizen
    assert decide("test_returning_citizen.json", "watchlist.json", "countries.json") == ["Accept", "Accept"]
    # test for traveller in watchlist
    assert decide("test_watchlist.json", "watchlist.json", "countries.json") == ["Secondary"]
    # test for medical advisory
    assert decide("test_quarantine.json", "watchlist.json", "countries.json") == ["Quarantine"]
    # test for visitor visa
    assert decide("test_visitor_visa.json", "watchlist.json", "countries.json") == ["Accept"]
    # test for transit visa
    assert decide("test_transit_visa.json", "watchlist.json", "countries.json") == ["Accept", "Quarantine"]
    # test for lowercase
    assert decide("test_lowercase.json", "watchlist.json", "countries.json") == ["Accept"]


def test_files():
    # file not found test cases
    with pytest.raises(FileNotFoundError):
        decide("test_returning_citizen.json", "", "countries.json")
        decide("test_watchlist.json", "watchlist.json", "")
        decide("test_visitor_visa.json", "watchlist.json", "")
        decide("", "", "countries.json")


def test_invalid():
    # test for invalid test cases
    # test for invalid passport number
    assert decide("test_passport.json", "watchlist.json", "countries.json") == ["Reject"]
    # test for invalid birthdate
    assert decide("test_birthdate.json", "watchlist.json", "countries.json") == ["Reject"]
    # test for invalid visa
    assert decide("test_visa.json", "watchlist.json", "countries.json") == ["Reject"]
    # test for invalid name
    assert decide("test_name.json", "watchlist.json", "countries.json") == ["Reject"]

