import six
from argparse import Namespace
from contextlib import ExitStack
from unittest import mock, TestCase

import responses
from botocore.credentials import Credentials
from botocore.exceptions import NoCredentialsError
from botocore.session import Session

from awscli_console_login.login import ConsoleLogin


class ConsoleLoginTestCase(TestCase):
    def setUp(self):
        super().setUp()
        self.command = ConsoleLogin(Session())


class AttributeTestCase(ConsoleLoginTestCase):
    def test_class_attributes(self):
        self.assertEqual(ConsoleLogin.NAME, 'console-login')
        self.assertEqual(
            ConsoleLogin.DESCRIPTION,
            'Logs into the AWS browser console'
        )
        self.assertEqual(
            ConsoleLogin.SYNOPSIS,
            'aws console-login [--duration secs] [--browser browser-name]'
        )
        six.assertCountEqual(
            self,
            ConsoleLogin.ARG_TABLE,
            [
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
        )


class RunMainTestCase(ConsoleLoginTestCase):
    def test_delegates_console_signin(self):
        parsed_args = Namespace()
        parsed_args.duration = '3600'
        parsed_args.browser = 'firefox'
        with ExitStack() as stack:
            context_managers = (
                mock.patch.object(self.command, '_load_credentials'),
                mock.patch.object(self.command, '_get_signin_token'),
                mock.patch.object(self.command, '_open_console'),
            )
            for context_manager in context_managers:
                stack.enter_context(context_manager)

            self.command._run_main(parsed_args, Namespace())
            self.command._load_credentials.assert_called_once_with()
            self.command._get_signin_token.assert_called_once_with(
                self.command._load_credentials.return_value,
                '3600'
            )
            self.command._open_console.assert_called_once_with(
                self.command._get_signin_token.return_value,
                'firefox'
            )


class LoadCredentialsTestCase(ConsoleLoginTestCase):
    def test_return_botocore_credentials(self):
        dummy_credentials = Credentials('access_key', 'secret_key')
        with mock.patch.object(
            self.command._session,
            'get_credentials',
            return_value=dummy_credentials
        ):
            credentials = self.command._load_credentials()
        self.assertIs(credentials, dummy_credentials)

    def test_raise_error_on_missing_credentials(self):
        with mock.patch.object(
            self.command._session,
            'get_credentials',
            return_value=None
        ):
            with self.assertRaises(NoCredentialsError):
                self.command._load_credentials()


class GetSigninTokenTestCase(ConsoleLoginTestCase):
    @responses.activate
    def test_request_signin_token(self):
        responses.add(
            responses.GET,
            'https://signin.aws.amazon.com/federation',
            status=200,
            json={'SigninToken': 'some_token'},
        )

        credentials = Credentials('access_key', 'secret_key')
        signin_token = self.command._get_signin_token(credentials, '3600')
        self.assertEqual(signin_token, 'some_token')

        call = responses.calls[0]
        self.assertIn('SessionDuration=3600', call.request.path_url)
        self.assertIn('Session=', call.request.path_url)
        self.assertIn(credentials.access_key, call.request.path_url)
        self.assertIn(credentials.secret_key, call.request.path_url)
        self.assertIn(str(credentials.token), call.request.path_url)


class OpenConsoleTestCase(ConsoleLoginTestCase):
    def test_open_browser_url(self):
        with mock.patch('webbrowser.get') as mock_get_browser:
            self.command._open_console('some_token', browser='chrome')

        mock_get_browser.assert_called_once_with('chrome')
        mock_get_browser.return_value.open.assert_called_once_with(
            'https://signin.aws.amazon.com/federation?Action=login'
            '&Issuer=&Destination={}&SigninToken=some_token'.format(
                six.moves.urllib_parse.quote_plus('https://console.aws.amazon.com/')
            )
        )
