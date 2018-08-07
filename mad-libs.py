import random

currency = ["Etherium", "Bitcoin", "Litecoin", "Steem"]
movement = ["is holding steady", "is gaining", "is retreating",
            "is seeing resistance",
            "started off the impulse with a bullish Cup & Handle",
            "is shaping out an upward pointing wedge",
            "is working diligently to pattern out the handle formation",
            "shows the bull flag just looks more and more developed as the days pass",
            "has a lot of overlapping waves and there seem to be no real impulse direction and all seems to be going sideways"]
newsfrom = ["Korea", "major exchanges", "the States", "WSJ"]


for count in range(0, 10):
    this_currency = currency[random.randint(0, len(currency)-1)]
    this_movement = movement[random.randint(0, len(movement)-1)]
    this_newsfrom = newsfrom[random.randint(0, len(newsfrom)-1)]

    print()
    print("SUMMARY\n\nHere is the long term chart of {} where it {} after news from {}.".format(this_currency, this_movement, this_newsfrom))
    print("Is this a safe time to be buying?")