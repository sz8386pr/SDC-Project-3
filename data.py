import sqlite3, traceback, os, sys, json
from ui import message
from classes import Game, Merchandise, Sales

dbFolder = "Data"
dbFile = os.path.join(dbFolder, "sales.db")

db = sqlite3.connect(dbFile) # Creates or opens database file
cur = db.cursor() # Need a cursor object to perform operations

''' initial setup to create table and insert intial records'''
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
        cur.execute("CREATE TABLE if not exists \"sales\" ( `gameID` INTEGER NOT NULL, `mercID` INTEGER NOT NULL, `sold` INTEGER DEFAULT 0, FOREIGN KEY(`gameID`) REFERENCES `games`(`gameID`), FOREIGN KEY(`mercID`) REFERENCES `merchandise`(`mercID`), UNIQUE ('gameID', `mercID`) );")
        db.commit()

    except sqlite3.Error as e:
        print("{} error has occured".format(e))
        traceback.print_exc() # Displays a stack trace, useful for debugging
        db.rollback()    # Optional - depends on what you are doing with the db

    # Load table values from JSON files
    venuesData, gamesData, mercData, salesData  = loadRecordsFromJSON()

    # Insert/replace table values if not exist
    # Some reference from https://devopsheaven.com/sqlite/databases/json/python/api/2017/10/11/sqlite-json-data-python.html
    try:
        for venue in venuesData:
            cur.execute("INSERT OR REPLACE INTO 'venues' ('venueID', 'name') VALUES (?,?)", [venue['venueID'],venue['name']])
        db.commit()
    except sqlite3.Error as e:
        print("{} error has occured".format(e))
        traceback.print_exc()
        db.rollback()

    try:
        for game in gamesData:
            cur.execute("INSERT OR REPLACE INTO 'games' ('gameID', 'dates', 'venueID') VALUES (?,?,?)", [game['gameID'],game['dates'],game['venueID']])
        db.commit()
    except sqlite3.Error as e:
        print("{} error has occured".format(e))
        traceback.print_exc()
        db.rollback()

    try:
        for merc in mercData:
            cur.execute("INSERT OR REPLACE INTO 'merchandise' ('mercID', 'name', 'price') VALUES (?,?,?)", [merc['mercID'],merc['name'],merc['price']])
        db.commit()
    except sqlite3.Error as e:
        print("{} error has occured".format(e))
        traceback.print_exc()
        db.rollback()

    try:
        for sale in salesData:
            cur.execute("INSERT OR REPLACE INTO 'sales' ('gameID', 'mercID', 'sold') VALUES (?,?,?)", [sale['gameID'],sale['mercID'],sale['sold']])
        db.commit()
    except sqlite3.Error as e:
        print("{} error has occured".format(e))
        traceback.print_exc()
        db.rollback()


''' load default dataset from the json files'''
def loadRecordsFromJSON():
    ''' JSON file name/path '''
    VENUES_FILE = os.path.join('data', 'venues.json')
    GAMES_FILE =  os.path.join('data', 'games.json')
    MERCHANDISE_FILE = os.path.join('data', 'merchandise.json')
    SALES_FILE = os.path.join('data', 'sales.json')

    try :
        with open(VENUES_FILE) as f:
            venuesData = json.load(f)
    except FileNotFoundError:
        venuesData = None

    try :
        with open(GAMES_FILE) as f:
            gamesData = json.load(f)
    except FileNotFoundError:
        gamesData = None

    try :
        with open(MERCHANDISE_FILE) as f:
            mercData = json.load(f)
    except FileNotFoundError:
        mercData = None

    try :
        with open(SALES_FILE) as f:
            salesData = json.load(f)
    except FileNotFoundError:
        salesData = None

    return venuesData, gamesData, mercData, salesData



''' read/create objects/lists '''
def readDB():
    try:
        cur.execute('SELECT * FROM games')
        gamesData = cur.fetchall()
        cur.execute('SELECT * FROM merchandise')
        mercData = cur.fetchall()
        cur.execute('SELECT * FROM sales')
        salesData = cur.fetchall()
        cur.execute('SELECT * FROM venues')
        venuesData = cur.fetchall()

        return gamesData, mercData, salesData, venuesData

    except sqlite3.Error:
        return None, None, None, None



