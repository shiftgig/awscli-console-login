import webbrowser
from six.moves import urllib_parse

import botocore.exceptions
import requests
from awscli.customizations.commands import BasicCommand


class ConsoleLogin(BasicCommand):
    """Login to the AWS Console, opening the browser of choice."""
    NAME = 'console-login'
    DESCRIPTION = 'Logs into the AWS browser console'
    SYNOPSIS = 'aws console-login [--duration secs] [--browser browser-name]'
    ARG_TABLE = [
        {
            'name': 'duration',
            'default': '43200',
            'required': False,
            'help_text': 'Duration of the session to create (default: 43200)',
        },
        {
            'name': 'browser',
            'required': False,
            'help_text': 'Browser in which to open the console',
        },
    ]

    def _run_main(self, parsed_args, parsed_globals):
        credentials = self._load_credentials()
        signin_token = self._get_signin_token(credentials, parsed_args.duration)
        self._open_console(signin_token, parsed_args.browser)

    def _load_credentials(self):
        """Retrieve credentials from current session.

        :return: the credentials of the current session, if any
        :rtype: botocore.credentials.Credentials
        :raises botocore.exceptions.NoCredentialsError:
            if no credentials could be located
        :raises botocore.exceptions.PartialCredentialsError:
            if the obtained credentials do not resolve a session token
        """
        credentials = self._session.get_credentials()
        if not credentials:
            raise botocore.exceptions.NoCredentialsError()

        # TODO: Obtain a session token if one is not included in the loaded
        # credentials.
        # Console login can be accomplished only if the loaded credentials
        # include a session token, eg. for a profile that assumes a role. It
        # will not work if the creds provide a direct Access Key and Secret Key
        if not credentials.token:
            raise botocore.exceptions.PartialCredentialsError(
                provider=credentials.method,
                cred_var='token'
            )
        return credentials

    def _get_signin_token(self, credentials, duration):
        """Make a GET request to retrieve a sign-in token.

        :param credentials: the user credentials of the current session
        :type crendentials: botocore.credentials.Credentials
        :param duration: the number of seconds the console session should last
        :type duration: int or str
        :return: the newly-created sign-in token
        :rtype: str
        :raises requests.exceptions.RequestException:
            if the AWS response has a status code >= 400
        """
        session_param = {
            'sessionId': credentials.access_key,
            'sessionKey': credentials.secret_key,
            'sessionToken': credentials.token,
        }
        response = requests.get(
            'https://signin.aws.amazon.com/federation',
            params={
                'Action': 'getSigninToken',
                'SessionDuration': duration,
                'Session': str(session_param),
            },
        )
        if not response.ok:
            response.raise_for_status()
        token_response = response.json()
        return token_response['SigninToken']

    def _open_console(self, signin_token, browser=None):
        """Open the console with the specified browser.

        :param signin_token: an AWS sign-in token
        :type signin_token: str
        :param browser: the browser in which to open the console
        :type browser: str or None
        """
        url = (
            'https://signin.aws.amazon.com/federation'
            '?Action=login'
            '&Issuer='
            '&Destination={dest}'
            '&SigninToken={token}'
        ).format(
            dest=urllib_parse.quote_plus('https://console.aws.amazon.com/'),
            token=signin_token,
        )
        webbrowser.get(browser).open(url)
