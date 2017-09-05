# flow
Stitching together all the tools that organize my life to maximize personal capacity and free my mind.

## setup
- Have Python 3.3.* as default version on OS (`python`)
- At base of repository run: 
    + `python -m venv venv`
    + Activate your venv: `. ./venv/bin/activate`
    + `pip install --upgrade pip`
    + `pip install -r requirements.txt`
- Use the following shebang: `#!/usr/bin/env python`
- Before running any script, activate your venv: `./venv/bin/activate`
- Before releasing, use pip freeze > requirements.txt
    + remove `pkg-resources` line from requirements.txt
- To run tests: `python -m unittest discover`
- To run tests with coverage: `coverage run -m unittest discover`
- To generate coverage report: `coverage html --omit="*/venv*"`
- View report by opening: `./htmlcov/index.html`
- You'll need to provide credentials for each piece of the flow to work
    + Gmail will require an app password: https://support.google.com/accounts/answer/185833
    + Trello will require oauth tokens
- These credentials should be stored in *.cred files in the `credentials` directory
- Also, in a Windows terminal, you may encounter issues when echoing unicode characters for debug purposes, so execute the following: `chcp 65001`

Now all scripts should reference the version of python in that venv, install all additional libs from that path

Sublime Text libraries will need to be installed in the plugin itself, which should only be done when development is complete.  Maybe we can trick sublime with links in the meantime?

I'll have to write a python package for vyte_in, it's too new to have one exist already.

I'll also need to figure out how to make Outlook and OneNote play nice with python as well.  Perhaps COM plugins?

## attribution
- https://github.com/todotxt/todotxt
- https://github.com/dropbox/dropbox-sdk-python
- https://github.com/rakanalh/pocket-api
- https://vyte.readme.io/v1.0/docs

## useful
- https://github.com/dertuxmalwieder/SublimeTodoTxt
- https://github.com/QTodoTxt/QTodoTxt2
- https://developers.google.com/gmail/api/v1/reference/
- https://developers.google.com/google-apps/calendar/v3/reference/
- https://developers.google.com/resources/api-libraries/documentation/drive/v2/python/latest/
- https://developers.google.com/drive/v3/web/quickstart/python