''' database manipulations '''
'''games table'''
def gameManipulate(gameObj, option):
    gameID = gameObj.gameID
    dates = gameObj.dates
    venueID = gameObj.venueID

    venueName = getVenueName(venueID)

    # add/insert new game data
    if option == 1:
        try:
            cur.execute("INSERT INTO games ('gameID', 'dates', 'venueID') values(?,?,?)", (gameID, dates, venueID,))
            # db.commit()
            message("GameID:{} Game on {} at {} record has been added to the database".format(gameID, dates, venueName))
            return True
        except sqlite3.Error as e:
            print("{} error has occured".format(e))
            traceback.print_exc() # Displays a stack trace, useful for debugging
            db.rollback()    # Optional - depends on what you are doing with the db
            return False

    # modify an existing game data
    elif option == 2:
        try:
            cur.execute("UPDATE games SET dates = (?), venueID = (?) WHERE gameID = (?)", (dates, venueID, gameID,))
            # db.commit()
            message("GameID:{} has been updated with the game on {} at {}".format(gameID, dates, venueName))
            return True
        except sqlite3.Error as e:
            print("{} error has occured".format(e))
            traceback.print_exc() # Displays a stack trace, useful for debugging
            db.rollback()    # Optional - depends on what you are doing with the db
            return False

    # delete an existing game data
    elif option == 3:
        try:
            cur.execute("DELETE FROM games WHERE 'gameID' =(?)", (gameID,))
            # db.commit()
            message("GameID:{} has been deleted from the database".format(gameID))
            return True
        except sqlite3.Error as e:
            print("{} error has occured".format(e))
            traceback.print_exc() # Displays a stack trace, useful for debugging
            db.rollback()    # Optional - depends on what you are doing with the db
            return False



'''merchandise table'''
def merchandiseManipulate(merchandiseObj, option):
    mercID = merchandiseObj.mercID
    name = merchandiseObj.name
    price = merchandiseObj.price

    # add/insert new merchandise data
    if option == 1:
        try:
            cur.execute("INSERT INTO merchandise ('mercID', 'name', 'price') values(?, ?,?)", (mercID, name, price,))
            # db.commit()
            message("A new merchandiseID:{} {} for ${:.2f} has been added to the database".format(mercID, name, price))
            return True
        except sqlite3.Error as e:
            print("{} error has occured".format(e))
            traceback.print_exc() # Displays a stack trace, useful for debugging
            db.rollback()    # Optional - depends on what you are doing with the db
            return False

    # modify an existing merchandise data
    elif option == 2:
        try:
            cur.execute("UPDATE merchandise SET name = (?), price = (?) WHERE mercID = (?)", (name, price, mercID,))
            # db.commit()
            message("MerchandiseID:{} record has been updated with {} for ${}".format(mercID, name, price))
            return True
        except sqlite3.Error as e:
            print("{} error has occured".format(e))
            traceback.print_exc() # Displays a stack trace, useful for debugging
            db.rollback()    # Optional - depends on what you are doing with the db
            return False

    # delete an existing merchandise data
    elif option == 3:
        try:
            cur.execute("DELETE FROM merchandise WHERE 'mercID' =(?)", (mercID,))
            # db.commit()
            message("MerchandiseID:{} has been deleted from the database".format(mercID))
            return True
        except sqlite3.Error as e:
            print("{} error has occured".format(e))
            traceback.print_exc() # Displays a stack trace, useful for debugging
            db.rollback()    # Optional - depends on what you are doing with the db
            return False


