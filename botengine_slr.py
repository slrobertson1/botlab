# uncompyle6 version 3.3.5
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.16 (default, Jun 19 2019, 07:40:37) 
# [GCC 4.2.1 Compatible Apple LLVM 10.0.1 (clang-1001.0.46.4)]
# Embedded file name: botengine
# Compiled at: 2019-06-20 18:15:47
"""
BotEngine

Dependencies:
* Python 2.7
* requests - use "pip install requests" to install
* dateutil - use "pip install python-dateutil" to install
* tzlocal  - use "pip install tzlocal" to install
* dill     - use "pip install dill" to install
* lz4      - use "pip install lz4" to install

@author:     David Moss

@copyright:  2012 - 2019 People Power Company. All rights reserved.

@contact:    dmoss@peoplepowerco.com
"""
from __future__ import print_function
from __builtin__ import True, False
from dill import source
if hasattr(__builtins__, 'raw_input'):
    input = raw_input
import os, importlib, json, logging, sys, urllib, time, datetime
from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter
DEFAULT_BASE_SERVER_URL = 'app.presencepro.com'
__all__ = []
__version__ = 5.4
__date__ = '2012-08-02'
__updated__ = '2019-06-20'
DEBUG = 0
TESTRUN = 0
PROFILE = 0
BOT_CATEGORY_DICT = {'E': 'Energy', 
   'S': 'Security', 
   'C': 'Care', 
   'L': 'Lifestyle', 
   'H': 'Health', 
   'W': 'Wellness'}
VERSION_STATUS_DICT = {0: 'Waiting for upload', 
   1: 'Privately Available', 
   2: 'Submitted for Review', 
   3: 'Under Review', 
   4: 'Publicly Available', 
   5: 'Bot Shop Rejected', 
   6: 'Developer Rejected', 
   7: 'Replaced by a newer version', 
   8: 'Suspended'}
LOGGING_LEVEL_DICT = {'debug': logging.DEBUG, 
   'info': logging.INFO, 
   'warn': logging.WARN, 
   'error': logging.ERROR}
BOT_KEY_TYPE_NORMAL = 0
BOT_KEY_TYPE_DEVELOPER = 1
STATUS_BOT_INCOMPLETE = 0
STATUS_BOT_ACTIVE = 1
STATUS_BOT_INACTIVE = 2
_servermode = False
_bot_logger = None
_https_proxy = None
MAXIMUM_VARIABLE_SIZE_BYTES = 8000000
MAXINT = 9223372036854775807
CORE_VARIABLE_NAME = '-core-'
TIMERS_VARIABLE_NAME = '[t]'
QUESTIONS_VARIABLE_NAME = '[q]'
COUNT_VARIABLE_NAME = '[c]'
TAR = True
MICROSERVICES_DIRECTORY = 'intelligence'
DEVICE_MICROSERVICES_KEY = 'DEVICE_MICROSERVICES'
LOCATION_MICROSERVICES_KEY = 'LOCATION_MICROSERVICES'
ORGANIZATION_MICROSERVICES_KEY = 'ORGANIZATION_MICROSERVICES'
MICROSERVICES_FOUNDATION_BOT = 'com.ppc.Bot'

def execute_on_server(argv):
    """
    Expedited execution on a docker server
    """
    global _bot_logger
    global _servermode
    parser = ArgumentParser()
    parser.add_argument('-r', '--run', dest='run_bundle_id')
    parser.add_argument('-j', '--json', dest='json')
    parser.add_argument('--loglevel', dest='loglevel', choices=['debug', 'info', 'warn', 'error'], default='error')
    parser.add_argument('--servermode', action='store_true')
    args = parser.parse_args()
    sys.argv = []
    _bot_logger = _create_logger('bot', LOGGING_LEVEL_DICT[args.loglevel], False, None)
    if args.json.startswith("'"):
        args.json = args.json[1:]
    if args.json.endswith("'"):
        args.json = args.json[:-1]
    inputs = None
    try:
        inputs = json.loads(str(args.json))
    except:
        sys.stderr.write("Couldn't parse the JSON input data\n")
        sys.stderr.write(args.json)
        sys.stderr.write('\n\n')
        if _servermode:
            _bot_logger.error("Couldn't parse the JSON input data, date=" + str(args.json))
        return 1

    base_path = os.path.join(os.getcwd(), args.run_bundle_id)
    sys.path.insert(0, base_path)
    bot = importlib.import_module('bot')
    _run(bot, inputs, _bot_logger)
    return 0


playback_user_info = {}
playback_timer_timestamp = None
playback_current_timestamp = None
playback_variables = None

def playback_download_binary_variable(name):
    global playback_variables
    return playback_variables


def playback_flush_binary_variables():
    pass


def playback_flush_commands():
    pass


def playback_flush_questions():
    pass


def playback_flush_rules():
    pass


def playback_flush_tags():
    pass


def playback_cancel_timers(reference=None):
    pass


def playback_delete_all_rules(status=None, rule_id_list=[], device_type_list=[], device_id_list=[], default=None, hidden=None, user_id=None):
    pass


def playback_get_user_info(user_id=None):
    global playback_user_info
    return playback_user_info


def playback_execute_again_at_timestamp(timestamp_ms):
    global playback_timer_timestamp
    playback_timer_timestamp = timestamp_ms


def playback_notify(push_content=None, push_sound=None, email_subject=None, email_content=None, email_html=False, email_attachments=[], push_template_filename=None, push_template_model=None, email_template_filename=None, email_template_model=None, sms_content=None, sms_template_filename=None, sms_template_model=None, sms_group_chat=False, brand=None, language=None, user_id=None, user_id_list=[], to_residents=False, to_supporters=False, to_admins=False):
    global playback_current_timestamp
    import pytz
    dt = datetime.datetime.fromtimestamp(playback_current_timestamp / 1000, pytz.timezone(playback_user_info['locations'][0]['timezone']['id']))
    if sms_content is not None:
        out = '[' + str(playback_current_timestamp) + ' - ' + dt.isoformat() + '] SMS: ' + sms_content + '\n'
        print(out)
        with open('playback.txt', 'a') as (myfile):
            myfile.write(out)
    if push_content is not None:
        out = '[' + str(playback_current_timestamp) + ' - ' + dt.isoformat() + '] PUSH NOTIFICATION: ' + push_content + '\n'
        print(out)
        with open('playback.txt', 'a') as (myfile):
            myfile.write(out)
    if email_subject is not None:
        out = '[' + str(playback_current_timestamp) + ' - ' + dt.isoformat() + '] EMAIL: ' + email_subject + '\n'
        print(out)
        with open('playback.txt', 'a') as (myfile):
            myfile.write(out)
    return


def playback_set_mode(location_id, mode):
    import pytz
    dt = datetime.datetime.fromtimestamp(playback_current_timestamp / 1000, pytz.timezone(playback_user_info['locations'][0]['timezone']['id']))
    out = '[' + str(playback_current_timestamp) + ' - ' + dt.isoformat() + '] SET MODE: ' + mode + '\n'
    print(out)
    with open('playback.txt', 'a') as (myfile):
        myfile.write(out)


