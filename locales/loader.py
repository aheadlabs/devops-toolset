from core.settings import Settings
import gettext

settings = Settings()
gettext.translation("base", localedir="locales", languages=[settings.language]).install()
