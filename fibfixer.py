import json

from BuildFixes import BuildFixes
from ChangeCommentParser import ChangeCommentParser
from pyteamcity.pyteamcity.future import TeamCity

tc = TeamCity.from_environ()
since_date_string = '20170101T000000+0000'
builds = tc.builds.all().filter(
    build_type="Hotfix",
    since_date=since_date_string,
    count=100)

#print(builds.get(just_url=True))

build_fixes = []

for build in builds:
    build_fixes.append(BuildFixes(build.id, build.number, build.status, build.build_type_id))

for build_fix in build_fixes:
    changes = tc.changes.all().filter(
        build=build_fix.id)
#    print(changes.get(just_url=True))
    for change in changes:
        details = change.details
        #print(details.comment)
        change_comment = ChangeCommentParser(details.comment)
        if change_comment.fixed_references is not None:
            for fix in change_comment.fixed_references:
                build_fix.add_fixed(fix)
        if change_comment.merge_reference is not None:
            build_fix.add_merged(change_comment.merge_reference)

build_fixes = sorted(build_fixes, key=lambda _: _.id)

for build_fix in build_fixes:
    print(build_fix.build_type_id + ": " + build_fix.number + " - " + str(build_fix.id) + " - " + build_fix.status)
    for fix in build_fix.fixed_references:
        print("FIXED: " + fix)
    for fix in build_fix.merged_references:
        print("MERGED: " + fix)
