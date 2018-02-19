from ui import message
from classes import Game, Merchandise, Sales, Venue
from datetime import datetime
import data, ui
from operator import itemgetter


globalData = {}

''' create a duplicate of the database as a dictionary for the local data processing to reduce sql queries '''
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
            globalData['sales'].append({'gameID': row[0], 'mercID': row[1], 'sold': row[2]})

    if len(venuesData) != 0:
        for row in venuesData:
            globalData['venues'].append({'venueID': row[0], 'name': row[1]})


''' data manipulations '''

''' for adding/inserting a new record '''
# max values references from https://www.w3resource.com/python-exercises/dictionary/python-data-type-dictionary-exercise-15.php
# sorting list of dictionaries by key values references from https://stackoverflow.com/questions/72899/how-do-i-sort-a-list-of-dictionaries-by-values-of-the-dictionary-in-python
def insertData(option):
    # games
    if option == '1':
        date, venueID, exist = gameDataValidation()
        # if there are no games data with the same date, create a new game object
        if not exist:
            # newGameID is the max gameID + 1
            newGameID = max([x['gameID'] for x in globalData['games']])+1
            newGameObj = Game(newGameID, date, venueID)

            # if added to the database successfully, append to the globalData as well
            if data.gameManipulate(newGameObj, 1):
                globalData['games'].append({'gameID': newGameID, 'dates': date, 'venueID': venueID})
                globalData['games'] = sorted(globalData['games'], key=itemgetter('gameID'))


    # merchandise
    elif option == '2':
        mercName, price, exist = mercDataValidation()
        # if there are no merchandise data with the same name, create a new merchandise object
        if not exist:
            # newMercID is the max mercID + 1
            newMercID = max([x['mercID'] for x in globalData['merchandise']])+1
            newMercObj = Merchandise(newMercID, mercName, price)

            # if added to the database successfully, append to the globalData as well
            if data.merchandiseManipulate(newMercObj, 1):
                globalData['merchandise'].append({'mercID': newMercID, 'name': mercName, 'price': price})
                globalData['merchandise'] = sorted(globalData['merchandise'], key=itemgetter('mercID'))

    # sales
    elif option == '3':
        newGameID, newMercID, exist = salesDataValidation()
        # if it doesn't exist, continue on to gather information about the number of item sold. Otherwise, back to the main menu
        if not exist:
            mercName, price = data.getMercInfo(newMercID)
            sold = soldValidation(mercName)
            # create a new Sales object
            newSalesObj = Sales(newGameID, newMercID, sold)

            # if added to the database successfully, append to the globalData as well
            if data.salesManipulate(newSalesObj, 1):
                globalData['sales'].append({'gameID': newGameID, 'mercID': newMercID, 'sold': sold})
                globalData['sales'] = sorted(globalData['sales'], key=itemgetter('gameID'))
        else:
            message('Sale record with the same GameID and MerchandiseID already exist!')

    # venues
    elif option == '4':
        venueName, exist = venuesDataValidation()
        # create new Venues object if the record with the same venue name does not exist
        if not exist:
            # newVenueID is the max VenueID + 1
            newVenueID = max([x['venueID'] for x in globalData['venues']])+1
            newVenueObj = Venue(newVenueID, venueName)

            # if added to the database successfully, append to the globalData as well
            if data.venuesManipulate(newVenueObj, 1):
                globalData['venues'].append({'venueID': newVenueID, 'name': venueName})
                globalData['venues'] = sorted(globalData['venues'], key=itemgetter('venueID'))



