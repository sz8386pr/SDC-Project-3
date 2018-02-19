import ui, rpcManager, data

def main():

    # Try to read DB
    gamesData, mercData, salesData, venuesData = data.readDB()
    # If fails, recreate DB from the backup file
    if gamesData == None or mercData == None or salesData == None or venuesData == None:
        data.setup()
    # Otherwise create dictionary from the db data
    else:
        rpcManager.createDictionaries(gamesData, mercData, salesData, venuesData)

    quit = 'q'
    choice = None

    while choice != quit:
        choice = ui.mainMenu()
        rpcManager.mainChoices(choice)

if __name__ == '__main__':
    main()
