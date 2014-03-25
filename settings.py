import ConfigParser
import os





class Settings ():
    def __init__(self):
        self._settingParser = ConfigParser.RawConfigParser()
        # TODO: self._settingFilePath = os.path.join('~.mail-tracker', 'settings.cfg')
        self._settingFilePath = os.path.join(os.path.dirname(__file__), 'settings.cfg')
        self._settingParser.read(self._settingFilePath)
        # [mail]
        self.username = self._settingParser.get("mail","username")
        self.password = self._settingParser.get("mail","password")
        self.smtp_server = self._settingParser.get("mail","smtp_server")