def main(argv=None):
    """Command line options."""
    global TAR
    global _bot_logger
    global _https_proxy
    global _servermode
    global playback_current_timestamp
    global playback_timer_timestamp
    global playback_user_info
    global playback_variables
    if argv is None:
        argv = sys.argv
    else:
        sys.argv.extend(argv)
    _servermode = '--servermode' in argv
    if _servermode:
        return execute_on_server(argv)
    if sys.version_info < (2, 7) or sys.version_info >= (3, 0):
        print('Python version info: ' + str(sys.version_info))
        raise RuntimeError('This BotEngine is designed for Python 2.7 for cloud compatibility')
    try:
        importlib.import_module('requests')
    except ImportError:
        sys.stderr.write("Missing the 'requests' module!\n")
        sys.stderr.write("Please install this module by running 'pip install requests'\n")
        return 1
    else:
        try:
            importlib.import_module('dateutil')
        except ImportError:
            sys.stderr.write("Missing the 'python-dateutil' module!\n")
            sys.stderr.write("Please install this module by running 'pip install python-dateutil'\n")
            return 1
        else:
            try:
                importlib.import_module('dill')
            except ImportError:
                sys.stderr.write("Missing the 'dill' module!\n")
                sys.stderr.write("Please install this module by running 'pip install dill'\n")
                return 1

            try:
                importlib.import_module('tzlocal')
            except ImportError:
                sys.stderr.write("Missing the 'tzlocal' module!\n")
                sys.stderr.write("Please install this module by running 'pip install tzlocal'\n")
                return 1

        program_version = 'v%s' % __version__
        program_build_date = str(__updated__)
        program_version_message = '%%(prog)s %s (%s)' % (program_version, program_build_date)
        program_shortdesc = __import__('__main__').__doc__.split('\n')[1]
        program_license = '%s\n\n  Created by David Moss\n\n  Copyright 2019 People Power Company. All rights reserved.\n\n  Distributed on an "AS IS" basis without warranties\n  or conditions of any kind, either express or implied.\n\nUSAGE\n' % program_shortdesc
        try:
            parser = ArgumentParser(description=program_license, formatter_class=RawDescriptionHelpFormatter, add_help=False)
            developer_group = parser.add_argument_group(Color.BOLD + 'BOT LAB - Create and manage your own Bot services' + Color.END)
            developer_group.add_argument('--commit', dest='commit_bundle_id', help='Commit the given bot bundle to the server')
            developer_group.add_argument('--my_developer_bots', dest='listapps', action='store_true', help='Get a list of the bots you created')
            developer_group.add_argument('--publish', dest='publish_bundle_id', help='Submit this bot for review to become publicly available')
            developer_group.add_argument('--makeitso', dest='make_it_so', help='Commit, publish, review, and approve - for senior admin-level bot developers only')
            developer_group.add_argument('--approve', dest='approve_bundle_id', help='Used by administrators to approve a bot for publishing')
            developer_group.add_argument('--botinfo', dest='info_bundle_id', help='Get the details of your given bot bundle')
            developer_group.add_argument('--stats', dest='stats_bundle_id', help='Get the statistics of your given bot bundle')
            developer_group.add_argument('--errors', dest='errors_bundle_id', help='Get the errors from your given bot bundle executing on the cloud across all users')
            developer_group.add_argument('--logs', dest='logs_bundle_id', help='Get the logs from your given bot bundle executing on the cloud across all users')
            developer_group.add_argument('--reject_bot_under_review', dest='reject_bundle_id', help='Reject the given bot from being reviewed or published publicly. Used after you --publish and need to make changes.')
            developer_group.add_argument('--add_organization', dest='bundle_for_organization', help='Allow the given Bundle ID to be purchased by the given --organization')
            developer_group.add_argument('--remove_organization', dest='remove_organization', help='Bundle ID to prevent from being purchased by the --organization')
            developer_group.add_argument('--organization_development_mode', dest='organization_development_mode', action='store_true', help='Allow the organization to use the bot in developer mode instead of only purchasing publicly available bots. This is always used in conjunction with --add_organization')
            beta_group = parser.add_argument_group(Color.BOLD + 'BOT BETA TESTING - Privately beta test your bots' + Color.END)
            beta_group.add_argument('--beta_test_bot', dest='beta_bundle_id', help='Specify a bot bundle ID to configure for beta testing. Typically used in conjunction with --beta_add_user and --beta_delete_user. If used alone, it returns a list of existing beta tester user IDs.')
            beta_group.add_argument('--beta_add_user', dest='beta_add_user_id', help='Specify a user ID to add as a beta tester for the given --beta_test_bot, or used with --beta_purchase_bot for an admin to purchase the bot into the given account.')
            beta_group.add_argument('--beta_delete_user', dest='beta_delete_user_id', help='Specify a user ID to remove as a beta tester for the given --beta_test_bot')
            beta_group.add_argument('--beta_purchase_bot', dest='beta_purchase_bot', help='As an admin, purchase the given bot bundle ID into a user account to begin running it. Use this in conjunction with --beta_add_user to specify the recipient user ID.')
            run_group = parser.add_argument_group(Color.BOLD + 'BOT ENGINE - Execute Bots' + Color.END)
            run_group.add_argument('-r', '--run', dest='run_bundle_id', help="Run a bot. Pass in the bundle identifier of the bot, which must also be the name of the bot's directory below your current working directory")
            run_group.add_argument('-i', '--instance', dest='run_instance_id', help='Run the specific bot instance ID')
            run_group.add_argument('-j', '--json', dest='json', help='The JSON that would be passed to the bot over the command line, in the format \'{"hello": "world"}\'')
            run_group.add_argument('-a', '--apikey', dest='user_key', help="User's API key, instead of a username / password")
            run_group.add_argument('-l', '--location', dest='location_id', help='Location ID')
            run_group.add_argument('--servermode', dest='servermode', action='store_true', help='Run this bot on server environment')
            run_group.add_argument('--https_proxy', dest='https_proxy', help='If your corporate network requires a proxy, type in the full HTTPS proxy address here (i.e. http://10.10.1.10:1080)')
            appstore_group = parser.add_argument_group(Color.BOLD + 'BOT SHOP - Browse the Bot Shop and manage purchased bots.' + Color.END)
            appstore_group.add_argument('--search', dest='search', action='store_true', help='Search the bot store for all available bots')
            appstore_group.add_argument('--searchfor', dest='search_criteria', help='Search the bot store for bots matching the given search criteria')
            appstore_group.add_argument('--lookat', dest='view_bundle_id', help='View the details of an bot on the bot store')
            appstore_group.add_argument('--purchase', dest='purchase_bundle_id', help='Obtain or purchase access to an bot on the bot store')
            appstore_group.add_argument('--configure', dest='configure_bot_instance_id', help='Grant permission for an bot instance to access devices and communications')
            appstore_group.add_argument('--my_purchased_bots', dest='my_purchased_bots', action='store_true', help='Get a list of the bots you have obtained or purchased')
            appstore_group.add_argument('--pause', dest='pause_bot_instance_id', help='Stop the given bot instance from executing on your account')
            appstore_group.add_argument('--play', dest='play_bot_instance_id', help='Resume execution of the given bot instance on your account')
            appstore_group.add_argument('--delete', dest='delete_bot_instance_id', help='Delete the given bot instance ID or bundle ID out of my account')
            appstore_group.add_argument('--permissions', dest='permissions_bot_instance_id', help='Discover what your purchased bot has permission to access')
            appstore_group.add_argument('--questions', dest='questions_bot_instance_id', help='Answer questions asked by the given bot instance ID or bundle ID')
            optional_group = parser.add_argument_group(Color.BOLD + 'Optional Arguments' + Color.END)
            optional_group.add_argument('-o', '--organization_id', dest='organization_id', help="Add in the organization ID we're talking about, used in conjunction with --purchase, --add_organization, --remove_organization")
            optional_group.add_argument('-h', '--help', dest='help', action='store_true', help='Show this help message and exit')
            optional_group.add_argument('-u', '--username', dest='username', help='Username')
            optional_group.add_argument('-p', '--password', dest='password', help='Password')
            optional_group.add_argument('--admin_username', dest='admin_username', help='Administrative username')
            optional_group.add_argument('--admin_password', dest='admin_password', help='Administrative password')
            optional_group.add_argument('-b', '--brand', dest='brand', help="Brand name partner to interact with the correct servers: 'myplace', 'origin', 'presence', etc.")
            optional_group.add_argument('-s', '--server', dest='server', help='Base server URL (default is ' + DEFAULT_BASE_SERVER_URL + ')')
            optional_group.add_argument('-c', '--challenge', dest='challenge_id', help='Challenge ID')
            optional_group.add_argument('--loglevel', dest='loglevel', choices=['debug', 'info', 'warn', 'error'], default='info', help='The logging level, default is debug')
            optional_group.add_argument('--httpdebug', dest='httpdebug', action='store_true', help='HTTP debug logger output')
            optional_group.add_argument('--logfile', dest='logfile', help='Append the debug output to the given filename')
            optional_group.add_argument('--zip', dest='zip', action='store_true', help='Commit the bot using the .zip (old) method of bot generation, instead of .tar (new) method.')
            tools_group = parser.add_argument_group(Color.BOLD + 'Handy Developer Tools' + Color.END)
            tools_group.add_argument('--my_devices', dest='list_devices', action='store_true', help='Get a list of your devices')
            tools_group.add_argument('--my_locations', dest='list_locations', action='store_true', help='Get a list of the locations your account has access to')
            tools_group.add_argument('--user_id', dest='user_id', action='store_true', help='Get your user ID')
            tools_group.add_argument('--device_types', dest='device_types', action='store_true', help='Get a list of available device types on this server')
            tools_group.add_argument('--model', dest='device_type_model', help='Get a list of parameters to be expected for a given device type')
            tools_group.add_argument('--parameter', dest='parameter', help='Get a description of a specific parameter name')
            tools_group.add_argument('--download_device', dest='download_device_id', help='Download data from a specific device ID in CSV format')
            tools_group.add_argument('--download_type', dest='download_device_type', help='Download data from all devices of a specific device type in CSV format')
            # SLR addition
            tools_group.add_argument('--download_devices', dest='download_devices', action='store_true', help='Download data from all your devices in CSV format')
            tools_group.add_argument('--record', dest='record', action='store_true', help='Record all device and mode data from your account for rapid playback and bot testing')
            tools_group.add_argument('--playback', dest='playback', help='Specify a recorded .json filename to playback. Use the --run command to specify the bot.')
            tools_group.add_argument('--generate', dest='generate_bot_bundle_id', help='Generate the bot locally for analysis, without installing dependencies or uploading.')
            settings_group = parser.add_argument_group(Color.BOLD + 'Version Control' + Color.END)
            settings_group.add_argument('--version', action='version', version=program_version_message)
            settings_group.add_argument('--update', dest='update', action='store_true', help='Update this BotEngine framework from the server')
            args = parser.parse_args()
            sys.argv = []
            _bot_logger = _create_logger('bot', LOGGING_LEVEL_DICT[args.loglevel], True, args.logfile)
            if args.help:
                parser.print_help()
                return 0
            username = args.username
            password = args.password
            botname = args.run_bundle_id
            instance = args.run_instance_id
            server = args.server
            challenge_id = args.challenge_id
            device_server = None
            commit = args.commit_bundle_id
            update = args.update
            publish = args.publish_bundle_id
            reject = args.reject_bundle_id
            httpdebug = args.httpdebug
            listdevices = args.list_devices
            listapps = args.listapps
            botinfo = args.info_bundle_id
            botstats = args.stats_bundle_id
            boterrors = args.errors_bundle_id
            botlogs = args.logs_bundle_id
            forever = args.json is None
            download_device_id = args.download_device_id
            download_device_type = args.download_device_type
            # SLR addition
            download_devices = args.download_devices
            # end SLR addition
            search_criteria = args.search_criteria
            search = args.search or search_criteria is not None
            appstore_view_bundle_id = args.view_bundle_id
            my_purchased_bots = args.my_purchased_bots
            delete_bot_instance_id = args.delete_bot_instance_id
            purchase_bundle_id = args.purchase_bundle_id
            configure_bot_instance_id = args.configure_bot_instance_id
            pause_bot_instance_id = args.pause_bot_instance_id
            play_bot_instance_id = args.play_bot_instance_id
            organization_id = args.organization_id
            organization_development_mode = args.organization_development_mode
            add_organization = args.bundle_for_organization
            remove_organization = args.remove_organization
            permissions_bot_instance_id = args.permissions_bot_instance_id
            devicetypes = args.device_types
            parameter = args.parameter
            device_type_model = args.device_type_model
            user_key = args.user_key
            record = args.record
            playback = args.playback
            beta_add_user_id = args.beta_add_user_id
            beta_purchase_bot = args.beta_purchase_bot
            beta_delete_user_id = args.beta_delete_user_id
            beta_test_bot = args.beta_bundle_id
            generate = args.generate_bot_bundle_id
            user_id = args.user_id
            brand = args.brand
            approve = args.approve_bundle_id
            admin_username = args.admin_username
            admin_password = args.admin_password
            location_id = args.location_id
            list_locations = args.list_locations
            if brand is not None:
                brand = brand.lower()
                if brand == 'presence':
                    print(Color.BOLD + '\nPresence by People Power' + Color.END)
                    server = 'app.presencepro.com'
                elif brand == 'myplace':
                    print(Color.BOLD + '\nMyPlace - Smart. Simple. Secure.' + Color.END)
                    server = 'iot.peoplepowerco.com'
                elif brand == 'origin':
                    print(Color.BOLD + '\nOrigin Home HQ' + Color.END)
                    server = 'app.originhomehq.com.au'
                elif brand == 'innogy':
                    print(Color.BOLD + '\ninnogy SmartHome' + Color.END)
                    server = 'innogy.presencepro.com'
                else:
                    sys.stderr.write('This brand does not exist: ' + str(brand) + '\n\n')
                    return 1
            if location_id is not None:
                print(Color.BOLD + ('Location ID: {}').format(location_id) + Color.END)
                location_id = int(location_id)
            _https_proxy = None
            if args.https_proxy is not None:
                _https_proxy = {'https': args.https_proxy}
            if args.zip is not None:
                if args.zip:
                    TAR = False
            make_it_so = args.make_it_so
            if make_it_so is not None:
                commit = make_it_so
                publish = make_it_so
            if approve:
                publish = approve
            if httpdebug:
                try:
                    import http.client as http_client
                except ImportError:
                    import httplib as http_client
                    http_client.HTTPConnection.debuglevel = 1

                logging.basicConfig()
                logging.getLogger().setLevel(logging.DEBUG)
                requests_log = logging.getLogger('requests.packages.urllib3')
                requests_log.setLevel(logging.DEBUG)
                requests_log.propagate = True
            user_info = None
            botengine_key = None
            inputs = None
            if args.json is not None:
                json_input = args.json
                if json_input.startswith("'"):
                    json_input = json_input[1:]
                if json_input.endswith("'"):
                    json_input = json_input[:-1]
                try:
                    inputs = json.loads(str(json_input))
                    botengine_key = inputs['apiKey']
                    server = inputs['apiHost']
                except:
                    sys.stderr.write("Couldn't parse the JSON input data\n")
                    sys.stderr.write(json_input)
                    sys.stderr.write('\n\n')
                    if _servermode:
                        _bot_logger.error("Couldn't parse the JSON input data, date=" + str(json_input))
                    return 1

            if not server:
                server = DEFAULT_BASE_SERVER_URL
            if 'http' not in server:
                server = 'https://' + server
            print('Bot Server: ' + server)
            if listdevices:
                if user_key is None:
                    user_key = _login(server, username, password)
                _summarize_devices(server, user_key, location_id)
                return 0
            if list_locations:
                if user_key is None:
                    user_key = _login(server, username, password)
                user_info = _get_user_info(server, user_key)
                if 'locations' not in user_info:
                    print(Color.RED + 'This user account does not have access to any locations.\n\n' + Color.END)
                else:
                    print(Color.BOLD + 'Locations' + Color.END)
                    print('-' * 50)
                    for location_object in user_info['locations']:
                        print(('\t{}{}{}: {}').format(Color.BOLD, str(location_object['id']), Color.END, location_object['name'].encode('utf-8')))

                print()
                return 0
            if devicetypes:
                if user_key is None:
                    user_key = _login(server, username, password)
                _summarize_device_types(server, user_key)
                return 0
            if device_type_model:
                if user_key is None:
                    user_key = _login(server, username, password)
                _print_model(server, user_key, device_type_model)
                print('\n' + the_bot() + 'Done!')
                return 0
            if parameter:
                if user_key is None:
                    user_key = _login(server, username, password)
                p = _get_parameters(server, user_key, parameter)
                if 'deviceParams' not in p:
                    print(Color.RED + 'This parameter is not defined on this server.' + Color.END)
                else:
                    p = p['deviceParams'][0]
                    print(Color.BOLD + Color.GREEN + parameter + Color.END)
                    if 'numeric' in p:
                        if p['numeric']:
                            print(Color.BOLD + 'Type: ' + Color.END + 'Numeric values')
                        else:
                            print(Color.BOLD + 'Type: ' + Color.END + 'Non-numeric values')
                    if 'systemUnit' in p:
                        print(Color.BOLD + 'Units: ' + Color.END + p['systemUnit'])
                    if 'scale' in p:
                        print(Color.BOLD + 'Accuracy: ' + Color.END + 'Store up to ' + str(p['scale']) + ' digits after the decimal')
                    profiled = False
                    configured = False
                    historical = None
                    if 'profiled' in p:
                        profiled = p['profiled']
                    if 'configured' in p:
                        configured = p['configured']
                    if 'historical' in p:
                        historical = p['historical']
                    if profiled and configured:
                        print(Color.BOLD + 'Usage: ' + Color.END + 'Measurement & Command')
                    elif profiled and not configured:
                        print(Color.BOLD + 'Usage: ' + Color.END + 'Measurement only')
                    elif configured and not profiled:
                        print(Color.BOLD + 'Usage: ' + Color.END + 'Command only')
                    if historical is not None:
                        if historical == 0:
                            print(Color.BOLD + 'Storage: ' + Color.END + 'Current state only, no database history')
                        elif historical == 1:
                            print(Color.BOLD + 'Storage: ' + Color.END + 'Update database history every 15 minutes or when the value changes more than 25%')
                        elif historical == 2:
                            print(Color.BOLD + 'Storage: ' + Color.END + 'Update database history on every change')
                print('\n' + the_bot() + 'Done!')
                return 0
            if listapps:
                if user_key is None:
                    user_key = _login(server, username, password)
                _summarize_apps(server, user_key)
                return 0
            if beta_purchase_bot:
                if user_key is None:
                    user_key = _login(server, username, password)
                bundle = beta_purchase_bot
                bundle = bundle.replace('/', '')
                j = _beta_purchase_bot(server, user_key, bundle, beta_add_user_id)
                print('Result: ' + json.dumps(j, indent=2, sort_keys=True))
                print()
                return 0
            if beta_add_user_id or beta_delete_user_id:
                if beta_test_bot is None:
                    sys.stderr.write('Need to also specify a --beta_test_bot bundle ID.\n')
                    return 1
                if user_key is None:
                    user_key = _login(server, username, password)
                if beta_add_user_id:
                    print('Adding user ID ' + str(beta_add_user_id) + ' to beta test ' + beta_test_bot + '...')
                    _add_bot_beta_testers(server, user_key, beta_test_bot, beta_add_user_id)
                else:
                    _delete_bot_beta_testers(server, user_key, beta_test_bot, beta_delete_user_id)
            if beta_test_bot:
                if user_key is None:
                    user_key = _login(server, username, password)
                j = _get_bot_beta_testers(server, user_key, beta_test_bot)
                if 'betaTesters' in j:
                    if len(j['betaTesters']) == 0:
                        print('There are no beta testers for this bot.')
                    else:
                        if len(j['betaTesters']) == 1:
                            print('There is one beta tester for this bot.')
                        else:
                            print('There are ' + str(j['betaTesters']) + ' beta testers for this bot.')
                        for tester in j['betaTesters']:
                            print('\t* User ID: ' + str(tester['userId']))

                print()
                return 0
            if user_id:
                if user_key is None:
                    user_key = _login(server, username, password)
                user_info = _get_user_info(server, user_key)
                print(('User ID: {}{}{}\n').format(Color.BOLD, user_info['user']['id'], Color.END))
                return 0
            if botinfo:
                if user_key is None:
                    user_key = _login(server, username, password)
                bundle = botinfo
                bundle = bundle.replace('/', '')
                j = _get_apps(server, user_key, bundle)
                bots = j.get('bots')
                if bots is None:
                    sys.stderr.write("The bot '" + bundle + "' does not belong to you, or you haven't created it yet.\n")
                    return 1
                sys.stderr.write(Color.BOLD + '\nAPP MARKETING INFO ON THE SERVER\n' + Color.END)
                sys.stderr.write(json.dumps(bots[0], indent=2, sort_keys=True))
                sys.stderr.write('\n\n')
                j = _get_versions(server, user_key, bundle)
                versions = j.get('versions')
                if versions is None:
                    sys.stderr.write(Color.RED + "The bot '" + bundle + "' does not have any version!" + Color.END)
                    sys.stderr.write(Color.RED + "\nUse 'botengine --commit " + bundle + "' to commit your first version.\n\n" + Color.END)
                    return 1
                sys.stderr.write(Color.BOLD + '\nAPP VERSION INFO ON THE SERVER\n' + Color.END)
                sys.stderr.write(json.dumps(versions, indent=2, sort_keys=True))
                sys.stderr.write('\n\n')
                return 0
            if botstats:
                if user_key is None:
                    user_key = _login(server, username, password)
                bundle = botstats
                bundle = bundle.replace('/', '')
                stats = _get_app_statistics(server, user_key, bundle)
                print(Color.BOLD + 'RATINGS' + Color.END)
                print('Average rating across all versions: ' + str(stats['rating']['average']))
                stars_dict = stats['rating']
                TOTAL_STARS = 20
                ordered_keys = ['star5', 'star4', 'star3', 'star2', 'star1']
                if stars_dict['total'] > 0:
                    for key in ordered_keys:
                        stars = int(float(stars_dict[key]) / float(stars_dict['total']) * TOTAL_STARS)
                        title = Color.BOLD + key.replace('star', '') + '-stars' + Color.END
                        print(title + ': [' + '*' * stars + ' ' * (TOTAL_STARS - stars) + ']')

                versions_dict = {}
                for v in stats['versions']:
                    versions_dict[int(v['creationDateMs'])] = v

                first = True
                i = 0
                for key in sorted(versions_dict.keys(), reverse=False):
                    i += 1
                    print('-' * 50)
                    if i == len(versions_dict.keys()):
                        print(Color.GREEN + Color.BOLD + 'NEWEST VERSION' + Color.END)
                    print(Color.BOLD + 'VERSION ' + str(versions_dict[key]['version']) + Color.END)
                    print('\t' + Color.BOLD + 'Creation Date: ' + Color.END + str(versions_dict[key]['creationDate']))
                    print('\t' + Color.BOLD + 'Average Execution Time: ' + Color.END + Color.PURPLE + str(versions_dict[key]['averageExecutionTime']) + ' [ms]' + Color.END)
                    print('\t' + Color.BOLD + 'Total Executions: ' + Color.END + str(versions_dict[key]['totalExecutions']))
                    print('\t' + Color.BOLD + 'Failed Executions: ' + Color.END + str(versions_dict[key]['failedExecutions']))
                    if float(versions_dict[key]['totalExecutions']) > 0:
                        print('\t' + Color.BOLD + 'Failure Rate: ' + Color.END + '%.2f' % (100 * (float(versions_dict[key]['failedExecutions']) / float(versions_dict[key]['totalExecutions']))) + '%')
                    print('\t' + Color.BOLD + 'Current Status: ' + Color.END + str(VERSION_STATUS_DICT[versions_dict[key]['status']]))
                    print('\t' + Color.BOLD + 'Status updated on: ' + Color.END + str(versions_dict[key]['statusChangeDate']))
                    print()
                    stars_dict = versions_dict[key]['rating']
                    if stars_dict['total'] > 0:
                        for key in ordered_keys:
                            stars = int(float(stars_dict[key]) / float(stars_dict['total']) * TOTAL_STARS)
                            title = key.replace('star', '') + '-stars'
                            print('\t' + title + ': [' + '*' * stars + ' ' * (TOTAL_STARS - stars) + ']')

                    else:
                        print('\tNo ratings.')
                    print('\n')

                print(Color.GREEN + Color.BOLD + 'TOTAL STATISTICS' + Color.END)
                print(Color.BOLD + 'Total current users: ' + Color.END + str(stats['totalCurrentUsers']))
                print(Color.BOLD + 'Total current bot instances: ' + Color.END + str(stats['totalCurrentInstances']))
                print(Color.BOLD + 'Total executions: ' + Color.END + str(stats['totalExecutions']))
                print(Color.BOLD + 'Total execution time: ' + Color.END + str(float(stats['totalExecutionTime']) / 1000.0) + ' [sec]; %.2f' % (float(stats['totalExecutionTime']) / 1000.0 / 60.0 / 60.0) + ' [hours]; %.2f' % (float(stats['totalExecutionTime']) / 1000.0 / 60.0 / 60.0 / 24.0) + ' [days]; %.2f' % (float(stats['totalExecutionTime']) / 1000.0 / 60.0 / 60.0 / 24.0 / 30.0) + ' [months]')
                print()
                return 0
            if boterrors:
                if user_key is None:
                    user_key = _login(server, username, password)
                bundle = boterrors
                bundle = bundle.replace('/', '')
                exists = False
                try:
                    j = _get_bot_errors(server, user_key, bundle, developer=False)
                    print(Color.BOLD + '\n\nPUBLIC VERSION' + Color.END)
                    print(json.dumps(j, indent=2, sort_keys=True))
                    exists = True
                except:
                    pass
                else:
                    try:
                        j = _get_bot_errors(server, user_key, bundle, developer=True)
                        print(Color.BOLD + '\n\nDEVELOPER VERSION' + Color.END)
                        print(json.dumps(j, indent=2, sort_keys=True))
                        exists = True
                    except:
                        pass

                if not exists:
                    print(Color.BOLD + Color.RED + '\n\nThat bot does not exist.' + Color.END)
                return 0
            if botlogs:
                if user_key is None:
                    user_key = _login(server, username, password)
                bundle = botlogs
                bundle = bundle.replace('/', '')
                j = _get_bot_errors(server, user_key, bundle, errors_only=False)
                print(json.dumps(j, indent=2, sort_keys=True))
                return 0
            if search:
                if user_key is None:
                    user_key = _login(server, username, password)
                search_results = _botstore_search(server, user_key, searchBy=search_criteria)
                for bot in search_results:
                    if bot['compatible']:
                        compatibility = Color.GREEN + '(Compatible)' + Color.END
                    else:
                        compatibility = Color.RED + '(Incompatible)' + Color.END
                    print(Color.BOLD + '+ ' + bot['name'] + ' - by ' + bot['author'] + ' ' + compatibility + Color.END)
                    print('\t' + Color.UNDERLINE + bot['bundle'] + Color.END)
                    try:
                        print('\t' + bot['description'].replace('\n', '\n\t\t'))
                    except:
                        pass
                    else:
                        print('\n')

                return 0
            if appstore_view_bundle_id:
                if user_key is None:
                    user_key = _login(server, username, password)
                appstore_view_bundle_id = appstore_view_bundle_id.replace('/', '')
                app_info = _botstore_botinfo(server, user_key, appstore_view_bundle_id)
                sys.stderr.write(json.dumps(app_info, indent=2, sort_keys=True))
                sys.stderr.write('\n\n')
                return 0
            if my_purchased_bots:
                if user_key is None:
                    user_key = _login(server, username, password)
                bots = _botstore_mybots(server, user_key, location_id=location_id, organization_id=organization_id)
                if bots is not None:
                    for bot in bots:
                        status = Color.RED + 'Unknown status' + Color.END
                        if bot['status'] == 0:
                            status = Color.RED + 'NOT CONFIGURED' + Color.END
                        elif bot['status'] == 1:
                            status = Color.GREEN + 'ACTIVE' + Color.END
                        elif bot['status'] == 2:
                            status = Color.RED + 'INACTIVE' + Color.END
                        print('Bot Instance ' + str(bot['appInstanceId']) + ': ' + bot['bundle'] + '; Version ' + bot['version'] + '; ' + status)

                else:
                    sys.stderr.write(Color.RED + 'You have not obtained or purchased any bots.' + Color.END)
                print('\n' + the_bot() + 'Done!')
                return 0
            if pause_bot_instance_id:
                if user_key is None:
                    user_key = _login(server, username, password)
                try:
                    _botstore_mybots(server, user_key, pause_bot_instance_id, location_id=location_id, organization_id=organization_id)
                except BotError as e:
                    bundle = pause_bot_instance_id
                    print('Trying bundle ' + bundle)
                    bundle = bundle.replace('/', '')
                    pause_bot_instance_id = _get_instance_id_from_bundle_id(server, user_key, bundle)
                    if pause_bot_instance_id is None:
                        sys.stderr.write(Color.RED + 'This bot instance is not in your personal account.\n\n' + Color.END)
                        return 1
                    print('Found bot instance ' + Color.BOLD + str(pause_bot_instance_id) + Color.END + ' matching the bundle ID you provided')
                else:
                    result = _botstore_configure(server, user_key, pause_bot_instance_id, None, STATUS_BOT_INACTIVE, location_id)
                    if result:
                        print(the_bot() + 'Paused!')
                        return 0

                print('Something went wrong during configuration.')
                return 1
            if play_bot_instance_id:
                if user_key is None:
                    user_key = _login(server, username, password)
                try:
                    current_app_configuration = _botstore_mybots(server, user_key, play_bot_instance_id, location_id=location_id, organization_id=organization_id)
                except Exception as e:
                    bundle = play_bot_instance_id
                    print('Trying bundle ' + play_bot_instance_id)
                    bundle = bundle.replace('/', '')
                    play_bot_instance_id = _get_instance_id_from_bundle_id(server, user_key, bundle, location_id=location_id)
                    if play_bot_instance_id is None:
                        sys.stderr.write(Color.RED + 'This bot instance is not in your personal account.\n\n' + Color.END)
                        return 1
                    print('Found bot instance ' + Color.BOLD + str(play_bot_instance_id) + Color.END + ' matching the bundle ID you provided')
                else:
                    result = _botstore_configure(server, user_key, play_bot_instance_id, None, STATUS_BOT_ACTIVE, location_id)
                    if result:
                        print(the_bot() + 'Resuming execution!')
                        return 0

                print('Something went wrong during configuration.')
                return 1
            if delete_bot_instance_id:
                if user_key is None:
                    user_key = _login(server, username, password)
                if _botstore_deletebot(server, user_key, delete_bot_instance_id, location_id):
                    print(the_bot() + 'Bot instance ' + str(delete_bot_instance_id) + ' deleted!')
                else:
                    delete_bot_instance_id = delete_bot_instance_id.replace('/', '')
                    delete_bot_instance_id = _get_instance_id_from_bundle_id(server, user_key, delete_bot_instance_id, location_id=location_id)
                    print('Found bot instance ' + Color.BOLD + str(delete_bot_instance_id) + Color.END + ' matching the bundle ID you provided')
                    if _botstore_deletebot(server, user_key, delete_bot_instance_id, location_id):
                        print(the_bot() + 'Bot instance ' + str(delete_bot_instance_id) + ' deleted!')
                    else:
                        print(Color.RED + 'That bot instance is not in your account.' + Color.END)
                sys.stderr.write('\n\n')
                return 0
            if args.questions_bot_instance_id:
                if user_key is None:
                    user_key = _login(server, username, password)
                instance_id = None
                try:
                    instance_id = int(args.questions_bot_instance_id)
                except:
                    bundle = args.questions_bot_instance_id
                    print('Trying bundle ' + bundle)
                    bundle = bundle.replace('/', '')
                    instance_id = _get_instance_id_from_bundle_id(server, user_key, bundle, location_id=location_id)
                    if instance_id is None:
                        sys.stderr.write(Color.RED + 'This bot instance is not in your personal account.\n\n' + Color.END)
                        return 1
                    print('Found bot instance ' + Color.BOLD + str(instance_id) + Color.END + ' matching the bundle ID you provided')

                all_questions = False
                while True:
                    if all_questions:
                        response = _get_questions(server, user_key, answer_status=(1,
                                                                                   2,
                                                                                   3,
                                                                                   4), location_id=location_id)
                    else:
                        response = _get_questions(server, user_key, instance_id=instance_id, answer_status=(1,
                                                                                                            2,
                                                                                                            3,
                                                                                                            4), location_id=location_id)
                    if 'questions' not in response:
                        sys.stderr.write(Color.RED + '\n\nThis bot has asked no questions.' + Color.END)
                    print('QUESTIONS: ' + str(json.dumps(response, indent=2, sort_keys=True)))
                    questions = []
                    if 'questions' in response:
                        questions = response['questions']
                    front_page_questions = []
                    editable_questions = {}
                    questions_by_id = {}
                    question_id = 0
                    for q in questions:
                        if q['front']:
                            front_page_questions.append(q)
                            questions_by_id[question_id] = q
                            question_id += 1
                        if q['editable']:
                            if q['sectionId'] not in editable_questions:
                                editable_questions[q['sectionId']] = []
                            editable_questions[q['sectionId']].append(q)

                    for section_id in sorted(editable_questions.iterkeys()):
                        editable_questions[section_id].sort(key=lambda x: x['questionWeight'], reverse=False)
                        if 'sectionTitle' in editable_questions[section_id][0]:
                            print('\n' + Color.BOLD + editable_questions[section_id][0]['sectionTitle'] + Color.END)
                        for q in editable_questions[section_id]:
                            print('[' + Color.GREEN + str(question_id) + Color.END + '] : ' + q['question'])
                            questions_by_id[question_id] = q
                            question_id += 1

                    print('\n\n' + Color.BOLD + 'Settings' + Color.END)
                    if all_questions:
                        print('[' + Color.PURPLE + 'B' + Color.END + '] : Show only the questions for the bot instance you selected.')
                    else:
                        print('[' + Color.PURPLE + 'A' + Color.END + '] : Show all questions, not filtered by a bot instance.')
                    print('[' + Color.PURPLE + 'Enter' + Color.END + '] : Exit.')
                    choice = raw_input('\nSelect a question ID to answer (ENTER to quit): ')
                    if choice == '':
                        print()
                        exit(0)
                    if choice.lower() == 'a':
                        all_questions = True
                        continue
                    elif choice.lower() == 'b':
                        all_questions = False
                        continue
                    try:
                        choice = int(choice)
                    except:
                        print(Color.RED + 'Please type a number.' + Color.END)
                        continue
                    else:
                        _print_question(questions_by_id[choice])
                        answer = raw_input('\nYour answer (ENTER to skip): ')
                        if answer == '':
                            print()
                            continue
                        else:
                            _answer_question(server, user_key, questions_by_id[choice], answer, location_id)

                return
            if commit:
                import shutil
                if len(commit.split('.')) != 3:
                    sys.stderr.write(Color.RED + "Your new bot name must conform to reverse domain-name notation, as in 'com.yourname.BotName'" + Color.END)
                    sys.stderr.write('\n\n')
                    return 1
                bundle = commit.replace('/', '')
                base_path = os.path.join(os.getcwd(), '.precommit_' + bundle)
                temporary_bot_directory = None
                _merge_redirects(os.path.join(os.getcwd(), commit), base_path)
                if user_key is None:
                    user_key = _login(server, username, password)
                marketing_file = os.path.join(base_path, 'marketing.json')
                version_file = os.path.join(base_path, 'runtime.json')
                if not os.path.exists(marketing_file):
                    sys.stderr.write(marketing_file + ' does not exist')
                    sys.stderr.write('\n\n')
                    if os.path.isdir(base_path):
                        shutil.rmtree(base_path, ignore_errors=True)
                    return 1
                if not os.path.exists(version_file):
                    sys.stderr.write(version_file + ' does not exist')
                    sys.stderr.write('\n\n')
                    if os.path.isdir(base_path):
                        shutil.rmtree(base_path, ignore_errors=True)
                    return 1
                marketing_text = ''
                with open(marketing_file) as (f):
                    for line in f:
                        line = line.strip()
                        if not line.startswith('#'):
                            marketing_text += line

                version_text = ''
                with open(version_file) as (f):
                    for line in f:
                        line = line.strip()
                        if not line.startswith('#'):
                            version_text += line

                try:
                    marketing_data = json.loads(marketing_text)
                except:
                    sys.stderr.write(Color.RED + "Your 'marketing.json' file isn't fully JSON-compliant.\n" + Color.END)
                    sys.stderr.write(Color.RED + 'Make sure all quotations are closed, and that your commas are not too many or too few.\n' + Color.END)
                    sys.stderr.write(Color.RED + 'How about taking it over to a JSON validator, like http://jsonlint.com or https://jsonformatter.curiousconcept.com\n\n' + Color.END)
                    if os.path.isdir(base_path):
                        shutil.rmtree(base_path, ignore_errors=True)
                    return 1
                else:
                    try:
                        version_data = json.loads(version_text)
                    except:
                        sys.stderr.write(Color.RED + "Your 'runtime.json' file isn't fully JSON-compliant.\n" + Color.END)
                        sys.stderr.write(Color.RED + 'Make sure all quotations are closed, and that your commas are not too many or too few.\n' + Color.END)
                        sys.stderr.write(Color.RED + 'How about taking it over to a JSON validator, like http://jsonlint.com or https://jsonformatter.curiousconcept.com' + Color.END)
                        if os.path.isdir(base_path):
                            shutil.rmtree(base_path, ignore_errors=True)
                        return 1

                bot_path = None
                try:
                    _bot_filename = '_bot_' + bundle
                    print('Uploading the marketing file...')
                    _create_or_update_app(server, user_key, bundle, marketing_data)
                    organizational_bot = False
                    if 'organizational' in marketing_data['app']:
                        organizational_bot = marketing_data['app']['organizational'] == 1
                    if 'version' not in version_data:
                        print("Your runtime.json file is missing a 'version' element. That's bizarre. Please fix it.")
                        if os.path.isdir(base_path):
                            shutil.rmtree(base_path, ignore_errors=True)
                        return -1
                    if 'runtime' not in version_data['version']:
                        version_data['version']['runtime'] = 1
                    print('Uploading the runtime configuration...')
                    _update_latest_version(server, user_key, bundle, version_data)
                    print('Generating the bot...')
                    aws_lambda = version_data['version']['runtime'] == 1
                    temporary_bot_directory = '.' + os.sep + '.bot_' + bundle
                    bot_subdirectory = ''
                    if not aws_lambda:
                        bot_subdirectory = os.sep + 'content'
                    if os.path.isdir(temporary_bot_directory):
                        shutil.rmtree(temporary_bot_directory, ignore_errors=True)
                    ignore_list = [
                     '.botignore', '.DS_Store', 'icon.png', '.redirect']
                    botignore_file = base_path + os.sep + '.botignore'
                    if os.path.isfile(botignore_file):
                        with open(botignore_file) as (f):
                            for line in f:
                                if not line.startswith('#') and line.strip() != '':
                                    ignore_list.append(line.strip())

                    print('Ignoring files (add more in your .botignore file): \n' + str(ignore_list))
                    shutil.copytree(base_path, temporary_bot_directory + bot_subdirectory, ignore=shutil.ignore_patterns(*ignore_list))
                    if aws_lambda:
                        import pip
                        pip_install = ['dill', 'requests', 'python-dateutil', 'tzlocal']
                        pip_install = list(set(pip_install) | set(_extract_packages(temporary_bot_directory + bot_subdirectory, True)))
                        pip_install_remotely = _extract_packages(temporary_bot_directory + bot_subdirectory, False)
                        print('Locally installed packages: ' + str(pip_install))
                        print('Remotely installed packages: ' + str(pip_install_remotely))
                        import subprocess
                        command_line = [
                         sys.executable, '-m', 'pip', 'install']
                        command_line.extend(pip_install)
                        command_line.extend(['-t', temporary_bot_directory])
                        reqs = subprocess.check_output(command_line)
                    if os.path.exists('botengine'):
                        with open('botengine', 'r') as (f):
                            first_line = f.readline()
                            if first_line.strip() == '#!/usr/bin/env python':
                                if os.path.exists('botengine_bytecode'):
                                    os.remove('botengine_bytecode')
                                import py_compile
                                py_compile.compile('botengine', 'botengine_bytecode')
                    if aws_lambda:
                        if os.path.exists('.' + os.sep + 'botengine_bytecode'):
                            shutil.copyfile('.' + os.sep + 'botengine_bytecode', temporary_bot_directory + os.sep + 'botengine.pyc')
                        if os.path.exists('.' + os.sep + 'lambda.py'):
                            shutil.copyfile('.' + os.sep + 'lambda.py', temporary_bot_directory + os.sep + 'lambda.py')
                    elif os.path.exists('.' + os.sep + 'botengine'):
                        shutil.copyfile('.' + os.sep + 'botengine', temporary_bot_directory + os.sep + 'botengine')
                    else:
                        if os.path.exists('.' + os.sep + 'botengine_bytecode'):
                            shutil.copyfile('.' + os.sep + 'botengine_bytecode', temporary_bot_directory + os.sep + 'botengine_bytecode')

                    if TAR:
                        shutil.make_archive(_bot_filename, 'tar', temporary_bot_directory)
                        size = os.path.getsize(_bot_filename + '.tar')
                    else:
                        shutil.make_archive(_bot_filename, 'zip', temporary_bot_directory)
                        size = os.path.getsize(_bot_filename + '.zip')
                    print('Uploading the bot [' + str(size / 1000000) + 'MB]...')
                    response = _upload_bot(server, user_key, bundle, _bot_filename, TAR)
                    icon_path = os.path.join(base_path, 'icon.png')
                    if os.path.exists(icon_path):
                        print('Uploading the icon...')
                        _upload_icon(server, user_key, bundle, icon_path)
                    else:
                        print('Missing the icon...')
                    if TAR:
                        if 'requestId' not in response:
                            sys.stderr.write(Color.RED + 'This bot was not uploaded properly.\n' + Color.END)
                            sys.stderr.write(Color.RED + 'The response from the server was : ' + json.dumps(response, indent=2, sort_keys=True) + '\n\n' + Color.END)
                            return -1
                        sys.stdout.write('Processing the bot at the server...')
                        sys.stdout.flush()
                        while True:
                            status = _check_bot_processing(server, user_key, response['requestId'])
                            if 'resultCode' in status['result']:
                                if status['result']['resultCode'] == 0:
                                    break
                                elif 'resultCodeMessage' in status['result']:
                                    sys.stderr.write(Color.RED + '\n\n' + status['result']['resultCodeMessage'] + '\n' + Color.END)
                                    return -1
                                else:
                                    sys.stderr.write(Color.RED + '\n\nThis bot was not processed properly at the server.\n' + Color.END)
                                    sys.stderr.write(json.dumps(status, indent=2, sort_keys=True))
                                    return -1

                            sys.stdout.write('.')
                            sys.stdout.flush()
                            time.sleep(1)

                        sys.stdout.write('\n')
                        sys.stdout.flush()
                except BotError as e:
                    sys.stderr.write('BotEngine Error: ' + e.msg)
                    sys.stderr.write('\n\n')
                    if os.path.isdir(base_path):
                        shutil.rmtree(base_path, ignore_errors=True)
                    return 2
                finally:
                    if bot_path:
                        os.remove(bot_path)
                    if temporary_bot_directory is not None:
                        if os.path.isdir(temporary_bot_directory):
                            shutil.rmtree(temporary_bot_directory, ignore_errors=True)
                    if base_path is not None:
                        if os.path.isdir(base_path):
                            shutil.rmtree(base_path, ignore_errors=True)
                    if os.path.exists(_bot_filename + '.tar'):
                        os.remove(_bot_filename + '.tar')

                if make_it_so is None:
                    bots = _botstore_mybots(server, user_key, location_id=location_id, organization_id=organization_id)
                    if bots is not None:
                        for bot in bots:
                            if bot['bundle'] == bundle:
                                print(the_bot() + 'Done!')
                                return 0

                    purchase_bundle_id = bundle
                    choice = 'n'
                    if not organizational_bot:
                        choice = raw_input('Purchase this bot into your personal account (y/n)? ')
                    if choice.lower() != 'y':
                        print(the_bot() + 'Done!\n')
                        return 0
            if purchase_bundle_id:
                if user_key is None:
                    user_key = _login(server, username, password)
                purchase_bundle_id = purchase_bundle_id.replace('/', '')
                bot_instance_id = _botstore_purchasebot(server, user_key, purchase_bundle_id, location_id=location_id, organization_id=organization_id)
                print(the_bot() + Color.BOLD + 'Purchased bot instance ID: ' + Color.GREEN + str(bot_instance_id) + Color.END + '\n')
                configure_bot_instance_id = bot_instance_id
                return 0
            if configure_bot_instance_id:
                if user_key is None:
                    user_key = _login(server, username, password)
                user_info = _get_user_info(server, user_key)
                bundle = ''
                try:
                    full_configuration = _botstore_mybots(server, user_key, configure_bot_instance_id, location_id=location_id, organization_id=organization_id)
                    current_app_configuration = full_configuration[0]
                    bundle = current_app_configuration['bundle']
                    new_app_configuration = get_editable_bot_configuration(current_app_configuration)
                except Exception:
                    bundle = configure_bot_instance_id
                    bundle = bundle.replace('/', '')
                    configure_bot_instance_id = _get_instance_id_from_bundle_id(server, user_key, bundle, location_id=location_id)
                    if configure_bot_instance_id is None:
                        sys.stderr.write(Color.RED + 'This bot instance is not in your personal account.\n\n' + Color.END)
                        return 1
                    print('Found bot instance ' + Color.BOLD + str(configure_bot_instance_id) + Color.END + ' matching the bundle ID you provided')
                    full_configuration = _botstore_mybots(server, user_key, configure_bot_instance_id, location_id=location_id, organization_id=organization_id)
                    current_app_configuration = full_configuration[0]
                    new_app_configuration = get_editable_bot_configuration(current_app_configuration)
                else:
                    general_app_info = _botstore_botinfo(server, user_key, bundle)
                    devices = _get_devices_from_location(server, user_key, location_id)
                    is_organizational_app = False
                    if 'organizational' in general_app_info:
                        is_organizational_app = general_app_info['organizational'] == 1
                    print(Color.BOLD + '\n\nNICKNAME' + Color.END)
                    try:
                        nickname = current_app_configuration['nickname']
                    except:
                        nickname = None
                    else:
                        if not nickname:
                            try:
                                nickname = current_app_configuration['name']
                            except:
                                nickname = None

                        print("The bot's current nickname in your account is '" + Color.BOLD + str(nickname) + Color.END + "'.")
                        new_nickname = raw_input(Color.GREEN + 'Change the nickname, or press enter to keep the current nickname: ' + Color.END)
                        if new_nickname:
                            nickname = new_nickname
                        new_app_configuration['app']['nickname'] = nickname
                        from tzlocal import get_localzone
                        new_timezone = str(get_localzone())
                        try:
                            original_timezone = new_app_configuration['app']['timezone']
                        except:
                            original_timezone = None
                        else:
                            if original_timezone:
                                print(Color.BOLD + '\n\nTIMEZONE' + Color.END)
                                print("The bot's current timezone is '" + Color.BOLD + original_timezone + Color.END + "'.")
                                change_timezone = raw_input(Color.GREEN + "Update it to '" + Color.BOLD + new_timezone + Color.END + "'? (y/n): " + Color.END)
                                if change_timezone:
                                    if change_timezone.lower() != 'y':
                                        new_timezone = original_timezone
                            new_app_configuration['app']['timezone'] = new_timezone
                            print(Color.BOLD + '\n\nMODE AND FILE PERMISSIONS' + Color.END)
                            try:
                                access_block = general_app_info['access']
                            except:
                                access_block = None

                            new_access_block = []
                            if access_block:
                                for access in access_block:
                                    if access['category'] == 1:
                                        for location in user_info['locations']:
                                            print("At your '" + Color.BOLD + location['name'] + Color.END + "' location:")
                                            print('This bot wants access to your modes')
                                            for r in access['reason']:
                                                print('\t' + r + ': ' + access['reason'][r])

                                            ok = raw_input(Color.GREEN + "\tEnter to accept, 'n' to opt-out: " + Color.END)
                                            print('')
                                            configured_access_block = {}
                                            if ok and ok.lower() != 'y':
                                                pass
                                            else:
                                                configured_access_block['category'] = access['category']
                                                configured_access_block['locationId'] = location['id']
                                                configured_access_block['trigger'] = access['trigger']
                                                configured_access_block['read'] = access['read']
                                                configured_access_block['control'] = access['control']
                                                new_access_block.append(configured_access_block)

                                    elif access['category'] == 2:
                                        print('This bot wants to access your ' + Color.BOLD + 'Media Files' + Color.END + '.')
                                        for r in access['reason']:
                                            print('\t' + r + ': ' + access['reason'][r])

                                        ok = raw_input(Color.GREEN + "\tEnter to accept, 'n' to opt-out: " + Color.END)
                                        print('')
                                        configured_access_block = {}
                                        if ok and ok.lower() != 'y':
                                            pass
                                        else:
                                            configured_access_block['category'] = access['category']
                                            configured_access_block['trigger'] = access['trigger']
                                            configured_access_block['read'] = access['read']
                                            configured_access_block['control'] = access['control']
                                            new_access_block.append(configured_access_block)
                                            continue
                                            if access['category'] == 3:
                                                print('This bot wants to access your ' + Color.BOLD + 'Professional Monitoring Services' + Color.END + '.')
                                                for r in access['reason']:
                                                    print('\t' + r + ': ' + access['reason'][r])

                                                ok = raw_input(Color.GREEN + "\tEnter to accept, 'n' to opt-out: " + Color.END)
                                                print('')
                                                configured_access_block = {}
                                                if ok and ok.lower() != 'y':
                                                    pass
                                                else:
                                                    configured_access_block['category'] = access['category']
                                                    configured_access_block['trigger'] = access['trigger']
                                                    configured_access_block['read'] = access['read']
                                                    configured_access_block['control'] = access['control']
                                                    new_access_block.append(configured_access_block)
                                            elif access['category'] == 5:
                                                print('This bot wants to access your ' + Color.BOLD + 'Challenges' + Color.END + '.')
                                                for r in access['reason']:
                                                    print('\t' + r + ': ' + access['reason'][r])

                                                ok = raw_input(Color.GREEN + "\tEnter to accept, 'n' to opt-out: " + Color.END)
                                                print('')
                                                configured_access_block = {}
                                                if ok and ok.lower() != 'y':
                                                    pass
                                                else:
                                                    configured_access_block['category'] = access['category']
                                                    configured_access_block['trigger'] = access['trigger']
                                                    configured_access_block['read'] = access['read']
                                                    configured_access_block['control'] = access['control']
                                                    new_access_block.append(configured_access_block)
                                            elif access['category'] == 6:
                                                print('This bot wants to access your ' + Color.BOLD + 'Rules' + Color.END + '.')
                                                for r in access['reason']:
                                                    print('\t' + r + ': ' + access['reason'][r])

                                                ok = raw_input(Color.GREEN + "\tEnter to accept, 'n' to opt-out: " + Color.END)
                                                print('')
                                                configured_access_block = {}
                                                if ok and ok.lower() != 'y':
                                                    pass
                                                else:
                                                    configured_access_block['category'] = access['category']
                                                    configured_access_block['trigger'] = access['trigger']
                                                    configured_access_block['read'] = access['read']
                                                    configured_access_block['control'] = access['control']
                                                    new_access_block.append(configured_access_block)
                                            continue

                            try:
                                devices_block = general_app_info['deviceTypes']
                            except:
                                devices_block = None

                        if devices_block and not is_organizational_app:
                            print(Color.BOLD + '\n\nDEVICE PERMISSIONS' + Color.END)
                            for device_block in devices_block:
                                for focused_device in devices:
                                    if focused_device['type'] == device_block['id']:
                                        print("This bot wants to access your '" + Color.BOLD + focused_device['desc'].encode('utf-8') + Color.END + "'.")
                                        for r in device_block['reason']:
                                            print('\t' + r + ': ' + device_block['reason'][r])

                                        ok = raw_input(Color.GREEN + "\tEnter to accept, 'n' to opt-out: " + Color.END)
                                        print('')
                                        configured_access_block = {}
                                        configured_access_block['category'] = 4
                                        configured_access_block['deviceId'] = focused_device['id']
                                        if ok and ok.lower() != 'y':
                                            configured_access_block['excluded'] = True
                                        else:
                                            configured_access_block['excluded'] = False
                                        new_access_block.append(configured_access_block)

                        try:
                            communications_block = general_app_info['communications']
                        except:
                            communications_block = None

                    new_communications_block = []
                    if communications_block:
                        print(Color.BOLD + '\n\nCOMMUNICATION PERMISSIONS' + Color.END)
                        for comm in communications_block:
                            destinations = []
                            if comm['email']:
                                destinations.append('email')
                            if comm['msg']:
                                destinations.append('in-bot messages')
                            if comm['push']:
                                destinations.append('push notifications')
                            if comm['sms']:
                                destinations.append('sms')
                            phrase = ''
                            i = 0
                            for m in destinations:
                                i = i + 1
                                if len(destinations) > 1:
                                    if i == len(destinations):
                                        phrase = phrase + 'and ' + m
                                    if i < len(destinations):
                                        phrase = phrase + m + ', '
                                else:
                                    phrase = m

                            if comm['category'] == 0:
                                print(Color.GREEN + 'This bot wants to send' + Color.BOLD + ' you ' + Color.END + Color.GREEN + phrase + ". Enter to accept, 'n' to opt-out: " + Color.END)
                                ok = raw_input('> ')
                            elif comm['category'] == 1:
                                print(Color.GREEN + 'This bot wants to send' + Color.BOLD + ' your friends ' + Color.END + Color.GREEN + phrase + ". Enter to accept, 'n' to opt-out: " + Color.END)
                                ok = raw_input('> ')
                            elif comm['category'] == 2:
                                print(Color.GREEN + 'This bot wants to send' + Color.BOLD + ' your family ' + Color.END + Color.GREEN + phrase + ". Enter to accept, 'n' to opt-out: " + Color.END)
                                ok = raw_input('> ')
                            elif comm['category'] == 3:
                                print(Color.GREEN + 'This bot wants to send' + Color.BOLD + ' your community group ' + Color.END + Color.GREEN + phrase + ". Enter to accept, 'n' to opt-out: " + Color.END)
                                ok = raw_input('> ')
                            elif comm['category'] == 4:
                                print(Color.GREEN + 'This bot wants to send' + Color.BOLD + ' your admins ' + Color.END + Color.GREEN + phrase + ". Enter to accept, 'n' to opt-out: " + Color.END)
                                ok = raw_input('> ')
                            if ok:
                                if ok.lower() != 'y':
                                    continue
                            configured_comms_block = {}
                            configured_comms_block['category'] = comm['category']
                            configured_comms_block['email'] = comm['email']
                            configured_comms_block['push'] = comm['push']
                            configured_comms_block['sms'] = comm['sms']
                            configured_comms_block['msg'] = comm['msg']
                            new_communications_block.append(configured_comms_block)

                    new_app_configuration['app']['access'] = new_access_block
                    new_app_configuration['app']['communications'] = new_communications_block
                    new_app_configuration['app']['status'] = STATUS_BOT_ACTIVE
                    status = STATUS_BOT_ACTIVE
                    result = _botstore_configure(server, user_key, configure_bot_instance_id, new_app_configuration, status, location_id)
                    if result:
                        print(the_bot() + 'Configured!')
                        return 0

                print('Something went wrong during configuration.')
                return 1
            if permissions_bot_instance_id:
                if user_key is None:
                    user_key = _login(server, username, password)
                bundle = ''
                try:
                    full_configuration = _botstore_mybots(server, user_key, permissions_bot_instance_id, location_id=location_id, organization_id=organization_id)
                    current_app_configuration = full_configuration[0]
                    bundle = current_app_configuration['bundle']
                    new_app_configuration = get_editable_bot_configuration(current_app_configuration)
                except Exception:
                    bundle = permissions_bot_instance_id
                    bundle = bundle.replace('/', '')
                    permissions_bot_instance_id = _get_instance_id_from_bundle_id(server, user_key, bundle, location_id=location_id)
                    if permissions_bot_instance_id is None:
                        sys.stderr.write(Color.RED + 'This bot instance is not in your personal account.\n\n' + Color.END)
                        return 1
                    print('Found bot instance ' + Color.BOLD + str(permissions_bot_instance_id) + Color.END + ' matching the bundle ID you provided')
                    full_configuration = _botstore_mybots(server, user_key, permissions_bot_instance_id, location_id=location_id, organization_id=organization_id)
                    current_app_configuration = full_configuration[0]
                    new_app_configuration = get_editable_bot_configuration(current_app_configuration)

                devices = _get_devices_from_location(server, user_key, location_id)
                print(Color.BOLD + '\nLOCATIONS' + Color.END)
                found = False
                for access in current_app_configuration['access']:
                    if access['category'] == 1:
                        found = True
                        permissions = ''
                        if access['read']:
                            permissions += Color.GREEN + 'r' + Color.END
                        else:
                            permissions += Color.RED + '-' + Color.END
                        if access['control']:
                            permissions += Color.GREEN + 'w' + Color.END
                        else:
                            permissions += Color.RED + '-' + Color.END
                        if access['trigger']:
                            permissions += Color.GREEN + 'x' + Color.END
                        else:
                            permissions += Color.RED + '-' + Color.END
                        print(permissions + ' Location ' + str(access['locationId']))

                if not found:
                    print(Color.RED + '---' + Color.END + ' This bot cannot access any of your Locations or modes' + Color.END)
                print(Color.BOLD + '\nPROFESSIONAL MONITORING' + Color.END)
                found = False
                for access in current_app_configuration['access']:
                    if access['category'] == 3:
                        found = True
                        permissions = ''
                        if access['read']:
                            permissions += Color.GREEN + 'r' + Color.END
                        else:
                            permissions += Color.RED + '-' + Color.END
                        if access['control']:
                            permissions += Color.GREEN + 'w' + Color.END
                        else:
                            permissions += Color.RED + '-' + Color.END
                        if access['trigger']:
                            permissions += Color.GREEN + 'x' + Color.END
                        else:
                            permissions += Color.RED + '-' + Color.END
                        print(permissions + ' Professional Monitoring Services')

                if not found:
                    print(Color.RED + '---' + Color.END + ' This bot cannot access professional monitoring services.')
                print(Color.BOLD + '\nDEVICES' + Color.END)
                found = False
                for access in current_app_configuration['access']:
                    if access['category'] == 4:
                        for device in devices:
                            if 'deviceId' in access:
                                if device['id'] == access['deviceId']:
                                    found = True
                                    permissions = ''
                                    if access['read']:
                                        permissions += Color.GREEN + 'r' + Color.END
                                    else:
                                        permissions += Color.RED + '-' + Color.END
                                    if access['control']:
                                        permissions += Color.GREEN + 'w' + Color.END
                                    else:
                                        permissions += Color.RED + '-' + Color.END
                                    if access['trigger']:
                                        permissions += Color.GREEN + 'x' + Color.END
                                    else:
                                        permissions += Color.RED + '-' + Color.END
                                    print((permissions + ' [' + access['deviceId'] + '] ' + device['desc']).encode('utf-8'))

                if not found:
                    print(Color.RED + '---' + Color.END + ' This bot cannot access any of your devices' + Color.END)
                print('\n' + the_bot() + 'Done!')
                return 0
            if update:
                import subprocess
                print("If asked, please provide your computer's password to install an update")
                subprocess.call('curl -s https://raw.githubusercontent.com/peoplepower/botlab/master/installer.sh | sudo /bin/bash', shell=True)
                return 0
            if publish:
                if make_it_so is None and approve is None:
                    are_you_sure = raw_input('Are you sure you want to submit this bot for review to make it public? (y/n): ')
                    if are_you_sure.lower() != 'y':
                        print(the_bot() + 'Ok, aborting.')
                        return 0
                if user_key is None:
                    if username is not None and password is not None:
                        user_key = _login(server, username, password)
                    elif admin_username is None and password is None:
                        user_key = _login(server, username, password)
                bundle = publish.replace('/', '')
                if user_key is not None:
                    _update_version_status(server, user_key, bundle, 2, ignore_errors=True)
                try:
                    if make_it_so is not None or approve is not None:
                        if admin_username is None:
                            admin_username = username
                        if admin_password is None:
                            admin_password = password
                        admin_key = _login(server, admin_username, admin_password, admin=True)
                        print(the_bot() + 'Submitted for review.')
                        _update_version_status(server, admin_key, bundle, 3)
                        print(the_bot() + 'Under review.')
                        _update_version_status(server, admin_key, bundle, 4)
                        print(the_bot() + 'Published. Done!\n')
                        return 0
                except BotError as e:
                    sys.stderr.write('BotEngine Error: ' + e.msg)
                    sys.stderr.write('\n\n')
                    return 2

                print(the_bot() + 'Awaiting review! You can always --reject this version if you need to make updates.')
                return 0
            if reject:
                if user_key is None:
                    user_key = _login(server, username, password)
                bundle = reject.replace('/', '')
                try:
                    _update_version_status(server, user_key, bundle, 6)
                except BotError as e:
                    sys.stderr.write('BotEngine Error: ' + e.msg)
                    sys.stderr.write('\n\n')
                    return 2

                print(the_bot() + 'Developer rejected!')
                return 0
            if add_organization:
                if user_key is None:
                    user_key = _login(server, username, password)
                if organization_id is None:
                    sys.stderr.write('Supply the ID of the organization with --organization\n\n')
                    return 2
                try:
                    _allow_organization_to_purchase_bot(server, user_key, add_organization, organization_id, organization_development_mode)
                except BotError as e:
                    sys.stderr.write('BotEngine Error: ' + e.msg)
                    sys.stderr.write('\n\n')
                    return 2

                print(the_bot() + 'Done!')
                return 0
            if remove_organization:
                if user_key is None:
                    user_key = _login(server, username, password)
                if organization_id is None:
                    sys.stderr.write('Supply the ID of the organization with --organization\n\n')
                    return 2
                try:
                    _prevent_organization_from_purchasing_bot(server, user_key, add_organization, organization_id)
                except BotError as e:
                    sys.stderr.write('BotEngine Error: ' + e.msg)
                    sys.stderr.write('\n\n')
                    return 2

                print(the_bot() + 'Done!')
                return 0
            if download_device_id or download_device_type or download_devices:
                if user_key is None:
                    user_key = _login(server, username, password)
                daysAgo = raw_input('How many days ago to start collecting data: ')
                try:
                    initialization_days = int(daysAgo)
                except:
                    initialization_days = 1
                else:
                    import dateutil.relativedelta
                    start_date = datetime.date.today() + dateutil.relativedelta.relativedelta(days=-initialization_days)
                    if download_device_id:
                        device_name = 'NONAME'
                        device_type = 'NOTYPE'
                        all_devices = _get_devices_from_location(server, user_key, location_id)
                        for device in all_devices:
                            if device['id'] == download_device_id:
                                device_name = str(device['desc'].encode('utf-8'))
                                device_type = str(device['type'])
                                break

                        _downloaded_data_to_csv(server, user_key, start_date, download_device_id, device_type, device_name, location_id=location_id)
                        print(the_bot() + 'Done!')
                        return 0
                    if download_device_type:
                        if organization_id:
                            devices = _get_devices_from_organization(server, user_key, organization_id, download_device_type)
                            for device in devices['devices']:
                                print('Downloading ' + str(device['id'].encode('utf-8')) + " '" + str(device['desc'].encode('utf-8')) + "' from user " + str(device['user']['id']) + ' ...')
                                _downloaded_data_to_csv(server, user_key, start_date, device['id'].encode('utf-8'), download_device_type, str(device['desc'].encode('utf-8')), location_id=location_id, user_id=device['user']['id'])

                        else:
                            devices = _get_devices_from_location(server, user_key, location_id)
                            for device in devices:
                                if int(device['type']) == int(download_device_type):
                                    print('Downloading ' + str(device['id'].encode('utf-8')) + " - '" + str(device['desc'].encode('utf-8')) + "' ...")
                                    _downloaded_data_to_csv(server, user_key, start_date, device['id'].encode('utf-8'), location_id=location_id, device_type=download_device_type, device_name=str(device['desc'].encode('utf-8')))

                        print(the_bot() + ' Done!')
                        return 0
                    if download_devices:
                        print('Downloading all devices')
                        device_name = 'NONAME'
                        device_type = 'NOTYPE'
                        all_devices = _get_devices_from_location(server, user_key, location_id)
                        for device in all_devices:
                            device_name = str(device['desc'].encode('utf-8'))
                            device_type = str(device['type'])
                            print('Downloading ' + device_name + ' ' + device_type)
                            _downloaded_data_to_csv(server, user_key, start_date, device['id'].encode('utf-8'), device_type, device_name, location_id=location_id)

                        print(the_bot() + 'Done!')
                        return 0

            if record:
                if user_key is None:
                    user_key = _login(server, username, password)
                daysAgo = raw_input('How many days ago to record: ')
                try:
                    initialization_days = int(daysAgo)
                except:
                    initialization_days = 1

                destination = raw_input('What directory should we save this into: ')
                if not os.path.exists(destination):
                    os.makedirs(destination)
                if organization_id is not None:
                    org_users = _get_organization_users(server, user_key, organization_id)
                    if len(org_users) == 0:
                        print('This organization has no users.')
                        exit(1)
                    users = []
                    print(('Capturing information on {} users...').format(len(org_users)))
                    iteration = 0
                    for u in org_users:
                        iteration += 1
                        amount_done = float(iteration) / float(len(org_users))
                        sys.stdout.write(('\rProgress: [{0:50s}] {1:.1f}%').format('#' * int(amount_done * 50), amount_done * 100))
                        users += [_get_user_info(server, user_key, u['id'])]

                else:
                    users = [
                     _get_user_info(server, user_key)]
                for user_info in users:
                    location_id = user_info['locations'][0]['id']
                    user_id = user_info['user']['id']
                    destination_directory = destination + os.sep + str(user_id)
                    if not os.path.exists(destination_directory):
                        os.makedirs(destination_directory)
                    filenames = []
                    import dateutil.relativedelta
                    start_date = datetime.date.today() + dateutil.relativedelta.relativedelta(days=-initialization_days)
                    filenames.append(_download_modes_history_to_csv(server, user_key, location_id, start_date, destination_directory=destination_directory))
                    if organization_id is not None:
                        devices = _get_devices_from_organization(server, user_key, organization_id, user_id=user_id)
                    else:
                        devices = _get_devices_from_location(server, user_key, location_id)
                    for device in devices:
                        print('Capturing ' + str(device['id'].encode('utf-8')) + " - '" + str(device['desc'].encode('utf-8')) + "' ...")
                        filenames += _downloaded_data_to_csv(server, user_key, start_date, device['id'].encode('utf-8'), user_id=user_id, location_id=location_id, device_type=device['type'], device_name=str(device['desc'].encode('utf-8')), destination_directory=destination_directory)

                    open_files = {}
                    headers = {}
                    for filename in filenames:
                        headers[filename] = {}
                        open_files[filename] = open(filename)
                        headers[filename]['headers'] = open_files[filename].readline().replace('\n', '').split(',')
                        for header in headers[filename]['headers']:
                            if header != '':
                                headers[filename][header] = None

                        values = open_files[filename].readline().replace('\n', '').split(',')
                        for i in range(0, len(values)):
                            if len(values) != len(headers[filename]['headers']):
                                print('# values != # headers for filename ' + filename)
                                print('values: ' + str(values))
                                print('headers: ' + str(headers[filename]['headers']))
                            headers[filename][headers[filename]['headers'][i]] = values[i]

                    output_filename = destination_directory + os.sep + 'recording_user_' + str(user_info['user']['id']) + '-' + str(initialization_days) + '_days.json'
                    print('Writing ' + output_filename + '...')
                    with open(output_filename, 'w') as (out):
                        out.write('{\n')
                        out.write('"user_info":' + json.dumps(user_info) + ',\n')
                        out.write('"data":[\n')
                        first_entry = True
                        while True:
                            oldest_timestamp_ms = None
                            oldest_filename = None
                            for filename in filenames:
                                if 'timestamp_ms' in headers[filename]:
                                    if headers[filename]['timestamp_ms'] is not None:
                                        if oldest_timestamp_ms is None:
                                            oldest_timestamp_ms = int(headers[filename]['timestamp_ms'])
                                            oldest_filename = filename
                                        elif int(headers[filename]['timestamp_ms']) < oldest_timestamp_ms:
                                            oldest_timestamp_ms = int(headers[filename]['timestamp_ms'])
                                            oldest_filename = filename

                            if oldest_filename is None:
                                break
                            output = headers[oldest_filename].copy()
                            del output['headers']
                            if '' in output:
                                del output['']
                            if first_entry:
                                first_entry = False
                            else:
                                out.write(',\n')
                            out.write(str(json.dumps(output)))
                            values = open_files[oldest_filename].readline().replace('\n', '').split(',')
                            headers[oldest_filename]['timestamp_ms'] = None
                            for i in range(0, len(values)):
                                headers[oldest_filename][headers[oldest_filename]['headers'][i]] = values[i]

                        out.write('\n]}\n')
                    for file in open_files:
                        open_files[file].close()

                print(the_bot() + ' Done!')
                return 0
            if playback:
                try:
                    os.remove('playback.txt')
                except:
                    pass

                recording = json.load(open(playback))
                print('Loaded ' + str(len(recording['data'])) + ' records from ' + playback)
                raw_access_content = {}
                user_info = recording['user_info']
                playback_user_info = user_info
                location_id = user_info['locations'][0]['id']
                location_timezone = user_info['locations'][0]['timezone']
                location_name = user_info['locations'][0]['name']
                location_zip = None
                location_lat = None
                location_long = None
                if 'zip' in user_info['locations'][0]:
                    location_zip = user_info['locations'][0]['zip']
                if 'latitude' in user_info['locations'][0]:
                    location_lat = user_info['locations'][0]['latitude']
                if 'longitude' in user_info['locations'][0]:
                    location_long = user_info['locations'][0]['longitude']
                base_path = os.path.join(os.getcwd(), '.' + botname)
                _merge_redirects(os.path.join(os.getcwd(), botname), base_path)
                sys.path.insert(0, base_path)
                bot = importlib.import_module('bot')
                runtime_text = ''
                with open(os.path.join(base_path, 'runtime.json')) as (f):
                    for line in f:
                        line = line.strip()
                        if not line.startswith('#'):
                            runtime_text += line

                runtime = json.loads(runtime_text)['version']
                if runtime['trigger'] & 2 != 0:
                    raw_access_content['location'] = {'category': 1, 
                       'control': True, 
                       'location': {'event': 'HOME', 
                                    'latitude': location_lat, 
                                    'locationId': location_id, 
                                    'longitude': location_long, 
                                    'name': location_name, 
                                    'timezone': location_timezone, 
                                    'zip': location_zip}, 
                       'read': True, 
                       'trigger': False}
                device_type_triggers = []
                device_id_params = {}
                for device in runtime['deviceTypes']:
                    device_type_triggers.append(device['id'])

                botengine = BotEngine({'apiKey': None, 'apiHosts': []})
                botengine._download_binary_variable = playback_download_binary_variable
                botengine.flush_binary_variables = playback_flush_binary_variables
                botengine.flush_commands = playback_flush_commands
                botengine.flush_questions = playback_flush_questions
                botengine.flush_rules = playback_flush_rules
                botengine.flush_tags = playback_flush_tags
                botengine.delete_all_rules = playback_delete_all_rules
                botengine.get_user_info = playback_get_user_info
                botengine._execute_again_at_timestamp = playback_execute_again_at_timestamp
                botengine.notify = playback_notify
                botengine.set_mode = playback_set_mode
                botengine.cancel_timers = playback_cancel_timers
                if 'run' in dir(bot):
                    for d in recording['data']:
                        inputs = {}
                        inputs['access'] = []
                        trigger = int(d['trigger'])
                        timestamp = int(d['timestamp_ms'])
                        if 'location' in raw_access_content:
                            if 'prevEvent' in raw_access_content['location']:
                                del raw_access_content['location']['prevEvent']
                        for access_id in raw_access_content:
                            raw_access_content[access_id]['trigger'] = False

                        if trigger == 2:
                            if 'location' in raw_access_content:
                                raw_access_content['location']['location']['prevEvent'] = raw_access_content['location']['location']['event']
                                raw_access_content['location']['location']['event'] = d['event']
                                raw_access_content['location']['trigger'] = True
                            else:
                                continue
                        elif trigger == 8:
                            if int(d['device_type']) in device_type_triggers:
                                raw_access_content[d['device_id']] = {'category': 4, 'control': False, 
                                   'device': {'connected': True, 
                                              'description': d['description'], 
                                              'deviceId': d['device_id'], 
                                              'deviceType': int(d['device_type']), 
                                              'locationId': int(location_id), 
                                              'measureDate': timestamp, 
                                              'startDate': 0, 
                                              'updateDate': timestamp}, 
                                   'read': True, 
                                   'trigger': True}
                                if d['device_id'] not in device_id_params:
                                    device_id_params[d['device_id']] = {}
                                inputs['measures'] = []
                                for parameter in d:
                                    measure = {'deviceId': d['device_id'], 
                                       'name': parameter}
                                    if parameter in device_id_params[d['device_id']]:
                                        measure['prevTime'] = device_id_params[d['device_id']][parameter]['time']
                                        measure['prevValue'] = device_id_params[d['device_id']][parameter]['value']
                                        measure['updated'] = d[parameter] != measure['prevValue']
                                    else:
                                        measure['updated'] = True
                                    measure['time'] = timestamp
                                    measure['value'] = d[parameter]
                                    device_id_params[d['device_id']][parameter] = measure
                                    inputs['measures'].append(measure)

                            else:
                                continue
                        for access_id in raw_access_content:
                            inputs['access'].append(raw_access_content[access_id])

                        inputs['time'] = timestamp
                        inputs['trigger'] = trigger
                        inputs['userId'] = user_info['user']['id']
                        while playback_timer_timestamp is not None and playback_timer_timestamp < timestamp:
                            timer_inputs = {}
                            timer_inputs['time'] = playback_timer_timestamp
                            timer_inputs['trigger'] = 64
                            timer_inputs['userId'] = user_info['user']['id']
                            timer_inputs['access'] = []
                            for access_id in raw_access_content:
                                timer_inputs['access'].append(raw_access_content[access_id])

                            playback_current_timestamp = playback_timer_timestamp
                            playback_timer_timestamp = None
                            _run(bot, {'inputs': [timer_inputs]}, _bot_logger, botengine_override=botengine)
                            playback_variables = botengine.variables

                        playback_current_timestamp = timestamp
                        _run(bot, {'inputs': [inputs]}, _bot_logger, botengine_override=botengine)
                        playback_variables = botengine.variables

                print(the_bot() + ' Done!')
                return 0
            if generate:
                botname = generate.replace('/', '')
                base_path = os.path.join(os.getcwd(), '.' + botname)
                _merge_redirects(os.path.join(os.getcwd(), botname), base_path)
                print(('Bot generated in directory: {}').format(os.path.join(os.getcwd(), base_path)))
                print(the_bot() + ' Done!')
                return 0
            if not botname and not instance:
                sys.stderr.write('No bot selected to run, use --help\n')
                if _servermode:
                    _bot_logger.error('No bot selected to run\n\n')
                return 1
            if botname or instance:
                if botname:
                    botname = botname.replace('/', '')
                if botname is not None and organization_id is not None and instance is None:
                    sys.stderr.write(Color.RED + 'Missing the bot instance ID.\n' + Color.END)
                    sys.stderr.write(Color.RED + 'To run a bot under an organization:  -r <bot_bundle_id> -o <organization_id> -i <bot_instance_id>' + Color.END)
                    sys.stderr.write('\n\n')
                    return 1
                if not botengine_key:
                    if user_key is None:
                        user_key = _login(server, username, password)
                    try:
                        if not instance:
                            instance = _get_instance_id_from_bundle_id(server, user_key, botname, challenge_id, location_id=location_id)
                            if instance is None:
                                sys.stderr.write(Color.RED + 'You must first purchase and configure a bot in your account before you can run it.' + Color.END)
                                sys.stderr.write('\n\n')
                                return 1
                    except BotError as e:
                        sys.stderr.write('BotEngine Error: ' + e.msg)
                        sys.stderr.write('\n\n')
                        return 2

                base_path = os.path.join(os.getcwd(), '.' + botname)
                _merge_redirects(os.path.join(os.getcwd(), botname), base_path)
                if os.path.exists('botengine'):
                    with open('botengine', 'r') as (f):
                        first_line = f.readline()
                        if first_line.strip() == '#!/usr/bin/env python':
                            if os.path.exists('botengine_bytecode'):
                                os.remove('botengine_bytecode')
                            import py_compile
                            py_compile.compile('botengine', 'botengine_bytecode')
                import shutil
                if os.path.exists('.' + os.sep + 'botengine_bytecode'):
                    shutil.copyfile('.' + os.sep + 'botengine_bytecode', base_path + os.sep + 'botengine.pyc')
                if os.path.exists('.' + os.sep + 'lambda.py'):
                    shutil.copyfile('.' + os.sep + 'lambda.py', base_path + os.sep + 'lambda.py')
                sys.path.insert(0, base_path)
                bot = importlib.import_module('bot')
                if 'run' in dir(bot):
                    if forever:
                        version_file = os.path.join(base_path, 'runtime.json')
                        if not os.path.exists(version_file):
                            sys.stderr.write(Color.RED + version_file + ' does not exist' + Color.END)
                            sys.stderr.write(Color.RED + "You must run the BotEngine a level below your bot's directory" + Color.END)
                            sys.stderr.write('\n\n')
                            return 1
                        if not device_server:
                            device_server = _get_ensemble_server_url(server)
                        if 'http' not in device_server:
                            device_server = 'https://' + device_server
                        device_server = device_server.replace('sbox2', 'sbox1').replace('sboxall', 'sbox1')
                        print('Device Server: ' + device_server)
                        print('Running forever, until you press CTRL+Z to quit\n')
                        _run_locally_forever(server, device_server, user_key, bot, instance)
                    else:
                        _run(bot, inputs, _bot_logger)
                else:
                    sys.stderr.write("This bot does not contain a 'run' method\n\n")
                    _bot_logger.error("This bot does not contain a 'run' method")
                    return 1
            return 0
        except KeyboardInterrupt:
            return 0
        except SystemExit:
            return 0
        except BotError as e:
            _bot_logger.error('BotEngine Error: ' + e.msg)
            if _servermode:
                _bot_logger.error('BotEngine Error: code=%s, msg=%s' % (e.code, e.msg))
            return 2
        except:
            e = sys.exc_info()[0]
            import traceback
            s = traceback.format_exc()
            sys.stderr.write(s + '\n\n')
            _bot_logger.error(s)
            if _servermode:
                _bot_logger.error(s)
            return 3

    return


