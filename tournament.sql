-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- Create the tournament database, if it doesn't already exist
-- Comment this line out of you don't need to create\recreate the database
--CREATE DATABASE tournament;

-- Now that the database exists, connect to it
\c tournament;

-- Drop the all the tables, to start from a clean slate.
DROP TABLE matches;
DROP TABLE players;

-- Create the players table.
-- This table is used to track all the players in each of the tournaments
-- The columns in this table are
--     id: the unique identifier for this tournament
--         this is also the primary key
--     full_name: the full name of the player
--     wins: the number of wins the player has in this tournament
--     losses: the number of losses the player has in this tournament
CREATE TABLE players (id serial primary key,
                        full_name text,
                        wins integer DEFAULT 0,
                        losses integer DEFAULT 0
                     );

-- Create the matches table.
-- This table is used to track all the matches between players in a tournament
-- The columns in this table are
--     id: the unique identifier for this match in the tournament
--     round: the round the players are competing in for this match
--     player_1_id: the unique id of the first player in this match
--     player_2_id: the unique id of the second player in this match
--                  this value might be NULL. This means that player 1 had a bye.
CREATE TABLE matches (  id serial PRIMARY KEY,
                        round integer,
                        player_1_id integer NULL,
                        player_2_id integer NULL,
                        FOREIGN KEY (player_1_id) REFERENCES players (id),
                        FOREIGN KEY (player_2_id) REFERENCES players (id)
                     );

-- Create a View for the Current Standings.
-- This View ranks all the players by wins first, and then OpponentMatchWins
-- The View is structured as follows
--     id: the unique identifier for the player in the tournament
--     full_name: the name of the player
--     wins: the number of matches this player has won in this tournament
--     matches: the total number of matches this player has played in
                the tournament
--     opp_wins: the combined total number of wins from the opponents of this
                 particular player
CREATE VIEW standings AS
    SELECT id,
           full_name,
           wins,
           (wins + losses) AS matches,
           (SELECT SUM(wins) AS opp_wins
            FROM (SELECT player_1_id,
                      players1.wins
               FROM matches
                   INNER JOIN players AS players1
                   ON matches.player_1_id = players1.id
               WHERE player_2_id = players.id
               UNION ALL
               SELECT player_2_id,
                      players2.wins
               FROM matches
                   INNER JOIN players AS players2
                   ON matches.player_2_id = players2.id
               WHERE player_1_id = players.id)
               AS opponentResults)
    FROM players
    ORDER BY wins DESC, opp_wins DESC;