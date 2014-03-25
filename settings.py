import ConfigParser
import os






class Settings ():
    def __init__(self):
        self._settingParser = ConfigParser.RawConfigParser()
        self._settingFilePath = os.path.join(os.path.dirname(__file__), 'settings.cfg')
        self._settingParser.read(self._settingFilePath)
        # Email
        self.username = self._settingParser.get("mail","username")
        self.password = self._settingParser.get("mail","password")
        self.smtp_server = self._settingParser.get("mail","smtp_server")
