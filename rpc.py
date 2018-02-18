from ui import message
from classes import Game, Merchandise, Sales
from datetime import datetime
import data, ui


# global globalData
globalData = {}

def createDictionaries(gamesData, mercData, salesData, venuesData):
    # global globalData

    globalData['games'] = []
    globalData['merchandise'] = []
    globalData['sales'] = []
    globalData['venues'] = []

    if len(gamesData) != 0:
        for row in gamesData:
            globalData['games'].append({'gameID': row[0], 'dates': row[1], 'venueID': row[2]})

    if len(mercData) != 0:
        for row in mercData:
            globalData['merchandise'].append({'mercID': row[0], 'name': row[1], 'price': row[2]})

    if len(salesData) != 0:
        for row in salesData:
            globalData['sales'].append({'dateID': row[0], 'mercID': row[1], 'sold': row[2]})

    if len(venuesData) != 0:
        for row in venuesData:
            globalData['venues'].append({'venueID': row[0], 'name': row[1]})



''' for adding/inserting a new record '''
# max values references from https://www.w3resource.com/python-exercises/dictionary/python-data-type-dictionary-exercise-15.php
def insertData(option):
    # games
    if option == 1:
        date, venueID, exist = gameDataValidation()

        # if there are no games data with the same date, create a new game object
        if not exist:
            # newGameID is the max gameID + 1
            newGameID = max([x['gameID'] for x in globalData['games']])+1
            newGameObj = Game(newGameID, date, venueID)

            # if added to the database successfully, append to the globalData as well
            if data.gameManipulate(newGameObj, 1):
                globalData['games'].append({'gameID': newGameID, 'dates': date, 'venueID': venueID})

    # merchandise
    elif option == 2:
        mercName, price, exist = mercDataValidation()

        # if there are no merchandise data with the same name, create a new merchandise object
        if not exist:
            # newMercID is the max mercID + 1
            newMercID = max([x['mercID'] for x in globalData['merchandise']])+1
            newMercObj = Merchandise(newMercID, mercName, price)

            # if added to the database successfully, append to the globalData as well
            if data.merchandiseManipulate(newMercObj, 1):
                globalData['merchandise'].append({'mercID': newMercID, 'name': mercName, 'price': price})

    # sales
    elif option == 3:

        newGameID, newMercID, exist = salesDataValidation()

        # if it doesn't exist, continue on to gather information about the number of item sold. Otherwise, back to the main menu
        if not exist:
            sold = soldValidation()

            # create a new Sales object
            newSalesObj = Sales(newGameID, newMercID, sold)

            # if added to the database successfully, append to the globalData as well
            if data.salesManipulate(newSalesObj, 1):
                globalData['sales'].append({'dateID': newGameID, 'mercID': newMercID, 'sold': sold})

    # venues
    elif option == 4:
        venueName, exists = venuesDataValidation()

        # create new Venues object if the record with the same venue name does not exist
        if not exists:
            # newVenueID is the max VenueID + 1
            newVenueID = max([x['venueID'] for x in globalData['venues']])+1
            newVenueObj = Venue(newVenueID, venueName)

            # if added to the database successfully, append to the globalData as well
            if data.venuesManipulate(newVenueObj, 1):
                globalData['venues'].append({'venueID': newVenueID, 'name': venueName})