def _print_model(server, user_key, device_type_model):
    """
    Print the model for a given device type
    :param device_type_model: Device type ID to print the model for
    """
    name = None
    model = []
    parameters = _get_parameters(server, user_key)
    parameters = parameters['deviceParams']
    try:
        device_type_model = int(device_type_model)
    except:
        print(Color.RED + 'Please provide an integer device type.' + Color.END + '\n')
        return 0

    if device_type_model == 22 or device_type_model == 23 or device_type_model == 24:
        if device_type_model == 22:
            name = 'Web Camera'
        elif device_type_model == 23:
            name = 'Android Camera'
        elif device_type_model == 24:
            name = 'iOS Camera'
        model = ['accessCameraSettings', 'audioStreaming', 'videoStreaming', 'ppc.hdStatus', 'ppc.rapidMotionStatus', 'batteryLevel', 'ppc.charging', 'motionStatus', 'selectedCamera', 'ppc.autoFocus', 'ppc.recordSeconds', 'ppc.motionSensitivity', 'version', 'ppc.robotConnected', 'ppc.robotMotionDirection', 'ppc.robotOrientation', 'ppc.robotVantageSphericalCoordinates', 'ppc.robotVantageTimer', 'ppc.robotVantageConfigurationStatus', 'ppc.robotVantageName', 'ppc.robotVantageSequence', 'ppc.robotVantageMoveToIndex', 'ppc.availableBytes', 'twitterAutoShare', 'twitterDescription', 'ppc.twitterReminder', 'ppc.twitterStatus', 'ppc.motionCountDownTime', 'ppc.blackoutScreenOn', 'ppc.warningStatus', 'ppc.warningText', 'ppc.recordFullDuration', 'ppc.flashOn', 'streamError', 'ppc.streamStatus', 'model', 'timeZoneId', 'ppc.motionActivity', 'ppc.outputVolume', 'ppc.captureImage', 'recordStatus', 'ppc.alarm', 'ppc.countdown', 'ppc.playSound', 'ppc.motionAlarm', 'ppc.cameraName', 'ppc.throttleStatus']
    elif device_type_model == 31:
        name = 'Gateway'
        model = ['firmware', 'ipAddress', 'manufacturer', 'model', 'numberOfChildren', 'permitJoining', 'zbChannel', 'reboot', 'cloud', 'firmwareUpdateStatus', 'firmwareUrl', 'firmwareChecksum']
    elif device_type_model == 130:
        name = 'LintAlert PRO Plus'
        model = ['sig.led', 'sig.pressure', 'sig.wciPressure', 'sig.status', 'sig.runtime', 'sig.maxled', 'sig.curMaxLed', 'sig.type', 'sig.table', 'sig.clean', 'waterLeak', 'version', 'rssi']
    elif device_type_model == 4200:
        name = 'Netatmo Healthy Home Coach'
        model = ['degC', 'co2', 'relativeHumidity', 'noise', 'firmware', 'wifiSignal', 'pressure', 'nam.healthIdx']
    elif device_type_model == 4201:
        name = 'Netatmo Weather Station Indoor Module'
        model = ['degC', 'co2', 'relativeHumidity', 'noise', 'pressure', 'firmware', 'wifiSignal']
    elif device_type_model == 4202:
        name = 'Netatmo Weather Station Outdoor Module'
        model = ['degC', 'relativeHumidity', 'firmware', 'signalStrength', 'batteryLevel']
    elif device_type_model == 4204:
        name = 'Netatmo Welcome'
        model = ['status', 'ipc.sdStatus', 'ppc.charging', 'ipc.mainVideoUrl']
    elif device_type_model == 4220:
        name = 'Sensibo'
        model = ['degC', 'relativeHumidity', 'powerStatus', 'systemMode', 'coolingSetpoint', 'fanMode', 'swingMode', 'systemModeValues', 'fanModeValues', 'swingValues', 'tempValues']
    elif device_type_model == 9001:
        name = 'GE Dimmer Switch'
        model = ['currentLevel', 'state', 'lqi', 'rssi', 'model', 'manufacturer']
    elif device_type_model == 9002:
        name = 'Siren'
        model = ['ppc.alarmWarn', 'ppc.alarmDuration', 'ppc.alarmStrobe', 'ppc.alarmSquawk', 'batteryLevel', 'batteryVoltage', 'lqi', 'rssi', 'model', 'manufacturer']
    elif device_type_model == 9003:
        name = 'Temperature & Humidity Sensor'
        model = ['relativeHumidity', 'degC', 'batteryLevel', 'batteryVoltage', 'lqi', 'rssi', 'model', 'manufacturer']
    elif device_type_model == 9006:
        name = 'Fire Alarm'
        model = ['alarmStatus', 'batteryLevel', 'batteryVoltage', 'lqi', 'rssi', 'model', 'manufacturer']
    elif device_type_model == 9007:
        name = 'Smoke Detector'
        model = ['alarmStatus', 'batteryLevel', 'batteryVoltage', 'lqi', 'rssi', 'model', 'manufacturer']
    elif device_type_model == 9008:
        name = 'Heat Detector'
        model = ['alarmStatus', 'batteryLevel', 'batteryVoltage', 'lqi', 'rssi', 'model', 'manufacturer']
    elif device_type_model == 9010:
        name = 'Smart Lock'
        model = ['degC', 'lockStatus', 'lqi', 'rssi', 'model', 'manufacturer']
    elif device_type_model == 10014:
        name = 'Entry Sensor'
        model = ['doorStatus', 'batteryLevel', 'batteryVoltage', 'lqi', 'rssi', 'model', 'manufacturer']
    elif device_type_model == 10017:
        name = 'Water Sensor'
        model = ['waterLeak', 'batteryLevel', 'batteryVoltage', 'lqi', 'rssi', 'model', 'manufacturer']
    elif device_type_model == 10019:
        name = 'Touch Sensor'
        model = ['vibrationStatus', 'batteryLevel', 'batteryVoltage', 'lqi', 'rssi', 'model', 'manufacturer']
    elif device_type_model == 10031:
        name = 'Gateway'
        model = ['firmware', 'ipAddress', 'model', 'numberOfChildren', 'permitJoining', 'zbChannel']
    elif device_type_model == 10033:
        name = 'Temperature Sensor'
        model = ['degC', 'batteryLevel', 'batteryVoltage', 'lqi', 'rssi', 'model', 'manufacturer']
    elif device_type_model == 10034:
        name = 'Humidity Sensor'
        model = ['relativeHumidity', 'batteryLevel', 'batteryVoltage', 'lqi', 'rssi', 'model', 'manufacturer']
    elif device_type_model == 10035:
        name = 'Smart Plug'
        model = ['power', 'energy', 'outletStatus', 'lqi', 'rssi', 'model', 'manufacturer']
    elif device_type_model == 10036:
        name = 'Smart Bulb'
        model = ['currentLevel', 'state', 'batteryLevel', 'batteryVoltage', 'lqi', 'rssi', 'model', 'manufacturer']
    elif device_type_model == 10037:
        name = 'Thermostat'
        model = ['degC', 'fanModeSequence', 'systemMode', 'controlSequenceOfOperation', 'coolingSetpoint', 'heatingSetpoint', 'batteryLevel', 'batteryVoltage', 'lqi', 'rssi', 'model', 'manufacturer']
    elif device_type_model == 10038:
        name = 'Motion Sensor'
        model = ['motionStatus', 'batteryLevel', 'batteryVoltage', 'lqi', 'rssi', 'model', 'manufacturer']
    if len(model) > 0:
        print(Color.GREEN + name + Color.END)
        for m in model:
            description = ''
            for p in parameters:
                if p['name'] == m:
                    description = '('
                    if 'systemUnit' in p:
                        description += p['systemUnit'] + ', '
                    if p['numeric']:
                        description += 'numeric'
                    else:
                        description += 'non-numeric'
                    if 'description' in p:
                        description += ', ' + p['description']
                    description += ')'

            print('  ' + Color.BOLD + m + Color.END + ' ' + description)

    else:
        print(Color.RED + 'This device type does not yet have a model defined.' + Color.END)
    return


def _merge_redirects(bot_directory, merge_directory):
    """
    Merge the bot_directory with any other bot it redirects to, into the merge_directory - to produce the final branded bot.
    :param bot_directory: Original bot directory, possibly containing a .redirect file pointing to another bot to pull in and override specific files
    :param merge_directory: Destination directory to produce the final, merged bot files
    :return: final directory
    """
    import shutil
    from distutils.dir_util import copy_tree
    if os.path.isdir(merge_directory):
        shutil.rmtree(merge_directory, ignore_errors=True)
    redirect_bundle = None
    merge_list = [
     bot_directory]
    while True:
        redirect_bundle = _extract_redirect(merge_list[(-1)])
        if redirect_bundle is not None and redirect_bundle.strip() != '':
            merge_list.append(os.path.join(os.getcwd(), redirect_bundle))
        else:
            break

    pip_install = []
    pip_install_remotely = []
    microservices = []
    safe_delete_microservices = []
    for source in reversed(merge_list):
        pip_install = list(set(set(pip_install) | set(_extract_packages(source, True))))
        pip_install_remotely = list(set(set(pip_install_remotely) | set(_extract_packages(source, False))))
        microservices = list(set(set(microservices) | set(_extract_microservice_links(source))))
        safe_delete_microservices = list(set(set(safe_delete_microservices) | set(_extract_safe_delete_microservice_links(source))))
        copy_tree(source, merge_directory)

    for source in microservices:
        pip_install = list(set(set(pip_install) | set(_extract_packages(source, True))))
        pip_install_remotely = list(set(set(pip_install_remotely) | set(_extract_packages(source, False))))
        copy_tree(source, os.path.join(merge_directory, 'intelligence' + os.sep + source.split(os.sep)[(-1)]))

    for source in safe_delete_microservices:
        copy_tree(source, os.path.join(merge_directory, 'intelligence' + os.sep + source.split(os.sep)[(-1)]))
        index_file = os.path.join(merge_directory, 'intelligence' + os.sep + source.split(os.sep)[(-1)] + os.sep + 'index.py')
        if os.path.exists(index_file):
            os.remove(index_file)

    with open(os.path.join(merge_directory, 'structure.json'), 'w') as (outfile):
        json.dump({'pip_install': pip_install, 'pip_install_remotely': pip_install_remotely}, outfile, indent=2, sort_keys=True)
    index_filename = os.path.join(os.path.join(merge_directory, MICROSERVICES_DIRECTORY), 'index.py')
    device_microservices = {}
    location_microservices = {}
    organization_microservices = {}
    if os.path.exists(index_filename):
        for current_dir, dirs, files in os.walk(merge_directory):
            if os.path.exists(os.path.join(current_dir, 'index.py')):
                index_json = _extract_microservices_from_index(os.path.join(current_dir, 'index.py'))
                if DEVICE_MICROSERVICES_KEY in index_json:
                    for device_type in index_json[DEVICE_MICROSERVICES_KEY]:
                        if device_type not in device_microservices:
                            device_microservices[device_type] = {}
                        for service in index_json[DEVICE_MICROSERVICES_KEY][device_type]:
                            device_microservices[device_type][service['module']] = service['class']

                if LOCATION_MICROSERVICES_KEY in index_json:
                    for service in index_json[LOCATION_MICROSERVICES_KEY]:
                        location_microservices[service['module']] = service['class']

                if ORGANIZATION_MICROSERVICES_KEY in index_json:
                    for service in index_json[ORGANIZATION_MICROSERVICES_KEY]:
                        organization_microservices[service['module']] = service['class']

        merged_index = {DEVICE_MICROSERVICES_KEY: {}, LOCATION_MICROSERVICES_KEY: [], ORGANIZATION_MICROSERVICES_KEY: []}
        for device_type in device_microservices:
            merged_index[DEVICE_MICROSERVICES_KEY][device_type] = []
            for module_name in device_microservices[device_type]:
                merged_index[DEVICE_MICROSERVICES_KEY][device_type].append({'module': module_name, 'class': device_microservices[device_type][module_name]})

        for module_name in location_microservices:
            merged_index[LOCATION_MICROSERVICES_KEY].append({'module': module_name, 'class': location_microservices[module_name]})

        for module_name in organization_microservices:
            merged_index[ORGANIZATION_MICROSERVICES_KEY].append({'module': module_name, 'class': organization_microservices[module_name]})

        with open(index_filename, 'w') as (outfile):
            outfile.write('MICROSERVICES = ' + json.dumps(merged_index, indent=2, sort_keys=True))
    runtime_json = {'version': {}}
    for source in microservices:
        for current_dir, dirs, files in os.walk(source):
            if os.path.exists(os.path.join(current_dir, 'runtime.json')):
                runtime_json = _merge_runtime_json(runtime_json, _extract_json_from_file(os.path.join(current_dir, 'runtime.json')))

    for source in merge_list:
        if MICROSERVICES_FOUNDATION_BOT not in source:
            for current_dir, dirs, files in os.walk(source):
                if os.path.exists(os.path.join(current_dir, 'runtime.json')):
                    runtime_json = _merge_runtime_json(runtime_json, _extract_json_from_file(os.path.join(current_dir, 'runtime.json')))

    runtime_filename = os.path.join(merge_directory, 'runtime.json')
    with open(runtime_filename, 'w') as (outfile):
        json.dump(runtime_json, outfile, indent=2, sort_keys=True)
    return


def _merge_runtime_json(primary, secondary):
    """
    Merge 2 runtime JSON dictionary structures.
    :param primary: Takes precedence whenever there's a conflict
    :param secondary: Secondary JSON runtime structure that can get overwritten when there's a conflict.
    :return: a final runtime dictionary structure
    """
    primary = primary['version']
    secondary = secondary['version']
    return_json = {}
    if 'version' in primary:
        return_json['version'] = primary['version']
    elif 'version' in secondary:
        return_json['version'] = secondary['version']
    if 'whatsnew' in primary:
        return_json['whatsnew'] = primary['whatsnew']
    elif 'whatsnew' in secondary:
        return_json['whatsnew'] = secondary['whatsnew']
    if 'runtime' in primary:
        return_json['runtime'] = primary['runtime']
    elif 'runtime' in secondary:
        return_json['runtime'] = secondary['runtime']
    if 'maxPurchaseOccurrence' in primary:
        return_json['maxPurchaseOccurrence'] = primary['maxPurchaseOccurrence']
    elif 'maxPurchaseOccurrence' in secondary:
        return_json['maxPurchaseOccurrence'] = secondary['maxPurchaseOccurrence']
    trigger = 0
    if 'trigger' in primary:
        trigger |= primary['trigger']
    if 'trigger' in secondary:
        trigger |= secondary['trigger']
    if trigger > 0:
        return_json['trigger'] = trigger
    memory = 0
    if 'memory' in primary:
        if primary['memory'] > memory:
            memory = primary['memory']
    if 'memory' in secondary:
        if secondary['memory'] > memory:
            memory = secondary['memory']
    if memory > 0:
        return_json['memory'] = memory
    timeout = 0
    if 'timeout' in primary:
        if primary['timeout'] > timeout:
            timeout = primary['timeout']
    if 'timeout' in secondary:
        if secondary['timeout'] > timeout:
            timeout = secondary['timeout']
    if timeout > 0:
        return_json['timeout'] = timeout
    schedules = {}
    if 'schedule' in primary:
        schedules['DEFAULT'] = primary['schedule']
    elif 'schedule' in secondary:
        schedules['DEFAULT'] = secondary['schedule']
    if 'schedules' in secondary:
        for schedule_id in secondary['schedules']:
            schedules[schedule_id] = secondary['schedules'][schedule_id]

    if 'schedules' in primary:
        for schedule_id in primary['schedules']:
            schedules[schedule_id] = primary['schedules'][schedule_id]

    if len(schedules) > 0:
        return_json['schedules'] = schedules
    datastreams = set([])
    if 'dataStreams' in primary:
        for d in primary['dataStreams']:
            datastreams.add(d['address'])

    if 'dataStreams' in secondary:
        for d in secondary['dataStreams']:
            datastreams.add(d['address'])

    if len(datastreams) > 0:
        return_json['dataStreams'] = []
        for d in datastreams:
            return_json['dataStreams'].append({'address': d})

    if 'communications' in primary or 'communications' in secondary:
        communications = []
        if 'communications' in primary:
            communications = primary['communications']
        if 'communications' in secondary:
            for secondary_comms_block in secondary['communications']:
                found = False
                for primary_comms_block in communications:
                    if primary_comms_block['category'] == secondary_comms_block['category']:
                        found = True
                        for item in primary_comms_block:
                            if item in secondary_comms_block:
                                primary_comms_block[item] |= secondary_comms_block[item]

                        for item in secondary_comms_block:
                            if item not in primary_comms_block:
                                primary_comms_block[item] = secondary_comms_block[item]

                        break

                if not found:
                    communications.append(secondary_comms_block)

        return_json['communications'] = communications
    if 'access' in primary or 'access' in secondary:
        access = []
        if 'access' in primary:
            access = primary['access']
        if 'access' in secondary:
            for secondary_access_block in secondary['access']:
                found = False
                for primary_access_block in access:
                    if primary_access_block['category'] == secondary_access_block['category']:
                        found = True
                        for item in ['trigger', 'read', 'control']:
                            if item in primary_access_block:
                                if item in secondary_access_block:
                                    primary_access_block[item] |= secondary_access_block[item]
                            elif item in secondary_access_block:
                                primary_access_block[item] = secondary_access_block[item]

                        break

                if not found:
                    access.append(secondary_access_block)

        return_json['access'] = access
    if 'deviceTypes' in primary or 'deviceTypes' in secondary:
        device_types = []
        if 'deviceTypes' in primary:
            device_types = primary['deviceTypes']
        if 'deviceTypes' in secondary:
            for secondary_dt_block in secondary['deviceTypes']:
                found = False
                control = False
                read = False
                trigger = False
                if 'read' in secondary_dt_block:
                    read = secondary_dt_block['read']
                if 'control' in secondary_dt_block:
                    control = secondary_dt_block['control']
                if 'trigger' in secondary_dt_block:
                    trigger = secondary_dt_block['trigger']
                for primary_dt_block in device_types:
                    if primary_dt_block['id'] == secondary_dt_block['id']:
                        found = True
                        if 'read' in primary_dt_block:
                            read |= primary_dt_block['read']
                        if 'control' in primary_dt_block:
                            control |= primary_dt_block['control']
                        if 'trigger' in primary_dt_block:
                            trigger |= primary_dt_block['trigger']
                        primary_dt_block['read'] = read
                        primary_dt_block['control'] = control
                        primary_dt_block['trigger'] = trigger
                        break

                if not found:
                    device_types.append(secondary_dt_block)

        return_json['deviceTypes'] = device_types
    return {'version': return_json}


