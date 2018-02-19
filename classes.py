class Game:
    def __init__(self, gameID, dates, venueID):
        self.gameID = gameID
        self.dates = dates
        self.venueID = venueID
        # self.venueName = venueName

class Merchandise:
    def __init__(self, mercID, name, price):
        self.mercID = mercID
        self.name = name
        self.price = price

class Sales:
    def __init__(self, gameID, mercID, sold):
        self.gameID = gameID
        self.mercID = mercID
        self.sold = sold

class Venue:
    def __init__(self, venueID, venueName):
        self.venueID = venueID
        self.venueName = venueName