''' modify/update existing record '''
def updateData(option):
    # games
    if option == 1:
        # GameID confirmation/validation
        while True:
            try:
                gameID = int(input('Enter a GameID to update: '))
            except ValueError:
                message('Enter a valid number')

            if gameID not in [game['gameID'] for game in globalData['games']]:
                message('GameID:{} does not exist in the database'.format(gameID))
            else:
                for game in globalData['games']:
                    if game['gameID'] == gameID:
                        date = game['dates']
                        venueID = game['venueID']
                        venueName = data.getVenueName(venueID)
                confirm = False
                while confirm == False:
                    yn = input('GameID:{} record is for the game on {} at {}. Is this what you want to update?(Y/N)'.format(gameID, date, venueName)).upper()
                    confirm = ui.confirm(yn)
                if yn == 'Y':
                    break

        # validate/get new date and venueID values
        date, venueID, exist = gameDataValidation()

        # create a game object if the record with the same date does not exist
        if not exist:
            updateGamesObj = Game(gameID, date, venueID)

            # if updated database successfully, modify the globalData with the new values as well
            if data.gameManipulate(updateGamesObj, 2):
                for game in globalData['games']:
                    if game['gameID'] == gameID:
                        game['dates'] = date
                        game['venueID'] = venueID

    # merchandise
    elif option == 2:
        # mercID validation/confirmation
        while True:
            try:
                mercID = int(input('Enter a merchandiseID to update'))
            except ValueError:
                message('Enter a valid mercID')

            # Check if mercID is found in the database
            if mercID not in [item['mercID'] for item in globalData['merchandise']]:
                message('MerchandiseID:{} does not exist in the database'.format(mercID))
            else:
                mercName, mercPrice = data.getMercInfo(mercID)

                confirm = False
                while confirm == False:
                    yn = input('MerchandiseID:{} {} for ${}. Is this what you want to update?(Y/N)'.format(mercID, mercName, mercPrice)).upper()
                    confirm = ui.confirm(yn)
                if yn == 'Y':
                    break

        mercName, price, exist = mercDataValidation()

        # create a merchandise object if the record with the same name does not exist
        if not exist:
            updateMercObj = Merchandise(mercID, mercName, price)

            # if updated database successfully, modify the globalData with the new values as well
            if data.merchandiseManipulate(updateMercObj, 2):
                for item in globalData['merchandise']:
                    if item['mercID'] == gameID:
                        item['name'] = mercName
                        item['price'] = price

    # sales
    elif option == 3:
        gameID, mercID, exist = salesDataValidation()

        # continue updating if the data with the same gameID and mercID combination
        if exists:
            sold = soldValidation()

            updateSalesObj = Sales(gameID, mercID, sold)

            # if updated database successfully, modify the globalData with the new values as well
            if data.salesManipulate(updateSalesObj, 2):
                for sale in globalData['sales']:
                    if sale['gameID'] == gameID and sale['mercID'] == mercID:
                        sale['sold'] = sold

    # venues
    elif option == 4:
        venueName, exist = venuesDataValidation()

        if not exist:





''' validates game dates and venueID values and returns them '''
def gameDataValidation():
    validDates = False
    while validDates == False:
        date = input('\nEnter the date for the game(YYYY-MM-DD): ')
        validDates = validateDate(date)

    # venues string values for display
    # venueIDs is list of venueIDs
    venues, venueIDs = ui.venueLists(globalData['venues'])

    # user must enter a valid venueID
    venueID = 0
    while venueID not in venueIDs:
        try:
            venueID = int(input('\nEnter a number for the venue({})'.format(venues)))
            if venueID not in venueIDs:
                message('Enter a valid number')
        except ValueError or TypeError:
            message('Enter a valid number')


    if date in [game['dates'] for game in globalData['games']]:
        for game in globalData['games']:
            if game['dates'] == date:
                message('Record with the same date already exist with the GameID:{}'.format(game['gameID']))
        exist = True
    else:
        exist = False



    return date, venueID, exist


def mercDataValidation():
    # make sure merchandise name is not an empty string
    mercName = ''
    while mercName == '':
        mercName = str(input('\nEnter a new merchandise name: '))


    # price validation
    while True:
        price = input('\nEnter the price for {}: '.format(mercName))

        # Reference to check 2 decimal places https://stackoverflow.com/questions/23307209/checking-if-input-is-a-float-and-has-exactly-2-numbers-after-the-decimal-point?rq=1
        try:
            if len(price[price.rfind('.')+1:]) > 2:
                raise ValueError
            else:
                price = float(price)
                break
        except ValueError as v:
            message('Enter valid number')

    # If the record exists with the same date, message that there is a record and return to main menu
    if mercName in [item['name'] for item in globalData['merchandise']]:
        for item in globalData['merchandise']:
            if item['name'] == mercName:
                message('Record with the same date already exist with the MerchandiseID:{}'.format(item['mercID']))
        exist = True
    else:
        exist = False

    return mercName, price, exist


