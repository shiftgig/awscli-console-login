# awscli-console-login

The awscli-console-login plugin converts roles [described in `~/.aws/config`](https://docs.aws.amazon.com/cli/latest/userguide/cli-roles.html) into active AWS console sessions in your browser.

[While the console enables cross-account access](https://aws.amazon.com/blogs/security/how-to-enable-cross-account-access-to-the-aws-management-console/), its support is limited to 5 roles. Any multi-account strategy is likely to require a greater number of roles. This plugin simplifies and unifies the management of those role ARNs via the local config file.


## Usage

To get started, simply install the package and add it to your config file's plugin section. Note that the second step can be performed by manually editing `~/.aws/config` instead.

```bash
$ pip install awscli-console-login
$ aws configure set plugins.console awscli_console_login
```

Thereafter, invoke the command on the appropriate profile. A logged-in console session should open in your browser of choice:

```bash
$ aws console-login --profile poc
```


## Sponsors

This plugin was made possible by [Shiftgig](https://www.shiftgig.com/).


## License

This plugin is released under the Apache License, Version 2.0.


## Support

Please file an issue on the github repository if you think anything isn't working properly or an improvement is required.
