import json
from pyteamcity.pyteamcity.future import TeamCity

# This initialises the Client with the settings passed. <port> has to be an integer.
tc = TeamCity.from_environ()
since_date_string = '20170101T000000+0000'
builds = tc.builds.all().filter(
    build_type="Hotfix",
    since_date=since_date_string,
    count=3)
for build in builds:
    print(build.build_type_id + ": " + build.number + " - " + str(build.id))
    changes = tc.changes.all().filter(
        count=5)
    for change in changes:
        print (change.username)