'''sales table'''
def salesManipulate(salesObj, option):
    gameID = salesObj.gameID
    mercID = salesObj.mercID
    sold = salesObj.sold
    date = getDates(gameID)
    mercName, price = getMercInfo(mercID)

    # add/insert new merchandise data
    if option == 1:
        try:
            cur.execute("INSERT INTO sales ('gameID', 'mercID', 'sold') values(?,?,?)", (gameID, mercID, sold,))
            # db.commit()
            message("A new record has been added to the database: Sold {} {} On {}".format(sold, mercName, date))
            return True
        except sqlite3.Error as e:
            print("{} error has occured".format(e))
            traceback.print_exc() # Displays a stack trace, useful for debugging
            db.rollback()    # Optional - depends on what you are doing with the db
            return False

    # modify an existing merchandise data
    elif option == 2:
        try:
            cur.execute("UPDATE sales SET sold = (?) WHERE gameID = (?) AND mercID = (?)", (sold, gameID, mercID,))
            # db.commit()
            message("Number of sales for {} on {} has changed to {}".format(mercName, date, sold))
            return True
        except sqlite3.Error as e:
            print("{} error has occured".format(e))
            traceback.print_exc() # Displays a stack trace, useful for debugging
            db.rollback()    # Optional - depends on what you are doing with the db
            return False

    # delete an existing merchandise data
    elif option == 3:
        try:
            cur.execute("DELETE FROM sales WHERE gameID = (?) AND mercID = (?)", (gameID, mercID,))
            # db.commit()
            message("A sales record for {} on {} has been deleted".format(mercName, date))
            return True
        except sqlite3.Error as e:
            print("{} error has occured".format(e))
            traceback.print_exc() # Displays a stack trace, useful for debugging
            db.rollback()    # Optional - depends on what you are doing with the db
            return False



''' veues table '''
def venuesManipulate(venuesObj, option):
    venueID = venuesObj.venueID
    name = venuesObj.name

    # add/insert new merchandise data
    if option == 1:
        try:
            cur.execute("INSERT INTO venues ('venueID', 'name') values(?,?)", (venueID, name,))
            # db.commit()
            message("A venue ID:{} {} has been added to the database".format(venueID, name))
            return True
        except sqlite3.Error as e:
            print("{} error has occured".format(e))
            traceback.print_exc() # Displays a stack trace, useful for debugging
            db.rollback()    # Optional - depends on what you are doing with the db
            return False

    # modify an existing merchandise data
    elif option == 2:
        try:
            cur.execute("UPDATE venues SET name = (?) WHERE venueID = (?)", (name, venueID,))
            # db.commit()
            message("VenueID:{} record has been updated with {}".format(venueID, name))
            return True
        except sqlite3.Error as e:
            print("{} error has occured".format(e))
            traceback.print_exc() # Displays a stack trace, useful for debugging
            db.rollback()    # Optional - depends on what you are doing with the db
            return False

    # delete an existing merchandise data
    elif option == 3:
        try:
            cur.execute("DELETE FROM venue WHERE 'venueID' = (?)", (venueID,))
            # db.commit()
            message("venueID:{} has been deleted from the database".format(venueID))
            return True
        except sqlite3.Error as e:
            print("{} error has occured".format(e))
            traceback.print_exc() # Displays a stack trace, useful for debugging
            db.rollback()    # Optional - depends on what you are doing with the db
            return False


''' get names/dates... etc '''
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


def getDates(gameID):
    try:
        cur.execute("SELECT dates FROM games WHERE gameID = ?", (gameID,))
        dates = cur.fetchone()[0]
        return dates

    except sqlite3.Error as e:
        print("{} error has occured".format(e))
        traceback.print_exc() # Displays a stack trace, useful for debugging
        db.rollback()    # Optional - depends on what you are doing with the db
        return None

    except TypeError:
        message("Game with GameID {} does not exist".format(gameID))
        return None


def getMercInfo(mercID):
    try:
        cur.execute("SELECT name, price FROM merchandise WHERE mercID = ?", (mercID,))
        mercData = cur.fetchone()
        name, price = mercData[0], mercData[1]
        return name, price

    except sqlite3.Error as e:
        print("{} error has occured".format(e))
        traceback.print_exc() # Displays a stack trace, useful for debugging
        db.rollback()    # Optional - depends on what you are doing with the db
        return None

    except TypeError:
        message("MerchandiseID {} does not exist".format(mercID))
        return None, None


''' Checks if sales record already exist. Return True if exist, False if not '''
def checkSalesExist(salesObj):
    gameID = salesObj.gameID
    mercID = salesObj.mercID
    date = getDates(gameID)
    mercName, price = getMercInfo(mercID)

    try:
        cur.execute("SELECT * FROM sales WHERE gameID = (?) AND mercID = (?)", (gameID, mercID,))
        exist = cur.fetchone()[0]
        return True

    except sqlite3.Error as e:
        print("{} error has occured".format(e))
        traceback.print_exc() # Displays a stack trace, useful for debugging
        db.rollback()    # Optional - depends on what you are doing with the db

    except TypeError:
        return False


''' Close DB '''
def quit():
    message("Closing database")
    db.close


setup()
