# from rpc import globalData

def message(message):
    '''Output for the user'''
    print(message)

# returns list of venues with the numbers and return the list of venueID
def venueLists(venueData):
    venues = []
    venueIDs =[]

    for venue in venueData:
        venues.append('{}:{}'.format(str(venue['venueID']),venue['name']))
        venueIDs.append(venue['venueID'])

    return ', '.join(venues), venueIDs

def confirm(confirm):
    if confirm.upper() == "Y" or confirm.upper() == "N":
        return True
    else:
        message("Please enter Y or N")
        return False
