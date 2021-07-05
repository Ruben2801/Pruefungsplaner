from datetime import datetime, timedelta

#Funktion um nächsten Werktag zu ermitteln
def n_werktag(date: datetime):
    if date.weekday() == 4:
        tag = date.date() + timedelta(days=3)
    else:
        tag = date + timedelta(days=1)
    return tag