def _extract_microservices_from_index(file_location):
    """
    Extract the DEVICE_MICROSERVICES and LOCATION_MICROSERVIECS from the index.py file found at the file location
    :param file_location: Absolute location of the index.py file
    :return: JSON structure
    """
    with open(file_location, 'r') as (f):
        index_text = ''
        for line in f:
            if not line.strip().startswith('#'):
                index_text += line.strip()

        try:
            index_text = index_text.replace(' ', '')
            index_text = index_text.replace('MICROSERVICES=', '')
            index_json = eval(index_text)
        except SyntaxError as e:
            print(Color.RED + 'Problem with: ' + str(file_location) + Color.END)
            raise e

        return index_json
    return {}


def _extract_json_from_file(file_location):
    """
    Extract JSON content from a file
    :param file_location:
    :return:
    """
    with open(file_location, 'r') as (f):
        content = ''
        for line in f:
            if not line.strip().startswith('#'):
                content += line.strip()

        return json.loads(content)
    return {}


def _extract_packages(directory, local=True):
    """
    Extract a list of pip install packages from the structure.json file in the given directory
    :param directory: Directory that might have a structure.json file in it
    :param local: True to extract the packages names that should be installed locally
    :return: A list
    """
    pip_install = []
    for current_dir, dirs, files in os.walk(directory):
        if os.path.exists(os.path.join(current_dir, 'structure.json')):
            structure_text = ''
            with open(os.path.join(current_dir, 'structure.json'), 'r') as (f):
                for line in f:
                    if not line.strip().startswith('#'):
                        structure_text += line

                structure_json = json.loads(structure_text)
                if local:
                    if 'pip_install' in structure_json:
                        for item in structure_json['pip_install']:
                            if item not in pip_install:
                                pip_install.append(item)

                elif 'pip_install_remotely' in structure_json:
                    for item in structure_json['pip_install_remotely']:
                        if item not in pip_install:
                            pip_install.append(item)

    return pip_install


def _extract_microservice_links(directory):
    """
    Extract a list of microservice directories from the structure.json file in the given directory
    :param directory:
    :return:
    """
    microservices = []
    for current_dir, dirs, files in os.walk(directory):
        if os.path.exists(os.path.join(current_dir, 'structure.json')):
            structure_text = ''
            with open(os.path.join(current_dir, 'structure.json'), 'r') as (f):
                for line in f:
                    if not line.strip().startswith('#'):
                        structure_text += line

                structure_json = json.loads(structure_text)
                if 'microservices' in structure_json:
                    for item in structure_json['microservices']:
                        item = item.replace('/', os.sep).replace('\\', os.sep)
                        if item not in microservices:
                            microservices.append(item)

    return microservices


def _extract_safe_delete_microservice_links(directory):
    """
    Extract a list of microservice directories to safely delete, from the structure.json file in the given directory
    :param directory:
    :return:
    """
    microservices = []
    for current_dir, dirs, files in os.walk(directory):
        if os.path.exists(os.path.join(current_dir, 'structure.json')):
            structure_text = ''
            with open(os.path.join(current_dir, 'structure.json'), 'r') as (f):
                for line in f:
                    if not line.strip().startswith('#'):
                        structure_text += line

                structure_json = json.loads(structure_text)
                if 'safe_delete_microservices' in structure_json:
                    for item in structure_json['safe_delete_microservices']:
                        item = item.replace('/', os.sep).replace('\\', os.sep)
                        if item not in microservices:
                            microservices.append(item)

    return microservices


def _extract_redirect(directory):
    """
    Extract the redirect directory name from any existing .redirect file
    :return: Redirect directory name if it exists, None if it doesn't exist
    """
    if os.path.exists(os.path.join(directory, 'structure.json')):
        structure_text = ''
        with open(os.path.join(directory, 'structure.json'), 'r') as (f):
            for line in f:
                if not line.strip().startswith('#'):
                    structure_text += line

            try:
                structure_json = json.loads(structure_text)
            except ValueError as e:
                print(Color.BOLD + Color.RED + ('Error loading JSON content from {}').format(os.path.join(directory, 'structure.json')) + Color.END)
                print(('Error: {}').format(e) + '\n')
                exit(1)
            else:
                if 'extends' in structure_json:
                    return structure_json['extends']

    return


def _get_instance_id_from_bundle_id(server, user_key, bundle_id, challenge_id=None, location_id=None):
    """Get the instance ID from the bundle ID
    :param server: Server to use.
    :param user_key: User's /cloud API key.
    :param bundle_id: Bundle ID to find an bot instance for.
    :param challenge_id: Challange id which was used for creating bot instance id.
    :param location_id: Location ID
    """
    bots = _botstore_mybots(server, user_key, location_id=location_id)
    if bots is None:
        print('No bots')
        return
    else:
        potential_apps = []
        for bot in bots:
            if bot['bundle'] == bundle_id and bot['status'] >= 0 and bot['status'] < 5:
                try:
                    nickname = bot['nickname']
                except:
                    nickname = bot['name']

                potential_apps.append((nickname, bot['appInstanceId']))

        if len(potential_apps) == 0:
            print('No potential bots')
            return
        if len(potential_apps) == 1:
            n, i = potential_apps[0]
            instance = i
        elif challenge_id:
            if challenge_id != '0':
                for bot in bots:
                    try:
                        if int(challenge_id) == bot['access'][0]['challengeId']:
                            instance = bot['appInstanceId']
                    except:
                        pass

            else:
                instance = 0
                for bot in bots:
                    try:
                        if bot['access'][0]['challengeId'] and bot['appInstanceId'] > instance:
                            instance = bot['appInstanceId']
                    except:
                        pass

                print(Color.BOLD + 'Bot instance ID: ' + str(instance) + Color.END)
        else:
            print(Color.BOLD + 'Here are your available bot instances that match this bundle ID:' + Color.END)
            selection = None
            while selection == None:
                for n, i in potential_apps:
                    print('\t' + Color.BOLD + str(i) + Color.END + ' : ' + n, end='')
                    for bot in bots:
                        if bot['appInstanceId'] == i:
                            try:
                                challengeId = bot['access'][0]['challengeId']
                                print(' (' + Color.BOLD + 'challengeId = ' + str(challengeId) + Color.END + ')', end='')
                            except:
                                pass

                    print()

                selection = raw_input('Which bot instance should we execute: ')
                ok = False
                for n, i in potential_apps:
                    if str(i) == selection:
                        ok = True
                        break

                if not ok:
                    selection = None
                else:
                    instance = selection

        return instance


def _get_local_files(local_dir, walk=False):
    """Retrieve local files list
    result_list == a list of dictionaries with path and mtime keys. ex: {'path':<file_path>,'mtime':<file last modified time>}
    ignore_dirs == a list of directories to ignore, should not include the base_dir.
    ignore_files == a list of files to ignore.
    ignore_file_ext == a list of extentions to ignore.

    """
    result_list = []
    ignore_dirs = [
     'CVS', '.svn', '.git', '__pycache__']
    ignore_files = ['.project', '.pydevproject', 'marketing.json', 'runtime.json', 'icon.png']
    ignore_file_ext = ['.pyc']
    base_dir = os.path.abspath(local_dir)
    for current_dir, dirs, files in os.walk(base_dir):
        for this_dir in ignore_dirs:
            if this_dir in dirs:
                dirs.remove(this_dir)

        sub_dir = current_dir.replace(base_dir, '')
        if not walk and sub_dir:
            break
        for this_file in files:
            if this_file not in ignore_files and os.path.splitext(this_file)[(-1)].lower() not in ignore_file_ext:
                file_path = os.path.join(current_dir, this_file)
                file_monitor_dict = {'path': file_path, 
                   'mtime': os.path.getmtime(file_path)}
                result_list.append(file_monitor_dict)

    return result_list


def _get_ensemble_server_url(server, device_id=None):
    """Get Ensemble server URL"""
    import requests
    http_headers = {'Content-Type': 'application/json'}
    params = {'type': 'deviceio', 'ssl': True}
    if not device_id:
        params['deviceId'] = 'nodeviceid'
    else:
        params['deviceId'] = device_id
    r = requests.get(server + '/cloud/json/settingsServer', params=params, headers=http_headers, proxies=_https_proxy)
    return r.text


def _login(server, username, password, admin=False):
    """
    Login and obtain an API key
    :param server: Server address
    :param username: Username
    :param password: Password
    :return: API Key
    """
    import pickle
    if not username:
        username = raw_input('Email address: ')
    if not password:
        import getpass
        password = getpass.getpass()
    try:
        import requests
        type = 'user'
        if admin:
            type = 'admin'
        fixed_server = server.replace('http://', '').replace('https://', '').split('.')[0]
        filename = ('{}.{}.{}').format(username, fixed_server, type)
        if os.path.isfile(filename):
            with open(filename, 'rb') as (f):
                key = pickle.load(f)
            params = {'keyType': 0}
            if admin:
                params['keyType'] = 11
                params['expiry'] = 2
            http_headers = {'API_KEY': key, 'Content-Type': 'application/json'}
            r = requests.get(server + '/cloud/json/loginByKey', params=params, headers=http_headers, proxies=_https_proxy)
            j = json.loads(r.text)
            if j['resultCode'] == 0:
                key = j['key']
                with open(filename, 'wb') as (f):
                    pickle.dump(key, f)
                return key
        params = {'username': username}
        if admin:
            params['keyType'] = 11
        http_headers = {'PASSWORD': password, 'Content-Type': 'application/json'}
        r = requests.get(server + '/cloud/json/login', params=params, headers=http_headers, proxies=_https_proxy)
        j = json.loads(r.text)
        if j['resultCode'] == 17:
            passcode = raw_input('Type in the passcode you received on your phone: ')
            passcode = passcode.upper()
            params['expiry'] = 2
            http_headers['passcode'] = passcode
            r = requests.get(server + '/cloud/json/login', params=params, headers=http_headers, proxies=_https_proxy)
            j = json.loads(r.text)
            if j['resultCode'] == 0:
                key = j['key']
                with open(filename, 'wb') as (f):
                    pickle.dump(key, f)
        _check_for_errors(j)
        return j['key']
    except BotError as e:
        sys.stderr.write('BotEngine Error: ' + e.msg)
        sys.stderr.write('\nCreate an account on ' + server + ' and use it to sign in')
        sys.stderr.write('\n\n')
        raise e


def _get_user_info(server, user_key, user_id=None):
    """
    Get the user info
    :param server: Server address
    :param user_key: User API key
    :param user_id: User ID for administrator access
    """
    import requests
    try:
        http_headers = {'API_KEY': user_key, 'Content-Type': 'application/json'}
        params = {}
        if user_id is not None:
            params['userId'] = user_id
        r = requests.get(server + '/cloud/json/user', params=params, headers=http_headers, proxies=_https_proxy)
        j = json.loads(r.text)
        _check_for_errors(j)
        return j
    except BotError as e:
        sys.stderr.write('BotEngine Error: ' + e.msg)
        sys.stderr.write('\n\n')
        raise e

    return


def _get_organization_users(server, user_key, organization_id):
    """
    Get a list of users from an organization
    :param server:
    :param user_key:
    :param organization_id:
    :return:
    """
    import requests
    try:
        http_headers = {'API_KEY': user_key, 'Content-Type': 'application/json'}
        r = requests.get(server + '/admin/json/organizations/' + str(organization_id) + '/users', headers=http_headers, proxies=_https_proxy)
        j = json.loads(r.text)
        _check_for_errors(j)
        return j.get('users', [])
    except BotError as e:
        sys.stderr.write('BotEngine Error: ' + e.msg)
        sys.stderr.write('\n\n')
        raise e


def _get_botengine_key(server, user_key, bot_key_type, bot_instance_id):
    """Get a BotEngine API key by appKey
    :param server: Server to use
    :param user_key: User's /cloud API key
    :param bot_key_type: 0 = normal bot; 1 = developer bot
    :param bot_instance_id: Application instance ID to execute
    """
    import requests
    http_headers = {'API_KEY': user_key, 'Content-Type': 'application/json'}
    params = {'appType': bot_key_type, 
       'appInstanceId': bot_instance_id}
    r = requests.get(server + '/analytic/appkey', params=params, headers=http_headers, proxies=_https_proxy)
    j = json.loads(r.text)
    _check_for_errors(j)
    return j['key']


def _compile():
    """Compile all .py files to .pyc"""
    pass


def _create_or_update_app(server, key, bundle, data):
    """Create or update the bot"""
    import requests
    j = json.dumps(data)
    http_headers = {'API_KEY': key, 'Content-Type': 'application/json'}
    r = requests.put(server + '/cloud/developer/apps?bundle=' + bundle, headers=http_headers, data=j, proxies=_https_proxy)
    j = json.loads(r.text)
    _check_for_errors(j)
    return j


def _get_apps(server, key, bundle=None):
    """Get created bots"""
    import requests
    http_headers = {'API_KEY': key, 'Content-Type': 'application/json'}
    params = {}
    if bundle is not None:
        params['bundle'] = bundle
    r = requests.get(server + '/cloud/developer/apps', params=params, headers=http_headers, proxies=_https_proxy)
    j = json.loads(r.text)
    _check_for_errors(j)
    return j


def _upload_icon(server, key, bundle, filePath):
    """Upload the icon using 1024x1024 px png"""
    import requests
    with open(filePath, 'rb') as (payload):
        http_headers = {'API_KEY': key, 'Content-Type': 'image/png'}
        r = requests.put(server + '/cloud/developer/objects/icon?bundle=' + bundle, headers=http_headers, data=payload, proxies=_https_proxy)
        j = json.loads(r.text)
        _check_for_errors(j)
        return j


def _check_bot_processing(server, key, request_id):
    """
    Check to see if the bot got processed correctly
    :param server:
    :param key:
    :param request_id:
    :return: response from the server
    """
    import requests
    http_headers = {'API_KEY': key, 'Content-Type': 'application/json'}
    r = requests.get(server + '/cloud/developer/upload/' + str(request_id), headers=http_headers, proxies=_https_proxy)
    j = json.loads(r.text)
    _check_for_errors(j)
    return j


def _get_versions(server, key, bundle, params=None):
    """Get versions of the specified bot"""
    import requests
    if params is None:
        params = {}
    params['bundle'] = bundle
    http_headers = {'API_KEY': key, 'Content-Type': 'application/json'}
    r = requests.get(server + '/cloud/developer/versions', params=params, headers=http_headers, proxies=_https_proxy)
    j = json.loads(r.text)
    _check_for_errors(j)
    return j


def _update_latest_version(server, key, bundle, data):
    """Update latest version for the specified bot"""
    import requests
    j = json.dumps(data)
    http_headers = {'API_KEY': key, 'Content-Type': 'application/json'}
    r = requests.put(server + '/cloud/developer/versions?bundle=' + bundle, headers=http_headers, data=j, proxies=_https_proxy)
    j = json.loads(r.text)
    _check_for_errors(j)
    return j


def _update_version_status(server, key, bundle, status, ignore_errors=False):
    """Update status of latest version of the specified bot"""
    import requests
    params = {'bundle': bundle, 'status': status}
    http_headers = {'API_KEY': key, 'Content-Type': 'application/json'}
    r = requests.put(server + '/cloud/developer/versionStatus', params=params, headers=http_headers, proxies=_https_proxy)
    j = json.loads(r.text)
    if not ignore_errors:
        _check_for_errors(j)
    return j


def _upload_bot(server, key, bundle, bot_filename, tar):
    """Upload the bot to bot store with zip format"""
    import requests
    if tar:
        bot_filename += '.tar'
        content_type = 'application/x-tar'
        params = {'source': True, 
           'async:': True}
    else:
        bot_filename += '.zip'
        content_type = 'application/zip'
        params = {}
    with open(bot_filename, 'rb') as (payload):
        http_headers = {'API_KEY': key, 'Content-Type': content_type}
        r = requests.post(server + '/cloud/developer/upload?bundle=' + bundle, headers=http_headers, params=params, data=payload, proxies=_https_proxy)
        j = json.loads(r.text)
        _check_for_errors(j)
        return j


def _get_app_statistics(server, key, bundle):
    """Get the statistics of the specified bot"""
    import requests
    params = {}
    params['bundle'] = bundle
    http_headers = {'API_KEY': key, 'Content-Type': 'application/json'}
    r = requests.get(server + '/cloud/developer/stats', params=params, headers=http_headers, proxies=_https_proxy)
    j = json.loads(r.text)
    _check_for_errors(j)
    return j


def _get_bot_beta_testers(server, user_key, bundle_id):
    """
    Get the list of bot beta testers for the given bot bundle
    :param server: Server
    :param user_key: Developer's user API key
    :param bundle_id: Bot bundle ID
    :return: JSON
    """
    import requests
    params = {}
    params['bundle'] = bundle_id
    http_headers = {'API_KEY': user_key, 'Content-Type': 'application/json'}
    r = requests.get(server + '/cloud/developer/tester', params=params, headers=http_headers, proxies=_https_proxy)
    j = json.loads(r.text)
    _check_for_errors(j)
    return j


def _add_bot_beta_testers(server, user_key, bundle_id, user_id):
    """
    Add a bot beta tester to the given bot bundle
    :param server: Server
    :param user_key: Developer's user API key
    :param bundle_id: Bot bundle ID
    :param user_id: User ID to add to the bundle
    :return: JSON
    """
    import requests
    params = {}
    params['bundle'] = bundle_id
    http_headers = {'API_KEY': user_key, 'Content-Type': 'application/json'}
    r = requests.put(server + '/cloud/developer/tester/' + str(user_id), params=params, headers=http_headers, proxies=_https_proxy)
    j = json.loads(r.text)
    _check_for_errors(j)
    return j


def _delete_bot_beta_testers(server, user_key, bundle_id, user_id):
    """
    Delete a bot beta tester from the given bot bundle
    :param server: Server
    :param user_key: Developer's user API key
    :param bundle_id: Bot bundle ID
    :param user_id: User ID to add to the bundle
    :return: JSON
    """
    import requests
    params = {}
    params['bundle'] = bundle_id
    http_headers = {'API_KEY': user_key, 'Content-Type': 'application/json'}
    r = requests.delete(server + '/cloud/developer/tester/' + str(user_id), params=params, headers=http_headers, proxies=_https_proxy)
    j = json.loads(r.text)
    _check_for_errors(j)
    return j


def _beta_purchase_bot(server, user_key, bundle_id, user_id=None):
    """
    As an approved beta tester, purchase the bot into your account for beta testing
    :param server:
    :param user_key:
    :param bundle_id:
    :return:
    """
    import requests
    params = {}
    params['bundle'] = bundle_id
    if user_id is not None:
        params['userId'] = user_id
    http_headers = {'API_KEY': user_key, 'Content-Type': 'application/json'}
    r = requests.post(server + '/cloud/developer/tester', params=params, headers=http_headers, proxies=_https_proxy)
    j = json.loads(r.text)
    _check_for_errors(j)
    return j


def _listen(device_server, user_key, bot_instance_id, timeout=2, clean=True, cleanTime=None):
    """
    Apps running on the developer's local computer will listen to Ensemble for incoming device data.
    :param device_server: Device Server URL
    :param user_key: User's /cloud API key
    :param timeout: HTTP timeout in seconds
    :param clean: Set to 'true' to avoid having the server repeat itself
    """
    import requests
    params = {'appInstanceId': bot_instance_id, 
       'timeout': timeout}
    if cleanTime:
        params['cleanTime'] = cleanTime
    else:
        params['clean'] = clean
    http_headers = {'API_KEY': user_key, 'Content-Type': 'application/json'}
    r = requests.get(device_server + '/deviceio/analytic', params=params, headers=http_headers, proxies=_https_proxy)
    j = json.loads(r.text)
    return j


def _check_for_errors(json_response):
    """
    Check some JSON response for BotEngine errors
    """
    if not json_response:
        raise BotError('No response from the server!', -1)
    if json_response['resultCode'] > 0:
        msg = 'Unknown error!'
        if 'resultCodeMessage' in json_response.keys():
            msg = json_response['resultCodeMessage']
        elif 'resultCodeDesc' in json_response.keys():
            msg = json_response['resultCodeDesc']
        raise BotError(msg, json_response['resultCode'])
    del json_response['resultCode']


def _get_device(server, user_key, device_id, check_connected=False):
    """Maybe we need this api to obtain the device type and others, or send device Object via command line"""
    import requests
    params = {'checkConnected': check_connected}
    http_headers = {'API_KEY': user_key, 'Content-Type': 'application/json'}
    r = requests.get(server + '/cloud/json/devices/' + device_id, params=params, headers=http_headers, proxies=_https_proxy)
    j = json.loads(r.text)
    _check_for_errors(j)
    return j['device']


def _get_devices_from_location(server, user_key, location_id):
    """
    Get all the devices from your location
    
    :param server: Server
    :param user_key: API Key
    :param location_id: Location ID
    """
    http_headers = {'API_KEY': user_key, 'Content-Type': 'application/json'}
    import requests
    params = {'locationId': location_id}
    r = requests.get(server + '/cloud/json/devices', headers=http_headers, params=params, proxies=_https_proxy)
    j = json.loads(r.text)
    _check_for_errors(j)
    return j.get('devices', [])


def _get_devices_from_organization(server, user_key, organization_id, linked_to=1, device_type=None, user_id=None):
    """
    Get devices from an organization
    http://docs.iotadmins.apiary.io/#reference/users-and-locations/locations-in-an-organization/get-devices
    
    :param server: Server
    :param user_key: User Key
    :param linked_to: 1=users; 2=locations; 3=user and locations
    :param organization_id: Organization ID to pull devices from
    :param device_type: Device type to filter by
    :param user_id: User ID to filter by
    """
    import requests
    http_headers = {'API_KEY': user_key, 'Content-Type': 'application/json'}
    params = {'linkedTo': linked_to}
    if device_type:
        params['deviceType'] = device_type
    if user_id:
        params['userId'] = user_id
    r = requests.get(server + '/admin/json/organizations/' + str(organization_id) + '/devices', params=params, headers=http_headers, proxies=_https_proxy)
    j = json.loads(r.text)
    _check_for_errors(j)
    return j.get('devices', [])


def _summarize_apps(server, user_key, bundle=None):
    """
    Developer helper method

    This method will print out all the bots in the user's account
    """
    j = _get_apps(server, user_key, bundle)
    bots = j.get('apps', [])
    sys.stderr.write('\n')
    sys.stderr.write(Color.BOLD + ('BUNDLE').ljust(45) + ('STATUS').ljust(30) + '(CATEGORY)' + Color.END)
    sys.stderr.write('\n')
    for bot in bots:
        version_info = _get_versions(server, user_key, bot['bundle'])
        try:
            status = version_info['versions'][0]['status']
        except:
            status = 0
        else:
            sys.stderr.write(bot['bundle'].ljust(45) + str(VERSION_STATUS_DICT[status]).ljust(30) + '(' + bot.get('category', '') + ')\n')

    sys.stderr.write('\n')


def _summarize_versions(server, user_key, bundle=None, version=None):
    """Developer helper method

    This method will print out all the versions of your bot in the user's account"""
    if not bundle:
        _summarize_apps(server, user_key)
        bundle = raw_input('Which bundle ID should we use to: ')
    j = _get_versions(server, user_key, bundle)
    versions = j.get('versions')
    sys.stderr.write('\n')
    sys.stderr.write(('VERSION').ljust(40) + '\t(STATUS - CREATION DATE)\n')
    sys.stderr.write('\n')
    for v in versions:
        status = VERSION_STATUS_DICT.get(v['status'], v['status'])
        sys.stderr.write(v['version'].ljust(40) + '\t(' + status + ' - ' + v['creationDate'] + ')\n')

    sys.stderr.write('\n')


def _summarize_devices(server, user_key, location_id):
    """
    Print all available devices in the given location
    :param server:
    :param user_key:
    :param location_id:
    :return:
    """
    devices = _get_devices_from_location(server, user_key, location_id)
    if not devices:
        return
    connected = []
    disconnected = []
    relevant_devices = []
    for device in devices:
        if device['connected'] is True:
            relevant_devices.append(device)
            connected.append((device['type'], device['id'].ljust(40) + '\t(' + str(device['type']) + " - '" + device.get('desc', '') + "' - Connected)\n"))

    sys.stderr.write('\n')
    for device in devices:
        if device['connected'] is False:
            relevant_devices.append(device)
            disconnected.append((device['type'], device['id'].ljust(40) + '\t(' + str(device['type']) + " - '" + device.get('desc', '') + "' - Disconnected)\n"))

    connected = sorted(connected)
    disconnected = sorted(disconnected)
    sys.stderr.write(('\n\nDEVICE ID').ljust(40) + '\t\t(TYPE - NICKNAME - STATUS)\n')
    for device in connected:
        sys.stderr.write(str(device[1].encode('utf-8')))

    if len(connected) > 0:
        sys.stderr.write('\n')
    for device in disconnected:
        sys.stderr.write(str(device[1].encode('utf-8')))

    sys.stderr.write('\n')
    return relevant_devices


def _summarize_device_types(server, user_key):
    """
    Summarize and print out all the device types available on this server
    """
    http_headers = {'API_KEY': user_key, 'Content-Type': 'application/json'}
    import requests
    r = requests.get(server + '/cloud/json/deviceTypes', headers=http_headers, proxies=_https_proxy)
    device_types = json.loads(r.text)
    _check_for_errors(device_types)
    print('\n' + Color.BOLD + 'Available Device Types' + Color.END)
    print('-' * 40)
    categories = {}
    for device_type in device_types['deviceTypes']:
        if device_type['id'] > 3:
            if 'attributes' in device_type:
                for attribute in device_type['attributes']:
                    if attribute['name'] == 'category':
                        if int(attribute['value']) not in categories:
                            categories[int(attribute['value'])] = {}
                        categories[int(attribute['value'])][device_type['id']] = device_type

    for category_id in sorted(categories):
        print(Color.BOLD + _device_category_to_string(category_id) + Color.END)
        for device_type_id in sorted(categories[category_id]):
            url = ''
            if 'attributes' in categories[category_id][device_type_id]:
                for attr in categories[category_id][device_type_id]['attributes']:
                    if attr['name'] == 'storeUrl':
                        url = '(' + attr['value'] + ')'
                        break

            print('\t' + Color.BOLD + str(device_type_id) + Color.END + ' : ' + categories[category_id][device_type_id]['name'] + url)

        print()

    print('\n' + the_bot() + 'Done!')


def _get_parameters(server, user_key, parameter=None):
    """
    Get the details of all the public parameters in the system
    :param server: Server
    :param user_key: User key
    :return: API response
    """
    http_headers = {'API_KEY': user_key, 'Content-Type': 'application/json'}
    import requests
    params = {}
    if parameter is not None:
        params = {'paramName': parameter}
    r = requests.get(server + '/cloud/json/deviceParameters', params=params, headers=http_headers, proxies=_https_proxy)
    parameters = json.loads(r.text)
    _check_for_errors(parameters)
    return parameters


def _device_category_to_string(category_id):
    """
    :param category_id: Category ID to convert to a string
    :return: Category description
    """
    if category_id < 50:
        return 'Reserved'
    if category_id < 1000:
        return 'Temporary'
    if category_id < 2000:
        return 'Administrative Tools'
    if category_id < 3000:
        return 'Alarms'
    if category_id < 4000:
        return 'Analytics'
    if category_id < 5000:
        return 'Appliances'
    if category_id < 6000:
        return 'Audio'
    if category_id < 7000:
        return 'Cameras'
    if category_id < 8000:
        return 'Climate Control'
    if category_id < 9000:
        return 'Displays'
    if category_id < 10000:
        return 'Environmental'
    if category_id < 11000:
        return 'Health'
    if category_id < 12000:
        return 'Lighting'
    if category_id < 13000:
        return 'Locks'
    if category_id < 14000:
        return 'Media'
    if category_id < 15000:
        return 'Meters'
    if category_id < 16000:
        return 'Perimeter Monitoring'
    if category_id < 17000:
        return 'Remote Controls'
    if category_id < 18000:
        return 'Robotics'
    if category_id < 19000:
        return 'Routers and Gateways'
    if category_id < 20000:
        return 'Security'
    if category_id < 21000:
        return 'Sensors'
    if category_id < 22000:
        return 'Shades'
    if category_id < 23000:
        return 'Social'
    if category_id < 24000:
        return 'Switches'
    if category_id < 25000:
        return 'Toys'
    if category_id < 26000:
        return 'Transportation'
    if category_id < 27000:
        return 'Videos'
    if category_id < 28000:
        return 'Water'


def _botstore_search(server, user_key, searchBy=None, category=('E', 'S', 'C', 'L', 'H', 'W'), compatible=False, lang=None):
    """Search the bot store for bots
    :param server: Server to use
    :param user_key: User's /cloud API key
    :param searchBy: Optional string. Search for a name, author, or keywords
    :param category: Optional tuple. Search by category, multiple are allowed, i.e. ('E','S','C','L','H','W')
        E = Energy
        S = Security
        C = Care
        L = Lifestyle
        H = Health
        W = Wellness
    :param compatible: Optional boolean. True to only return bots that are compatible with this user's account
    :param lang: Optional string. Search for bots in a particular language, i.e. "en", "zh", etc.
    :returns: List of bots matching the search criteria in JSON format
    """
    params = {}
    if searchBy:
        params['searchBy'] = searchBy
    if category:
        params['category'] = category
    if compatible:
        params['compatible'] = compatible
    if lang:
        params['lang'] = lang
    http_headers = {'API_KEY': user_key, 'Content-Type': 'application/json'}
    import requests
    r = requests.get(server + '/cloud/appstore/search', params=params, headers=http_headers, proxies=_https_proxy)
    j = json.loads(r.text)
    _check_for_errors(j)
    return j['apps']


def _botstore_botinfo(server, user_key, bundle, lang=None):
    """View the details of an bot on the bot store
    :param server: Server to use
    :param user_key: User's /cloud API key
    :param bundle: Bundle ID to view
    :param lang: Optional string. View the bot information in a particular language, i.e. "en", "zh", etc.
    :returns: Bot information from the bot store in JSON format
    """
    params = {'bundle': bundle}
    if lang:
        params['lang'] = lang
    http_headers = {'API_KEY': user_key, 'Content-Type': 'application/json'}
    import requests
    r = requests.get(server + '/cloud/appstore/appInfo', params=params, headers=http_headers, proxies=_https_proxy)
    j = json.loads(r.text)
    _check_for_errors(j)
    return j['app']


def _allow_organization_to_purchase_bot(server, user_key, bundle, organization_id, development_mode=False):
    """
    Allow an organization to purchase a bot
    :param server: Server to use
    :param user_key: User's /cloud API key
    :param bundle: Bot bundle ID to obtain or purchase
    :param organization_id: Organization ID to allow to purchase the bot
    :param development_mode: True to allow this organization to have the latest and greatest developer version of this bot, False to let the organization purchase only the publicly available version
    :return: Purchased bot instance ID
    """
    params = {'bundle': bundle, 
       'developmentMode': development_mode}
    http_headers = {'API_KEY': user_key, 'Content-Type': 'application/json'}
    import requests
    r = requests.put(server + '/cloud/developer/organizations/' + str(organization_id), params=params, headers=http_headers, proxies=_https_proxy)
    j = json.loads(r.text)
    _check_for_errors(j)


def _prevent_organization_from_purchasing_bot(server, user_key, bundle, organization_id):
    """
    Prevent an organization from purchasing a bot
    :param server: Server to use
    :param user_key: User's /cloud API key
    :param bundle: Bot bundle ID to obtain or purchase
    :param organization_id: Organization ID to allow to purchase the bot
    :return: Purchased bot instance ID
    """
    params = {'bundle': bundle}
    http_headers = {'API_KEY': user_key, 'Content-Type': 'application/json'}
    import requests
    r = requests.delete(server + '/cloud/developer/organizations/' + str(organization_id), params=params, headers=http_headers, proxies=_https_proxy)
    j = json.loads(r.text)
    _check_for_errors(j)


def _botstore_purchasebot(server, user_key, bundle, location_id=None, organization_id=None):
    """Delete an bot instance you previously purchased
    :param server: Server to use
    :param user_key: User's /cloud API key
    :param bundle: Bot bundle ID to obtain or purchase
    :return: Purchased bot instance ID
    """
    params = {'bundle': bundle}
    if organization_id is not None:
        print('Attempting to purchasing the bot ' + bundle + ' into organization ID ' + str(organization_id))
        params['organizationId'] = organization_id
    if location_id is not None:
        print('Attempting to purchasing the bot ' + bundle + ' into location ID ' + str(location_id))
        params['locationId'] = location_id
    http_headers = {'API_KEY': user_key, 'Content-Type': 'application/json'}
    import requests
    r = requests.post(server + '/cloud/appstore/appInstance', params=params, headers=http_headers, proxies=_https_proxy)
    j = json.loads(r.text)
    _check_for_errors(j)
    return j['appInstanceId']


def _botstore_configure(server, user_key, bot_instance_id, configuration, status, location_id=None):
    """Configure an bot that was purchased on the bot store
    :param server: Server to use
    :param user_key: User's /cloud API key
    :param bot_instance_id: Bot instance ID to configure in the user's account
    :param configuration: Configuration dictionary
    :param status: 0=incomplete; 1=active; 2=inactive
    :returns: True if the bot was configured
    """
    params = {'appInstanceId': bot_instance_id, 
       'status': status}
    if location_id is not None:
        params['locationId'] = location_id
    http_headers = {'API_KEY': user_key, 'Content-Type': 'application/json'}
    import requests
    body = json.dumps(configuration)
    r = requests.put(server + '/cloud/appstore/appInstance', params=params, headers=http_headers, data=body, proxies=_https_proxy)
    j = json.loads(r.text)
    print('Response: ' + json.dumps(j, indent=2, sort_keys=True))
    try:
        _check_for_errors(j)
        return True
    except BotError as e:
        sys.stderr.write(e.msg + '\n\n')
        return False

    return


def _botstore_deletebot(server, user_key, app_instance_id, location_id=None):
    """Delete an bot instance you previously purchased
    :param server: Server to use
    :param user_key: User's /cloud API key
    :param app_instance_id: Bot instance ID to delete
    :return: True if the bot was deleted, False if the bot wasn't found
    """
    params = {'appInstanceId': app_instance_id}
    if location_id is not None:
        params['locationId'] = location_id
    http_headers = {'API_KEY': user_key, 'Content-Type': 'application/json'}
    import requests
    r = requests.delete(server + '/cloud/appstore/appInstance', params=params, headers=http_headers, proxies=_https_proxy)
    j = json.loads(r.text)
    return j['resultCode'] == 0


