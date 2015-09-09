#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches(tournament_id):
    """Remove all the match records from the database."""
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM matches WHERE tournament_id=(%s);", (tournament_id,))
    conn.commit()
    conn.close()


def deletePlayers(tournament_id):
    """Remove all the player records from the database."""
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM players WHERE tournament_id=(%s);", (tournament_id,))
    conn.commit()
    conn.close()


def countPlayers(tournament_id):
    """Returns the number of players currently registered."""
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(id) FROM players WHERE tournament_id=(%s);", (tournament_id,))
    result = cursor.fetchone()[0]
    conn.close()
    return result


def registerPlayer(name, tournament_id):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO players (tournament_id, full_name) VALUES (%s, %s);", (tournament_id, name,))
    conn.commit()
    conn.close()


def playerStandings(tournament_id):
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    conn = connect()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, full_name, wins, (wins + losses) AS matches FROM players WHERE tournament_id=(%s) ORDER BY wins DESC;",
        (tournament_id,))
    results = cursor.fetchall()
    conn.close()
    return results


def reportMatch(winner, loser, tournament_id):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("UPDATE players SET wins = wins+1 WHERE tournament_id = (%s) AND id=(%s);", (tournament_id, winner,))
    cursor.execute("UPDATE players SET losses = losses+1 WHERE tournament_id = (%s) AND id=(%s);",
                   (tournament_id, loser,))
    conn.commit()
    conn.close()


def swissPairings(tournament_id):
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    conn = connect()
    cursor = conn.cursor()
    standings = playerStandings(tournament_id)
    cursor.execute("SELECT MAX(round) FROM matches WHERE tournament_id=(%s);", (tournament_id,))
    curRound = cursor.fetchone()[0]
    if type(curRound) != int:
        curRound = 0
    for rank in range(0, len(standings), 2):
        cursor.execute(
            "INSERT INTO matches (tournament_id, round, player_1_id, player_2_id) VALUES ((%s), (%s), (%s), (%s));",
            (tournament_id, curRound, standings[rank][0], standings[rank + 1][0],))
        conn.commit()
    cursor.execute('''SELECT player_1_id,
                             players1.full_name,
                             player_2_id,
                             players2.full_name
                      FROM matches
                      INNER JOIN players AS players1
                      ON matches.player_1_id = players1.id
                      INNER JOIN players AS players2
                      ON matches.player_2_id = players2.id
                      WHERE matches.tournament_id=(%s)
                        AND players1.tournament_id=(%s)
                        AND players2.tournament_id=(%s);''', (tournament_id, tournament_id, tournament_id,))
    results = cursor.fetchall()
    conn.close()
    return results
