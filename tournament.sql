-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- Create the tournament database, if it doesn't already exist
-- Comment this line out of you don't need to recreate the database
--CREATE DATABASE tournament;

-- Now that the database exists, connect to it
\c tournament;

-- Drop the all the tables, to start from a clean slate.
DROP TABLE tournaments;
DROP TABLE players;
DROP TABLE matches;

-- Create the tournaments table, if it doesn't already exist
-- This table will hold all the different activities/sports that players
-- are competing against each other in.
-- The columns in this table are
--     id: the unique identifier for this tournament
--         this is also the primary key
--     sport: the sport/activity players are competing in
CREATE TABLE tournaments (id serial primary key, sport text);

-- Insert into the tournaments table, a sport/activity that people are
-- competing in.
--INSERT INTO tournaments (sport) VALUES ('chess');

-- Create the players table.
-- This table is used to track all the players in each of the tournaments
-- The columns in this table are
--     id: the unique identifier for this tournament
--         this is also the primary key
--     tournament_id: the id of the tournament this player is competing in
--     full_name: the full name of the player
--     wins: the number of wins the player has in this tournament
--     losses: the number of losses the player has in this tournament
CREATE TABLE players (id serial primary key,
                        tournament_id integer references tournaments (id),
                        full_name text,
                        wins integer DEFAULT 0,
                        losses integer DEFAULT 0,
                        );

-- Create the matches table.
CREATE TABLE matches (tournament_id integer references tournaments (id),
                        round integer,
                        player_1_id integer,
                        player_2_id integer,
                        match_result integer,
                        primary key (tournament_id, round, player_1_id, player_2_id)
                        );