''' modify/update an existing record '''
def updateData(option):
    # games
    if option == '1':
        gameID = gameIDValidation('update')
        newDate, newVenueID, exist = gameDataValidation()
        # create a game object if the record with the same date does not exist
        if not exist:
            updateGamesObj = Game(gameID, newDate, newVenueID)

            # if updated database successfully, modify the globalData with the new values as well
            if data.gameManipulate(updateGamesObj, 2):
                for game in globalData['games']:
                    if game['gameID'] == gameID:
                        game['dates'] = newDate
                        game['venueID'] = newVenueID

    # merchandise
    elif option == '2':
        mercID = mercIDValidation('update')
        newMercName, newPrice, exist = mercDataValidation()
        # create a merchandise object if the record with the same name does not exist
        if not exist:
            updateMercObj = Merchandise(mercID, newMercName, newPrice)

            # if updated database successfully, modify the globalData with the new values as well
            if data.merchandiseManipulate(updateMercObj, 2):
                for item in globalData['merchandise']:
                    if item['mercID'] == mercID:
                        item['name'] = newMercName
                        item['price'] = newPrice

    # sales
    elif option == '3':
        gameID, mercID, exist = salesDataValidation()
        # continue updating if the data with the same gameID and mercID combination
        if exist:
            mercName, price = data.getMercInfo(mercID)
            sold = soldValidation(mercName)

            updateSalesObj = Sales(gameID, mercID, sold)

            # if updated database successfully, modify the globalData with the new values as well
            if data.salesManipulate(updateSalesObj, 2):
                for sale in globalData['sales']:
                    if sale['gameID'] == gameID and sale['mercID'] == mercID:
                        sale['sold'] = sold
        else:
            message('Sales record with the same GameID and MerchandiseID does not exist!')

    # venues
    elif option == '4':
        venueID = venueIDValidation('update')
        newVenueName, exist = venuesDataValidation()
        if not exist:
            updateVenueObj = Venue(venueID, newVenueName)

            # if updated database successfully, modify the globalData with the new values as well
            if data.venuesManipulate(updateVenueObj, 2):
                for venue in globalData['venues']:
                    if venue['venueID'] == venueID :
                        venue['name'] = newVenueName


''' delete an existing record '''
def deleteData(option):
    # games
    if option == '1':
        gameID = gameIDValidation('delete')

        # delete object only needs a proper ID to find and delete the records from the table
        deleteGameObj = Game(gameID, '', 1)

        # if the record has been successfully deleted, delete from the list as well
        if data.gameManipulate(deleteGameObj, 3):
            for game in globalData['games']:
                if game['gameID'] == gameID:
                    globalData['games'].remove(game)

    # merchandise
    elif option == '2':
        mercID = mercIDValidation('delete')

        # delete object only needs a proper ID to find and delete the records from the table
        deleteMercObj = Merchandise(mercID, '', 1)

        # if the record has been successfully deleted, delete from the list as well
        if data.merchandiseManipulate(deleteMercObj, 3):
            for item in globalData['merchandise']:
                if item['mercID'] == mercID:
                    globalData['merchandise'].remove(item)

    # sales
    elif option == '3':
        gameID, mercID, exist = salesDataValidation()

        # only perform deletion when the record with the same gameID and mercID exists
        if exist:
            # delete object only needs a proper ID to find and delete the records from the table
            deleteSalesObj = Sales(gameID, mercID, 0)

            # if the record has been successfully deleted, delete from the list as well
            if data.salesManipulate(deleteSalesObj, 3):
                for sale in globalData['sales']:
                    if sale['gameID'] == gameID and sale['mercID'] == mercID:
                        globalData['sales'].remove(sale)
        else:
            message('Sales record with the same GameID and MerchandiseID does not exist!')

    # venues
    elif option == '4':
        venueID = venueIDValidation('delete')

        # delete object only needs a proper ID to find and delete the records from the table
        deleteVenueObj = Venue(venueID, '')

        # if the record has been successfully deleted, delete from the list as well
        if data.venuesManipulate(deleteVenueObj, 3):
            for venue in globalData['venues']:
                if venue['venueID'] == venueID:
                    globalData['venues'].remove(venue)



''' Validations '''

''' games validation '''
def gameIDValidation(option):
    # GameID confirmation/validation
    while True:
        try:
            gameID = int(input('Enter a GameID to {}: '.format(option)))


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
                    yn = input('GameID:{} record is for the game on {} at {}. Is this what you want to {}?(Y/N) '.format(gameID, date, venueName, option)).upper()
                    confirm = ui.confirm(yn)
                if yn == 'Y':
                    break
        except ValueError:
            message('Enter a valid number')

    return gameID


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


