import ui, rpcManager, data

def main():

    data.dbConnectionSetup()
    # Try to read DB
    gamesData, mercData, salesData, venuesData = data.readDB()
    # If fails, recreate DB from the backup file and try again
    if gamesData == None or mercData == None or salesData == None or venuesData == None:
        print('Database doesn\'t exist. Rebuild database from the backup files')
        data.rebuild()
        gamesData, mercData, salesData, venuesData = data.readDB()
        # If it fails again, quit program
        if gamesData == None or mercData == None or salesData == None or venuesData == None:
            ui.message('Rebuilding failed. Exiting the program')
            return
        rpcManager.createDictionaries(gamesData, mercData, salesData, venuesData)
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