def salesDataValidation():
    # GameID validation/confirmation
    while True:
        gameID = int(input('Enter a gameID: '))
        gameDate = data.getDates(gameID)
        if gameDate is None:
            message("There are no data with that GameID")
        else:
            confirm = False
            while confirm == False:
                yn = input('ID:{} is for the game on {}. Is this correct?(Y/N) '.format(gameID, gameDate)).upper()
                confirm = ui.confirm(yn)
            if yn == 'Y':
                yn = ''
                break

    # mercID validation/confirmation
    while True:
        mercID = int(input('Enter a merchandiseID: '))
        mercName, mercPrice = data.getMercInfo(mercID)
        if (mercName or mercPrice) is None:
            message("There are no data with that merchandiseID")
        else:
            confirm = False
            while confirm == False:
                yn = input('ID:{} is for the {} that costs ${}. Is this correct?(Y/N) '.format(mercID, mercName, mercPrice)).upper()
                confirm = ui.confirm(yn)
            if yn == 'Y':
                break

    # create a temporary sales object to check if the sales record with the same gameID and mercID already exist
    tempSalesObj = Sales(gameID, mercID, 0)

    exist = data.checkSalesExist(tempSalesObj):

    return gameID, mercID, exist


def soldValidation():
    while True:
        try:
            sold = int(input('Enter number of {} sold: '.format(newMercName)))
            if sold < 0:
                message('Enter a positive number')
            else:
                break
        except ValueError:
            message('Enter a whole number')

    return sold


def venuesDataValidation():
    venueName = ''
    while venueName == '':
        venueName = str(input('\nEnter a new venue name: '))

    # If the record exists with the same date, message that there is a record and return to main menu
    if venueName in [venue['name'] for venue in globalData['venues']]:
        for venue in globalData['venues']:
            if venue['name'] == venueName:
                message('Record with the same venue already exist with the VenueID:{}'.format(venue['venueID']))
        exist = True
    else:
        exist = False

    return venueName, exist




''' date format validation '''
# Reference from https://stackoverflow.com/questions/16870663/how-do-i-validate-a-date-string-format-in-python
def validateDate(date):
    try:
        datetime.strptime(date, '%Y-%m-%d')
        return True
    except ValueError:
        message("Incorrect date format, should be YYYY-MM-DD")
        return False



# def sample():
#     for key in globalData['merchandise']:
#         for k in key:
#             # # price of foam rock
#             # if key[k] == 'Foam Rock':
#             #     print(key['price'])
#
#             # # key and value combo
#             # print(k, key[k])
#
#             # # get the names value
#             # if k == 'name':
#             #     print(key[k])



#
gamesData, mercData, salesData, venuesData = data.readDB()
createDictionaries(gamesData, mercData, salesData, venuesData)
# numVenues = len(globalData['venues'])
# venues = []
# for x in range (0, numVenues):
#     venues.append(str(x+1) + ':' + globalData['venues'][x]['name'])
# venues = ', '.join(venues)
# print (venues)
# print(globalData['venues'][1]['name'])
# for venue in globalData['venues']:
#     venues.append(venue['name'])
# venues = ', '.join(venues)
# print(venues)
# venues = ''
# for venue in globalData['venues']:
#     venues += venue['name']
#     venues += ', '
# print (venues)
# maxi = globalData['games'][1]['gameID']
# print(maxi)

# # gameID in games
# seq = [x['gameID'] for x in globalData['games']]
# print (seq)

# print([x['gameID'] for x in globalData['games']])

updateData(1)