''' merchandise validation '''
def mercIDValidation(option):
    # mercID validation/confirmation
    while True:
        try:
            mercID = int(input('Enter a merchandiseID to {}: '.format(option)))
            # Check if mercID is found in the database


            if mercID not in [item['mercID'] for item in globalData['merchandise']]:
                message('MerchandiseID:{} does not exist in the database'.format(mercID))
            else:
                mercName, mercPrice = data.getMercInfo(mercID)

                confirm = False
                while confirm == False:
                    yn = input('MerchandiseID:{} {} for ${}. Is this what you want to {}?(Y/N) '.format(mercID, mercName, mercPrice, option)).upper()
                    confirm = ui.confirm(yn)
                if yn == 'Y':
                    break
        except ValueError:
            message('Enter a valid merchandiseID')

    return mercID


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


''' sales validation '''
def salesDataValidation():
    # GameID validation/confirmation
    while True:
        try:
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
        except ValueError:
            message('Enter a valid merchandiseID')

    # mercID validation/confirmation
    while True:
        try:
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
        except ValueError:
            message('Enter a valid merchandiseID')

    # create a temporary sales object to check if the sales record with the same gameID and mercID already exist
    tempSalesObj = Sales(gameID, mercID, 0)

    exist = data.checkSalesExist(tempSalesObj)

    return gameID, mercID, exist


def soldValidation(newMercName):
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



''' venues validation '''
def venueIDValidation(option):
    # venueID validation/confirmation
    while True:
        try:
            venueID = int(input('Enter a VenueID to {}: '.format(option)))

            # Check if venueID exist in the database
            venueName = data.getVenueName(venueID)
            if venueName is not None:
                confirm = False
                while confirm == False:
                    yn = input('VenueID:{} {}. Is this what you want to {}?(Y/N) '.format(venueID, venueName, option)).upper()
                    confirm = ui.confirm(yn)
                if yn == 'Y':
                    break
        except ValueError:
            message('Enter a valid VenueID')

    return venueID

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



''' ui menu handling '''
def mainChoices(choice):
    # Search
    if choice == '0':
        searchMenuChoices()
    # Insert
    elif choice == '1':
        GMSVMenuChoices(choice)
    # Update
    elif choice == '2':
        GMSVMenuChoices(choice)
    # Delete
    elif choice == '3':
        GMSVMenuChoices(choice)
    # Analysis
    elif choice == '4':
        reportChoices()
    # Quit
    elif choice == 'q':
        quit()

    else:
        message('Please enter a valid selection')


def searchMenuChoices():
    while True:
        searchChoice = ui.searchMenu()
        if searchChoice in ['1', '2', 'b']:
            break
        else:
            message('Please enter a valid selection')

    # search for a record
    if searchChoice == '1':
        GMSVSearchChoices()
    # display a table
    elif searchChoice == '2':
        GMSVTableChoices()
    else:
        return


def GMSVMenuChoices(choice):
    while True:
        if choice == '1':
            gmsv = ui.GMSVMenu('Add a new record on...')
        elif choice == '2':
            gmsv = ui.GMSVMenu('Update an existing record on...')
        elif choice == '3':
            gmsv = ui.GMSVMenu('Delete an existing record on...')

        if gmsv in ['1', '2', '3', '4', 'b']:
            break
        else:
            message('Please enter a valid selection')

    # If user selected back to main menu, exit function and back to main menu
    if gmsv == 'b':
        return

    if choice == '1':
        insertData(gmsv)
    elif choice == '2':
        updateData(gmsv)
    elif choice == '3':
        deleteData(gmsv)


