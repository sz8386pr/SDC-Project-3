import sqlite3, traceback, os, sys, json
from ui import message

''' initial setup to create table and insert intial records'''
dbFolder = "Data"
dbFile = os.path.join(dbFolder, "sales.db")

db = sqlite3.connect(dbFile) # Creates or opens database file
cur = db.cursor() # Need a cursor object to perform operations

def setup():

    ''' makedirs referenced from https://stackoverflow.com/questions/273192/how-can-i-create-a-directory-if-it-does-not-exist '''
    try:
        os.makedirs(dbFolder)
    except OSError as e:
        pass #Do nothing if directory exists

    cur.execute("PRAGMA foreign_keys=ON") # Enforces foreign key constraints

    # Create tables if not exist
    try:
        cur.execute("CREATE TABLE if not exists \"venues\" ( `venueID` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, `name` TEXT NOT NULL );")
        cur.execute("CREATE TABLE if not exists \"games\" ( `gameID` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, `dates` TEXT, `venueID` INTEGER, FOREIGN KEY(`venueID`) REFERENCES `venues`(`venueID`) );")
        cur.execute("CREATE TABLE if not exists \"merchandise\" ( `mercID` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, `name` TEXT, `price` INTEGER );")
        cur.execute("CREATE TABLE if not exists \"dailySales\" ( `dateID` INTEGER NOT NULL, `mercID` INTEGER NOT NULL, `sold` INTEGER DEFAULT 0, FOREIGN KEY(`dateID`) REFERENCES `games`(`gameID`), FOREIGN KEY(`mercID`) REFERENCES `merchandise`(`mercID`), UNIQUE ('dateID', `mercID`) );")
        db.commit()

    except sqlite3.Error as e:
        print("{} error has occured".format(e))
        traceback.print_exc() # Displays a stack trace, useful for debugging
        db.rollback()    # Optional - depends on what you are doing with the db

    # Load table values from JSON files
    VENUES, GAMES, MERCHANDISE, DAILYSALES  = loadRecordsFromJSON()

    # Insert/replace table values if not exist
    # Some reference from https://devopsheaven.com/sqlite/databases/json/python/api/2017/10/11/sqlite-json-data-python.html
    try:
        for venue in VENUES:
            cur.execute("INSERT OR REPLACE INTO 'venues' ('venueID', 'name') VALUES (?,?)", [venue['venueID'],venue['name']])
        db.commit()
    except sqlite3.Error as e:
        print("{} error has occured".format(e))
        traceback.print_exc()
        db.rollback()

    try:
        for game in GAMES:
            cur.execute("INSERT OR REPLACE INTO 'games' ('gameID', 'dates', 'venueID') VALUES (?,?,?)", [game['gameID'],game['dates'],game['venueID']])
        db.commit()
    except sqlite3.Error as e:
        print("{} error has occured".format(e))
        traceback.print_exc()
        db.rollback()

    try:
        for merc in MERCHANDISE:
            cur.execute("INSERT OR REPLACE INTO 'merchandise' ('mercID', 'name', 'price') VALUES (?,?,?)", [merc['mercID'],merc['name'],merc['price']])
        db.commit()
    except sqlite3.Error as e:
        print("{} error has occured".format(e))
        traceback.print_exc()
        db.rollback()

    try:
        for sale in DAILYSALES:
            cur.execute("INSERT OR REPLACE INTO 'dailySales' ('dateID', 'mercID', 'sold') VALUES (?,?,?)", [sale['dateID'],sale['mercID'],sale['sold']])
        db.commit()
    except sqlite3.Error as e:
        print("{} error has occured".format(e))
        traceback.print_exc()
        db.rollback()



