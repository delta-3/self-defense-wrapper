#!/usr/bin/env python

import sys
import os
import shutil
import re

#dir = "/home/wil/delta3/src/mysite" #/app
SETTINGS = "settings.py"
SUFFIX = ".original"
REGEX_APPS = "([\w\W]*INSTALLED_APPS\s*=\s*\([\s\'\"a-zA-Z.,0-9_#]*)([\w\W]*)"
REGEX_MIDDLEWARE = "([\w\W]*MIDDLEWARE_CLASSES\s*=\s*\([\s\'\"a-zA-Z.,0-9_#]*)([\w\W]*)"
RELATIVE_CLASSPATH = "middlewares.Repair"
APP_NAME = 'secure_app'


def get_middleware_string(filepath):
    parent = os.path.split(os.path.dirname(filepath))[1]
    return "\n    '" + parent + "." + RELATIVE_CLASSPATH + "',"

def get_app_string():
    return "\n\t" + APP_NAME + "',"

def output(filepath, new_content):
    f2 = open(filepath, 'w')
    f2.write(new_content)
    f2.close()

def inject(filepath):
    backup = filepath + SUFFIX
    if not os.path.exists(backup):
        # First back up original
        shutil.move(filepath, backup)
        f = open (backup, 'r')
        s = f.read()
        f.close()

        #Add middleware
        m_middle = re.match(REGEX_MIDDLEWARE, s)
        injected_middle = m_middle.group(1) + get_middleware_string(filepath) + m_middle.group(2)
       
        #Add the app
        m_app = re.match(REGEX_APPS, injected_middle)
        injected_app = m_app.group(1) + get_app_string() + m_app.group(2)


        output(filepath, injected_app)

    else:
        print "Looks like its already injected, aborting"

if __name__ == "__main__":
    dir = sys.argv[1]

    for root, dirs, files in os.walk(dir):
        for file in files:
            if file == SETTINGS:
                fullpath = os.path.join(root, file)
                inject(fullpath)
                break

