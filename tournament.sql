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