def GMSVSearchChoices():
    while True:
        gmsv = ui.GMSVMenu('Search on...')

        if gmsv in ['1', '2', '3', '4', 'b']:
            break
        else:
            message('Please enter a valid selection')

    if gmsv == 'b':
        return

    # games
    elif gmsv == '1':
        while True:
            gameSearch = ui.gamesSearchMenu()
            if gameSearch in ['1', '2', '3', 'b']:
                break
            else:
                message('Please enter a valid selection')

        if gameSearch == 'b':
            return

        # run search function(gameSearch)
        searchData(gmsv, gameSearch)

    # merchandise
    elif gmsv == '2':
        while True:
            mercSearch = ui.mercSearchMenu()
            if mercSearch in ['1', '2', '3', 'b']:
                break
            else:
                message('Please enter a valid selection')

        if mercSearch == 'b':
            return

        # run search function(mercSearch)
        searchData(gmsv, mercSearch)

    # sales
    elif gmsv == '3':
        while True:
            salesSearch = ui.salesSearchMenu()
            if salesSearch in ['1', '2', '3', 'b']:
                break
            else:
                message('Please enter a valid selection')

        if salesSearch == 'b':
            return

        # run search function(salesSearch)
        searchData(gmsv, salesSearch)

    # venues
    elif gmsv == '4':
        while True:
            venuesSearch = ui.venuesSearchMenu()
            if venuesSearch in ['1', '2', 'b']:
                break
            else:
                message('Please enter a valid selection')

        if venuesSearch == 'b':
            return

        # run search function(venuesSearch)
        searchData(gmsv, venuesSearch)


def GMSVTableChoices():
    while True:
        gmsv = ui.GMSVMenu('Display a table on...')

        if gmsv in ['1', '2', '3', '4', 'b']:
            break
        else:
            message('Please enter a valid selection')

    if gmsv == 'b':
        return
    else:
        createTable(gmsv)


def reportChoices():
    while True:
        reportChoice = ui.reportMainMenu()

        if reportChoice in ['1', '2', '3', 'b']:
            break
        else:
            message('Please enter a valid selection')

    if reportChoice == 'b':
        return

    # daily report
    elif reportChoice == '1':
        createDailyReportData()
    # merchandise report
    elif reportChoice == '2':
        createMercReportData()
    # venue report
    elif reportChoice == '3':
        createDailyTotalReport()


''' reports '''

def createDailyReportData():
    gameID = gameIDValidation('generate report on')
    daySaleData = data.getDailySales(gameID)
    date = data.getDates(gameID)

    if len(daySaleData) > 0:
        reportData = {}
        reportData[date] = []
        dailySold = 0
        dailyPrice = 0
        dailyTotal = 0
        for row in daySaleData:
            mercID = row[0]
            sold = row[1]
            name, price = data.getMercInfo(mercID)
            total = price * sold
            dailySold += sold
            dailyPrice += price
            dailyTotal += total
            reportData[date].append({'MERCHANDISE': name, 'SOLD': sold, 'PRICE': price, 'TOTAL': total})
        # append daily grandtotal line
        reportData[date].append({'MERCHANDISE': 'DAILY TOTAL', 'SOLD': dailySold, 'PRICE': dailyPrice, 'TOTAL': dailyTotal})

        ui.displayDailyReport(reportData)

    else:
        message('There are no sales records on GameID:{} on {}'.format(gameID, date))


def createMercReportData():
    mercID = mercIDValidation('generate report on')
    mercName, price = data.getMercInfo(mercID)

    mercSalesList = []
    for row in globalData['sales']:
        if row['mercID'] == mercID:
            mercSalesList.append(row)

    if len(mercSalesList) > 0:
        reportData = {}

        maxSold = max([x['sold'] for x in mercSalesList])
        minSold = min([x['sold'] for x in mercSalesList])
        totalSold = sum([x['sold'] for x in mercSalesList])
        totalPrice = totalSold * price
        print(maxSold, minSold, totalSold)

        minGameList = []
        maxGameList = []
        for row in globalData['sales']:
            if row['sold'] == minSold and row['mercID'] == mercID:
                minGameList.append(row['gameID'])
            elif row['sold'] == maxSold and row['mercID'] == mercID:
                maxGameList.append(row['gameID'])

        minGameDays = []
        maxGameDays = []
        for row in globalData['games']:
            if row['gameID'] in minGameList:
                minGameDays.append(row['dates'])
            elif row['gameID'] in maxGameList:
                maxGameDays.append(row['dates'])

        reportData['name'] = mercName
        reportData['price'] = price
        reportData['min'] = minSold
        reportData['max'] = maxSold
        reportData['minDateID'] = minGameList
        reportData['maxDateID'] = maxGameList
        reportData['minDate'] = minGameDays
        reportData['maxDate'] = maxGameDays
        reportData['total'] = totalSold
        reportData['totalPrice'] = totalPrice

        ui.displayMercReport(reportData)


