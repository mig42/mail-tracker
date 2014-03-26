import ConfigParser
import os

SECTION = "mail"

MAIL_USERNAME = "username"
MAIL_PASSWORD = "password"
MAIL_SERVER = "smtp_server"

DEFAULT_MAIL_USERNAME = "mailtrackerpython"
DEFAULT_MAIL_PASSWORD = "oyapulpo"
DEFAULT_MAIL_SERVER = "smtp.gmail.com:587"

class Settings ():

    def __init__(self, file_name):
        # TODO: self._settingFilePath = os.path.join('~.mail-tracker', 'settings.cfg')
        _settingParser = ConfigParser.SafeConfigParser({
            MAIL_USERNAME: DEFAULT_MAIL_USERNAME,
            MAIL_PASSWORD: DEFAULT_MAIL_PASSWORD,
            MAIL_SERVER: DEFAULT_MAIL_SERVER})
        _settingParser.read(get_settings_file_path(file_name))

        # [mail]
        self.username = _settingParser.get(SECTION, MAIL_USERNAME)
        self.password = _settingParser.get(SECTION, MAIL_PASSWORD)
        self.smtp_server = _settingParser.get(SECTION, MAIL_SERVER)


def get_settings_file_path(file_name):
    return os.path.join(os.path.dirname(__file__), file_name)
