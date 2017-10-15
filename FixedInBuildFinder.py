from BuildFixes import BuildFixes
from ChangeCommentParser import ChangeCommentParser
from future import TeamCity

class FixedInBuildFinder:
    def __init__(self,
                 username=None,
                 password=None,
                 protocol='http',
                 server='127.0.0.1',
                 port=None):
        skip_failed_builds = True
        tc = TeamCity(
            server=server,
            protocol=protocol,
            username=username,
            password=password,
        )
        since_date_string = '20160101T000000+0000'
        builds = tc.builds.all().filter(
            build_type="Hotfix",
            since_date=since_date_string,
            count=100)

        # print(builds.get(just_url=True))

        build_fixes = []

        for build in builds:
            build_fixes.append(BuildFixes(build.id, build.number, build.status, build.build_type_id))

        for build_fix in build_fixes:
            changes = tc.changes.all().filter(
                build=build_fix.id)
            #    print(changes.get(just_url=True))
            for change in changes:
                details = change.details
                # print(details.comment)
                change_comment = ChangeCommentParser(details.comment)
                if change_comment.fixed_references is not None:
                    for fix in change_comment.fixed_references:
                        build_fix.add_fixed(fix)
                if change_comment.merge_reference is not None:
                    build_fix.add_merged(change_comment.merge_reference)

        build_fixes = sorted(build_fixes, key=lambda _: _.id)

        # Carry over fixes in failed builds, if they are to be ignored
        accumulated_fixes = []
        accumulated_merges = []
        if skip_failed_builds:
            for build_fix in build_fixes:
                if build_fix.status != "SUCCESS":
                    accumulated_fixes.extend(build_fix.fixed_references)
                    accumulated_merges.extend(build_fix.merged_references)
                else:
                    build_fix.extend_fixes(accumulated_fixes)
                    build_fix.extend_merges(accumulated_merges)
                    accumulated_fixes = []
                    accumulated_merges = []

        for build_fix in build_fixes:
            if skip_failed_builds and build_fix.status != "SUCCESS":
                continue
            print(
            build_fix.build_type_id + ": " + build_fix.number + " - " + str(build_fix.id) + " - " + build_fix.status)
            for fix in build_fix.fixed_references:
                print("FIXED: " + fix)
            for fix in build_fix.merged_references:
                print("MERGED: " + fix)

        # build you-track issue to build map
        fixedInBuildMap = {}

        for build_fix in build_fixes:
            if skip_failed_builds and build_fix.status != "SUCCESS":
                continue
            for fix in build_fix.fixed_references:
                if fix not in fixedInBuildMap:
                    fixedInBuildMap[fix] = build_fix.number
            for fix in build_fix.merged_references:
                if fix not in fixedInBuildMap:
                    fixedInBuildMap[fix] = build_fix.number

        for (issue_id, version) in fixedInBuildMap.items():
            print(issue_id + " fixed in build " + version)