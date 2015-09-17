Getting Started
    Pre-requisites
        1) Follow steps 1-3 from the project instructions
           https://www.udacity.com/course/viewer#!/c-nd004/l-3532028970/m-3631428767
            1) Install Vagrant and Virtual Box
            2) Clone the fullstack-nanodegree-vm repository
            3) Launch the Vagrant VM
    Steps
        2) Create a sub-directory, locally, in the Vagrant directory
            1) Name it whatever you like
        3) Clone project files from:
           https://github.com/ninjasan/P2-TournamentResults.git
           and place them the Vagrant sub-directory you just created.
        4) After SSH-ing into the VM, navigate to the sub-directory where the
           files are stored.
        5) Run the following command in the VM commandline
            psql
        6) If the tournament database already exists, skip this step, if not
           keep reading.
            1) Locally, open the tournament.sql file and uncomment the line 12
               Note: assuming the first line is line 1, not line 0)
               Note: There is also a comment right before that line, pointing
                     you to it.
        7) Once running PostgreSQL, run the command
            \i tournament.sql
        8) Now that the database and tables have been created, you can leave
           exit PostgreSQL, by running the following command
            \q
        9) Run tournaments_test.py and verify the output shows all tests are
           passing.
    Optional other steps
        10) Write/Run other tests to view/check the functionality of the methods
            and database

What's included
    - tournament.py - contains method definitions for interacting with the DB
    - tournament.sql - contains schema definitions for the DB
    - tournament_test.py - contains unit tests for the methods
    - tournament_my_test.py - contains longer functional/scenario tests for the
                              methods
    - this README.txt

Supported Features
    - Creates a database and tables to store players registering for a
      tournament and matches in the tournament
    - Allows for an odd number of players to be registered
    - Ranks players not only by wins, but OpponentMatchWins as well

Credits
    - The Udacity team (created skeleton of tournament.py and tournament_test.py)

Creators
    - Pooja Mathur
