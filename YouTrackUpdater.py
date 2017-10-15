from youtrack.connection import Connection

#
# Generate api_key:
# # In YouTrack, open Settings -> Users -> Authentication -> New Token...
#

class YouTrackUpdater:
    def __init__(self, host, user, password, api_key):
        connection = Connection(
            url=host,
            api_key=api_key)


        # get one issue
        issue = connection.getIssue('PI-1000')

        # get first 10 issues in project JT for query 'for: me #unresolved'
        issues = connection.getIssues('pi', '#Resolved Fixed in build: {Next Build}', 0, 10)
        for issue in issues:
            print(issue);