import json
from pyteamcity.pyteamcity.future import TeamCity

# This initialises the Client with the settings passed. <port> has to be an integer.
tc = TeamCity.from_environ()
since_date_string = '20170101T000000+0000'
builds = tc.builds.all().filter(
    build_type="Hotfix",
    since_date=since_date_string,
    count=30)

print(builds.get(just_url=True))

for build in builds:
    print(build.build_type_id + ": " + build.number + " - " + str(build.id))
    changes = tc.changes.all().filter(
        build=str(build.id))
    print(changes.get(just_url=True))
    for change in changes:
        details = change.details
        print(change.username + ": " + details.comment)
