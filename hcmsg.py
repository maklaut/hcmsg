# -*- coding: utf-8 -*-
from sys import stdin
import argparse
import ConfigParser
from os.path import expanduser

from hypchat import HypChat
from hypchat.restobject import User, Room

HIPCHAT_DEFAULT_URL = 'https://api.hipchat.com/v2'
CONFIG_FILE = expanduser('~/.hcmsg')

parser = argparse.ArgumentParser(description='Send message to HipChat.')
parser.add_argument('-u', '--user', action='append', default=None, metavar='user@example.com',  # type=int, nargs='+',
                    help="User email or id (can specify multiple times)")
parser.add_argument('-r', '--room', action='append', default=None,  # type=int, nargs='+',
                    help="Room name or id (can specify multiple times)")
parser.add_argument('--list-rooms', action='store_true',  # type=int, nargs='+',
                    help="Show available rooms and exit")

args = parser.parse_args()

config = ConfigParser.RawConfigParser({'token': None, 'hipchat_url': HIPCHAT_DEFAULT_URL})
config.read(CONFIG_FILE)
token = config.get('DEFAULT', 'token')
HIPCHAT_URL = config.get('DEFAULT', 'hipchat_url')

if not token:
    print "Can't read token from config file {config}\n\nConfig example (don't forget chmod 600):\n" + \
          "[DEFAULT]\ntoken = 012345678901234567890\nhipchat_url = {url}".format(
              config=CONFIG_FILE, url=HIPCHAT_DEFAULT_URL)
    exit(1)

hc = HypChat(token)
hc.capabilities.url = '{hipchat}/capabilities'.format(hipchat=HIPCHAT_URL)
hc.emoticons.url = '{hipchat}/emoticon'.format(hipchat=HIPCHAT_URL)
hc.rooms.url = '{hipchat}/room'.format(hipchat=HIPCHAT_URL)
hc.users_url = '{hipchat}/user'.format(hipchat=HIPCHAT_URL)

if args.list_rooms:
    rooms = hc.rooms()
    i = 0
    if 'items' in rooms and rooms['items']:
        print 'Cnt\tID\tName'
        print '----\t----\t----'
        for room in rooms['items']:
            i += 1
            print '{num}:\t{id}\t{name_}'.format(num=i, id=room.id, name_=room.name)
    exit(0)

if 'user' not in args and 'room' not in args or (not args.user and not args.room):
    parser.print_help()
    exit(1)


message = stdin.read()
#message = "Test message"

if args.user:
    for user_id in args.user:
        user = User(hc.fromurl('{hipchat}/user/{user}'.format(hipchat=HIPCHAT_URL, user=user_id)))
        user._requests = hc._requests
        user.message(message)

if args.room:
    for room_id in args.room:
        room = Room(hc.fromurl('{hipchat}/room/{room}'.format(hipchat=HIPCHAT_URL, room=room_id)))
        room._requests = hc._requests
        room.message(message)

