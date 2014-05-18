import ConfigParser

config = ConfigParser.RawConfigParser()

# When adding sections or items, add them in the reverse order of
# how you want them to be displayed in the actual file.
# In addition, please note that using RawConfigParser's and the raw
# mode of ConfigParser's respective set functions, you can assign
# non-string values to keys internally, but will receive an error
# when attempting to write to a file or when you get it in non-raw
# mode. SafeConfigParser does not allow such assignments to take place.
config.add_section('server')
config.set('server', 'database_prefix', 'ttrss_')
config.set('server', 'password', '')
config.set('server', 'user', 'ttrss')
config.set('server', 'database', 'ttrss')
config.set('server', 'host', '127.0.0.1')

config.add_section('debug')
config.set('debug', 'debug_enabled', 'True')

config.add_section('filter')
config.set('filter', 'bigram_enabled', 'True')


config.add_section('statistics')
config.set('statistics', 'statistics_enabled', 'True')

# Writing our configuration file to 'example.cfg'
with open('config.cfg', 'wb') as configfile:
    config.write(configfile)