def createDailyTotalReport():
    dailyTotalData = data.getDailyTotal()
    dataTitle = 'RPC Sales Report'
    totalData = {}
    totalData[dataTitle] = []
    for row in dailyTotalData:
        totalData[dataTitle].append({'GameID': row[0], 'Date': row[1], 'Venue': row[2], 'Daily Total': row[3]})
    ui.displayTotalReport(totalData)



''' create table '''
def createTable(gmsv):
    if gmsv == '1':
        gamesData = globalData['games']
        ui.displayTable(gamesData, gmsv)
    elif gmsv == '2':
        mercData = globalData['merchandise']
        ui.displayTable(mercData, gmsv)
    elif gmsv == '3':
        salesData = globalData['sales']
        ui.displayTable(salesData, gmsv)
    elif gmsv == '4':
        venuesData = globalData['venues']
        ui.displayTable(venuesData, gmsv)


''' search data '''
def searchData(gmsv, searchBy):
    # games
    if gmsv == '1':
        if searchBy == '1':
            column = 'gameID'
        elif searchBy == '2':
            column = 'dates'
        elif searchBy == '3':
            column = 'venueID'

        searchValue = searchInputValidation(column)

        # get the record that matches the search string
        gamesData = globalData['games']
        result = []
        for game in gamesData:
            if str(game[column]).upper() == str(searchValue).upper():
                result.append(game)

        if len(result) > 0:
            ui.displayTable(result, gmsv)
        else:
            message('There are no records found with {}: {}'.format(column, searchValue))

    # merchandise
    elif gmsv == '2':
        if searchBy == '1':
            column = 'mercID'
        elif searchBy == '2':
            column = 'name'
        elif searchBy == '3':
            column = 'price'

        searchValue = searchInputValidation(column)

        # get the record that matches the search string
        mercData = globalData['merchandise']
        result = []
        for item in mercData:
            if str(item[column]).upper() == str(searchValue).upper():
                result.append(item)

        if len(result) > 0:
            ui.displayTable(result, gmsv)
        else:
            message('There are no records found with {}: {}'.format(column, searchValue))

    # sales
    elif gmsv == '3':
        if searchBy == '1':
            column = 'gameID'
        elif searchBy == '2':
            column = 'mercID'
        elif searchBy == '3':
            column = 'sold'

        searchValue = searchInputValidation(column)

        # get the record that matches the search string
        salesData = globalData['sales']
        result = []
        for sale in salesData:
            if str(sale[column]).upper() == str(searchValue).upper():
                result.append(sale)

        if len(result) > 0:
            ui.displayTable(result, gmsv)
        else:
            message('There are no records found with {}: {}'.format(column, searchValue))

    # venues
    elif gmsv == '4':
        if searchBy == '1':
            column = 'venueID'
        elif searchBy == '2':
            column = 'name'

        searchValue = searchInputValidation(column)

        # get the record that matches the search string
        venuesData = globalData['venues']
        result = []
        for venue in venuesData:
            if str(venue[column]).upper() == str(searchValue).upper():
                result.append(venue)

        if len(result) > 0:
            ui.displayTable(result, gmsv)
        else:
            message('There are no records found with {}: {}'.format(column, searchValue))

# Make sure ID are valid and also it's not an empty string value
def searchInputValidation(column):
    if column == 'gameID':
        searchInput = gameIDValidation('search with')
    elif column == 'mercID':
        searchInput = mercIDValidation('search with')
    elif column == 'venueID':
        searchInput = venueIDValidation('search with')
    else:
        searchInput = ''
        while searchInput == '':
            searchInput = str(input('\nEnter a {} value to search with: '.format(column)))

    return searchInput



'''Perform shutdown tasks'''
def quit():
    data.quit()

    confirm = False
    while confirm == False:
        yn = input('Would you like to backup database into the backup folder? (Y/N) ').upper()
        confirm = ui.confirm(yn)
    if yn == 'Y':
        data.backupDB(globalData)

    message('End of program')
