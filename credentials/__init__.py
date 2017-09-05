#!/usr/bin/env python
import os

def read_credentials(service=None):
    basedir = os.path.abspath(os.path.dirname(__file__))
    credentials = {service:{}}
    with open(os.path.join(basedir,'.'.join([service,'cred']))) as fh:
        for line in fh.read().strip().split('\n'):
            if line:
                protocol, key, value = line.split()
                credentials[protocol][key] = value
    return credentials
