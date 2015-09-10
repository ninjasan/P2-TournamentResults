#!/usr/bin/env python
#
# Test cases for tournament.py

from tournament import *
from random import randint, random
from math import log, ceil


def clean_tables():
    # Start from a clean slate
    deleteMatches()
    deletePlayers()

    # Verify starting from a clean slate
    c = countPlayers()
    if c != 0:
        raise ValueError("After deleting, countPlayers should return zero.")
    else:
        print "Old data removed!"


def add_four_players():
    # Add 4 players into players table
    registerPlayer("Ross Gellar")
    registerPlayer("Monica Gellar")
    registerPlayer("Rachel Green")
    registerPlayer("Chandler Bing")

    # Verify four players are registered
    c = countPlayers()
    if c != 4:
        raise ValueError("After registering, countPlayers should return four.")
    else:
        print "Players Registered!"


def add_players(isEven):
    """

    :rtype : object
    """

    # How many players should be in this tournament, and make sure it's even
    num = randint(2, 256)
    if isEven and num % 2 != 0:
        num -= 1
    elif not isEven and num % 2 == 0:
        num += 1

    # register that many players
    for player in range(0, num):
        registerPlayer("first last")

    # Verify the players all registered
    c = countPlayers()
    if c != num:
        raise ValueError("After registering, countPlayers should return", num)
    else:
        print "Players Registered!", num


def play_tournament(players, rounds):
    print "Players in tournament: ", players
    print "Rounds to Play: ", rounds

    # Play all the rounds in the tournament
    for cur_round in range(0, rounds):
        print "Round: ", cur_round
        # Create the pairs for this round
        pairs = swissPairings()

        # Report results for each match matches
        for pair in range(0, len(pairs)):
            # The winner of the match is 50:50
            coin_flip = random()
            if coin_flip <= 0.5:
                # Player 1 won the match!
                reportMatch((pairs[pair])[0], (pairs[pair])[2])
            else:
                # Player 2 won the match!
                reportMatch((pairs[pair])[2], (pairs[pair])[0])


def get_final_results():
    standings = playerStandings()
    print standings
    id1 = (standings[0])[0]
    winsToBeat = (standings[0])[2]
    for player in range(1, len(standings)):
        if (standings[player])[2] > winsToBeat:
            raise ValueError("Your winner is not the winner!")
        elif (standings[player])[2] == winsToBeat:
            print "There's a tie with: ", (standings[player])[0]
    print "And the winner is: ", id1


def testScenario_BasicFourPersonTournament():
    clean_tables()
    add_four_players()

    # Create matches for round 1
    play_tournament(4, 2)

    # Final results
    get_final_results()

def testScenario_EvenPersonTournament():
    clean_tables()
    add_players(True)

    # Run log2(numplayers) rounds
    num_players = countPlayers()
    num_rounds = int(ceil(log(num_players, 2)))
    play_tournament(num_players, num_rounds)

    get_final_results()


def testScenario_OddPersonTournament():
    clean_tables()
    add_players(False)

    # Run log2(numplayers) rounds
    num_players = countPlayers()
    num_rounds = int(ceil(log(num_players, 2)))
    play_tournament(num_players, num_rounds)

    get_final_results()

if __name__ == '__main__':
    testScenario_BasicFourPersonTournament()
    testScenario_EvenPersonTournament()
    testScenario_OddPersonTournament()
    print "Success!  All functional tests pass!"


