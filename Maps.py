#TagMap
def createTagMap(zeitslots):
    tagmap = {}
    for t in zeitslots:
        if t.pruefungstag_nummer not in tagmap:
            tagmap[t.pruefungstag_nummer] = []
        tagmap[t.pruefungstag_nummer].append(t)
    return tagmap

#ZeitSlotMap
def createZeitSlotMap(zeitslots):
    map = {}
    for zeitslot in zeitslots:
        map[zeitslot.id] = zeitslot
    return map

#RaumMap
def createRaumMap(raeume):
    map = {}
    for raum in raeume:
        map[raum.id] = raum
    return map


def createAufsichtMap(aufsichten):
    map = {}
    for aufsicht in aufsichten:
        map[aufsicht.id] = aufsicht
    return map