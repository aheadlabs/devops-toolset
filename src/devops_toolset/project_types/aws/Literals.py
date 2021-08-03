"""AWS module literals"""

from devops_toolset.core.app import App
from devops_toolset.core.ValueDictsBase import ValueDictsBase

app: App = App()


class Literals(ValueDictsBase):
    """ValueDicts for the AWS module."""

    _info = {
        "cloudfront_invalidation_created": _("Created CloudFront invalidation with id {id}")
    }
    _errors = {}
