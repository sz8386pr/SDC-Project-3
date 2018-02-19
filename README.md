# SDC-Project-3: RPC(Rock Paper Scissors) Sales Manager
Feb 19, 2018
Created by Scott Kim

Backup: Backup data location
  -backup.json: db backupfile in JSON
Data: DB data dbFolder
  -sales.db: Main db file

-classes.py:  Class objects for holding table values. Mostly used for modifying db
-data.py: Mostly consist of SQL query handling. Also handles backup and restore
          db data.
-README.md: This file
-rpcManager.py: The main 'manager' codes that bridges data.py and ui.py
-rpcProgram.py: The main program. I just felt like having a separate file for
                the program execution
-ui.py: Handles user interface. Menu options as well as displaying table and
        reports



While this project was focused on working with the database using SQLite3,
I tried to minimize sql queries and tried to utilize nested dictionaries as
I haven't utilized dictionaries as much as I should have.
Even though that made coding a bit harder in some instances, I think it was a
good learning experience for me.

Advantage for using dictionaries over sql queries might be reduced traffic,
but also you have to careful about the data integrity too when working with
and manipulating the lists.

I tried to focus on input data validation and spent quite a bit of time working
on it, but I still can't guarantee that it's completely fool proof. I might need
more rigorous testing if time is given.

I also tried to utilize backup/restore features using json data. While I've only
performed a light testing on it, I think it's working smoothly.

Overall
