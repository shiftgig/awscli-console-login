import os.path

from awscli.customizations.commands import BasicCommand


class BrowserLogin(BasicCommand):
    """Login to the AWS Console, opening the browser of choice."""
    NAME = 'console-login'
    DESCRIPTION = 'Logs into the AWS browser console'
    # SYNOPSIS = ''
    # EXAMPLES = ''
    ARG_TABLE = [
        {
            'name': 'config',
            'required': False,
            'default': os.path.expanduser('~/.aws/config'),
            'help_text': 'Path to config file (default: ~/.aws/config)',
        },
        {
            'name': 'browser',
            'required': False,
            'help_text': 'Browser in which to open the console',
        },
    ]

    def _run_main(self, parsed_args, parsed_globals):
        # read credentials
        # get token
        # open console
        pass

    def _parse_credentials(self, config_path):
        """Retrieve credentials from current session."""
        pass

    def _get_login_token(self, credentials):
        """Make a GET request to retrieve a sign-in token."""
        pass

    def _open_console(self, signin_token, browser=None):
        """Open the console with the specified browser."""
        pass