def _botstore_mybots(server, user_key, app_instance_id=None, location_id=None, organization_id=None):
    """Get a list of the bots you've purchased
    :param server: Server to use
    :param user_key: User's /cloud API key
    :param app_instance_id: Optional ID of a specific bot to obtain information about
    :param organization_id: Optional Organization ID
    :param location_id: Optional Location ID
    :returns: Bot information on your purchased bots, in JSON format
    """
    params = {}
    if app_instance_id:
        params['appInstanceId'] = app_instance_id
    if organization_id is not None:
        params['organizationId'] = organization_id
    if location_id is not None:
        params['locationId'] = location_id
    http_headers = {'API_KEY': user_key, 'Content-Type': 'application/json'}
    import requests
    r = requests.get(server + '/cloud/appstore/appInstance', params=params, headers=http_headers, proxies=_https_proxy)
    j = json.loads(r.text)
    _check_for_errors(j)
    try:
        return j['apps']
    except:
        return

    return


def get_editable_bot_configuration(current_app_configuration):
    """Get an editable bot configuration
    :param current_app_configuration: Full JSON Dictionary definition of the bot instance from the server - not an array
    :returns: Editable configuration
    """
    config = current_app_configuration
    editable = {'app': {}}
    try:
        editable['app']['access'] = config['access']
    except:
        pass
    else:
        try:
            editable['app']['communications'] = config['communications']
        except:
            pass
        else:
            try:
                editable['app']['nickname'] = config['nickname']
            except:
                pass

        try:
            editable['app']['nickname'] = config['timezone']
        except:
            pass

    return editable


def _get_questions(server, user_key, instance_id=None, question_id=None, answer_status=None, location_id=None, organization_id=None, collection_name=None, general_public=None, language=None):
    """
    Get questions for the specific bot instance ID
    :param server: Server instance
    :param user_key: API key
    :param instance_id: Optional Bot instance ID to obtain questions from - if left blank, all the user's questions will be returned
    :param answer_status: Return questions with a specific answer status. By default, questions with statuses 2 and 3 are returned. Multiple values are supported.
    :param location_id: Location ID
    :param organization_id: Filter by organization ID
    :param collection_name: Filter by collection name
    :param general_public: True to return only public questions, False to return private questions
    :param language: Questions text language to return
    """
    params = {}
    if instance_id is not None:
        params['appInstanceId'] = instance_id
    if question_id is not None:
        params['questionId'] = question_id
    if answer_status is not None:
        params['answerStatus'] = answer_status
    if location_id is not None:
        params['locationId'] = location_id
    if organization_id is not None:
        params['organizationId'] = organization_id
    if collection_name is not None:
        params['collectionName'] = collection_name
    if language is not None:
        params['lang'] = language
    if general_public is not None:
        params['generalPublic'] = general_public
    http_headers = {'API_KEY': user_key, 'Content-Type': 'application/json'}
    import requests
    r = requests.get(server + '/cloud/json/questions', params=params, headers=http_headers, proxies=_https_proxy)
    j = json.loads(r.text)
    _check_for_errors(j)
    return j


def _print_question(question):
    """
    Print out a question
    """
    print('\n\n' + Color.UNDERLINE + question['question'] + Color.END)
    display_type = 0
    if 'displayType' in question:
        display_type = question['displayType']
    default_answer = None
    if 'defaultAnswer' in question:
        default_answer = question['defaultAnswer']
    response_options = None
    if 'responseOptions' in question:
        response_options = question['responseOptions']
    answer_status = question['answerStatus']
    if question['responseType'] == BotEngine.QUESTION_RESPONSE_TYPE_BOOLEAN:
        if display_type == BotEngine.QUESTION_DISPLAY_BOOLEAN_ONOFF:
            print('\t=> This is a boolean ON/OFF switch question (0 = OFF; 1 = ON)')
            if answer_status == 4:
                print('\t=> User selected answer is ' + str(question['answer']))
            elif default_answer:
                print('\t=> Current answer is ' + str(default_answer))
            else:
                print('\t=> Current answer is 0')
        elif display_type == BotEngine.QUESTION_DISPLAY_BOOLEAN_YESNO:
            print('\t=> This is a boolean YES/NO question (0 = NO; 1 = YES)')
            if answer_status == 4:
                print('\t=> User selected answer is ' + str(question['answer']))
            elif default_answer:
                print('\t=> Current answer is ' + str(default_answer))
            else:
                print('\t=> Current answer is 0')
        elif display_type == BotEngine.QUESTION_DISPLAY_BOOLEAN_BUTTON:
            print('\t=> This is a single button question. (1 = tap the button).')
            if 'placeholder' in question:
                print("\t=> The button's text says '" + str(question['placeholder']) + '"')
            else:
                print("\t=> The button's text says 'Yes'")
        else:
            print('\t=> Unknown display type (' + str(display_type) + ') for this Boolean question')
    elif question['responseType'] == BotEngine.QUESTION_RESPONSE_TYPE_MULTICHOICE_SINGLESELECT:
        if display_type == BotEngine.QUESTION_DISPLAY_MCSS_RADIO_BUTTONS:
            print('\t=> This is a Multiple Choice Single Select question with Radio buttons.')
            print('\t=> The answer will be the ID of the response option you want to select.')
        elif display_type == BotEngine.QUESTION_DISPLAY_MCSS_PICKER:
            print('\t=> This is a Multiple Choice Single Select question with a Picker.')
            print('\t=> The answer will be the ID of the response option you want to select.')
        else:
            print('\t=> Unknown display type (' + str(display_type) + ') for this Multiple Choice Single Select question')
        if answer_status == 4:
            print('\t=> User selected answer is ' + str(question['answer']))
        elif default_answer:
            print("\t=> The answer is currently: '" + str(default_answer) + "'")
        else:
            question['defaultAnswer'] = 0
            print("\t=> The answer is currently: '0'")
        if not response_options or len(response_options) == 0:
            print(Color.RED + '\t=> This question is incomplete because it is missing response options.' + Color.END)
        else:
            responses = {}
            for o in question['responseOptions']:
                responses[o['id']] = o

            print('\n\n\tOptions:')
            for response_id in sorted(responses.iterkeys()):
                print('\t[' + Color.GREEN + str(response_id) + Color.END + '] : ' + str(responses[response_id]['text']))

    elif question['responseType'] == BotEngine.QUESTION_RESPONSE_TYPE_MULTICHOICE_MULTISELECT:
        print('\t=> This is a Multiple Choice Multiple Select question (checkboxes).')
        print('\t=> Provide a BITMASK of the response options you want to select - either a decimal value, or hex value with a 0x prefix.')
        if answer_status == 4:
            print('\t=> User selected answer is ' + str(question['answer']))
        elif default_answer:
            print("\t=> The answer is currently: '" + str(default_answer) + "'")
        else:
            question['defaultAnswer'] = 0
            print("\t=> The answer is currently: '0'")
        if not response_options or len(response_options) == 0:
            print(Color.RED + '\t=> This question is incomplete because it is missing response options.' + Color.END)
        else:
            responses = {}
            for o in question['responseOptions']:
                responses[o['id']] = o

            print('\n\n\tOptions:')
            for response_id in sorted(responses.iterkeys()):
                print('\t[' + Color.GREEN + str(response_id) + Color.END + '] : ' + str(responses[response_id]['text']))

    elif question['responseType'] == BotEngine.QUESTION_RESPONSE_TYPE_DAYOFWEEK:
        if display_type == BotEngine.QUESTION_DISPLAY_DAYOFWEEK_MULTISELECT:
            print('\t=> This is a Multiple Choice Day of the Week question.')
            print('\t=> Provide a BITMASK-OR of the days you want to select - either a decimal value, or hex value with a 0x prefix.')
        elif display_type == BotEngine.QUESTION_DISPLAY_DAYOFWEEK_SINGLESELECT:
            print('\t=> This is a Single Choice Day of the Week question.')
            print('\t=> Provide the ID of the day you want to select.')
        else:
            print('\t=> Unknown display type (' + str(display_type) + ') for this Day of the Week question')
        if answer_status == 4:
            print('\t=> User selected answer is ' + str(question['answer']))
        elif default_answer:
            print("\t=> The answer is currently: '" + str(default_answer) + "'")
        else:
            question['defaultAnswer'] = 0
            print("\t=> The answer is currently: '0'")
        print('\n\n\tOptions:')
        print('\t[' + Color.GREEN + '1' + Color.END + '] : Sunday')
        print('\t[' + Color.GREEN + '2' + Color.END + '] : Monday')
        print('\t[' + Color.GREEN + '4' + Color.END + '] : Tuesday')
        print('\t[' + Color.GREEN + '8' + Color.END + '] : Wednesday')
        print('\t[' + Color.GREEN + '16' + Color.END + '] : Thursday')
        print('\t[' + Color.GREEN + '32' + Color.END + '] : Friday')
        print('\t[' + Color.GREEN + '64' + Color.END + '] : Saturday')
    elif question['responseType'] == BotEngine.QUESTION_RESPONSE_TYPE_SLIDER:
        slider_min = None
        slider_max = None
        slider_inc = None
        units = None
        if 'sliderMin' in question:
            slider_min = question['sliderMin']
        if 'sliderMax' in question:
            slider_max = question['sliderMax']
        if 'sliderInc' in question:
            slider_inc = question['sliderInc']
        if 'placeholder' in question:
            units = str(question['placeholder'])
        print('\t=> This is a Slider question.')
        if units:
            print('\t=> Description of the units of measurement: ' + str(units))
        print('\t=> Answer is a number between ' + str(slider_min) + ' and ' + str(slider_max) + ' in increments of ' + str(slider_inc) + '.')
        if display_type == BotEngine.QUESTION_DISPLAY_SLIDER_INTEGER:
            print('\t=> Answer will be an integer.')
        elif display_type == BotEngine.QUESTION_DISPLAY_SLIDER_FLOAT:
            print('\t=> Answer will be a floating point number.')
        elif display_type == BotEngine.QUESTION_DISPLAY_SLIDER_MINSEC:
            print('\t=> Answer will be in integer seconds.')
        else:
            print('\t=> Unknown display type (' + str(display_type) + ') for this Slider question')
        if answer_status == 4:
            print('\t=> User selected answer is ' + str(question['answer']))
        elif default_answer:
            print("\t=> The answer is currently: '" + str(default_answer) + "'")
        else:
            question['defaultAnswer'] = (slider_max - slider_min) / 2
            print("\t=> The answer is currently: '" + str(question['defaultAnswer']) + "'")
    elif question['responseType'] == BotEngine.QUESTION_RESPONSE_TYPE_TIME:
        if display_type == BotEngine.QUESTION_DISPLAY_TIME_HOURS_MINUTES_SECONDS_AMPM:
            print('\t=> This is a Time Since Midnight question, down to the second.')
            print('\t=> Answer will be in seconds since midnight.')
        elif display_type == BotEngine.QUESTION_DISPLAY_TIME_HOURS_MINUTES_AMPM:
            print('\t=> This is a Time Since Midnight question, down to the minute.')
            print('\t=> Answer will be in seconds since midnight, rounded to the nearest whole minute.')
        else:
            print('\t=> Unknown display type (' + str(display_type) + ') for this Time question')
        if answer_status == 4:
            print('\t=> User selected answer is ' + str(question['answer']))
        elif default_answer:
            print("\t=> The answer is currently: '" + str(default_answer) + "'")
        else:
            question['defaultAnswer'] = 43200
            print("\t=> The answer is currently: '43200'")
    elif question['responseType'] == BotEngine.QUESTION_RESPONSE_TYPE_DATETIME:
        if display_type == BotEngine.QUESTION_DISPLAY_DATETIME_DATE_AND_TIME:
            print('\t=> This is a Datetime question, including both date and time.')
            print('\t=> Answer will be of the form: YYYY-MM-DDThh:mm:ss[Z|(+|-)hh:mm]')
            if answer_status == 4:
                print('\t=> User selected answer is ' + str(question['answer']))
            elif default_answer:
                print("\t=> The answer is currently: '" + default_answer + "'")
            else:
                import pytz
                question['defaultAnswer'] = datetime.datetime.now(pytz.utc).isoformat()
                print('\t=> The answer is currently: ' + question['defaultAnswer'])
        elif display_type == BotEngine.QUESTION_DISPLAY_DATETIME_DATE:
            print('\t=> This is a Datetime question, with just the date and no time.')
            print('\t=> Answer will be of the form: YYYY-MM-DD')
            if answer_status == 4:
                print('\t=> User selected answer is ' + str(question['answer']))
            elif default_answer:
                print("\t=> The answer is currently: '" + default_answer + "'")
            else:
                question['defaultAnswer'] = datetime.datetime.today().strftime('%Y-%m-%d')
                print('\t=> The answer is currently: ' + question['defaultAnswer'])
        else:
            print('\t=> Unknown display type (' + str(display_type) + ') for this Datetime question')
    elif question['responseType'] == BotEngine.QUESTION_RESPONSE_TYPE_TEXT:
        print('\t=> This is an open-ended Text question.')
        if 'placeholder' in question:
            print("\t=> The placeholder in the text box says: '" + str(question['placeholder']) + "'")
        if answer_status == 4:
            print("\t=> User selected answer is '" + str(question['answer']) + "'")
        elif default_answer:
            print("\t=> The answer is currently: '" + default_answer + "'")
        else:
            print('\t=> The text box is blank.')
        print("\t=> Type any string response you'd like.")
    if 'deviceId' in question:
        print('\t=> deviceId is ' + str(question['deviceId']))
    if 'icon' in question:
        print('\t=> icon is ' + str(question['icon']))
    return


def _answer_question(server, user_key, question, answer, location_id=None):
    """
    Answer a question
    :param server: Server
    :param user_key: User Key
    :param question: Question JSON from the _get_questions API
    :param answer: Raw answer to provide
    """
    http_headers = {'API_KEY': user_key, 'Content-Type': 'application/json'}
    params = None
    if location_id is not None:
        params = {'locationId': location_id}
    body = {'questions': [
                   {'id': question['id'], 
                      'answer': answer}]}
    import requests
    r = requests.put(server + '/cloud/json/questions', headers=http_headers, data=json.dumps(body), params=params, proxies=_https_proxy)
    j = json.loads(r.text)
    _check_for_errors(j)
    return


def _create_logger(name, level, console_mode=False, filename=None):
    logger = logging.getLogger(name)
    logger.setLevel(level)
    fmt = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
    if filename is not None:
        f = logging.FileHandler(filename)
        f.setFormatter(fmt)
        logger.addHandler(f)
    if console_mode:
        console = logging.StreamHandler()
        console.setFormatter(fmt)
        logger.addHandler(console)
    if not console_mode and not filename:
        logger.addHandler(logging.NullHandler())
    return logger


def _download_only_get_newest_measurements(server, user_key, device_id, location_id=None, parameter_names=[], user_id=None):
    """
    This method will return the newest measurements from the given device

    @param device_id: Device ID
    @param parameter_names: Optional List of parameter name strings for which to download values
    """
    params = {'paramName': parameter_names}
    if location_id is not None:
        params['locationId'] = location_id
    if user_id:
        params['userId'] = user_id
    http_headers = {'API_KEY': user_key, 'Content-Type': 'application/json'}
    import requests
    r = requests.get(server + '/cloud/json/devices/' + device_id + '/parameters', params=params, headers=http_headers, proxies=_https_proxy)
    j = json.loads(r.text)
    _check_for_errors(j)
    return j


def _download_only_get_historical_measurements(server, user_key, device_id, start_date, end_date=None, parameter_names=[], parameter_index=None, aggregation_type=None, aggregation_interval=None, sort_collection=None, sort_by=None, row_count=None, sort_order=None, first_row=None, location_id=None, user_id=None):
    """
    This method will return historical measurements from the given device

    :param device_id: The exact device ID to send a command to. This is case-sensitive.
    :param start_date: startDate datetime
    :param end_date: Optional endDate datetime
    :param parameter_names: Optional List of parameter names for which to download values
    :param parameter_index: Optional parameter index
    :param aggregation_type: Option aggregation type, 8 = 'warm' data with 15 minute intervals (default); 9 = 'hot' data recently received from the device
    :param aggregation_interval: Optional, show readings aggregated by this interval
    :param sort_collection: Sort by a collection name (list name) which needs to be ordered or limited
    :param sort_by: The collection element property used for element comparisons in ordering, like 'timeStamp'
    :param sort_order: asc = Ascending; desc = Descending
    :param row_count: The number of collection elements to be returned
    :param first_row: The index of teh first collection element to be returned starting from zero. If it is not specified, the last rowCount elements will be returned
    :param user_id: User ID for administrators
    """
    params = {}
    if end_date is not None:
        params['endDate'] = end_date.strftime('%Y-%m-%dT%H:%M:%S')
    if len(parameter_names) > 0:
        params['paramName'] = parameter_names
    if parameter_index is not None:
        params['index'] = parameter_index
    if aggregation_type is not None:
        params['aggregation'] = aggregation_type
    if aggregation_interval is not None:
        params['interval'] = aggregation_interval
    if sort_collection is not None:
        params['sortCollection'] = sort_collection
    if sort_by is not None:
        params['sortBy'] = sort_by
    if row_count is not None:
        params['rowCount'] = row_count
    if sort_order is not None:
        params['sortOrder'] = sort_order
    if first_row is not None:
        params['firstRow'] = first_row
    if user_id is not None:
        params['userId'] = user_id
    if location_id is not None:
        params['locationId'] = location_id
    http_headers = {'API_KEY': user_key, 'Content-Type': 'application/json'}
    import requests
    r = requests.get(server + '/cloud/json/devices/' + device_id + '/parametersByDate/' + start_date.strftime('%Y-%m-%dT%H:%M:%S-00:00'), params=params, headers=http_headers, proxies=_https_proxy)
    j = json.loads(r.text)
    _check_for_errors(j)
    return j


def _download_modes_history_to_csv(server, user_key, location_id, start_date, oldest_first=False, destination_directory=None):
    """
    Download a history of this user's modes to CSV files
    :param server: Server to download from
    :param user_key: User key to download from
    :param location_id: User's location ID
    :param start_date: Datetime to start collecting data
    :param oldest_first: True to write the .csv file with oldest events first
    :param destination_directory: Destination directory
    :return: Filename
    """
    print('\t+ Downloading ...')
    data = _download_modes_history_data(server, user_key, location_id, start_date)
    filename = 'location_' + str(location_id) + '_modes_history.csv'
    if destination_directory is not None:
        filename = destination_directory + os.sep + filename
    f = open(filename, 'w')
    f.write('trigger,timestamp_ms,location_id,event,source_type,source_agent\n')
    if oldest_first:
        data['events'] = list(reversed(data['events']))
    if 'events' in data:
        for event in data['events']:
            source = None
            if 'sourceAgent' in event:
                source = event['sourceAgent'].replace(',', '_')
            f.write('2,' + str(event['eventDateMs']) + ',' + str(location_id) + ',' + str(event['event']) + ',' + str(event['sourceType']) + ',' + str(source) + '\n')

    f.close()
    print('\tSaved to: ' + filename + '\n')
    return filename


def _download_modes_history_data(server, user_key, location_id, start_date):
    """
    Download a history of this user's modes to CSV files
    :param server: Server to download from
    :param user_key: User key to download from
    :param location_id: User's location ID
    :param start_date: Datetime to start collecting data
    :return: data
    """
    http_headers = {'API_KEY': user_key, 'Content-Type': 'application/json'}
    params = {'startDate': start_date.strftime('%Y-%m-%dT%H:%M:%S-00:00')}
    import requests
    r = requests.get(server + '/cloud/json/location/' + str(location_id) + '/events', params=params, headers=http_headers, proxies=_https_proxy)
    j = json.loads(r.text)
    _check_for_errors(j)
    return j


def _downloaded_data_to_csv(server, user_key, start_date, device_id, device_type, device_name, location_id=None, user_id=None, oldest_first=False, destination_directory=None):
    """
    Download device data to .csv files
    :param server: server to connect with
    :param user_key: user key to download (could be an admin key)
    :param start_date: Datetime start date
    :param device_id: Download a single device - device ID to download
    :param device_type: Download all devices matching the type
    :param device_name: Name of the device
    :param user_id: User ID to download from if we're downloading as an administrator
    :param oldest_first: True to write the oldest records first to the .csv file
    :param destination_directory: Default is the current working directory, otherwise put it in this relative directory
    :return: List of filenames created
    """
    titles = set([])
    last_measurements = {}
    filenames = []
    try:
        data = _download_only_get_newest_measurements(server, user_key, device_id, location_id=location_id, user_id=user_id)
    except:
        return []
    else:
        try:
            device = data['devices'][0]
        except:
            print('No data for device ' + str(device_id))
            return []

    for p in device['parameters']:
        if 'name' in p and 'value' in p:
            titles.add(p['name'])
            last_measurements[p['name']] = p['value']

    titles = sorted(titles)
    output = 'trigger,device_type,device_id,description,timestamp_ms,timestamp_iso,timestamp_excel,'
    for t in titles:
        output = output + t + ','

    output = output + '\n'
    print('\t+ Downloading ...')
    readings = _download_only_get_historical_measurements(server, user_key, device_id, start_date, location_id=location_id, user_id=user_id)
    if 'readings' not in readings:
        print('\t- No readings\n')
    else:
        print('\t+ Processing ' + str(len(readings['readings'])) + ' readings ...')
        device_name = device_name.strip()
        original_device_name = device_name
        import re
        device_name = re.sub('[^0-9a-zA-Z]+', '-', device_name)
        if device_type is not None:
            filename = str(device_type) + '_' + device_id + '_' + device_name + '.csv'
        else:
            filename = device_id + '_' + device_name + '.csv'
        if user_id is not None:
            filename = str(device_type) + '_user' + str(user_id) + '_' + device_id + '_' + device_name.strip().replace(' ', '-') + '.csv'
        if destination_directory is not None:
            filename = destination_directory + os.sep + filename
        filenames.append(filename)
        f = open(filename, 'w')
        f.write(output)
        if oldest_first:
            readings['readings'] = list(reversed(readings['readings']))
        for r in readings['readings']:
            ts = datetime.datetime.fromtimestamp(int(r['timeStampMs']) / 1000.0).strftime('%m/%d/%Y %H:%M:%S')
            line = '8,' + str(device_type) + ',' + str(device_id) + ',' + str(original_device_name) + ',' + str(r['timeStampMs']) + ',' + str(r['timeStamp']) + ',' + ts + ','
            focused_dict = {}
            for p in r['params']:
                focused_dict[p['name']] = str(p['value'])
                last_measurements[p['name']] = str(p['value'])

            for t in titles:
                if t in focused_dict:
                    line = line + focused_dict[t] + ','
                else:
                    line = line + last_measurements[t].encode('utf-8').replace(',', '_') + ','

            f.write(line + '\n')

        f.close()
        print('\tSaved to: ' + filename + '\n')
    return filenames


def _get_bot_errors(server, user_key, bundle, errors_only=True, developer=False):
    """
    Get a list of errors that all users have experienced running your bot
    :param server: Server to use
    :param user_key: Developer user key
    :param bundle: Bot bundle ID
    :param errors_only: True to get errors only, False to get all logs (default is True)
    :return: JSON structure with all the errors
    """
    http_headers = {'API_KEY': user_key, 
       'Content-Type': 'application/json'}
    params = {'failuresOnly': errors_only, 
       'bundle': bundle, 
       'developer': developer}
    import requests
    r = requests.get(server + '/cloud/developer/logs', params=params, headers=http_headers, proxies=_https_proxy)
    j = json.loads(r.text)
    _check_for_errors(j)
    return j


def the_bot():
    """
    :return: the bot \xf0\x9f\xa4\x96 if our local machine supports it
    """
    import platform
    if platform.system() == 'Darwin':
        mac_version_string = platform.mac_ver()[0]
        mac_version_array = mac_version_string.split('.')
        if mac_version_array[0] >= 10 and mac_version_array[1] >= 7:
            return '\xf0\x9f\xa4\x96   '
    return ''


def cli_progress_bar(iteration, total, prefix='', suffix='', decimals=1, length=100, fill='\xe2\x96\x88'):
    """
    Quick copy/paste from https://stackoverflow.com/questions/3173320/text-progress-bar-in-the-console
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
    """
    percent = ('{0:.' + str(decimals) + 'f}').format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end='\r')
    if iteration == total:
        print()


def _run_locally_forever(bot_server, device_server, user_key, bot, bot_instance_id):
    """Run the bot locally forever, using HTTP long polling to listen for real-time streaming data from the server
    :param bot_server: Application server for bots
    :param device_server: Device Server URL
    :param user_key: User's /cloud API key
    :param bot: The imported bot module to call the run method within
    :param bot_instance_id: The specific bot instance ID we're executing against on the server
    """
    import traceback
    cleanTime = None
    while True:
        try:
            inputs = _listen(device_server, user_key, bot_instance_id, cleanTime=cleanTime, clean=False)
            if inputs:
                if 'apiKey' not in inputs:
                    pass
                else:
                    try:
                        _run(bot, inputs, _bot_logger, server_override=bot_server)
                    except Exception as e:
                        print('Bot Exception: \n', e)
                        traceback.print_exc()
                    else:
                        try:
                            cleanTime = int(inputs['inputs'][(len(inputs['inputs']) - 1)]['time'])
                        except Exception as e:
                            cleanTime = None

        except:
            pass

    return


def _run(bot, inputs, logger, server_override=None, botengine_override=None):
    """
    Run the given bot with the given parameters
    :param bot: bot to run
    :param inputs: the input JSON from the bot server
    :param logger: logger object
    :param server_override: Override the server URL with the known server when executing on someone's computer
    :param botengine_override: For playback simulators, override the botengine object
    """
    global _bot_logger
    _bot_logger = logger
    next_timer_at_server = None
    if botengine_override is None:
        services = None
        if 'services' in inputs:
            services = inputs['services']
        count = None
        if 'count' in inputs:
            count = int(inputs['count'])
        if 'timer' in inputs:
            next_timer_at_server = int(inputs['timer'])
        lang = None
        if 'lang' in inputs:
            lang = inputs['lang']
        cloud = None
        if 'cloud' in inputs:
            cloud = inputs['cloud']
        botengine = BotEngine(inputs, server_override=server_override, services=services, lang=lang, count=count, cloud=cloud)
    else:
        botengine = botengine_override
    botengine.start_time_sec = time.time()
    botengine._download_core_variables()
    botengine.load_variables_time_sec = time.time()
    for server in botengine._servers:
        if 'sbox' in server:
            botengine._validate_count()
            break

    all_triggers = []
    for i in inputs['inputs']:
        all_triggers.append(i['trigger'])

    botengine.all_trigger_types = all_triggers
    timers_existed = False
    botengine.triggers_total = len(all_triggers)
    for execution_json in inputs['inputs']:
        botengine.triggers_index += 1
        trigger = execution_json['trigger']
        if trigger > 0:
            botengine._set_inputs(execution_json)
            if trigger != 2048:
                saved_timers = botengine.load_variable(TIMERS_VARIABLE_NAME)
                if saved_timers is not None:
                    timers_existed |= len(saved_timers) > 1
                    for t in [ x[0] for x in saved_timers ]:
                        if t != MAXINT and t <= execution_json['time']:
                            focused_timer = saved_timers.pop(0)
                            botengine.all_trigger_types.append(64)
                            if callable(focused_timer[1]):
                                focused_timer[1](botengine, focused_timer[2])
                            else:
                                botengine.get_logger().error('BotEngine: Timer fired and popped, but cannot call the focused timer: ' + str(focused_timer))
                        else:
                            break

                    botengine.save_variable(TIMERS_VARIABLE_NAME, botengine.load_variable(TIMERS_VARIABLE_NAME))
            if trigger != 64:
                bot.run(botengine)
            elif saved_timers is not None and not timers_existed:
                botengine.get_logger().error('BotEngine: Timer fired but no recollection as to why.')
                botengine.get_logger().error('Current timer variable is: ' + str(saved_timers))
            botengine.flush_commands()
            botengine.flush_questions()

    botengine.flush_analytics()
    botengine.flush_binary_variables()
    if trigger != 2048:
        saved_timers = botengine.load_variable(TIMERS_VARIABLE_NAME)
        if saved_timers is not None and len(saved_timers) > 0:
            while True:
                try:
                    if saved_timers[0][0] != MAXINT:
                        if saved_timers[0][0] != next_timer_at_server:
                            botengine._execute_again_at_timestamp(saved_timers[0][0])
                            botengine.get_logger().info(('< Set alarm: {}').format(saved_timers[0]))
                        else:
                            botengine.get_logger().info(('| Alarm already set: {}').format(saved_timers[0]))
                    break
                except Exception as e:
                    botengine.get_logger().error(('Could not _execute_again_at_timestamp to set timer: {}').format(str(e)))
                    continue

    botengine.flush_rules()
    botengine.flush_tags()
    botengine.flush_asynchronous_requests()
    return