def loadRecordsFromJSON():
    ''' JSON file name/path '''
    VENUES_FILE = os.path.join('data', 'venues.json')
    GAMES_FILE =  os.path.join('data', 'games.json')
    MERCHANDISE_FILE = os.path.join('data', 'merchandise.json')
    DAILYSALES_FILE = os.path.join('data', 'dailySales.json')

    try :
        with open(VENUES_FILE) as f:
            VENUES = json.load(f)
    except FileNotFoundError:
        VENUES = None

    try :
        with open(GAMES_FILE) as f:
            GAMES = json.load(f)
    except FileNotFoundError:
        GAMES = None

    try :
        with open(MERCHANDISE_FILE) as f:
            MERCHANDISE = json.load(f)
    except FileNotFoundError:
        MERCHANDISE = None

    try :
        with open(DAILYSALES_FILE) as f:
            DAILYSALES = json.load(f)
    except FileNotFoundError:
        DAILYSALES = None

    return VENUES, GAMES, MERCHANDISE, DAILYSALES

def getVenueName(venueID):

    try:
        cur.execute("SELECT name FROM venues WHERE venueID = ?", (venueID,))
        venue = cur.fetchone()[0]
        return venue

    except sqlite3.Error as e:
        print("{} error has occured".format(e))
        traceback.print_exc() # Displays a stack trace, useful for debugging
        db.rollback()    # Optional - depends on what you are doing with the db

    except TypeError:
        message("Venue with venueID {} does not exist".format(venueID))
        return None

'''games table'''

def gameInsert(dates, venueID):

    venueName = getVenueName(venueID)

    if venueName is not None:
        try:
            cur.execute("INSERT OR REPLACE INTO games ('dates', 'venueID') values(?,?)", (dates, venueID,))
            db.commit()
            message("The game on {} at {} record has been added to the database".format(dates, venueName))
        except sqlite3.Error as e:
            print("{} error has occured".format(e))
            traceback.print_exc() # Displays a stack trace, useful for debugging
            db.rollback()    # Optional - depends on what you are doing with the db

def gameUpdate(gameID, dates, venueID):
    # global db
    # global cur

    venueName = getVenueName(venueID)

    if venueName is not None:
        try:
            cur.execute("UPDATE games SET dates = (?), venueID = (?) WHERE gameID = (?)", (dates, venueID, gameID,))
            db.commit()
            message("GameID: {} record has been updated with the game on {} at {}".format(gameID, dates, venueName))
        except sqlite3.Error as e:
            print("{} error has occured".format(e))
            traceback.print_exc() # Displays a stack trace, useful for debugging
            db.rollback()    # Optional - depends on what you are doing with the db


def gameDelete(gameID):

    try:
        cur.execute("DELETE FROM games WHERE 'gameID' =(?)", (gameID,))
        # db.commit()
        message("GameID {} has been deleted from the database".format(gameID))

    except sqlite3.Error as e:
        print("{} error has occured".format(e))
        traceback.print_exc() # Displays a stack trace, useful for debugging
        db.rollback()    # Optional - depends on what you are doing with the db


'''merchandise table'''
def merchandiseInsert(name, price):

    try:
        cur.execute("INSERT OR REPLACE INTO merchandise ('name', 'price') values(?,?)", (name, price*100,))
        # db.commit()
        message("A new merchandise {} for ${} has been added to the database".format(name, price))
    except sqlite3.Error as e:
        print("{} error has occured".format(e))
        traceback.print_exc() # Displays a stack trace, useful for debugging
        db.rollback()    # Optional - depends on what you are doing with the db


def merchandiseUpdate(mercID, name, price):
    
    try:
        cur.execute("UPDATE merchandise SET name = (?), price = (?) WHERE mercID = (?)", (name, price*100, mercID,))
        db.commit()
        message("MerchandiseID: {} record has been updated with {} for ${}".format(mercID, name, price))
    except sqlite3.Error as e:
        print("{} error has occured".format(e))
        traceback.print_exc() # Displays a stack trace, useful for debugging
        db.rollback()    # Optional - depends on what you are doing with the db




def quit():
    ''' Close DB '''
    # global db

    message("Closing database")
    db.close



# setup()
