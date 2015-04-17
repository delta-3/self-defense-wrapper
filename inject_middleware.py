#!/usr/bin/env python


import os
import shutil
import re

dir = "/home/wil/delta3/src/mysite" #/app
SETTINGS = "settings.py"
SUFFIX = ".original"
REGEX_MIDDLEWARE = "([\w\W]*MIDDLEWARE_CLASSES\s*=\s*\()([\w\W]*)"
RELATIVE_CLASSPATH = "middlewares.Repair"


def get_middleware_path(filepath):
    parent = os.path.split(os.path.dirname(filepath))[1]
    return "\n    '" + parent + "." + RELATIVE_CLASSPATH + "',"

def output(filepath, new_content):
    f2 = open(filepath, 'w')
    f2.write(new_content)
    f2.close()

def inject(filepath):
    backup = filepath + SUFFIX
    if not os.path.exists(backup):
        # First back up original
        shutil.move(filepath, backup)
        f = open (filepath, 'r')
        s = f.read()
        f.close()
        content = re.match(REGEX_MIDDLEWARE, s)
        new_content = content.group(1) + get_middleware_path(filepath) + content.group(2)
       
        output(filepath, new_content)

    else:
        print "Looks like its already injected, aborting"


for root, dirs, files in os.walk(dir):
    for file in files:
        if file == SETTINGS:
            fullpath = os.path.join(root, file)
            inject(fullpath)
            break
