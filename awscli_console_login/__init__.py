from .login import ConsoleLogin


def awscli_initialize(cli):
    cli.register('building-command-table.main', inject_commands)


def inject_commands(command_table, session, **kwargs):
    command_table['console-login'] = ConsoleLogin(session)
