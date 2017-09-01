# flow
Stitching together all the tools that organize my life to maximize personal capacity and free my mind.

## setup
- Have Python 3.3.* as default version on OS (`python`)
- At base of repository run: 
    + `python -m venv venv`
    + Activate your venv: `. ./venv/bin/activate`
    + `pip install --upgrade pip`
- Use the following shebang: `#!/usr/bin/env python`
- Before running any script, activate your venv: `./venv/bin/activate`
- Before releasing, use pip freeze > requirements.txt
    + remove `pkg-resources` line from requirements.txt
- To run tests: `python -m unittest discover`
- To run tests with coverage: `coverage run -m unittest discover`
- To generate coverage report: `coverage html`
- View report by opening: `./htmlcov/index.html`

Now all scripts should reference the version of python in that venv, install all additional libs from that path

Sublime Text libraries will need to be installed in the plugin itself, which should only be done when development is complete.  Maybe we can trick sublime with links in the meantime?

## attribution
https://github.com/todotxt/todotxt

## useful
https://github.com/dertuxmalwieder/SublimeTodoTxt
https://github.com/QTodoTxt/QTodoTxt2

