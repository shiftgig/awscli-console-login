from unittest import mock, TestCase

from botocore.hooks import HierarchicalEmitter
from botocore.session import Session

from awscli_console_login import (
    awscli_initialize,
    ConsoleLogin,
    inject_commands,
)


class AwscliInitializeTestCase(TestCase):
    def test_register_command_injection(self):
        emitter = HierarchicalEmitter()
        with mock.patch.object(emitter, 'register') as mock_register:
            awscli_initialize(emitter)
        mock_register.assert_called_once_with(
            'building-command-table.main',
            inject_commands
        )


class InjectCommandsTestCase(TestCase):
    def test_add_console_login_command(self):
        command_table = {}
        session = Session()
        inject_commands(command_table, session)
        self.assertIn('console-login', command_table.keys())
        self.assertIsInstance(command_table['console-login'], ConsoleLogin)
        self.assertIs(command_table['console-login']._session, session)