class BotEngine():
    """This BotEngine class runs your bot and connects to the Bot Server"""
    TRIGGER_NEW_VERSION = 0
    TRIGGER_SCHEDULE = 1
    TRIGGER_MODE = 2
    TRIGGER_DEVICE_ALERT = 4
    TRIGGER_DEVICE_MEASUREMENT = 8
    TRIGGER_QUESTION_ANSWER = 16
    TRIGGER_DEVICE_FILES = 32
    TRIGGER_METADATA = 128
    TRIGGER_DATA_STREAM = 256
    TRIGGER_COMMAND_RESPONSE = 512
    TRIGGER_LOCATION_CONFIGURATION = 1024
    TRIGGER_DATA_REQUEST = 2048
    ACCESS_CATEGORY_MODE = 1
    ACCESS_CATEGORY_FILE = 2
    ACCESS_CATEGORY_PROFESSIONAL_MONITORING = 3
    ACCESS_CATEGORY_DEVICE = 4
    ACCESS_CATEGORY_CHALLENGE = 5
    QUESTION_RESPONSE_TYPE_BOOLEAN = 1
    QUESTION_RESPONSE_TYPE_MULTICHOICE_SINGLESELECT = 2
    QUESTION_RESPONSE_TYPE_MULTICHOICE_MULTISELECT = 4
    QUESTION_RESPONSE_TYPE_DAYOFWEEK = 6
    QUESTION_RESPONSE_TYPE_SLIDER = 7
    QUESTION_RESPONSE_TYPE_TIME = 8
    QUESTION_RESPONSE_TYPE_DATETIME = 9
    QUESTION_RESPONSE_TYPE_TEXT = 10
    QUESTION_DISPLAY_BOOLEAN_ONOFF = 0
    QUESTION_DISPLAY_BOOLEAN_YESNO = 1
    QUESTION_DISPLAY_BOOLEAN_BUTTON = 2
    QUESTION_DISPLAY_MCSS_RADIO_BUTTONS = 0
    QUESTION_DISPLAY_MCSS_PICKER = 1
    QUESTION_DISPLAY_DAYOFWEEK_MULTISELECT = 0
    QUESTION_DISPLAY_DAYOFWEEK_SINGLESELECT = 1
    QUESTION_DISPLAY_SLIDER_INTEGER = 0
    QUESTION_DISPLAY_SLIDER_FLOAT = 1
    QUESTION_DISPLAY_SLIDER_MINSEC = 2
    QUESTION_DISPLAY_TIME_HOURS_MINUTES_SECONDS_AMPM = 0
    QUESTION_DISPLAY_TIME_HOURS_MINUTES_AMPM = 1
    QUESTION_DISPLAY_DATETIME_DATE_AND_TIME = 0
    QUESTION_DISPLAY_DATETIME_DATE = 1
    ANSWER_STATUS_NOT_ASKED = -1
    ANSWER_STATUS_DELAYED = 0
    ANSWER_STATUS_QUEUED = 1
    ANSWER_STATUS_AVAILABLE = 2
    ANSWER_STATUS_SKIPPED = 3
    ANSWER_STATUS_ANSWERED = 4
    ANSWER_STATUS_NO_ANSWER = 5
    PROFESSIONAL_MONITORING_NEVER_PURCHASED = 0
    PROFESSIONAL_MONITORING_PURCHASED_BUT_NOT_ENOUGH_INFO = 1
    PROFESSIONAL_MONITORING_REGISTRATION_PENDING = 2
    PROFESSIONAL_MONITORING_REGISTERED = 3
    PROFESSIONAL_MONITORING_CANCELLATION_PENDING = 4
    PROFESSIONAL_MONITORING_CANCELLED = 5
    PROFESSIONAL_MONITORING_ALERT_STATUS_QUIET = 0
    PROFESSIONAL_MONITORING_ALERT_STATUS_RAISED = 1
    PROFESSIONAL_MONITORING_ALERT_STATUS_CANCELLED = 2
    PROFESSIONAL_MONITORING_ALERT_STATUS_REPORTED = 3
    RULE_STATUS_INCOMPLETE = 0
    RULE_STATUS_ACTIVE = 1
    RULE_STATUS_INACTIVE = 2
    DATASTREAM_ORGANIZATIONAL_FIELD_TO_INDIVIDUALS = 1
    DATASTREAM_ORGANIZATIONAL_FIELD_TO_ORGANIZATIONS = 2
    DATASTREAM_ORGANIZATIONAL_FIELD_TO_ALL = 3
    NARRATIVE_PRIORITY_DEBUG = 0
    NARRATIVE_PRIORITY_DETAIL = 0
    NARRATIVE_PRIORITY_INFO = 1
    NARRATIVE_PRIORITY_WARNING = 2
    NARRATIVE_PRIORITY_CRITICAL = 3

    def __init__(self, raw_inputs, server_override=None, services=None, lang=None, count=None, cloud=None):
        """
        Constructor
        :param raw_inputs: The entire input JSON string from the Bot Server
        :param server_override: Option to override the server URL when executing on someone's computer instead of in the cloud
        :param services: List of subscription services in the user's account
        :param lang: User's selected language
        :param count: Each time the bot triggers, the count should increment by 1 when running on the server. The count is always 0 when running locally on a computer.
        :param cloud: Description of the cloud server
        """
        self.__key = raw_inputs['apiKey']
        del raw_inputs['apiKey']
        if server_override is not None:
            self._servers = [
             server_override]
        elif 'apiHosts' in raw_inputs:
            self._servers = raw_inputs['apiHosts']
        else:
            self._servers = [
             raw_inputs['apiHost']]
        self._raw_inputs = raw_inputs
        self._server_index = 0
        self._requests = importlib.import_module('requests')
        self._cloud = cloud
        self.services = services
        self.all_trigger_types = []
        self.count = count
        self.variables = {}
        self.variables_to_flush = {}
        self.question_answered = None
        self.commands_to_flush = {}
        self.data_requests = []
        self.tags_to_create = []
        self.tags_to_delete = []
        self.tags_to_create_by_user = {}
        self.tags_to_delete_by_user = {}
        self.rules = {}
        self.questions_to_ask = {}
        self.questions_to_delete = {}
        self.cancelled_timers = False
        self.lang = lang
        self.triggers_total = 0
        self.triggers_index = 0
        self._location_users_cache = None
        if 'startKey' in raw_inputs:
            if raw_inputs['startKey'] != 0:
                self._start(raw_inputs['startKey'])
        return

    def _http_get(self, path, headers={}, params=None, timeout=5, stream=False):
        """
        HTTP GET
        :param path: Path to retrieve
        :param headers: Dictionary of headers, which will override any default headers
        :param params: Dictionary of parameters
        :param timeout: Timeout in seconds, default is 5
        :param stream: True to stream. Default is False.
        :return: Response object from Requests module
        """
        h = self._build_common_headers()
        h.update(headers)
        while True:
            try:
                r = self._requests.get(self._servers[self._server_index] + path, params=params, headers=h, timeout=timeout, proxies=_https_proxy, stream=stream)
                return r
            except self._requests.HTTPError:
                self.get_logger().error('Generic HTTP error calling GET ' + str(self._servers[self._server_index] + path))
                self._server_index += 1
                self._server_index %= len(self._servers)
            except self._requests.ConnectionError:
                self.get_logger().error('Connection HTTP error calling GET ' + str(self._servers[self._server_index] + path))
                self._server_index += 1
                self._server_index %= len(self._servers)
            except self._requests.Timeout:
                timeout += 10
                if timeout >= 30:
                    raise self._requests.Timeout()
                self._server_index += 1
                self._server_index %= len(self._servers)
            except self._requests.TooManyRedirects:
                self.get_logger().error('Too many redirects HTTP error calling GET ' + str(self._servers[self._server_index] + path))
                self._server_index += 1
                self._server_index %= len(self._servers)
            except Exception:
                self.get_logger().error('Generic HTTP exception calling GET ' + str(self._servers[self._server_index] + path))
                self._server_index += 1
                self._server_index %= len(self._servers)

    def _http_post(self, path, headers={}, params=None, data=None, timeout=5):
        """
        HTTP POST
        :param path: Path to retrieve
        :param headers: Dictionary of headers, which will override any default headers
        :param params: Dictionary of parameters
        :param data: Data to POST
        :param timeout: Timeout in seconds, default is 5
        :return: Response object from Requests module
        """
        h = self._build_common_headers()
        h.update(headers)
        while True:
            try:
                r = self._requests.post(self._servers[self._server_index] + path, params=params, headers=h, data=data, timeout=timeout, proxies=_https_proxy)
                return r
            except self._requests.HTTPError:
                self.get_logger().error('Generic HTTP error calling POST ' + str(self._servers[self._server_index] + path))
                self._server_index += 1
                self._server_index %= len(self._servers)
            except self._requests.ConnectionError:
                self.get_logger().error('Connection HTTP error calling POST ' + str(self._servers[self._server_index] + path))
                self._server_index += 1
                self._server_index %= len(self._servers)
            except self._requests.Timeout:
                self.get_logger().error(str(timeout) + ' second HTTP Timeout calling POST ' + str(self._servers[self._server_index] + path))
                timeout += 5
                if timeout >= 25:
                    raise self._requests.Timeout()
                self._server_index += 1
                self._server_index %= len(self._servers)
            except self._requests.TooManyRedirects:
                self.get_logger().error('Too many redirects HTTP error calling POST ' + str(self._servers[self._server_index] + path))
                self._server_index += 1
                self._server_index %= len(self._servers)
            except Exception:
                self.get_logger().error('Generic HTTP exception calling POST ' + str(self._servers[self._server_index] + path))
                self._server_index += 1
                self._server_index %= len(self._servers)

    def _http_put(self, path, headers={}, params=None, data=None, timeout=5):
        """
        HTTP PUT
        :param path: Path to retrieve
        :param headers: Dictionary of headers, which will override any default headers
        :param params: Dictionary of parameters
        :param data: Data to PUT
        :param timeout: Timeout in seconds, default is 5
        :return: Response object from Requests module
        """
        h = self._build_common_headers()
        h.update(headers)
        while True:
            try:
                r = self._requests.put(self._servers[self._server_index] + path, params=params, headers=h, data=data, timeout=timeout, proxies=_https_proxy)
                return r
            except self._requests.HTTPError:
                self.get_logger().error('Generic HTTP error calling PUT ' + str(self._servers[self._server_index] + path))
                self._server_index += 1
                self._server_index %= len(self._servers)
            except self._requests.ConnectionError:
                self.get_logger().error('Connection HTTP error calling PUT ' + str(self._servers[self._server_index] + path))
                self._server_index += 1
                self._server_index %= len(self._servers)
            except self._requests.Timeout:
                self.get_logger().error(str(timeout) + ' second HTTP Timeout calling PUT ' + str(self._servers[self._server_index] + path))
                timeout += 5
                if timeout >= 25:
                    raise self._requests.Timeout()
                self._server_index += 1
                self._server_index %= len(self._servers)
            except self._requests.TooManyRedirects:
                self.get_logger().error('Too many redirects HTTP exception calling PUT ' + str(self._servers[self._server_index] + path))
                self._server_index += 1
                self._server_index %= len(self._servers)
            except Exception:
                self.get_logger().error('Generic HTTP exception calling PUT ' + str(self._servers[self._server_index] + path))
                self._server_index += 1
                self._server_index %= len(self._servers)

    def _http_delete(self, path, headers={}, params=None, timeout=5):
        """
        HTTP PUT
        :param path: Path to retrieve
        :param headers: Dictionary of headers, which will override any default headers
        :param params: Dictionary of parameters
        :param data: Data to PUT
        :param timeout: Timeout in seconds, default is 5
        :return: Response object from Requests module
        """
        h = self._build_common_headers()
        h.update(headers)
        while True:
            try:
                r = self._requests.delete(self._servers[self._server_index] + path, params=params, headers=h, timeout=timeout, proxies=_https_proxy)
                return r
            except self._requests.HTTPError:
                self.get_logger().error('Generic HTTP error calling DELETE ' + str(self._servers[self._server_index] + path))
                self._server_index += 1
                self._server_index %= len(self._servers)
            except self._requests.ConnectionError:
                self.get_logger().error('Connection HTTP error calling DELETE ' + str(self._servers[self._server_index] + path))
                self._server_index += 1
                self._server_index %= len(self._servers)
            except self._requests.Timeout:
                self.get_logger().error(str(timeout) + ' second HTTP Timeout calling DELETE ' + str(self._servers[self._server_index] + path))
                timeout += 5
                if timeout >= 25:
                    raise self._requests.Timeout()
                self._server_index += 1
                self._server_index %= len(self._servers)
            except self._requests.TooManyRedirects:
                self.get_logger().error('Too many redirects HTTP error calling DELETE ' + str(self._servers[self._server_index] + path))
                self._server_index += 1
                self._server_index %= len(self._servers)
            except Exception:
                self.get_logger().error('Generic HTTP exception calling DELETE ' + str(self._servers[self._server_index] + path))
                self._server_index += 1
                self._server_index %= len(self._servers)

    def _set_inputs(self, inputs):
        """
        Set the inputs for this execution
        :param inputs: Inputs for this next execution
        """
        self.inputs = inputs
        if self.inputs['trigger'] == BotEngine.TRIGGER_QUESTION_ANSWER:
            question_block = self.inputs['question']
            saved_questions = self.load_variable(QUESTIONS_VARIABLE_NAME)
            if saved_questions is not None:
                if question_block['key'] in saved_questions:
                    self.question_answered = saved_questions[question_block['key']]
                    self.question_answered.answer_time = question_block['answerTime']
                    if self.question_answered.response_type == BotEngine.QUESTION_RESPONSE_TYPE_BOOLEAN:
                        try:
                            self.question_answered.answer = bool(int(question_block['answer']))
                        except:
                            self.question_answered.answer = question_block['answer']

                    else:
                        self.question_answered.answer = question_block['answer']
        return

    def _enable_debug(self):
        """
        Enable debug logging
        """
        logging.basicConfig()
        logging.getLogger().setLevel(logging.DEBUG)
        requests_log = logging.getLogger('requests.packages.urllib3')
        requests_log.setLevel(logging.DEBUG)
        requests_log.propagate = True

    def _build_common_headers(self, content_type='application/json'):
        """
        Build common HTTP headers for API calls
        :param content_type: Content type of the request, default is 'application/json'
        :return: HTTP Header dictionary to inject into HTTP requests
        """
        return {'ANALYTIC_API_KEY': self.__key, 
           'Content-Type': content_type, 
           'User-Agent': 'BotEngine/' + str(__version__)}

    def _start(self, start_key):
        """
        Called once at the start of execution to prevent 2 bots of the same instance from executing in parallel.
        :param start_key:
        :return:
        """
        params = {'startKey': start_key}
        r = self._http_post('/analytic/start', params=params)
        j = json.loads(r.text)
        _check_for_errors(j)
        return j

    def get_inputs(self):
        """
        This method will return the inputs, e.g. apiKey, apiHost, trigger type, alerts, measurement blocks
        :return: all inputs in a JSON dictionary format
        """
        return self.inputs

    def get_trigger_type(self):
        """
        This method will return the type of trigger that your bot uses
        * Trigger 1 = Schedule (based off a cron schedule inside the runtime.json file)
        * Trigger 2 = Location Event (switching between home / away / etc.)
        * Trigger 4 = Device Alert
        * Trigger 8 = Device Measurements
        * Trigger 16 = Question Answered
        * Trigger 32 = New device file (like a video or picture)
        * Trigger 64 = Execute Again Countdown Timer
        * Trigger 256 = Data Stream Message
        
        :return: Trigger type that triggered this bot
        """
        return int(self.inputs['trigger'])

    def get_triggers(self):
        """
        This method will find and return the information about what triggered this bot.
        
        Location Events (Modes) Example:
          {
            'category':1,
            'control':True,
            'trigger':True,
            'location':{
               'locationId':62,
               'prevEvent':'HOME',
               'event':'AWAY'
            },
            'read':True
          }

        Device Measurements Example:
          {
            'trigger':True,
            'device':{
              'deviceType':10014,
               'updateDate':1465517032000,
               'deviceId':'FFFFFFFF00600a70',
               'description':'Practice\xa0Entry\xa0Sensor',
               'measureDate':1465517031000
            },
            'read':True,
            'control':True,
            'category':4
          }
          
        :return: JSON structure describing what triggered this bot
        """
        if 'access' not in self.inputs:
            return []
        self.trigger_blocks = []
        for block in self.inputs['access']:
            if 'trigger' in block:
                if block['trigger']:
                    self.trigger_blocks.append(block)

        return self.trigger_blocks

    def get_measures_block(self):
        """
        :return: the measurements block from our inputs, if any
        """
        if 'measures' in self.inputs:
            return self.inputs['measures']
        else:
            return

    def get_alerts_block(self):
        """
        :return: the alerts block from our inputs, if any
        """
        if 'alerts' in self.inputs:
            return self.inputs['alerts']
        else:
            return

    def get_access_block(self):
        """
        :return: the access block from our inputs, if any
        """
        if 'access' in self.inputs:
            return self.inputs['access']
        else:
            return

    def get_device_access_block(self, device_id):
        """
        Return the access block for a specific device
        :param device_id: Device ID to search for
        :return: Access block for a specific device, None if it doesn't exist
        """
        if 'access' in self.inputs:
            for a in self.inputs['access']:
                if a['category'] == BotEngine.ACCESS_CATEGORY_DEVICE:
                    if 'device' in a:
                        if a['device']['deviceId'] == device_id:
                            return a

        return

    def is_executing_timer(self):
        """
        :return: True if this execution includes a timer fire
        """
        return 64 in self.all_trigger_types

    def get_location_id(self):
        """
        :return: The location ID for this bot
        """
        return self.inputs['locationId']

    def get_location_info(self):
        """
        Returns this information:
            {
              "category": 1,
              "control": true,
              "location": {
                "event": "STAY",
                "latitude": "47.72328",
                "locationId": 755735,
                "longitude": "-122.17426",
                "name": "Apartment 103",
                "timezone": {
                  "dst": true,
                  "id": "US/Pacific",
                  "name": "Pacific Standard Time",
                  "offset": -480
                },
                "zip": "98034"
              },
              "read": true,
              "trigger": false
            }

        :param location_id: Location ID to extract
        :return: location information from the access block
        """
        for access in self.inputs['access']:
            if access['category'] == self.ACCESS_CATEGORY_MODE:
                return access

        return

    def get_location_name(self):
        """
        :return: Name of this location
        """
        location_info = self.get_location_info()
        if 'location' not in location_info:
            return 'Home'
        if 'name' not in location_info['location']:
            return 'Home'
        return location_info['location']['name'].encode('utf-8')

    def get_location_latitude(self):
        """
        :return: Location latitude, or None if it doesn't exist
        """
        location_info = self.get_location_info()
        if 'location' not in location_info:
            return None
        else:
            if 'latitude' not in location_info['location']:
                return None
            return float(location_info['location']['latitude'])

    def get_location_longitude(self):
        """
        :return: Location longitude, or None if it doesn't exist
        """
        location_info = self.get_location_info()
        if 'location' not in location_info:
            return None
        else:
            if 'longitude' not in location_info['location']:
                return None
            return float(location_info['location']['longitude'])

    def get_answered_question(self):
        """
        :return: the question that has been answered, if any
        """
        return self.question_answered

    def get_datastream_block(self):
        """
        :return: the data stream inputs, if any
        """
        if 'dataStream' in self.inputs:
            return self.inputs['dataStream']
        else:
            return

    def get_file_block(self):
        """
        :return: the 'file' block for an uploaded file, if any
        """
        if 'file' in self.inputs:
            return self.inputs['file']
        else:
            return

    def get_timestamp(self):
        """
        :return: the Unix timestamp of this execution, in milliseconds
        """
        return self.inputs['time']

    def get_data_stream_message(self):
        """
        :return: the data stream message
        """
        if 'dataStream' in self.inputs:
            return self.inputs['dataStream']
        else:
            return

    def get_users_block(self):
        """
        :return: The 'users' block for location configuration triggers
        """
        if 'users' in self.inputs:
            return self.inputs['users']
        else:
            return

    def get_data_block(self):
        """
        :return: The 'data' block for asynchronous data request inputs
        """
        if 'data' in self.inputs:
            return self.inputs['data']
        else:
            return

    def get_property(self, obj_arr, property_name, property_value, return_property_name):
        """
        This method will locate the specified first object from object array, and then return the specified property value

        :param obj_arr: object array
        :param property_name: the key in searching criteria
        :param property_value: the value in searching criteria
        :param return_property_name: the key in the object indicates which corresponding value will be returned
        """
        response = None
        for item in obj_arr:
            if item[property_name] == property_value:
                response = item[return_property_name]
                break

        return response

    def get_language(self):
        """
        :return: user's selected language
        """
        return self.lang

    def get_server_version(self):
        """
        Get the server version number, if it exists
        :return: Server version number
        """
        if 'version' in self._raw_inputs:
            return float(self._raw_inputs['version'])
        return 0

    def get_location_users(self):
        """
        Get the list of users at this location ID
        https://iotapps.docs.apiary.io/#reference/user-accounts/location-users/get-location-users
        :param location_id: Location ID
        """
        if self._location_users_cache is not None:
            return self._location_users_cache
        else:
            r = self._http_get(('/cloud/json/location/{}/users').format(self.get_location_id()))
            j = json.loads(r.text)
            _check_for_errors(j)
            if 'users' in j:
                self._location_users_cache = j['users']
                return j['users']
            self._location_users_cache = []
            return []
            return

    def get_resident_last_names(self):
        """
        Return a string that represents the resident's last names.
        If there are no last names, it returns ""
        If there is one last name, that last name is returned.
        If there are two or more last names like Moss and Neufeld then "Moss/Neufeld" is returned.
        :return: String representing location residents' last names.
        """
        last_name = ''
        first = True
        users = self.get_location_users()
        last_names_list = []
        for user in users:
            if user['category'] == 1:
                if 'lastName' in user:
                    if first:
                        first = False
                        last_name = user['lastName']
                        last_names_list.append(user['lastName'].lower().strip())
                    elif user['lastName'].lower().strip() not in last_names_list and user['lastName'].strip() != '':
                        last_name += ('/{}').format(user['lastName'])
                        last_names_list.append(user['lastName'].lower().strip())

        return last_name

    def get_location_user_names(self, to_residents=True, to_supporters=True, sms_only=True):
        """
        Get a list of users' names associated with the location.

        [
          {
            'firstName': 'David'
            'lastName': 'Moss'
          },
          ...
        ]

        :param residents: Extract residents
        :param supporters: Extract supporters
        :param sms_only: True if we only want to extract users who we can SMS
        :return: List of dictionaries containing first and last names
        """
        names = []
        users = self.get_location_users()
        if len(users) > 0:
            for user in users:
                if to_residents and user['category'] == 1 or to_supporters and user['category'] == 2:
                    if sms_only:
                        if 'smsStatus' in user:
                            if user['smsStatus'] == 3:
                                continue
                        if 'phoneType' in user:
                            if user['phoneType'] != 1:
                                continue
                    name = {'firstName': None, 
                       'lastName': None}
                    if 'firstName' in user:
                        name['firstName'] = user['firstName']
                    if 'lastName' in user:
                        name['lastName'] = user['lastName']
                    names.append(name)

            return names
        return []

    def get_name_by_user_id(self, user_id):
        """
        Returns a dictionary with 'firstName' and 'lastName' if the user exists, or None if the user doesn't exist
        :param user_id: User ID to extract the name
        :return: { 'firstName': "David", 'lastName': "Moss" }
        """
        users = self.get_location_users()
        for user in users:
            if int(user['id']) == int(user_id):
                name = {'firstName': '', 'lastName': ''}
                if 'firstName' in user:
                    name['firstName'] = user['firstName']
                if 'lastName' in user:
                    name['lastName'] = user['lastName']
                return name

        return

    def get_organization_locations(self, organization_id):
        """
        Get a list of locations within an organization, as a bot with admin priviledges
        :param organization_id:
        :return:
        """
        params = {'organizationId': organization_id}
        r = self._http_get('/admin/json/locations', params=params)
        j = json.loads(r.text)

    def save_variable(self, name, value, required_for_each_execution=False):
        """
        This method will cache a single variable to be saved to the cloud upon flush_variables()
        BotEngine will always flush variables to the cloud at the end of executing the bot.
        
        We use 'dill' to serialize data. Dill is a form of 'pickle', but can also store things like nested objects
        According to https://docs.python.org/3/library/pickle.html, the following can be pickled:
            * None, True, and False
            * integers, floating point numbers, complex numbers
            * strings, bytes, bytearrays
            * tuples, lists, sets, and dictionaries containing only picklable objects
            * functions defined at the top level of a module (using def, not lambda)
            * built-in functions defined at the top level of a module
            * classes that are defined at the top level of a module
            * instances of such classes whose __dict__ or the result of calling __getstate__() is
              picklable (see section Pickling Class Instances for details).
        
        :param name: Custom name of the variable to persist to the cloud
        :param value: Value of the variable to persist to the cloud
        :param required_for_each_execution: Set to True if this variable is required for every execution to increase performance. Setting to True without using this variable on every execution may decrease performance.
        """
        if name in self.variables[CORE_VARIABLE_NAME]:
            required_for_each_execution = True
        self.save_variables({name: value}, required_for_each_execution)

    def save_variables(self, variables_dictionary, required_for_each_execution=False):
        """
        This method will cache multiple variables from a dictionary to be saved to the cloud upon flush_variables()
        BotEngine will always flush variables to the cloud at the end of executing the bot.
        
        :param variables_dictionary: Dictionary of {name:value} variables to persist to the cloud
        :param required_for_each_execution: Set to True if this variable is required for every execution to increase performance. Setting to True without using this variable on every execution may decrease performance.
        """
        if required_for_each_execution:
            self.variables[CORE_VARIABLE_NAME].update(variables_dictionary)
            self.variables_to_flush[CORE_VARIABLE_NAME] = self.variables[CORE_VARIABLE_NAME]
        else:
            self.variables_to_flush.update(variables_dictionary)
            self.variables.update(variables_dictionary)

    def load_variable(self, name):
        """
        Extract a single variable
        :param name: Name of the variable to load
        :return: the value of the given variable name
        """
        if name in self.variables[CORE_VARIABLE_NAME]:
            return self.variables[CORE_VARIABLE_NAME][name]
        else:
            if name in self.variables:
                return self.variables.get(name)
            self._download_binary_variable(name)
            return self.variables.get(name)

    def load_variables(self, names):
        """
        Download and return a list of variables
        :param names: List of variable names to download and return
        :return: Dictionary of variable names and values
        """
        for name in names:
            if self.variables.get(name) is None:
                self._download_binary_variable(name)

        return_values = {}
        for name in names:
            return_values[name] = self.variables.get(name)

        return return_values

    def delete_variable(self, name):
        """
        Delete a variable from the cloud
        :param name: Name of the variable to delete at the cloud
        """
        self._http_delete('/analytic/variables/' + urllib.quote_plus(str(name)))
        try:
            del self.variables[name]
        except:
            pass
        else:
            try:
                del self.variables_to_flush[name]
            except:
                pass

    def flush_binary_variables(self):
        """
        This method will pickle and save multiple variables from the local variables cache to the cloud.
        It is always automatically called by the BotEngine at the end of bot execution.
        You do not need to call this manually.

        :param variables_dictionary: Dictionary of {name:value} variables to persist to the cloud

        According to https://docs.python.org/3/library/pickle.html, the following can be pickled:
            * None, True, and False
            * integers, floating point numbers, complex numbers
            * strings, bytes, bytearrays
            * tuples, lists, sets, and dictionaries containing only picklable objects
            * functions defined at the top level of a module (using def, not lambda)
            * built-in functions defined at the top level of a module
            * classes that are defined at the top level of a module
            * instances of such classes whose __dict__ or the result of calling __getstate__() is
              picklable (see section Pickling Class Instances for details).
        """
        import dill as pickle
        from collections import OrderedDict
        if len(self.variables_to_flush) == 0:
            return
        else:
            pickles = ''
            params = ''
            for name in self.variables_to_flush:
                v = pickle.dumps(self.variables_to_flush[name])
                pickles += v
                params += ('name={}&length={}&').format(name, len(v))

            while True:
                r = None
                try:
                    r = self._http_post(('/analytic/variables?{}').format(params), data=pickles, headers={'Content-Type': 'application/octet-stream'}, timeout=15)
                    j = json.loads(r.text)
                    _check_for_errors(j)
                    break
                except Exception as e:
                    self.get_logger().error('flush_binary_variables error: ' + str(e))
                    if r is not None:
                        self.get_logger().error('flush_binary_variables response from server: ' + r.text)

            self.variables_to_flush.clear()
            return

    def _download_core_variables(self):
        """
        Download and extract the core variables.
        This is to be called exactly once when the BotEngine class begins execution
        """
        self._download_binary_variable(CORE_VARIABLE_NAME)
        if CORE_VARIABLE_NAME not in self.variables:
            self.variables[CORE_VARIABLE_NAME] = {}
        if self.variables[CORE_VARIABLE_NAME] is None:
            self.variables[CORE_VARIABLE_NAME] = {}
        if type(self.variables[CORE_VARIABLE_NAME]) != type({}):
            self.variables[CORE_VARIABLE_NAME] = {}
        if TIMERS_VARIABLE_NAME not in self.variables[CORE_VARIABLE_NAME]:
            self.variables[CORE_VARIABLE_NAME][TIMERS_VARIABLE_NAME] = None
        if QUESTIONS_VARIABLE_NAME not in self.variables[CORE_VARIABLE_NAME]:
            self.variables[CORE_VARIABLE_NAME][QUESTIONS_VARIABLE_NAME] = None
        if COUNT_VARIABLE_NAME not in self.variables[CORE_VARIABLE_NAME]:
            self.variables[CORE_VARIABLE_NAME][COUNT_VARIABLE_NAME] = 0
        return

    def _validate_count(self):
        """
        Validate the count and log an error if our count isn't correct
        """
        if self._needs_resync():
            error_string = 'Expected trigger ID ' + str(self.variables[CORE_VARIABLE_NAME][COUNT_VARIABLE_NAME] + 1) + ' but got trigger ID ' + str(self.count) + ". That's " + str(self.count - (self.variables[CORE_VARIABLE_NAME][COUNT_VARIABLE_NAME] + 1)) + ' missed triggers.'
            self.get_logger().error(error_string)
            if 'sbox' in self._server:
                self.notify(email_content=error_string, email_subject='[sbox bot debugging] Missed trigger alert')
        self._save_count()

    def _needs_resync(self):
        """
        :return: True if we need to resynchronize with the server because our trigger count is off
        """
        return self.count > 0 and self.variables[CORE_VARIABLE_NAME][COUNT_VARIABLE_NAME] > 0 and self.variables[CORE_VARIABLE_NAME][COUNT_VARIABLE_NAME] + 1 != self.count

    def _save_count(self):
        """
        Save the trigger count
        Called explicitly because it adds computation
        """
        self.save_variable(COUNT_VARIABLE_NAME, self.count, required_for_each_execution=True)

    def _download_binary_variable(self, name):
        """
        Download a single binary variable
        """
        while True:
            import dill as pickle
            r = self._http_get('/analytic/variables/' + urllib.quote_plus(str(name)))
            try:
                self.variables[name] = pickle.loads(r.content)
                return
            except EOFError as e:
                if name == CORE_VARIABLE_NAME:
                    try:
                        self.get_logger().error(('BotEngine Core Variable Reset: EOFError in _download_binary_variable: Error message {}').format(str(e)))
                        self.get_logger().error(('\tBotEngine Core Variable Reset: HTTP status: {}').format(str(r.status_code)))
                        self.get_logger().error(('\tBotEngine Core Variable Reset: Variable text: {}').format(str(r.text)))
                        self.get_logger().error(('\tBotEngine Core Variable Reset: Variable content: {}').format(str(r.content)))
                    except Exception as e:
                        self.get_logger().error(('_download_binary_variable double error: {}').format(str(e)))

                self.variables[name] = None
                return
            except Exception as e:
                self.get_logger().error(('BotEngine: Unable to unpickle variable: {}. {}').format(name, str(e)))
                if 'maintenance' in r.content:
                    time.sleep(1)
                    continue
                else:
                    return

        return

    def notify(self, push_content=None, push_sound=None, push_info=None, email_subject=None, email_content=None, email_html=False, email_attachments=[], push_template_filename=None, push_template_model=None, email_template_filename=None, email_template_model=None, admin_domain_name=None, brand=None, sms_content=None, sms_template_filename=None, sms_template_model=None, sms_group_chat=True, language=None, user_id=None, user_id_list=[], to_residents=False, to_supporters=False, to_admins=False):
        """
        This method sends a push or email notification to the people you selected.

        :param push_sound: (optional) Eg: "sound.wav"
        :param push_content: (optional) Push notification text (limited to the push notification service maximum message size)
        :param email_subject: (optional) Email subject line
        :param email_content: (optional) Email body
        :param email_html: (optional) True or False; default is False.
        :param push_template_filename: directoryName/PushTemplateName.vm. If this is used, the 'push_content' field is ignored.
        :param push_template_model: Dictionary of key/value pairs to inject into the push template. Dependent upon what the template itself understands.
        :param email_template_filename: directoryName/EmailTemplateName.vm. If this is used, the 'email_content' and 'email_subject' fields are ignored.
        :param email_template_model: Dictionary of key/value pairs to inject into the email template. Dependent upon what the template itself understands.
        :param sms_content: Content for an SMS message
        :param sms_template_filename: SMS template filename. If this is used, the 'sms_content' field is ignored
        :param sms_template_model: Dictionary of key/value pairs to inject into the sms template. Dependent upon what the template itself understands.
        :param sms_group_chat: True to send SMS messages as a group chat message instead of one-on-one individual messages.
        :param brand: Case-sensitive brand for templates
        :param language: Language, for example 'en'
        :param user_id: (optional) Specific user ID to send to if the bot is running at the organizational level.
        :param user_id_list: (optional) Specific a list of user ID's to send to if the bot is running at the organizational level.
        :param to_residents: True to send the message to residents.
        :param to_supporters: True to send the message to supporters.
        :param to_admins: True to send the message to admins (email).
        :param admin_domain_name: Domain name / "short name" of the organization to send a notification to the admins
        """
        if push_content is None and push_info is None and push_template_filename is None and email_content is None and email_template_filename is None and sms_content is None and sms_template_filename is None:
            _bot_logger.error('< notify() nothing to notify')
            return
        else:
            notifications = {}
            if sms_content is not None or sms_template_filename is not None:
                if not to_residents and len(user_id_list) == 0:
                    to_residents = not to_supporters and not to_admins
                user_categories = []
                if to_residents:
                    user_categories.append(1)
                if to_supporters:
                    user_categories.append(2)
                users = []
                users += user_id_list
                if user_id is not None:
                    users.append(user_id)
                if len(users) > 0:
                    notifications['users'] = users
                if brand is not None:
                    notifications['brand'] = brand
                if language is not None:
                    notifications['language'] = language
                if sms_content is not None or sms_template_filename is not None:
                    notifications['smsMessage'] = {}
                    if len(user_categories) > 0:
                        notifications['userCategories'] = user_categories
                    notifications['smsMessage']['individual'] = not sms_group_chat
                    if sms_content:
                        notifications['smsMessage']['content'] = sms_content
                    if sms_template_filename:
                        notifications['smsMessage']['template'] = sms_template_filename
                    if sms_template_model:
                        notifications['smsMessage']['model'] = sms_template_model
                j = json.dumps(notifications)
                print(('Notification content: {}').format(json.dumps(notifications, indent=2, sort_keys=True)))
                location_id = self.get_location_id()
                r = self._http_post(('/analytic/location/{}/notifications').format(location_id), data=j)
                j = json.loads(r.text)
                try:
                    _check_for_errors(j)
                except BotError as e:
                    _bot_logger.error('BotEngine SMS notify(): ' + e.msg)
                    _bot_logger.error('Notification data: ' + str(notifications))

            if push_content is not None or email_content is not None or email_template_filename is not None:
                self._push_and_email_notification(push_content=push_content, push_sound=push_sound, push_info=push_info, email_subject=email_subject, email_content=email_content, email_html=email_html, email_attachments=email_attachments, push_template_filename=push_template_filename, push_template_model=push_template_model, email_template_filename=email_template_filename, email_template_model=email_template_model, admin_domain_name=admin_domain_name, brand=brand, to_admins=to_admins)
            return

    def _push_and_email_notification(self, push_content=None, push_sound=None, push_info=None, email_subject=None, email_content=None, email_html=False, email_attachments=[], push_template_filename=None, push_template_model=None, email_template_filename=None, email_template_model=None, admin_domain_name=None, brand=None, to_admins=False):
        """
        Send push and email notifications using the old method.
        :param push_content:
        :param push_sound:
        :param push_info:
        :param email_subject:
        :param email_content:
        :param email_html:
        :param email_attachments:
        :param push_template_filename:
        :param push_template_model:
        :param email_template_filename:
        :param email_template_model:
        :param admin_domain_name:
        :param to_admins:
        :param brand:
        """
        to_me = False
        if not to_admins:
            to_me = True
        params = {}
        user_categories = []
        if to_me:
            user_categories = [
             1]
            user_id_list = []
            category = 0
            users = self.get_location_users()
            for u in users:
                if u['category'] == 1:
                    user_id_list.append(u['id'])

        else:
            self.get_logger().warn(('botengine: Currently not longer sending emails to admins: {}').format(email_subject))
            return
        notifications = {'userCategories': user_categories, 
           'users': user_id_list}
        params = {'category': category}
        if push_content is None and push_info is None and push_template_filename is None and email_content is None and email_template_filename is None:
            return
        else:
            if push_content is not None or push_info is not None or push_template_filename is not None:
                notifications['pushMessage'] = {}
                if push_sound:
                    notifications['pushMessage']['sound'] = push_sound
                if push_content:
                    notifications['pushMessage']['content'] = push_content
                if push_info:
                    notifications['pushMessage']['info'] = push_info
                if push_template_filename:
                    notifications['pushMessage']['template'] = push_template_filename
                if push_template_model:
                    notifications['pushMessage']['model'] = push_template_model
            if email_content is not None or email_template_filename is not None:
                notifications['emailMessage'] = {}
                if email_subject:
                    notifications['emailMessage']['subject'] = email_subject
                if email_html:
                    notifications['emailMessage']['html'] = email_html
                if email_content:
                    notifications['emailMessage']['content'] = email_content
                if email_attachments:
                    notifications['emailMessage']['attachments'] = email_attachments
                if email_template_filename:
                    notifications['emailMessage']['template'] = email_template_filename
                    notifications['emailMessage']['html'] = True
                if email_template_model:
                    notifications['emailMessage']['model'] = email_template_model
            if brand is not None:
                notifications['brand'] = brand
            j = json.dumps(notifications)
            r = self._http_post('/analytic/notifications', params=params, data=j)
            j = json.loads(r.text)
            try:
                _check_for_errors(j)
            except BotError as e:
                _bot_logger.error('BotEngine notify(): ' + e.msg)
                _bot_logger.error('Notification params: ' + str(params))
                _bot_logger.error('Notification data: ' + str(notifications))

            return

    def add_email_attachment_from_camera(self, destination_attachment_array, device_file_id, content_id):
        """
        Add an email attachment from a camera with the content being pulled and delivered from the server inside the user's email
        :param destination_attachment_array: Destination array of attachments. Pass in [] if you are starting a new list of attachments.
        :param device_file_id: Device File ID
        :param content_id: Content ID String.  The thumbnail would then cite "cid:<content_id>" to reference this attachment.
        """
        attachment = {'deviceFileId': device_file_id, 
           'contentId': content_id}
        destination_attachment_array.append(attachment)
        return destination_attachment_array

    def add_email_attachment(self, destination_attachment_array, filename, content, content_type, content_id):
        """
        This helper method will create an email attachment block and add it to a destination array of existing email attachments

        :param destination_attachment_array: Destination array of attachments. Pass in [] if you are starting a new list of attachments.
        :param filename: Filename of the file, for example, "imageName.jpg"
        :param content: Content to attached, for example base64-encoded binary image content
        :param content_type: Content type of the file, for example "image/jpeg"
        :param content_id: Unique ID for the content, for example "inlineImageId". The email can reference this content with <img src="cid:inlineImageId">.

        :return the destination_attachment_array with the new attachment, ready to pass into the email_attachments argument in the notify() method
        """
        attachment = {'name': filename, 
           'content': content, 
           'contentType': content_type, 
           'contentId': content_id}
        destination_attachment_array.append(attachment)
        return destination_attachment_array

    def get_measurements(self, device_id, user_id=None, oldest_timestamp_ms=None, newest_timestamp_ms=None, param_name=None, index=None, last_rows=None):
        """
        This method will return measurements from the given device

        * param_name[*] --> getting current measurement
        * start_date, end_date[?], param_name[*], index[?] --> getting historical measurements
        * start_date, end_date[?], param_name[*], index[?], last_count --> getting last n measurements

        :param device_id: Device ID to extract parameters from
        :param user_id: User ID to access devices of specific user by an organization bot
        :param oldest_timestamp_ms: Start time in milliseconds to begin receiving measurements. If not set, only latest measurements will be returned. e.g. 1483246800000
        :param newest_timestamp_ms: End time in milliseconds to stop receiving measurements, default is the current time. e.g. 1483246800000
        :param param_name: Only obtain measurements for given parameter names. Multiple values can be passed, example: "batteryLevel" or ["batteryLevel", "doorStatus"]
        :param index: Only obtain measurements for parameters with this index number.
        :param last_rows: Receive only last N measurements
        """
        if newest_timestamp_ms is None:
            newest_timestamp_ms = self.get_timestamp()
        original_oldest_timestamp_ms = oldest_timestamp_ms
        params = {}
        if user_id:
            params['userId'] = int(user_id)
        if param_name:
            params['paramName'] = param_name
        if index:
            params['index'] = index
        if last_rows:
            params['lastRows'] = last_rows
        if newest_timestamp_ms:
            params['endDate'] = int(newest_timestamp_ms)
        if oldest_timestamp_ms is None:
            r = self._http_get('/analytic/devices/' + device_id + '/parameters', params=params, timeout=120)
            j = json.loads(r.text)
            _check_for_errors(j)
            return j
        else:
            import dateutil.relativedelta
            oldest_dt = datetime.datetime.utcfromtimestamp(newest_timestamp_ms / 1000).replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            return_json = {'measures': []}
            while newest_timestamp_ms > original_oldest_timestamp_ms:
                oldest_timestamp_ms = (oldest_dt - datetime.datetime(1970, 1, 1)).total_seconds() * 1000
                if oldest_timestamp_ms < original_oldest_timestamp_ms:
                    oldest_timestamp_ms = original_oldest_timestamp_ms
                params['startDate'] = int(oldest_timestamp_ms)
                params['endDate'] = int(newest_timestamp_ms)
                r = self._http_get('/analytic/devices/' + device_id + '/parameters', params=params, timeout=240)
                j = json.loads(r.text)
                _check_for_errors(j)
                if 'measures' not in j:
                    break
                elif len(j['measures']) == 0:
                    break
                return_json['measures'][0:0] = j['measures']
                newest_timestamp_ms = oldest_timestamp_ms
                oldest_dt = oldest_dt + dateutil.relativedelta.relativedelta(months=-1)

            return return_json
            return

    def request_data(self, device_id, oldest_timestamp_ms=None, newest_timestamp_ms=None, param_name_list=None, reference=None, index=None, ordered=1):
        """
        Selecting a large amount of data from the database can take a significant amount of time and impact server
        performance. To avoid this long waiting period while executing bots, a bot can submit a request for all the
        data it wants from this location asynchronously. The server gathers all the data on its own time, and then
        triggers the bot with trigger 2048. Your bot must include trigger 2048 to receive the trigger.

        Selected data becomes available as a file in CSV format, compressed by LZ4, and stored for one day.
        The bot receives direct access to this file.

        You can call this multiple times to extract data out of multiple devices. The request will be queued up and
        the complete set of requests will be flushed at the end of this bot execution.

        :param device_id: Device ID to download historical data from
        :param oldest_timestamp_ms: Oldest timestamp in milliseconds
        :param newest_timestamp_ms: Newest timestamp in milliseconds
        :param param_name_list: List of parameter names to download
        :param reference: Reference so when this returns we know who it's for
        :param index: Index to download when parameters are available with multiple indices
        :param ordered: 1=Ascending (default); -1=Descending.
        """
        request = {'type': 1, 
           'deviceId': device_id}
        if oldest_timestamp_ms is not None:
            request['startTime'] = oldest_timestamp_ms
        else:
            request['startTime'] = 1280707200000
        if newest_timestamp_ms is not None:
            request['endTime'] = newest_timestamp_ms
        else:
            request['endTime'] = self.get_timestamp()
        if param_name_list is not None:
            request['paramNames'] = param_name_list
        if reference is not None:
            request['key'] = reference
        if index is not None:
            request['index'] = index
        if ordered is not None:
            request['ordered'] = ordered
        self.data_requests.append(request)
        return

    def flush_asynchronous_requests(self):
        """
        Flush the complete set of asynchronous measurement requests to the server
        """
        if len(self.data_requests) == 0:
            return
        j = json.dumps({'dataRequests': self.data_requests})
        r = self._http_post('/analytic/dataRequests', data=j)
        j = json.loads(r.text)
        try:
            _check_for_errors(j)
        except BotError as e:
            _bot_logger.warn(('Error sending asynchronous measurement requests. We sent this body: {}').format(json.dumps({'dataRequests': self.data_requests}, indent=2, sort_keys=True)))

        self.data_requests = []

    def send_command(self, device_id, param_name, value, index=None, user_id=-1, command_timeout_ms=None, comment=None):
        """
        This method sends a command to the device ID

        :param device_id: The exact device ID to send a command to. This is case-sensitive.
        :param param_name: The name of the parameter to configure.
        :param value: The value to set for this parameter.
        :param index: Optional index number / letters. Default is None.
        :param user_id: user ID to access devices of specific user by an organization bot.cs
        :param comment: Reason why this command was sent
        """
        self.send_commands(device_id, self.form_command(param_name=param_name, index=index, value=value), user_id=user_id, command_timeout_ms=command_timeout_ms, comment=comment)

    def form_command(self, param_name, value, index=None):
        """
        This method will form a single command.

        You can pass in parameter name / optional index / value pairs and it will
        generate a dictionary to represent this command. This is a shortcut to send
        multiple commands with the send_commands(device_id, commands) method.

        Append multiple commands into a list and then use send_commands(..) to send them all.

        :param param_name: The name of the parameter to configure.
        :param value: The value to set for this parameter.
        :param index: Optional index number / letters. Default is None.
        """
        response = {'name': param_name, 
           'value': value}
        if index:
            response['index'] = index
        return response

    def send_commands(self, device_id, commands, user_id=-1, command_timeout_ms=None, comment=None):
        """
        This method sends one or multiple commands simultaneously to the given device ID
        'index' is optional - if your parameter does not use an index number, do not reference or populate it.

        :param device_id: The exact device ID to send a command to. This is case-sensitive.
        :param commands: Array of dictionaries of the form [{"name":"parameterName", "index":0, "value":"parameterValue"}, ...]
        :param user_id: User ID to access devices of specific user by an organization bot.
        :param command_timeout_ms: Relative timeout, in ms, to expire the command
        :param comment: Reason why this command was sent
        """
        if user_id not in self.commands_to_flush:
            self.commands_to_flush[user_id] = []
        commands_for_device = {'deviceId': device_id}
        exists = False
        for d in self.commands_to_flush[user_id]:
            if d['deviceId'] == device_id:
                commands_for_device = d
                exists = True
                break

        if 'params' not in commands_for_device:
            commands_for_device['params'] = []
        if command_timeout_ms is not None:
            commands_for_device['commandTimeout'] = command_timeout_ms
        if comment is not None:
            commands_for_device['comment'] = comment
        if not isinstance(commands, list):
            commands = [
             commands]
        import copy
        for command in commands:
            for param in copy.copy(commands_for_device['params']):
                if param['name'] == command['name']:
                    if 'index' in param and 'index' in command:
                        if param['index'] == command['index']:
                            commands_for_device['params'].remove(param)
                            break
                    else:
                        commands_for_device['params'].remove(param)
                        break

            commands_for_device['params'].append(command)

        if not exists:
            self.commands_to_flush[user_id].append(commands_for_device)
        return

    def cancel_command(self, device_id, param_name=None, user_id=-1):
        """
        Cancel a command to the device with the given parameter names.
        If no parameter name is given, this will cancel all commands to the device.
        :param device_id: Device ID to cancel commands for
        :param param_name: Parameter name to cancel commands for. Leave this None (default) to cancel all commands to the device.
        :param user_id: User ID to cancel commands for a specific user
        """
        if user_id in self.commands_to_flush:
            import copy
            for d in copy.copy(self.commands_to_flush[user_id]):
                if d['deviceId'] == device_id:
                    if param_name is None:
                        self.commands_to_flush[user_id].remove(d)
                        return
                    if 'params' in d:
                        for param in copy.copy(d['params']):
                            if param['name'] == param_name:
                                d['params'].remove(param)

                        if len(d['params']) == 0:
                            self.commands_to_flush[user_id].remove(d)
                        if len(self.commands_to_flush[user_id]) == 0:
                            del self.commands_to_flush[user_id]

        return

    def flush_commands(self):
        """
        Flush all the commands to the server and execute them.
        This is called automatically when the bot exits, you should never have to call this manually.
        """
        for user_id in self.commands_to_flush:
            params = {}
            if user_id > 0:
                params['userId'] = user_id
            body = {'devices': []}
            for d in self.commands_to_flush[user_id]:
                body['devices'].append(d)

            _bot_logger.info('Sending commands: ' + json.dumps(body, indent=2, sort_keys=True))
            j = json.dumps(body)
            r = self._http_put('/analytic/parameters', params=params, data=j)
            j = json.loads(r.text)
            _bot_logger.info('Command responses: ' + json.dumps(j, indent=2, sort_keys=True))
            try:
                _check_for_errors(j)
            except BotError as e:
                _bot_logger.warn('Error sending command to user ID ' + str(user_id) + '. ' + str(e.msg) + '; We sent this body: ' + str(body))

        self.commands_to_flush = {}

    def set_mode(self, location_id, mode, comment=None):
        """
        Set the mode
        :param location_id: Location ID of which to set the mode
        :param mode: Mode string to set, for example "AWAY" or "AWAY.SILENT"
        :param comment: Optional comment to describe why this mode changed.
        """
        data = None
        if comment is not None:
            data = json.dumps({'comment': comment})
        self._http_post('/cloud/json/location/' + str(location_id) + '/event/' + str(mode), data=data)
        return

    def get_mode_history(self, location_id, oldest_timestamp_ms=None, newest_timestamp_ms=None):
        """
        This method will return location mode history in backward order (lastest first)
        Including the source of the mode change
        :param location_id: Location ID
        :param oldest_timestamp_ms: Oldest timestamp to start pulling history
        :param newest_timestamp_ms: Newest timestamp to stop pulling history
        """
        params = {}
        if oldest_timestamp_ms is not None:
            params['startDate'] = int(oldest_timestamp_ms)
        if newest_timestamp_ms is not None:
            params['endDate'] = int(newest_timestamp_ms)
        r = self._http_get('/analytic/location/' + str(location_id) + '/events', params=params)
        j = json.loads(r.text)
        _check_for_errors(j)
        return j

    def get_mode(self, location_id):
        """
        Get the current mode
        :param location_id: Location ID to retrieve the mode for
        :return: The current mode, or "HOME.DEFAULT" by default if the location can't be found
        """
        location = self.get_location_info()
        if 'location' in location:
            if 'event' in location['location']:
                return location['location']['event']
        return 'HOME.DEFAULT'

    def download_file(self, file_id, local_filename, thumbnail=False):
        """
        Download a file
        :param file_id: File ID to download
        :param local_filename: Local filename to store the file into
        :param thumbnail: True to download the thumbnail for this file
        :return: local_filename
        """
        params = {'thumbnail': thumbnail}
        r = self._http_get(('/cloud/json/files/{}').format(file_id), params=params, stream=True)
        with open(local_filename, 'wb') as (f):
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)

        return local_filename

    def has_subscription(self, name):
        """
        :return: True if this user has the given subscription name
        """
        if self.services is not None:
            for service in self.services:
                if service['serviceName'] == name:
                    return True

        return False

    def has_professional_monitoring(self):
        """
        :return: True if this user has professional monitoring services
        """
        try:
            professional_monitoring = self.professional_monitoring_status()
            return professional_monitoring['callCenter']['status'] == BotEngine.PROFESSIONAL_MONITORING_REGISTERED
        except:
            return False

        return False

    def professional_monitoring_status(self):
        """This method will return call center service statuses"""
        r = self._http_get('/analytic/callCenter')
        j = json.loads(r.text)
        _check_for_errors(j)
        return j

    def professional_monitoring_alerts(self):
        """This method will return call center service alerts"""
        r = self._http_get('/analytic/callCenterAlerts')
        j = json.loads(r.text)
        _check_for_errors(j)
        return j

    def raise_professional_monitoring_alert(self, message, code, device_id=None):
        """Raise an alert to the professional monitoring services

        :param message: signal message
        :param code:        E130 - General burglary alarm
                             E131 - Perimeter alarm (door/window entry sensor)
                             E132 - Interior alarm (motion sensor)
                             E134 - Entry/exit alarm (more specific than E131, but I'm not sure we can declare that our door/window sensors will always be used on an entry/exit)
                             E154 - Water leak
                             E111 - Smoke alarm (future)
                             E114 - Heat alarm (future - analytics on temperature sensors above the stove, for example)
                             E158 - Environmental high temperature alarm (temperature sensor)
                             E159 - Environmental low temperature alarm (temperature sensor)
                             E100 - General medical alarm (future - Personal Emergency Reporting System (PERS) button)
                             E108 - Verify contact information

        :param device_id: device ID
        """
        return self._signal_professional_monitoring(1, message, code, device_id)

    def cancel_professional_monitoring_alert(self, message, code, device_id=None):
        """Cancel an alert to the professional monitoring services

        :param message: signal message
        :param code:        E130 - General burglary alarm
                             E131 - Perimeter alarm (door/window entry sensor)
                             E132 - Interior alarm (motion sensor)
                             E134 - Entry/exit alarm (more specific than E131, but I'm not sure we can declare that our door/window sensors will always be used on an entry/exit)
                             E154 - Water leak
                             E111 - Smoke alarm (future)
                             E114 - Heat alarm (future - analytics on temperature sensors above the stove, for example)
                             E158 - Environmental high temperature alarm (temperature sensor)
                             E159 - Environmental low temperature alarm (temperature sensor)
                             E100 - General medical alarm (future - Personal Emergency Reporting System (PERS) button)

        :param device_id: device ID
        """
        return self._signal_professional_monitoring(2, message, code, device_id)

    def _signal_professional_monitoring(self, alert_status, message, code, device_id=None):
        """This method can change the current alert status to raise or cancel it

        :param alert_status: 0   An alert was never raised
                              1   Raise an alert
                              2   Cancel an alert
                              3   Not available to set - The alert was reported to the professional monitoring services

        :param message: signal message
        :param code:        E130 - General burglary alarm
                             E131 - Perimeter alarm (door/window entry sensor)
                             E132 - Interior alarm (motion sensor)
                             E134 - Entry/exit alarm (more specific than E131, but I'm not sure we can declare that our door/window sensors will always be used on an entry/exit)
                             E154 - Water leak
                             E111 - Smoke alarm (future)
                             E114 - Heat alarm (future - analytics on temperature sensors above the stove, for example)
                             E158 - Environmental high temperature alarm (temperature sensor)
                             E159 - Environmental low temperature alarm (temperature sensor)
                             E100 - General medical alarm (future - Personal Emergency Reporting System (PERS) button)

        :param device_id: device ID
        """
        params = {'alertStatus': alert_status, 
           'signalMessage': message}
        if code:
            params['signalType'] = code
        if device_id:
            params['deviceId'] = device_id
        j = json.dumps({'callCenter': params})
        r = self._http_put('/analytic/callCenter', data=j)
        j = json.loads(r.text)
        _check_for_errors(j)
        return j

    def tag_user(self, tag, user_id=None):
        """
        Tag a user
        :param tag: The tag to give the user
        """
        self._tag(1, tag, user_id)

    def tag_location(self, tag):
        """
        Tag a location
        :param tag: The tag to give the location
        :param location_id: The location ID to tag
        """
        self._tag(2, tag, self.get_location_id())

    def tag_device(self, tag, device_id, user_id=None):
        """
        Tag a device
        :param tag: The tag to give the device
        :param device_id: The device ID to tag
        """
        self._tag(3, tag, device_id, user_id)

    def tag_file(self, tag, file_id, user_id=None):
        """
        Tag a file
        :param tag: The tag to give the file
        :param file_id: The file ID to tag
        """
        self._tag(4, tag, file_id, user_id)

    def delete_user_tag(self, tag, user_id=None):
        """
        Delete a user tag
        :param tag: Tag to delete
        """
        self._delete_tag(1, tag)

    def delete_location_tag(self, tag):
        """
        Delete a location tag
        :param tag: Tag to delete
        """
        self._delete_tag(2, tag, self.get_location_id())

    def delete_device_tag(self, tag, device_id):
        """
        Delete a location device
        :param tag: Tag to delete
        """
        self._delete_tag(3, tag, device_id)

    def delete_file_tag(self, tag, file_id):
        """
        Delete a location file
        :param tag: Tag to delete
        """
        self._delete_tag(4, tag, file_id)

    def get_tags(self, tag_type=None, tag_id=None, user_id=None):
        """
        Get tags
        :param tag_type: Optional, filter by type:
                1 - Users
                2 - Locations
                3 - Devices
                4 - Files
 
        :param tag_id: Optional, filter by location ID, device ID, or file ID
        :param user_id: Used with Organizational Apps - confine tags to a specific user
        """
        params = {}
        if user_id is not None:
            params['userId'] = user_id
        if tag_type is not None:
            params['type'] = tag_type
        if tag_id is not None:
            params['id'] = tag_id
        r = self._http_get('/analytic/tags', params=params)
        j = json.loads(r.text)
        _check_for_errors(j)
        return j

    def _tag(self, tag_type, tag, tag_id=None, user_id=None):
        """Private method to tag users, devices, locations, files

        :param tag_type:   1 - User
                       2 - Location
                       3 - Device
                       4 - Files

        :param tag: Tag to give the object
        :param tag_id: Location ID, Device ID, or File ID
        """
        if ' ' in tag:
            return 'Error: Tags cannot have any spaces'
        else:
            if '#' in tag:
                return 'Error: Tags cannot have any # signs'
            if '@' in tag:
                return 'Error: Tags cannot have any @ signs'
            tag_block = {'type': tag_type, 
               'tag': tag}
            if tag_id is not None:
                tag_block['id'] = tag_id
            if user_id is not None:
                if user_id not in self.tags_to_create_by_user:
                    self.tags_to_create_by_user[user_id] = []
                self.tags_to_create_by_user[user_id].append(tag_block)
            else:
                self.tags_to_create.append(tag_block)
            return

    def _delete_tag(self, tag_type, tag, tag_id=None, user_id=None):
        """Delete a tag

        :param tag_type:   1 - User
                       2 - Location
                       3 - Device
                       4 - Files

        :param tag: Tag to delete
        :param tag_id: Location ID, Device ID, or File ID
        """
        tag_block = {'type': tag_type, 
           'tag': tag}
        if tag_id is not None:
            tag_block['id'] = tag_id
        if user_id is not None:
            if user_id not in self.tags_to_delete_by_user:
                self.tags_to_delete_by_user[user_id] = []
            self.tags_to_delete_by_user[user_id].append(tag_block)
        else:
            self.tags_to_delete.append(tag_block)
        return

    def flush_tags(self):
        """
        Flush the new and deleted tags to the server,
        This is called automatically when the bot is finished executing. It should never have to be called manually.
        """
        if len(self.tags_to_create) > 0:
            j = json.dumps({'tags': self.tags_to_create})
            r = self._http_put('/analytic/tags', data=j)
            j = json.loads(r.text)
            try:
                _check_for_errors(j)
            except BotError as e:
                self.get_logger().error(e.msg + '; data=' + str(j))

        for params in self.tags_to_delete:
            r = self._http_delete('/analytic/tags', params=params)
            j = json.loads(r.text)

        for user_id in self.tags_to_create_by_user:
            params = {'userId': user_id}
            j = json.dumps({'tags': self.tags_to_create_by_user[user_id]})
            r = self._http_put('/analytic/tags', params=params, data=j)
            j = json.loads(r.text)
            try:
                _check_for_errors(j)
            except BotError as e:
                self.get_logger().error(e.msg + '; user_id=' + str(user_id) + '; data=' + str(j))

        for user_id in self.tags_to_delete_by_user:
            for params in self.tags_to_delete_by_user[user_id]:
                params['userId'] = user_id
                r = self._http_delete('/analytic/tags', params=params)

    def get_weather_forecast_by_geocode(self, latitude, longitude, units=None, hours=12):
        """
        Get the weather forecast by geocode (latitude, longitude)
        :param latitude: Latitude
        :param longitude: Longitude
        :param units: Default is Metric. 'e'=English; 'm'=Metric; 'h'=Hybrid (UK); 's'=Metric SI units (not available for all APIs)
        :param hours: Forecast depth in hours, default is 12. Available hours are 6, 12.
        :return: Weather JSON data
        """
        params = {}
        if units is not None:
            params['units'] = units
        if hours is not None:
            params['hours'] = hours
        r = self._http_get('/cloud/json/weather/forecast/geocode/' + str(latitude) + '/' + str(longitude), params=params)
        j = json.loads(r.text)
        _check_for_errors(j)
        return j

    def get_current_weather_by_geocode(self, latitude, longitude, units=None):
        """
        Get the current weather by geocode (latitude, longitude)
        :param latitude: Latitude
        :param longitude: Longitude
        :param units: Default is Metric. 'e'=English; 'm'=Metric; 'h'=Hybrid (UK); 's'=Metric SI units (not available for all APIs)
        :return: Weather JSON data
        """
        params = {}
        if units is not None:
            params['units'] = units
        r = self._http_get('/cloud/json/weather/current/geocode/' + str(latitude) + '/' + str(longitude), params=params)
        j = json.loads(r.text)
        _check_for_errors(j)
        return j

    def get_weather_forecast_by_location(self, location_id, units=None, hours=12):
        """
        Get the weather forecast by Location ID
        :param location_id: Location ID for which to retrieve the weather forecast
        :param units: Default is Metric. 'e'=English; 'm'=Metric; 'h'=Hybrid (UK); 's'=Metric SI units (not available for all APIs)
        :param hours: Forecast depth in hours, default is 12. Available hours are 6, 12.
        :return: Weather JSON data
        """
        params = {}
        if units is not None:
            params['units'] = units
        if hours is not None:
            params['hours'] = hours
        r = self._http_get('/cloud/json/weather/forecast/location/' + str(location_id), params=params)
        j = json.loads(r.text)
        _check_for_errors(j)
        return j

    def get_current_weather_by_location(self, location_id, units=None):
        """
        Get the current weather by Location ID
        :param location_id: Location ID for which to retrieve the weather forecast
        :param units: Default is Metric. 'e'=English; 'm'=Metric; 'h'=Hybrid (UK); 's'=Metric SI units (not available for all APIs)
        :return: Weather JSON data
        """
        params = {}
        if units is not None:
            params['units'] = units
        r = self._http_get('/cloud/json/weather/current/location/' + str(location_id), params=params)
        j = json.loads(r.text)
        _check_for_errors(j)
        return j

    def start_timer(self, seconds, function, argument=None, reference=None):
        """
        Start a timer with a relative time in seconds to fire.
        
        :param seconds: Number of seconds from now to execute.
        :param function: Function to execute when the timer fires. This must be a function, not be a class method.
        :param argument: Optional argument to inject into the fired timer
        :param reference: Optional ID to reference this timer. Useful if you plan on canceling the timer later.
        """
        absolute_time = self.get_timestamp()
        self.set_timer(int(absolute_time + seconds * 1000), function, argument, reference)

    def start_timer_s(self, seconds, function, argument=None, reference=None):
        """
        Start a timer with a relative time in seconds to fire.

        :param seconds: Number of seconds from now to execute.
        :param function: Function to execute when the timer fires. This must be a function, not be a class method.
        :param argument: Optional argument to inject into the fired timer
        :param reference: Optional ID to reference this timer. Useful if you plan on canceling the timer later.
        """
        absolute_time = self.get_timestamp()
        self.set_alarm(int(absolute_time + seconds * 1000), function, argument, reference)

    def start_timer_ms(self, milliseconds, function, argument=None, reference=None):
        """
        Start a timer with a relative time in milliseconds to fire.

        :param milliseconds: Number of milliseconds from now to execute.
        :param function: Function to execute when the timer fires. This must be a function, not be a class method.
        :param argument: Optional argument to inject into the fired timer
        :param reference: Optional ID to reference this timer. Useful if you plan on canceling the timer later.
        """
        absolute_time = self.get_timestamp()
        self.set_alarm(int(absolute_time + milliseconds), function, argument, reference)

    def set_alarm(self, timestamp_ms, function, argument=None, reference=None):
        """
        Set an alarm with an absolute timestamp
        :param timestamp_ms: Absolute unix epoch time in milliseconds to fire the timer.
        :param function: Function to execute when the timer fires. This must be a function, not be a class method.
        :param argument: Optional argument to inject into the fired timer
        :param reference: Optional ID to reference this timer. Useful if you plan on canceling the timer later.
        """
        if self.get_trigger_type() & self.TRIGGER_DATA_REQUEST != 0:
            self.get_logger().error(('botengine: You cannot start a timer/alarm while executing a data request trigger. Timer/Alarm reference={}').format(reference))
            return
        else:
            saved_timers = self.load_variable(TIMERS_VARIABLE_NAME)
            if saved_timers is None:
                saved_timers = []
            saved_timers.append((int(timestamp_ms), function, argument, reference))
            saved_timers = [ x for x in saved_timers if x[0] != MAXINT ]
            saved_timers.append((MAXINT, self.get_timestamp(), None, None))
            saved_timers.sort(key=lambda tup: tup[0])
            self.save_variable(TIMERS_VARIABLE_NAME, saved_timers)
            return

    def set_timer(self, timestamp, function, argument=None, reference=None):
        """
        Deprecated. Use set_alarm() instead.
        
        Set an alarm with an absolute timestamp.
        :param timestamp: Absolute unix epoch time to fire the timer.
        :param function: Function to execute when the timer fires. This must be a function, not be a class method.
        :param argument: Optional argument to inject into the fired timer
        :param reference: Optional ID to reference this timer. Useful if you plan on canceling the timer later.
        """
        self.set_alarm(timestamp, function, argument, reference)

    def is_timer_running(self, reference):
        """
        Find out if at least one instance of a particular timer is running
        :param reference: Search for timers with the given reference. Cannot be None.
        :return: True if there is at least 1 existing timer with this reference running
        """
        saved_timers = self.load_variable(TIMERS_VARIABLE_NAME)
        if saved_timers is None:
            return False
        else:
            for ref in [ x[3] for x in saved_timers ]:
                if ref == reference:
                    return True

            return False

    def cancel_timers(self, reference):
        """
        Cancel ALL timers with the given reference.
        
        :param reference: Search for timers with the given reference and destroy them. Cannot be None.
        """
        saved_timers = self.load_variable(TIMERS_VARIABLE_NAME)
        if saved_timers is None:
            saved_timers = []
        saved_timers = [ x for x in saved_timers if x[3] != reference and x[0] != MAXINT ]
        saved_timers.append((MAXINT, self.get_timestamp(), None, None))
        saved_timers.sort(key=lambda tup: tup[0])
        self.save_variable(TIMERS_VARIABLE_NAME, saved_timers)
        if not self.cancelled_timers and len(saved_timers) <= 1:
            self._cancel_execution_request()
            self.cancelled_timers = True
        return

    def _execute_again_in_n_seconds(self, seconds):
        """Execute this bot again at a relative time, N seconds from now, without an external trigger
        :param seconds
        """
        params = {'in': int(seconds)}
        r = self._http_put('/analytic/execute', params=params)
        j = json.loads(r.text)
        _check_for_errors(j)

    def _execute_again_at_timestamp(self, unix_timestamp_ms):
        """Execute this bot again at an absolute time, at the given timestamp, without an external trigger
        :param unix_timestamp_ms:
        """
        params = {'at': int(unix_timestamp_ms)}
        r = self._http_put('/analytic/execute', params=params)
        j = json.loads(r.text)
        _check_for_errors(j)

    def _cancel_execution_request(self):
        """Cancel any existing requests for delayed executions"""
        r = self._http_delete('/analytic/execute')
        j = json.loads(r.text)
        _check_for_errors(j)
        return j

    def generate_question(self, key_identifier, response_type, device_id=None, icon=None, display_type=None, editable=False, default_answer=None, correct_answer=None, answer_format=None, urgent=False, front_page=False, send_push=False, send_sms=False, send_email=False, ask_timestamp=None, section_id=0, question_weight=0):
        """
        Initializer

        :param key_identifier: Your own custom key to recognize this question regardless of the language or framing of the question to the user.
        :param response_type: Type of response we should expect the user to give
            1 = Boolean question
            2 = Multichoice, Single select (requires response options)
            4 = Multichoice, Multi select (requires response options)
            6 = Day of the Week
            7 = Slider (Default minimum is 0, default maximum is 100, default increment is 5)
            8 = Time in seconds since midnight
            9 = Datetime (xsd:dateTime format)
            10 = Open-ended text

        :param device_id: Device ID to ask a question about so the UI can reference its name
        :param icon: Icon to display when asking this question
        :param display_type: How to render and display the question in the UI. For example, a Boolean question can be an on/off switch, a yes/no question, or just a single button. See the documentation for more details.
        :param editable: True to make this question editable later. This makes the question more like a configuration for the bot that can be adjusted again and again, rather than a one-time question.
        :param default_answer: Default answer for the question
        :param correct_answer: This is a regular expression to determine if the user's answer is "correct" or not
        :param answer_format: Regular expression string that represents what a valid response would look like. All other responses would not be allowed.
        :param urgent: True if this question is urgent enough that it requires a push notification and should be elevated to the top of the stack after any current delivered questions. Use sparingly to avoid end-user burnout.
        :param front_page: True if this question should be delivered to the front page of mobile/web bot, when the user is ready to consume another question from the system.
        :param send_push: True to send this questions as a push notification. Use sparingly to avoid end user burnout.
        :param send_sms: True to send an SMS message. Because this costs money, this is currently disabled.
        :param send_email: True to send the question in an email. Use sparingly to avoid burnout and default to junk mail.
        :param ask_timestamp: Future timestamp to ask this question. If this is not set, the current time will be used.
        :param section_id: ID of a section, which acts as both the element to group by as well as the weight of the section vs. other sections in the UI. (default is 0)
        :param question_weight: Weight of an individual question within a grouped section. The lighter the weight, the more the question rises to the top of the list in the UI. (default is 0)
        """
        return Question(key_identifier, response_type, device_id, icon, display_type, editable, default_answer, correct_answer, answer_format, urgent, front_page, send_push, send_sms, send_email, ask_timestamp, section_id, question_weight)

    def ask_question(self, question):
        """
        Ask your question

        :param question: Question to ask, created by the generate_question method
        """
        self.questions_to_ask[question.key_identifier] = question

    def delete_question(self, question):
        """
        Delete the question.
        Best practice is to learn what we need to learn from a question and then delete a question after we're done with it.
        This can help free up space and increase execution time if we've already learned what we need to learn from this question.
        
        :param question: Question to delete
        """
        if question._question_id is None:
            if question.key_identifier in self.questions_to_ask:
                del self.questions_to_ask[question.key_identifier]
        saved_questions = self.load_variable(QUESTIONS_VARIABLE_NAME)
        if saved_questions is not None:
            if question.key_identifier in saved_questions:
                del saved_questions[question.key_identifier]
                self.save_variable(QUESTIONS_VARIABLE_NAME, saved_questions)
        self.questions_to_delete[question.key_identifier] = question
        return

    def flush_questions(self):
        """
        Synchronize all deleted and new questions with the server.
        This is called automatically when the bot is finished executing. It should never have to be called manually.
        """
        saved_questions = self.load_variable(QUESTIONS_VARIABLE_NAME)
        if saved_questions is None:
            saved_questions = {}
        original_saved_questions = saved_questions.copy()
        for q_id in self.questions_to_delete:
            question = self.questions_to_delete[q_id]
            params = {'questionId': question._question_id}
            r = self._http_delete('/analytic/questions', params=params)
            j = json.loads(r.text)
            if j['resultCode'] == 0:
                if question.key_identifier in saved_questions:
                    del saved_questions[question.key_identifier]

        if len(self.questions_to_ask) > 0:
            body = {'questions': []}
            for q_id in self.questions_to_ask:
                question = self.questions_to_ask[q_id]
                body['questions'].append(question._form_json_question())

            r = self._http_post('/analytic/questions', data=json.dumps(body))
            response = json.loads(r.text)
            if response['resultCode'] == 0 and 'questions' in response:
                for response_block in response['questions']:
                    question = self.questions_to_ask[response_block['key']]
                    question._question_id = response_block['id']
                    question.answer_status = BotEngine.ANSWER_STATUS_QUEUED
                    saved_questions[question.key_identifier] = question

        if original_saved_questions != saved_questions:
            self.save_variable(QUESTIONS_VARIABLE_NAME, saved_questions)
        self.questions_to_delete = {}
        self.questions_to_ask = {}
        return

    def get_list_of_asked_questions(self):
        """
        Retrieve a list of previously asked questions that still exist
        :return: a dictionary of questions we've previously asked. The question's ID is the dictionary's key, the question itself is the value.
        """
        saved_questions = self.load_variable(QUESTIONS_VARIABLE_NAME)
        if saved_questions is None:
            saved_questions = {}
        return saved_questions

    def retrieve_question(self, key):
        """
        Retrieve a single previously asked question based on its key
        :param key: Key Identifier generated by the bot developer to track this question
        :return: A Question object if the question was asked and still exists, None if the question wasn't asked or no longer exists because it was deleted
        """
        saved_questions = self.load_variable(QUESTIONS_VARIABLE_NAME)
        if saved_questions is None:
            saved_questions = {}
        if key not in saved_questions:
            return
        else:
            return saved_questions[key]

    def change_answer(self, question, new_answer):
        """
        Change the answer to a previously asked question.

        One of the best places to use this, for example, is with an Editable question that is being used to configure the bot.
        Let's say you ask an Editable question, the user answered it which configured your bot, and now your bot has to change
        behaviors again. You can update the user's answer to show the user what you're currently running off of, allowing the
        user to adjust the answer again if you want. Sort of a bi-directional back-and-forth "here are what the settings are
        going to be" so the user and bot can continually agree upon it.

        :param question: Question to update the answer for
        :param new_answer: New answer to inject into the question back to the user
        """
        if question._question_id is None:
            _bot_logger.warn('Cannot change answer to question: ' + str(question.key_identifier) + ' because is has never been asked. Set its default_answer instead, then ask it.')
            return
        else:
            body = {'answer': new_answer}
            params = {'questionId': question._question_id}
            j = json.dumps(body)
            r = self._http_put('/analytic/questions', params=params, body=j)
            j = json.loads(r.text)
            _check_for_errors(j)
            question.answer = new_answer
            saved_questions = self.load_variable(QUESTIONS_VARIABLE_NAME)
            if saved_questions is None:
                saved_questions = {}
            saved_questions[question.key_identifier] = question
            self.save_variable(QUESTIONS_VARIABLE_NAME, saved_questions)
            return

    def get_rules(self, device_id=None, details=False):
        """
        Get a list of rules from this user.
        This will raise a BotError if the rules are not accessible.
        
        Remember: Rule status 0=incomplete; 1=active; 2=inactive
        
        :param device_id: Only return a list of rules for this device ID
        :param details: True to return details for this rule including all triggers, states, and actions that compose the rule. False to return only the high level information about the rule, including the ID, description text, on/off status, whether this is a default rule, and whether this rule is hidden and not editable.
        :return: List of rules if accessible.
        """
        params = {'details': details}
        if device_id is not None:
            params['deviceId'] = device_id
        r = self._http_get('/cloud/json/rules', params=params)
        j = json.loads(r.text)
        _check_for_errors(j)
        return j

    def get_rule(self, rule_id, details=False):
        """
        Get a specific rule from this user
        This will raise a BotError if the rules are not accessible.
        
        :param rule_id: Rule ID to get
        :param details: True to return details for this rule including all triggers, states, and actions that compose the rule. False to return only the high level information about the rule, including the ID, description text, on/off status, whether this is a default rule, and whether this rule is hidden and not editable.
        :return: Complete rule definition
        """
        params = {'details': details}
        r = self._http_get('/cloud/json/rules/' + str(rule_id), params=params)
        j = json.loads(r.text)
        _check_for_errors(j)
        return j

    def delete_rule(self, rule_id):
        """
        Delete a user's rule
        This will raise a BotError if rules are not accessible
        
        :param rule_id: Rule ID to delete
        """
        r = self._http_delete('/cloud/json/rules/' + str(rule_id))
        j = json.loads(r.text)
        _check_for_errors(j)
        return j

    def get_rule_phrases(self):
        """
        Get the rule phrases from which we can compose new rules
        :return: Available rule phrases
        """
        r = self._http_get('/cloud/json/ruleConditions')
        j = json.loads(r.text)
        _check_for_errors(j)
        return j

    def toggle_rule(self, rule_id, enable):
        """
        Set an attribute for a rule, like changing the name of it or switching it on or off.
        :param rule_id: ID of the rule to update
        :param enable: True to turn the rule on, False to turn it off.
        """
        status = 1
        if not enable:
            status = 2
        self.rules[rule_id] = status

    def delete_all_rules(self, status=None, rule_id_list=[], device_type_list=[], device_id_list=[], default=None, hidden=None, user_id=None):
        """
        Delete all the rules that match the given criteria
        :param status: Specific rule statuses to delete. 0=incomplete; 1=active; 2=inactive
        :param rule_id_list: Optional list of rule ID's to specifically target
        :param device_type_list: Optional list of device types to specifically target
        :param device_id_list: Optional list of device ID's to specifically target
        :param default: If True or False, update only default or non-default rules
        :param hidden: If True or False, update only hidden or non-hidden rules
        :param user_id: Optional user ID to be used by administrative / organizational bots.
        :return: List of rule_id's that were updated
        """
        params = {}
        if status is not None:
            params['status'] = status
        if len(rule_id_list) > 0:
            params['ruleId'] = rule_id_list
        if len(device_type_list) > 0:
            params['deviceType'] = device_type_list
        if len(device_id_list) > 0:
            params['deviceId'] = device_id_list
        if default is not None:
            params['default'] = default
        if hidden is not None:
            params['hidden'] = hidden
        if user_id is not None:
            params['userId'] = user_id
        r = self._http_delete('/cloud/json/rules/', params=params)
        j = json.loads(r.text)
        try:
            _check_for_errors(j)
        except BotError as e:
            for device_id in device_id_list:
                rules = self.get_rules(device_id)
                if 'rules' in rules:
                    for r in rules['rules']:
                        self.get_logger().info('Deleting rule manually ' + str(r['id']))
                        self.delete_rule(r['id'])

            return {'resultCode': 0}

        return j

    def toggle_all_rules(self, enable, rule_id_list=[], device_type_list=[], device_id_list=[], default=None, hidden=None, user_id=None):
        """
        Toggle all rules that match the given criteria
        :param enable: True to enable the rules, False to disable the rules
        :param rule_id_list: Optional list of rule ID's to specifically target
        :param device_type_list: Optional list of device types to specifically target
        :param device_id_list: Optional list of device ID's to specifically target
        :param default: If True or False, update only default or non-default rules
        :param hidden: If True or False, update only hidden or non-hidden rules
        :param user_id: Optional user ID to be used by administrative / organizational bots.
        :return: List of rule_id's that were updated
        """
        status = 1
        if not enable:
            status = 2
        params = {}
        if len(rule_id_list) > 0:
            params['ruleId'] = rule_id_list
        if len(device_type_list) > 0:
            params['deviceType'] = device_type_list
        if len(device_id_list) > 0:
            params['deviceId'] = device_id_list
        if default is not None:
            params['default'] = default
        if hidden is not None:
            params['hidden'] = hidden
        if user_id is not None:
            params['userId'] = user_id
        r = self._http_put('/cloud/json/rulesStatus/' + str(status), params=params)
        j = json.loads(r.text)
        _check_for_errors(j)
        return j

    def flush_rules(self):
        """
        Flush all rule changes to the server. This is performed automatically at the end of execution.
        """
        for rule_id in self.rules:
            body = {'rule': {'status': self.rules[rule_id]}}
            self._http_put('/cloud/json/rules/' + str(rule_id) + '/attrs', data=json.dumps(body))

    def set_ui_content(self, location_id, address, json_content):
        """
        Set information to be consumed by user interfaces through a known address.

        Application-layer developers first collectively agree upon the data
        that needs to be produced by the bot to be rendered on a UI. Then the UI
        can read the address to extract the JSON information to render natively.

        It is therefore possible for the bot to also produce new addressable content,
        as long as the addresses are retrievable from a well known base address. For example,
        you could save some UI content that includes a list of reports, each report saved under
        a unique address. Then, save UI content for each report under their unique addresses.

        :param location_id: Location ID to set UI content within
        :param address: Address to save information into, in a way that can be recalled by an app.
        :param json_content: Raw JSON content to deliver to an app/UI.
        """
        body = {'value': json_content}
        params = {'name': address}
        self.get_logger().info(('Delivering UI content: {} =\n{}').format(address, json.dumps(body, indent=2, sort_keys=True)))
        self._http_put(('/cloud/json/locations/{}/state').format(location_id), params=params, data=json.dumps(body))

    def get_ui_content(self, location_id, address):
        """
        Get UI content by address
        :param location_id: Location ID to get UI content from
        :param address: Address to retrieve information from
        :return: The JSON value for this address, or None if it doesn't exist
        """
        params = {'name': address}
        r = self._http_get(('/cloud/json/locations/{}/state').format(location_id), params=params)
        j = json.loads(r.text)
        if 'value' in j:
            return j['value']
        else:
            return
            return

    def set_admin_content(self, organization_id, address, json_content, private=True):
        """
        Set administrator content. The content is expected to be JSON content.

        Note there are other API methods to upload images and other content by changing the Content-Type header if we ever need to support that.
        But JSON is expected here.
        https://iotadmins.docs.apiary.io/#reference/organizations/organization-large-objects/upload-large-object

        :param organization_id: Organization ID to save into
        :param address: Object name
        :param json_content: Content to store
        :param content_type: Content-Type header
        :param private: True if this is privately available to the organization. False to make it publicly accessible.
        """
        self._http_put(('/admin/json/organizations/{}/objects/{}').format(organization_id, address), params={'private': private}, data=json.dumps(json_content))

    def delete_admin_content(self, organization_id, address):
        """
        Delete administrator content.
        https://iotadmins.docs.apiary.io/#reference/organizations/organization-large-objects/delete-object
        :param organization_id: Organization ID to delete from
        :param address: Object name
        """
        self._http_delete(('/admin/json/organizations/{}/objects/{}').format(organization_id, address))

    def send_datastream_message(self, address, feed_dictionary, bot_instance_list=None, scope=1, location_id_list=None):
        """
        Send a Data Stream Message
        :param address: Data stream address
        :param feed_dictionary: Dictionary of key/value pairs to send to this data stream address
        :param bot_instance_list: Send data to specific list of bot instances.
        :param scope: Send the data stream message to - 1=Bots at a Location; 2=Bots in an Organization; 4=Bots in a Circle
        :param location_id_list: Send data to bots of the specific list of locations, used by Organizational Bots
        """
        params = {'address': address, 
           'scope': scope}
        body = {'feed': feed_dictionary}
        if bot_instance_list is not None:
            body['bots'] = bot_instance_list
        if location_id_list is not None:
            body['locations'] = location_id_list
        r = self._http_post('/analytic/stream', params=params, data=json.dumps(body))
        j = json.loads(r.text)
        _check_for_errors(j)
        return j

    def narrate(self, location_id, title=None, description=None, priority=None, icon=None, status=None, timestamp_ms=None, file_ids=None, extra_json_dict=None, update_narrative_id=None, update_narrative_timestamp=None, admin=False):
        """
        Narrate some activity
        :param location_id: Location ID
        :param title: Title of the event
        :param description: Description of the event
        :param priority: 0=debug; 1=info; 2=warning; 3=critical
        :param icon: Icon name, like 'motion' or 'phone-alert'. See http://peoplepowerco.com/icons
        :param status: Status of the narrative. 0=initial; 1=deleted; 2=resolved; 3=reopened
        :param timestamp_ms: Optional timestamp for this event. Can be in the future. If not set, the current timestamp is used.
        :param file_ids: List of file ID's (media) to reference and show as part of the record in the UI
        :param extra_json_dict: Any extra JSON dictionary content we want to communicate with the UI
        :param update_narrative_id: Specify a narrative ID to update an existing record.
        :param update_narrative_timestamp: Specify a narrative timestamp to update an existing record. This is a double-check to make sure we're not overwriting the wrong record.
        :param admin: True to alert an administrator; False (default) to deliver to the end user.
        :return: { "narrativeId": id, "narrativeTime": timestamp_ms } if successful, otherwise None.
        """
        narrative = {}
        if priority is not None:
            narrative['priority'] = priority
        if icon is not None:
            narrative['icon'] = icon
        if title is not None:
            narrative['title'] = title
        if description is not None:
            narrative['description'] = description
        if self.get_server_version() >= 1.7:
            if status is not None:
                narrative['status'] = status
        if timestamp_ms is not None:
            narrative['narrativeTime'] = timestamp_ms
        target = {}
        if file_ids is not None:
            target['fileIDs'] = file_ids
        if extra_json_dict is not None:
            target.update(extra_json_dict)
        if len(target) > 0:
            narrative['target'] = target
        params = {}
        if update_narrative_id is not None:
            params['narrativeId'] = update_narrative_id
        if update_narrative_timestamp is not None:
            params['narrativeTime'] = update_narrative_timestamp
        if admin:
            params['scope'] = 2
        else:
            params['scope'] = 1
        body = {'narrative': narrative}
        self.get_logger().info(('Narrate body: \n{}').format(json.dumps(narrative, indent=2, sort_keys=True)))
        self.get_logger().info(('Narrate params: {}').format(json.dumps(params, indent=2, sort_keys=True)))
        self.get_logger().info(('Narrate PUT URL: {}').format(('/cloud/json/locations/{}/narratives').format(location_id)))
        r = self._http_put(('/cloud/json/locations/{}/narratives').format(location_id), params=params, data=json.dumps(body))
        j = json.loads(r.text)
        self.get_logger().info(('Narrate response: \n{}').format(json.dumps(j, indent=2, sort_keys=True)))
        if 'narrativeTime' in j:
            if 'narrativeId' in j:
                narrativeId = j['narrativeId']
            else:
                narrativeId = update_narrative_id
            if narrativeId is not None:
                self.get_logger().info(('BotEngine: Narrative {}: title={}; description={}; priority={}').format(narrativeId, title, description, priority))
                return {'narrativeId': narrativeId, 
                   'narrativeTime': j['narrativeTime']}
        return

    def delete_narration(self, location_id, narrative_id, narrative_timestamp):
        """
        Delete a narrative record
        :param location_id: Location ID
        :param narrative_id: ID of the record to delete
        :param narrative_timestamp: Timestamp of the record to delete
        :return:
        """
        params = {'narrativeId': narrative_id, 
           'narrativeTime': narrative_timestamp}
        r = self._http_delete(('/cloud/json/locations/{}/narratives').format(location_id), params=params)
        j = json.loads(r.text)
        return j

    def create_challenge_from_template(self, challenge_name, start_timestamp_ms, end_timestamp_ms, parent_template_id):
        """
        Create a challenge
        :param challenge_name: Name of this challenge
        :param start_timestamp_ms: Start timestamp in milliseconds
        :param end_timestamp_ms: End timestamp in milliseconds
        :param parent_template_id: Challenge or template ID to copy settings from. When a challenge is created using a template, all the attributes which are not explicitly specified will be copied from the template.
        :return: JSON response dictionary with "challengeId" key of the challenge ID that was created
        """
        if 'organization' not in self.inputs:
            return
        params = {'parentId': parent_template_id}
        from dateutil.tz import tzlocal
        challenge = {'challenge': {'name': challenge_name, 
                         'startDate': datetime.datetime.fromtimestamp(int(start_timestamp_ms / 1000), tzlocal()).isoformat(), 
                         'endDate': datetime.datetime.fromtimestamp(int(end_timestamp_ms / 1000), tzlocal()).isoformat()}}
        r = self._http_post('/admin/json/organizations/' + str(self.inputs['organization']['organizationId']) + '/challenges', params=params, data=json.dumps(challenge))
        j = json.loads(r.text)
        _check_for_errors(j)
        return j

    def get_organization_challenge_participants(self, challenge_id, status=None, user_id=None, get_devices=None, device_category=None):
        """
        Get information about the participants of the challenge.
        This is accessible to Organizational Bots only.
        
        :param challenge_id: Challenge ID
        :param status: Participation status filter: 1=Not Responded; 2=Opt-in; 3=Opt-out
        :param user_id: Filter the response by user ID.
        :param get_devices: True or False. Return user devices as well.
        :param device_category: Filter devices by this category.
        """
        if 'organization' not in self.inputs:
            return
        params = {}
        if status:
            params['status'] = status
        if user_id:
            params['userId'] = user_id
        if get_devices:
            params['getDevices'] = get_devices
        if device_category:
            params['deviceCategory'] = device_category
        r = self._http_get('/analytic/admin/challenges/' + str(challenge_id) + '/participants', params=params)
        j = json.loads(r.text)
        _check_for_errors(j)
        return j

    def get_organization_groups(self, group_id=None, group_name=None, group_type=None, get_user_totals=False, get_average_bills=False, bill_start_date=None):
        """
        Get the groups in this organization.
        This is accessible to Organizational Bots only.
        
        :param group_id: Integer - Search by group ID
        :param group_name: String - Search by the first characters of a group name
        :param group_type: Integer - Search by group type. 0 = Residential; 1 = Business
        :param get_user_totals: Boolean - True to request the total approved, applied, and rejected users in this group
        :param get_average_bills: Boolean - True to request the average monthly energy bill information for a specific group ID.
        :param bill_start_date: Xsd:dateTime string - return monthly bills from the given start date
        :return: Dictionary
        """
        if 'organization' not in self.inputs:
            return
        params = {}
        if group_id:
            params['groupId'] = group_id
        if group_name:
            params['name'] = group_name
        if group_type:
            params['type'] = group_type
        if get_user_totals:
            params['userTotals'] = get_user_totals
        if get_average_bills:
            params['averageBills'] = get_average_bills
        if bill_start_date:
            params['billsStartDate'] = bill_start_date
        r = self._http_get('/admin/json/organizations/' + str(self.inputs['organization']['organizationId']) + '/groups', params=params)
        j = json.loads(r.text)
        _check_for_errors(j)
        return j

    def get_organization_users(self, group_id=None, status=None, search_by=None, search_tag=None, search_device_tag=None, points_from=None, points_to=None, limit=None, get_tags=False):
        """
        Get users in this organization.
        This is accessible to Organizational Bots only.
        
        :param group_id: Search by group ID
        :param status: String - Search for users with a specific status. 0=Applied; 1=Approved; -1=Rejected; -2=Opted Out
        :param search_by: String - Search for matching user login names, first name, last name, and email address. Use * for wildcard.
        :param search_tag: String - Search by user tag
        :param search_device_tag: String - Search by device tag
        :param points_from: Integer - Get users who have more points than this amount
        :param points_to: Integer - Get users who have less points than this amount
        :param limit: Integer - the maximum number of user records to retrieve in this request
        :param get_tags: Boolean - Return user tags
        :return: Dictionary
        """
        if 'organization' not in self.inputs:
            return
        params = {}
        if group_id:
            params['groupId'] = group_id
        if status:
            params['organizationStatus'] = status
        if search_by:
            params['searchBy'] = search_by
        if search_tag:
            params['searchTag'] = search_tag
        if search_device_tag:
            params['searchDeviceTag'] = search_device_tag
        if points_from:
            params['pointsFrom'] = points_from
        if points_to:
            params['pointsTo'] = points_to
        if limit:
            params['limit'] = limit
        if get_tags:
            params['getTags'] = get_tags
        r = self._http_get('/admin/json/organizations/' + str(self.inputs['organization']['organizationId']) + '/users', params=params)
        j = json.loads(r.text)
        _check_for_errors(j)
        return j

    def get_organization_devices(self, linked_to=1, group_id=None, user_id=None, location_id=None, tree=None, device_types_list=None, search_by=None, search_tag=None, last_update_date_older_than=None, last_update_date_newer_than=None, param_name=None, param_value=None, limit=None, get_tags=None):
        """
        Get devices in this organization.
        This is accessible to Organizational Bots only.
        
        :param linked_to: Integer - Request devices linked to 1=Users; 2=Locations; 3=Users&Locations
        :param group_id: Integer - Group ID to search within
        :param user_id: Integer - Filter by User ID
        :param location_id: Integer - Filter by Location ID
        :param tree: Boolean - True to retrieve devices from sub-locations as well
        :param device_types_list: List of Integers - Filter by these device types
        :param search_by: String - Search by device ID or description
        :param search_tag: String - Search by device tag
        :param last_update_date_older_than: Xsd:dateTime string - Request devices where the last update date is older than this
        :param last_update_date_newer_than: Xsd:dateTime string - Request devices where the last update date is newer than this
        :param param_name: String - Request devices that sent this parameter name to the cloud
        :param param_value: String - Requested parameter value
        :param limit: Integer - Limit the response size by this number
        :param get_tags: Boolean - True to return device tags
        :return: Dictionary
        """
        if 'organization' not in self.inputs:
            return
        params = {}
        if linked_to:
            params['linkedTo'] = linked_to
        if group_id:
            params['groupId'] = group_id
        if user_id:
            params['userId'] = user_id
        if location_id:
            params['locationId'] = location_id
        if tree:
            params['tree'] = tree
        if device_types_list:
            params['deviceType'] = device_types_list
        if search_by:
            params['searchBy'] = search_by
        if search_tag:
            params['searchTag'] = search_tag
        if last_update_date_older_than:
            params['lessUpdateDate'] = last_update_date_older_than
        if last_update_date_newer_than:
            params['moreUpdateDate'] = last_update_date_newer_than
        if param_name:
            params['paramName'] = param_name
        if param_value:
            params['paramValue'] = param_value
        if limit:
            params['limit'] = limit
        if get_tags:
            params['getTags'] = get_tags
        r = self._http_get('/admin/json/organizations/' + str(self.inputs['organization']['organizationId']) + '/devices', params=params)
        j = json.loads(r.text)
        _check_for_errors(j)
        return j

    def flush_analytics(self):
        """
        If you have included an analytics.py in the base bot directory, this will attempt
        to call the analytics.flush(botengine) method as the bot is exiting execution.

        You can then connect your analytics to whatever analytics platform you prefer.
        """
        try:
            analytics = importlib.import_module('analytics')
            if analytics.has_analytics(self):
                analytics.get_analytics(self).flush(self)
        except ImportError:
            return

    @staticmethod
    def _strftimestamp(ts):
        """This private method will convert the time in seconds to the string of IOS-8601 format, eg: '2014-06-20T12:47:11-07:00

        :param ts: the time in seconds, eg: 1403293631
        """
        t = datetime.datetime.fromtimestamp(ts)
        return t.astimezone().isoformat()

    @staticmethod
    def strftimestamp(ts):
        """This method will convert the time in milliseconds to the string of IOS-8601 format, eg: '2014-06-20T12:47:11-07:00

        :param ts: the time in seconds, eg: 1403293631000
        """
        response = BotEngine._strftimestamp(ts // 1000)
        return response

    @staticmethod
    def strftime(dt):
        """This method will convert the datetime object to the string of IOS-8601 format, eg: '2014-06-20T12:47:11-07:00

        :param dt: the datetime object
        """
        response = BotEngine._strftimestamp(dt.timestamp() // 1)
        return response

    @staticmethod
    def strptime(dt_str):
        """This method will convert the string of IOS-8601 to the datetime object

        :param dt_str: the string of IOS-8601 format (eg: '2014-06-20T12:47:11-07:00)
        """
        from dateutil.parser import parse
        response = parse(dt_str)
        return response

    @staticmethod
    def get_logger():
        return _bot_logger


class Question():
    """
    Class to hold a question and its answer
    """
    QUESTION_RESPONSE_TYPE_BOOLEAN = 1
    QUESTION_RESPONSE_TYPE_MULTICHOICE_SINGLESELECT = 2
    QUESTION_RESPONSE_TYPE_MULTICHOICE_MULTISELECT = 4
    QUESTION_RESPONSE_TYPE_DAYOFWEEK = 6
    QUESTION_RESPONSE_TYPE_SLIDER = 7
    QUESTION_RESPONSE_TYPE_TIME = 8
    QUESTION_RESPONSE_TYPE_DATETIME = 9
    QUESTION_RESPONSE_TYPE_TEXT = 10
    QUESTION_DISPLAY_BOOLEAN_ONOFF = 0
    QUESTION_DISPLAY_BOOLEAN_YESNO = 1
    QUESTION_DISPLAY_BOOLEAN_BUTTON = 2
    QUESTION_DISPLAY_MCSS_RADIO_BUTTONS = 0
    QUESTION_DISPLAY_MCSS_PICKER = 1
    QUESTION_DISPLAY_DAYOFWEEK_MULTISELECT = 0
    QUESTION_DISPLAY_DAYOFWEEK_SINGLESELECT = 1
    QUESTION_DISPLAY_SLIDER_INTEGER = 0
    QUESTION_DISPLAY_SLIDER_FLOAT = 1
    QUESTION_DISPLAY_SLIDER_MINSEC = 2
    QUESTION_DISPLAY_TIME_HOURS_MINUTES_SECONDS_AMPM = 0
    QUESTION_DISPLAY_TIME_HOURS_MINUTES_AMPM = 1
    QUESTION_DISPLAY_DATETIME_DATE_AND_TIME = 0
    QUESTION_DISPLAY_DATETIME_DATE = 1
    ANSWER_STATUS_NOT_ASKED = -1
    ANSWER_STATUS_DELAYED = 0
    ANSWER_STATUS_QUEUED = 1
    ANSWER_STATUS_AVAILABLE = 2
    ANSWER_STATUS_SKIPPED = 3
    ANSWER_STATUS_ANSWERED = 4
    ANSWER_STATUS_NO_ANSWER = 5

    def __init__(self, key_identifier, response_type, device_id=None, icon=None, display_type=None, editable=False, default_answer=None, correct_answer=None, answer_format=None, urgent=False, front_page=False, send_push=False, send_sms=False, send_email=False, ask_timestamp=None, section_id=0, question_weight=0):
        """
        Initializer

        :param key_identifier: Your own custom key to recognize this question regardless of the language or framing of the question to the user.
        :param response_type: Type of response we should expect the user to give
            1 = Boolean question
            2 = Multichoice, Single select (requires response options)
            4 = Multichoice, Multi select (requires response options)
            6 = Day of the Week
            7 = Slider (Default minimum is 0, default maximum is 100, default increment is 5)
            8 = Time in seconds since midnight
            9 = Datetime (xsd:dateTime format)
            10 = Open-ended text

        :param device_id: Device ID to ask a question about so the UI can reference its name
        :param icon: Icon to display when asking this question
        :param display_type: How to render and display the question in the UI. For example, a Boolean question can be an on/off switch, a yes/no question, or just a single button. See the documentation for more details.
        :param editable: True to make this question editable later. This makes the question more like a configuration for the bot that can be adjusted again and again, rather than a one-time question.
        :param default_answer: Default answer for the question
        :param correct_answer: This is a regular expression to determine if the user's answer is "correct" or not
        :param answer_format: Regular expression string that represents what a valid response would look like. All other responses would not be allowed.
        :param urgent: True if this question is urgent enough that it requires a push notification and should be elevated to the top of the stack after any current delivered questions. Use sparingly to avoid end-user burnout.
        :param front_page: True if this question should be delivered to the front page of mobile/web bot, when the user is ready to consume another question from the system.
        :param send_push: True to send this questions as a push notification. Use sparingly to avoid end user burnout.
        :param send_sms: True to send an SMS message. Because this costs money, this is currently disabled.
        :param send_email: True to send the question in an email. Use sparingly to avoid burnout and default to junk mail.
        :param ask_timestamp: Future timestamp to ask this question. If this is not set, the current time will be used.
        :param section_id: ID of a section, which acts as both the element to group by as well as the weight of the section vs. other sections in the UI. (default is 0)
        :param question_weight: Weight of an individual question within a grouped section. The lighter the weight, the more the question rises to the top of the list in the UI. (default is 0)
        """
        self.key_identifier = key_identifier
        self.response_type = response_type
        self.device_id = device_id
        self.icon = icon
        self.display_type = display_type
        self.editable = editable
        self.urgent = urgent
        self.front_page = front_page
        self.send_push = send_push
        self.send_sms = send_sms
        self.send_email = send_email
        self.correct_answer = correct_answer
        self.answer_format = answer_format
        self.default_answer = default_answer
        self.ask_timestamp = ask_timestamp
        self.tags = []
        self.question = {}
        self.placeholder = {}
        self.response_options = []
        self.section_title = {}
        self.section_id = section_id
        self.question_weight = question_weight
        self._question_id = None
        self.answer_status = self.ANSWER_STATUS_NOT_ASKED
        self.answer_time = None
        self.answer = None
        self.answer_correct = False
        self.answer_modified = False
        self.slider_min = 0
        if response_type == self.QUESTION_RESPONSE_TYPE_SLIDER:
            if display_type == self.QUESTION_DISPLAY_SLIDER_MINSEC:
                self.slider_max = 3600
                self.slider_inc = 15
            else:
                self.slider_max = 100
                self.slider_inc = 5
        return

    def _form_json_question(self):
        """
        Private function to form the JSON request to POST this question
        :return: JSON string ready to send to the server
        """
        body = {'key': self.key_identifier, 
           'urgent': self.urgent, 
           'front': self.front_page, 
           'push': self.send_push, 
           'sms': self.send_sms, 
           'email': self.send_email, 
           'responseType': self.response_type, 
           'editable': self.editable, 
           'question': self.question}
        if self.device_id is not None:
            body['deviceId'] = self.device_id
        if self.icon is not None:
            body['icon'] = self.icon
        if self.display_type is not None:
            body['displayType'] = int(self.display_type)
        if len(self.section_title) > 0:
            body['sectionTitle'] = self.section_title
        if self.section_id is not None:
            body['sectionId'] = int(self.section_id)
        if self.question_weight is not None:
            body['questionWeight'] = int(self.question_weight)
        if self.ask_timestamp:
            body['askDateMs'] = self.ask_timestamp
        if len(self.placeholder) > 0:
            body['placeholder'] = self.placeholder
        if self.response_type == self.QUESTION_RESPONSE_TYPE_SLIDER:
            body['sliderMin'] = self.slider_min
            body['sliderMax'] = self.slider_max
            body['sliderInc'] = self.slider_inc
            if self.default_answer is None:
                self.default_answer = int((self.slider_max - self.slider_min) / 2)
        if len(self.tags) > 0:
            body['tags'] = self.tags
        if self.answer:
            self.default_answer = self.answer
        if self.default_answer:
            body['defaultAnswer'] = self.default_answer
        if self.correct_answer:
            body['validAnswer'] = self.correct_answer
        if self.answer_format:
            body['answerFormat'] = self.answer_format
        if self.response_type == self.QUESTION_RESPONSE_TYPE_MULTICHOICE_MULTISELECT or self.response_type == self.QUESTION_RESPONSE_TYPE_MULTICHOICE_SINGLESELECT:
            body['responseOptions'] = []
            identifier = 0
            for option in self.response_options:
                body['responseOptions'].append(option._get_json_dictionary(identifier))
                identifier += 1

        return body

    def frame_question(self, question, language='en'):
        """
        Frame question in a specific language

        :param question: The question to ask in that language
        :param language: 'en', 'zh', etc. Default is 'en'
        """
        self.question[language] = question

    def slider_boundaries(self, slider_min=0, slider_max=100, slider_inc=5):
        """
        Set the boundaries of a question that expects a response in the form of a slider
        :param slider_min: Minimum slider boundary, default is 0
        :param slider_max: Maximum slider boundary, default is 100
        :param slider_inc: Incremental slider amount, default is 5
        """
        self.slider_min = slider_min
        self.slider_max = slider_max
        self.slider_inc = slider_inc

    def set_placeholder_text(self, placeholder, language='en'):
        """
        A placeholder adds an example to a question that expects a text-based response.
        For example, if the question was "What is your favorite color?" then the placeholder might be "Blue" in English.

        :param placeholder: Open-ended text example to prompt the user to type in their own answer.
        :param language: Language for the placeholder, 'en', 'zh', etc. Default is "en".
        """
        self.placeholder[language] = placeholder

    def set_section_title(self, section_title, language='en'):
        """
        Set the section title. 
        The top most question in the section (lowest weight) sets the title.
        
        :param section_title: Name of the section of questions
        :param language: Language for this section title, default is 'en'
        """
        self.section_title[language] = section_title

    def auto_tag_user(self, tag):
        """
        Auto-tag the user with this tag if they provide is the "correct" response, based on the correct_answer regular expression.
        Cannot be used with any list-type questions.
        Can be called multiple times to add multiple tags:  this simply does a self.tags.append(tag) so you could alternatively
        set it in a more Pythonic way by doing something like:  question.tags = ["tag1","tag2"]

        :param tag: Tag to tag the user's account with if they provide any valid response.
        """
        self.tags.append(tag)

    def generate_response_option(self, text=None, language='en'):
        """
        Get a QuestionResponseOption object
        :param text: Text for this response option
        :param language: Language identifier for that text, i.e. 'en'
        :return: QuestionResponseOption object that has been added to this question, for yours to edit
        """
        option = QuestionResponseOption(len(self.response_options), text, language)
        self.response_options.append(option)
        return option

    def ready_to_ask(self):
        """
        :return: True if this question is ready to ask
        """
        if len(self.question) == 0:
            return False
        if self.response_type == self.QUESTION_RESPONSE_TYPE_RADIO or self.response_type == self.QUESTION_RESPONSE_TYPE_DROPDOWN or self.response_type == self.QUESTION_RESPONSE_TYPE_CHECKBOX or self.response_type == self.QUESTION_RESPONSE_TYPE_MULTISELECT:
            return len(self.response_options) > 0
        return True


class QuestionResponseOption():
    """
    A single response option to a question that is a radio button, drop-down list, checkbox, or multi-select type of question
    """

    def __init__(self, identifier, text=None, language='en'):
        """
        Initialize
        :param identifier: Unique incremental identifier for this response, starting with 0
        :param text: Text for this response option
        :param language: Language identifier for that text, i.e. 'en'
        """
        self.identifier = identifier
        self.text = {}
        self.tags = []
        self.complete = False
        if text is not None:
            self.add_text(text, language)
        return

    def _get_json_dictionary(self, identifier):
        """
        Private method to get a dictionary representing the content that needs to get injected into a JSON API POST
        :param identifier: id of this response option relative to other option, starting with 0
        :return: Dictionary formatted to conform to the POST API
        """
        block = {'id': identifier, 
           'text': self.text}
        if len(self.tags) > 0:
            block['tags'] = self.tags
        return block

    def add_text(self, text, language='en'):
        """
        Add some text to this question's response option, in a specificied language

        :param text: Text for this option
        :param language: Language abbreviation, 'en' by default
        :return: self, so you can keep adding more if you want.
        """
        self.complete = True
        self.text[language] = text
        return self

    def add_tag(self, tag):
        """
        Tag a user with this tag if they answer in this way

        :param tag: Tag to tag the user with if they answer the question in this way
        :return: self, so you can keep adding more if you want.
        """
        self.tags.append(tag)
        return self


class BotError(Exception):
    """BotEngine exception to raise and log errors."""

    def __init__(self, msg, code):
        super(BotError).__init__(type(self))
        self.msg = msg
        self.code = code

    def __str__(self):
        return self.msg

    def __unicode__(self):
        return self.msg


class Color():
    """Color your command line output text with Color.WHATEVER and Color.END"""
    PURPLE = '\x1b[95m'
    CYAN = '\x1b[96m'
    DARKCYAN = '\x1b[36m'
    BLUE = '\x1b[94m'
    GREEN = '\x1b[92m'
    YELLOW = '\x1b[93m'
    RED = '\x1b[91m'
    BOLD = '\x1b[1m'
    UNDERLINE = '\x1b[4m'
    END = '\x1b[0m'


if __name__ == '__main__':
    if DEBUG:
        sys.argv.append('--debug')
    if TESTRUN:
        import doctest
        doctest.testmod()
    if PROFILE:
        import cProfile, pstats
        profile_filename = 'botengine.botengine_profile.txt'
        cProfile.run('main()', profile_filename)
        statsfile = open('profile_stats.txt', 'wb')
        p = pstats.Stats(profile_filename, stream=statsfile)
        stats = p.strip_dirs().sort_stats('cumulative')
        stats.print_stats()
        statsfile.close()
        sys.exit(0)
    sys.exit(main())
# okay decompiling botengine.pyc
