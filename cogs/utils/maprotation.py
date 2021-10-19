import json
import requests

from datetime import datetime
from . import constants as c


class CurrentMap:
    def __init__(self, name, remaining):
        self.name = name
        self.remaining = remaining  # TimeUnit

    def __repr__(self):
        res = f"{self.name} with {repr(self.remaining)} remaining"
        return res


class NextMap:
    def __init__(self, name, timestamp, duration):
        self.name = name
        self.timestamp = timestamp
        self.duration = duration

    def __repr__(self):
        now = datetime.now()
        future = datetime.fromtimestamp(self.timestamp)
        totalseconds = int((future - now).total_seconds())
        timeunit = TimeUnit.from_seconds(totalseconds)

        res = f"{self.name} in {repr(timeunit)} for {self.duration} minutes"
        return res


class TimeUnit:
    def __init__(self, h=0, m=0, s=0, totalseconds=None):
        self.h = h
        self.m = m
        self.s = s
        self.totalseconds = totalseconds

    def from_seconds(totalseconds):
        m, s = divmod(totalseconds, 60)
        h, m = divmod(m, 60)
        return TimeUnit(h=h, m=m, s=s, totalseconds=totalseconds)

    def display_shorthand(self):
        minute = self.m if self.m >= 10 else f"0{self.m}"
        second = self.s if self.s >= 10 else f"0{self.s}"
        if self.h > 0:
            return f"{self.h}:{minute}:{second}"
        else:
            return f"{minute}:{second}"

    def __repr__(self):
        minute = self.m if self.m >= 10 else f"0{self.m}"
        second = self.s if self.s >= 10 else f"0{self.s}"

        if self.h > 0:
            return f"{self.h}h {minute}m {second}s"
        else:
            return f"{self.m}m {second}s"


# returns a tuple of (CurrentMap, NextMap[] <of length count>)
# count is multiplied by number of maps since API does not support filtering
async def getmaps(count=(c.DEFAULT_COUNT * len(c.APEX_MAPS)), filter=None):
    try:
        response = requests.get(
            f"https://fn.alphaleagues.com/v2/apex/map/?next={count}")
        json_data = json.loads(response.text)

        # filter out "br" only (i.e. ignore "arenas" and other gamemodes)
        json_br = json_data['br']

        # generate Current Map
        name = json_br['map']
        totalseconds = json_br['times']['remaining']['seconds']  # e.g. 3555
        currmap = CurrentMap(name, TimeUnit.from_seconds(totalseconds))

        # generate Next Map objects
        nextmaps = []
        for j in json_br.get('next', []):
            mapname = j['map']
            if filter and mapname != filter:
                continue
            nextmap = NextMap(mapname, j['timestamp'], j['duration'])
            nextmaps.append(nextmap)
        return (currmap, nextmaps)

    except Exception as e:
        print(e)
        return None


async def stringifymaps(maps):
    currmaptext = f"**Currently:** {repr(maps[0])}\n"
    nextmaptext = "**Upcoming:**\n"
    for m in maps[1]:
        nextmaptext += repr(m) + "\n"
    return currmaptext + '\n' + nextmaptext
