'''Output for the user'''
def message(message):
    print(message)

''' returns list of venues with the numbers and return the list of venueID '''
def venueLists(venueData):
    venues = []
    venueIDs =[]

    for venue in venueData:
        venues.append('{}:{}'.format(str(venue['venueID']),venue['name']))
        venueIDs.append(venue['venueID'])

    return ', '.join(venues), venueIDs


''' confirmation validation '''
def confirm(confirm):
    if confirm.upper() == "Y" or confirm.upper() == "N":
        return True
    else:
        message("Please enter Y or N")
        return False


''' table '''
# line display options
def lineOption():
    lineOn = True   # Display lines?
    linePer = 10    # Lines every x row Default: 10
    lineShape = '-' # Line shape. Change for fun! Default: '-'
    lineCount = 0   # Line counter. No need to touch

    return lineOn, linePer, lineShape, lineCount


def displayTable(data, gmsv):
    if gmsv == '1':
        headerFormat = '|{:^8}|{:^12}|{:^9}|'
        tableFormat = '|{:^8}|{:^12}|{:^9}|'
        lineRepeat = 33   #repeat lineshape x times as needed
        # Table title
        message('\n========== GAMES TABLE ==========\n')
        # Table header
        tableHeader(data, headerFormat, lineRepeat)
        # Table values
        tableBody(data, tableFormat, lineRepeat)

    elif gmsv == '2':
        headerFormat = '|{:^8}|{:^20}|{:^8}|'
        tableFormat = '|{:^8}| {:<20}|${:-7}|'
        lineRepeat = 40  #repeat lineshape x times as needed
        # Table title
        message('\n========== MERCHANDISE TABLE ===========\n')
        # Table header
        tableHeader(data, headerFormat, lineRepeat)
        # Table values
        tableBody(data, tableFormat, lineRepeat)

    elif gmsv == '3':
        headerFormat = '|{:^8}|{:^8}|{:^6}|'
        tableFormat = '|{:^8}|{:^8}|{:^6}|'
        lineRepeat = 26  #repeat lineshape x times as needed
        # Table title
        message('\n====== SALES TABLE =======\n')
        # Table header
        tableHeader(data, headerFormat, lineRepeat)
        # Table values
        tableBody(data, tableFormat, lineRepeat)

    elif gmsv == '4':
        headerFormat = '|{:^8}|{:^20}|'
        tableFormat = '|{:^8}|{:19} |'
        lineRepeat = 31  #repeat lineshape x times as needed
        # Table title
        message('\n======== VENUES TABLE =========\n')
        # Table header
        tableHeader(data, headerFormat, lineRepeat)
        # Table values
        tableBody(data, tableFormat, lineRepeat)


def tableHeader(data, tableFormat, lineRepeat):
    colNum = len(data[0])
    lineOn, linePer, lineShape, lineCount = lineOption()
    line = lineShape * lineRepeat
    colHeader = []
    for key in data[0]:
        colHeader.append(key.upper())

    print(line)
    if colNum == 2:
        print(tableFormat.format(colHeader[0], colHeader[1]))
    elif colNum == 3:
        print(tableFormat.format(colHeader[0], colHeader[1], colHeader[2]))
    elif colNum == 4:
        print(tableFormat.format(colHeader[0], colHeader[1], colHeader[2], colHeader[3]))
    print(line)


def tableBody(data, tableFormat, lineRepeat):
    colNum = len(data[0])
    lineOn, linePer, lineShape, lineCount = lineOption()
    line = lineShape * lineRepeat

    for row in data:
        rowValue = []
        for key in row:
            rowValue.append(row[key])

        if colNum == 2:
            print(tableFormat.format(rowValue[0], rowValue[1]))
        elif colNum == 3:
            print(tableFormat.format(rowValue[0], rowValue[1], rowValue[2]))
        elif colNum == 4:
            print(tableFormat.format(rowValue[0], rowValue[1], rowValue[2], rowValue[3]))
        lineCount+= 1
        if (lineCount % linePer == 0) and lineOn:
            print(line)
    print(line)



