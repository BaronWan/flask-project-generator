# -*- coding: utf-8 -*-
__author__ = 'Pei-Zhi, Wan'
__version__ = '0.1'
__release__ = '1b'

from datetime import datetime
ndt = datetime.now()

__startdt__ = ndt.strftime("%a, %b %B, %Y at %X")

import sys,os,re

samplefiles = {
    "__init__.py": """from flask import Flask
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

from apps import routes
""",

    "routes.py": """from flask import render_template, request, url_for
from apps import app
form datetime import datetime

@app.route('/')
@app.route('/index/', method=['GET','POST'])
def index():
    user = {'username': 'Douglas'}
    return render_template('index.html',
        title="Index",
        user=user
        )

@app.route('/sample/<name>', method=['GET'])
def sample():

    regex = re.compile("[a-zA-Z]")
    data = {
        'name': name if regex.match(name) is not None else "visitor",
        'ndt': datetime.now().strftime("%a, %b %B, %Y at %X")
        }

    return render_template('sample.html', 
        title="Sample",
        data=data)
""",

    'default.css': "",

    'base.html': """<!DOCTYPE html>
<head>
    <meta charset="UTF-8">
    {% if title %}
    <title>{{ title }} - {project}</title>
    {% else %}
    <title> {project} of -X- </title>
    {% endif %}
</head>
<body>
    <div> {project}: <a href="{{ url_for('index') }}">Index</a>| 
        <a href="{{ url_for('sample') }}">Sample</a></div>
    <hr/>
    {% with messages = get_flashed_messages() %}
    {% if messages %}
    <ul>
    {% for msg in messages %}<li>{{ msg }}</li>{% endfor %}
    </ul>
    {% endif %}{% endwith %}
    {% block content %}{% endblock %}
</body>
</html>
""",

    'index.html': """{% extends "base.html" %}
{% block content %}
    <h3>Hi, my friend. {{ user.username }}</h3>
    <div> This is a test page. </div>
{% endblock %}
""",

    'sample.html': """{% extends "base.html" %}
{% block content %}
    <h3>Welcome in my sample page, {{ data.name }}. now is {{ data.ndt }}</h3>
{% endblock %}
""",

    'config.py': """import os
class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or os.urandom(32)
""",

    'run.py': """from apps import app
app.run(host='127.0.0.1', port=10080, debug=True)
"""}

makeprj = {"apps": {
            'attr': 'dir',
            'sub': {
                'template': {
                    'attr': 'dir',
                    'sub': {
                        'base.html': {'attr': 'file'},
                        'index.html': {'attr': 'file'},
                        'sample.html': {'attr': 'file'},
                    }
                },
                'static': {
                    'attr': 'dir',
                    'sub': {
                        'default.css': {'attr': 'file'}
                    }
                },
                '__init__.py': {'attr': 'file'},
                'routes.py': {'attr': 'file'}
            }
        },
        'config.py': {'attr': 'file'},
        'run.py': {'attr': 'file'},
    }


def CreateProject(data, dirs):
#    print ('layer=%d\r\n%s' %(layer,data))
    if 'olddir' not in locals():
        olddir = dirs

    for k,v in data.iteritems():
        if v['attr'] == 'file':
            print ('Get a FILE: "%s" in "%s"' %(k, olddir))
            if k in samplefiles.keys():
                try:
                    with open('%s/%s' %(olddir,k), 'w+') as fp:
                        fp.write(samplefiles[k])
                except Exception as e:
                    print ('Create a file: %s in %s failure!' %(k,olddir))
                    sys.stdout.errors(e)
                    return False
            
            continue

        if v['attr'] == 'dir':
            olddir = dirs
            newdirs = olddir +'/'+ k
            if os.path.isdir(newdirs) is False:
                print ('Will be create a Directory: %s' %(newdirs))
                try:                    
                    os.makedirs(newdirs)
                except Exception as e:
                    print ('make a directory: %s is fail!' %(newdirs))
                    sys.stdout.errors(e)
                    return False
            
            items = CreateProject(v['sub'], newdirs)
            if items is not None:
                return items

    
def OptionParser(args):
    from optparse import OptionParser
    optpsr = OptionParser(usage="Usage: %prog [options] arg1", 
                version="%s.%s" %(__version__, __release__), 
                description="Create a project for the Flask.")
    optpsr.add_option("-p","--project", action="store", 
        type="string", metavar="name", 
        help="Create a project")
    
    (options, args) = optpsr.parse_args(args)
    return options


if __name__ == '__main__':
    optpsr = OptionParser(sys.argv[1:])
  
    if optpsr.project is not None:
        print (optpsr.project)
        if os.path.isdir(optpsr.project):
        #    sys.exit(0)
        # else:
            if os.path.isdir(optpsr.project) is False:
                os.makedirs(optpsr.project)
        
            olddir = os.getcwd()
            try: 
               # os.chdir(optpsr.project)
                dirs = optpsr.project
            except Exception as e:
                sys.stdout.errors(e)
                sys.exit(-1)

            print ('current-path: %s' %(os.getcwd()))
            res = CreateProject(makeprj,dirs)
            print (res)

          #  os.chdir(olddir)
    print ("Today is %s." %(__startdt__))
