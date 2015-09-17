#!/usr/bin/env python
#
# Test cases for tournament.py

from tournament import *
from random import randint, random
from math import log, ceil


def clean_tables():
    """
        Cleans the tables in the database,
        to start the tests from a clean slate
    """
    # Start from a clean slate
    deleteMatches()
    deletePlayers()

    # Verify starting from a clean slate
    count = countPlayers()
    if count != 0:
        raise ValueError("After deleting, countPlayers should return zero.")
    else:
        print "Old data removed!"


def add_four_players():
    """
        Adds a specific number of players to the tournament
    """
    # Add 4 players into players table
    registerPlayer("Rose Gellar")
    registerPlayer("Monique Gellar")
    registerPlayer("Rachel Blue")
    registerPlayer("Chandler Ping")

    # Verify four players are registered
    count = countPlayers()
    if count != 4:
        raise ValueError("After registering, countPlayers should return four.")
    else:
        print "Players Registered!"


def add_players(is_even):
    """
        Adds a random number of players to the tournament
        Can add a even number or odd number, to test byes

        Args:
            is_even: boolean representing if an even or odd
                     number of players should be added to the tournament.
    """

    # Pick a number of players to add to the tournament
    # The number of players can be even, or odd (if you want to check on byes)
    num = randint(2, 256)
    if is_even and num % 2 != 0:
        num -= 1
    elif not is_even and num % 2 == 0:
        num += 1

    # Register players
    for player in range(0, num):
        name = "first last" + str(player)
        registerPlayer(name)

    # Verify the players all registered
    count = countPlayers()
    if count != num:
        raise ValueError("After registering, countPlayers should return", num)
    else:
        print "Players Registered!", num


def play_tournament():
    """
        Runs all the rounds required to determine a winner of the tournament
    """
    num_players = countPlayers()
    num_rounds = int(ceil(log(num_players, 2)))
    print "Players in tournament: ", num_players
    print "Rounds to Play: ", num_rounds

    for cur_round in range(0, num_rounds):
        print "Round: ", cur_round
        pairs = swissPairings()

        # Report results for each match matches. We'll make it random whether
        # player 1 or player 2 won, reporting the results accordingly
        for pair in range(0, len(pairs)):
            coin_flip = random()
            if coin_flip <= 0.5:
                reportMatch((pairs[pair])[0], (pairs[pair])[2])
            else:
                reportMatch((pairs[pair])[2], (pairs[pair])[0])


def get_final_results():
    """
        Gets the final standings and returns the wimmer based on wins
        and opponent wins.
    """
    standings = playerStandings()
    print "Final Standings:", standings
    id1 = (standings[0])[0]
    wins_to_beat = (standings[0])[2]

    for player in range(1, len(standings)):
        # Validating that the standings table is ordered correctly
        # Also lets you know how many people tied based on wins (alone)
        if (standings[player])[2] > wins_to_beat:
            raise ValueError("Your winner is not the winner!")
        elif (standings[player])[2] == wins_to_beat:
            print "There's a tie with: ", (standings[player])[0]

    print "And the winner is: ", id1


def test_scenario_basic_four_person_tournament():
    """
        Checks a specific four player scenario
    """
    clean_tables()
    add_four_players()
    play_tournament()
    get_final_results()


def test_scenario_even_person_tournament():
    """
        Checks the even player scenario
    """
    clean_tables()
    add_players(True)
    play_tournament()
    get_final_results()


def test_scenario_odd_person_tournament():
    """
        Checks the odd player scenario
    """
    clean_tables()
    add_players(False)
    play_tournament()
    get_final_results()

if __name__ == '__main__':
    test_scenario_basic_four_person_tournament()
    test_scenario_even_person_tournament()
    test_scenario_odd_person_tournament()
    print "Success!  All functional tests pass!"