''' reports '''
# display daily sales report
def displayDailyReport(data):
    for key in data:
        date = key

    headerFormat = '|{:^20}|{:^6}|{:^9}|{:^9}|'
    tableFormat = '| {:19}|{:^6.0f}|$ {:<7.2f}|${:8.2f}|'
    lineRepeat = 49  #repeat lineshape x times as needed
    # Table title
    message('\n============ {:10} Sales Report ============\n'.format(date))
    # Table header
    tableHeader(data[date], headerFormat, lineRepeat)
    # Table values
    tableBody(data[date], tableFormat, lineRepeat)


# display merchandise report
def displayMercReport(data):
    message('\n==== {} Sales Report ===='.format(data['name']))
    message('Price: ${:.2f} each'.format(data['price']))
    message('\nMinimum sold on record: {}'.format(data['min']))
    message('Sold on...')
    for x in range (len(data['minDate'])):
        message('GameID:{:2} on {:10}'.format(data['minDateID'][x],data['minDate'][x]))

    message('\nMaximum sold on record: {}'.format(data['max']))
    message('Sold on...')
    for x in range (len(data['maxDate'])):
        message('GameID:{:2} on {:10}'.format(data['maxDateID'][x],data['maxDate'][x]))

    message('\nTOTAL SOLD: {}'.format(data['total']))
    message('TOTAL SALES: ${:.2f}'.format(data['totalPrice']))


# display total sales report
def displayTotalReport(data):
    for key in data:
        title = key

    headerFormat = '|{:^8}|{:^12}|{:^20}|{:^11}|'
    tableFormat = '| {:^7}|{:^12}| {:19}|${:9.2f} |'
    lineRepeat = 56  #repeat lineshape x times as needed
    # Table title
    message('\n=================== {} ===================\n'.format(title))
    # Table header
    tableHeader(data[title], headerFormat, lineRepeat)
    # Table values
    tableBody(data[title], tableFormat, lineRepeat)



''' menus '''
'''Display choices for user, return users' selection'''

def mainMenu():
    print('''
        0. Search for records
        1. Add a new record
        2. Update an existing record
        3. Delete an existing record
        4. Sales data analysis
        q. Quit
    ''')

    choice = input('Enter your selection: ')

    return choice


def GMSVMenu(option):
    print('''
        {}
        1. Games records
        2. Merchandise records
        3. Sales records
        4. Venues records
        b. Back to main menu
    '''.format(option))

    gmsv = input('Enter your selection: ').lower()

    return gmsv


def searchMenu():
    print('''
        1. Search for records within a table
        2. Display a table
        b. Back to main menu
    ''')

    choice = input('Enter your selection: ').lower()

    return choice


def gamesSearchMenu():
    print('''
        Search by...
        1. GameID
        2. Game date
        3. Game Venue
        b. Back to main menu
    ''')

    choice = input('Enter your selection: ')

    return choice


def mercSearchMenu():
    print('''
        Search by...
        1. MerchandiseID
        2. Merchandise name
        3. Price
        b. Back to main menu
    ''')

    choice = input('Enter your selection: ')

    return choice


def salesSearchMenu():
    print('''
        Search by...
        1. GameID
        2. MerchandiseID
        3. Units sold
        b. Back to main menu
    ''')

    choice = input('Enter your selection: ')

    return choice


def venuesSearchMenu():
    print('''
        Search by...
        1. VenueID
        2. Venue name
        b. Back to main menu
    ''')

    choice = input('Enter your selection: ')

    return choice


''' reports menu '''
def reportMainMenu():
    print('''
        Sales Analysis Reports
        1. Daily sales report
        2. Merchandise report
        3. Total Sales report
        b. Back to main menu
    ''')

    choice = input('Enter your selection: ')

    return choice
