"""wordpress module commands"""

from core.ValueDictsBase import ValueDictsBase
from core.app import App

app: App = App()


class Commands(ValueDictsBase):
    """Commands for the wordpress module."""

    # Add your wordpress literal dictionaries here
    _commands = {
        "npm_install": "npm install {folder}",
        "npm_run": "npm run {command} {silent} {if_present} {extra_args}",
        "theme_src_build": "gulp build --theme-slug=\"{theme_slug}\" --wordpress-path=\"{path}\"",
        "theme_src_watch":
            "gulp watch --theme-slug=\"{theme_slug}\" --dev-proxy=\"{local_web_server}\" --wordpress-path=\"{path}\""
    }
