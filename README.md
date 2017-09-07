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
    + Oauth tokens will be used for most authetication
- These credentials should be stored in *.cred files in the `credentials` directory
- At work, you'll need to `set http_proxy=http://...` and `set https_proxy=http://...` to punch through that proxy
- Also, in a Windows terminal, you may encounter issues when echoing unicode characters for debug purposes, so execute the following: `chcp 65001`

Now all scripts should reference the version of python in that venv, install all additional libs from that path

Sublime Text libraries will need to be installed in the plugin itself, which should only be done when development is complete.  Maybe we can trick sublime with links in the meantime?

I'll have to write a python package for vyte_in, it's too new to have one exist already.

I'll also need to figure out how to make Outlook and OneNote play nice with python as well.  Perhaps COM plugins?

One of the massive problems I'll need to work around is the issue of proxied internet at work.
Consider https://google-auth.readthedocs.io/en/latest/
Or alternatively: https://stackoverflow.com/questions/31639742/how-to-pass-all-pythons-traffics-through-a-http-proxy

Need to make todo.txt manipulation atomic, to avoid clearing it accidentally!

Also, need some way of making todo.txt list links clickable.

Okay, so, I have this neat link_map technique for shortening URLs in tasks...but none of my applications support it.  Bummer.  I suppose I could extend the QTodoTxt2 app, but that still leaves Android hosed.   Now, I could consider that anywhere I'm going to act on outlook or gmail, I'll have access to the desktop application, yes, links won't be present, but I could create a helper to look at the link_map file in android?  So, should ALL links be compressed, or only outlook/mail?  What about file or photo links?


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
- https://www.howto-outlook.com/howto/selfcert.htm