#!/usr/bin/env python3

""" Module to test papers.py  """

__author__ = 'Susan Sim'
__email__ = "ses@drsusansim.org"

__copyright__ = "2014 Susan Sim"
__license__ = "MIT License"

__status__ = "Prototype"

# imports one per line
import pytest
from papers import decide


def test_basic():
    # test for valid test cases
    # test for returning citizen
    assert decide("/Users/irfanmavani/PycharmProjects/inf1340_2014_asst2/test_returning_citizen.json",
                  "/Users/irfanmavani/PycharmProjects/inf1340_2014_asst2/watchlist.json",
                  "/Users/irfanmavani/PycharmProjects/inf1340_2014_asst2/countries.json") == ["Accept", "Accept"]
    # test for traveller in watchlist
    assert decide("/Users/irfanmavani/PycharmProjects/inf1340_2014_asst2/test_watchlist.json",
                  "/Users/irfanmavani/PycharmProjects/inf1340_2014_asst2/watchlist.json",
                  "/Users/irfanmavani/PycharmProjects/inf1340_2014_asst2/countries.json") == ["Secondary"]
    # test for medical advisory
    assert decide("/Users/irfanmavani/PycharmProjects/inf1340_2014_asst2/test_quarantine.json",
                  "/Users/irfanmavani/PycharmProjects/inf1340_2014_asst2/watchlist.json",
                  "/Users/irfanmavani/PycharmProjects/inf1340_2014_asst2/countries.json") == ["Quarantine"]


def test_files():
    # file not found test cases
    with pytest.raises(FileNotFoundError):
        decide("test_returning_citizen.json", "", "countries.json")
        decide("test_watchlist.json", "watchlist.json", "")
        decide("test_returning_citizen.json", "watchlist.json", "")
        decide("", "", "countries.json")


def test_invalid():
    # test for invalid test cases
    # test for invalid passport number
    assert decide("/Users/irfanmavani/PycharmProjects/inf1340_2014_asst2/test_passport.json",
                  "/Users/irfanmavani/PycharmProjects/inf1340_2014_asst2/watchlist.json",
                  "/Users/irfanmavani/PycharmProjects/inf1340_2014_asst2/countries.json") == ["Reject"]
    # test for invalid birthdate
    assert decide("/Users/irfanmavani/PycharmProjects/inf1340_2014_asst2/test_birthdate.json",
                  "/Users/irfanmavani/PycharmProjects/inf1340_2014_asst2/watchlist.json",
                  "/Users/irfanmavani/PycharmProjects/inf1340_2014_asst2/countries.json") == ["Reject"]
    # test for invalid visa
    assert decide("/Users/irfanmavani/PycharmProjects/inf1340_2014_asst2/test_visa.json",
                  "/Users/irfanmavani/PycharmProjects/inf1340_2014_asst2/watchlist.json",
                  "/Users/irfanmavani/PycharmProjects/inf1340_2014_asst2/countries.json") == ["Reject"]

