import json

from configparser import ConfigParser

from FixedInBuildFinder import FixedInBuildFinder
from YouTrackUpdater import YouTrackUpdater
from youtrack.connection import Connection

config = ConfigParser()
config.read('config.ini')

youtrack_config = config['YouTrack']


# ytUpdater = YouTrackUpdater(youtrack_config['Host'], youtrack_config['User'], youtrack_config['Password'], youtrack_config['ApiKey'])


teamcity_config = config['TeamCity']

fibFinder = FixedInBuildFinder(
    server = teamcity_config['Host'],
    protocol = teamcity_config['Protocol'],
    username = teamcity_config['User'],
    password = teamcity_config['Password'])
