#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
import os
import sys
__author__ = 'Wan Pei Chih'
__version__ = '0.1'
__release__ = '9.2r'

from datetime import datetime
ndt = datetime.now()

__startdt__ = ndt.strftime("%a, %d %b, %Y at %X")

__pyVer__ = sys.version.split(' ')[0].split('.')[:-1]


class foo:
    def __init__(self, project):
        self.project = project
        self.samplefiles = {
            "__init__.py": """from flask import Flask
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

from apps import routes
""",

            "routes.py": """from flask import render_template, request, url_for
from apps import app
from datetime import datetime
import re

@app.route('/')
@app.route('/index/', methods=['GET','POST'])
def index():
    user = {{'username': 'Douglas'}}
    return render_template('index.html',
        title="Index",
        project="{project}",
        user=user
        )

@app.route('/sample/<name>', methods=['GET','POST'])
def sample(name):
    regex = re.compile("[a-zA-Z]")
    data = {{
        'name': name,
        'ndt': datetime.now().strftime('%a, %d %b, %Y at %X')
    }}

    return render_template('sample.html', 
        title="Sample",
        project="{project}",
        data=data)
""",

            'default.css': """div {
    font-size: 24pt;
    color: #253745;
}
a {
    font-size: 16pt,
}
""",

            'base.html': """<!DOCTYPE html>
<head>
    <meta charset="UTF-8">
    <link rel='stylesheet' href="{{ url_for('static', filename='default.css') }}">
    {% if title %}
    <title>{{ title }} - {{ project }}</title>
    {% else %}
    <title> {{ project }} of -X- </title>
    {% endif %}
</head>
<body>
    <div><b> {{ project }} </b> : <a href="{{ url_for('index') }}">Index</a> | 
        <a href="{{ url_for('sample', name='Visitor') }}">Sample</a></div>
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
    <h1>Hi, my friend. {{ user.username }}</h1>
    <div> This is a test page. </div>
{% endblock %}
""",

            'sample.html': """{% extends "base.html" %}
{% block content %}
    <div>Welcome in my sample page, <b>{{ data.name }}</b>.</div><h3> Current time is [ {{ data.ndt }} ]</h3>
{% endblock %}
""",

            'config.py': """import os
class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or os.urandom(32)
""",

            'run.py': """from apps import app
app.run(host='127.0.0.1', port=10080, debug=True)
"""}

        self.makeprj = {"apps": {
            'attr': 'dir',
            'sub': {
                'templates': {
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

    def CreateProject(self, data, dirs):
        if 'olddir' not in locals():
            olddir = dirs

        if __pyVer__[0] == '2':
            ITEM = data.iteritems()
        elif __pyVer__[0] == '3':
            ITEM = data.items()

        for k, v in ITEM:
            if v['attr'] == 'file':
                print('Get a FILE: "%s" in "%s"' % (k, olddir))
                if k in self.samplefiles.keys():
                    #    if k=='routes.py':
                    #        print (self.samplefiles[k].format(project=self.project))
                    try:
                        with open('%s/%s' % (olddir, k), 'w+') as fp:
                            fp.write(self.samplefiles[k].format(
                                project=self.project) if k == 'routes.py' else self.samplefiles[k])
                    except Exception as e:
                        print('Create a file: %s in %s failure!' % (k, olddir))
                        sys.stdout.errors(e)
                        return False

                continue

            if v['attr'] == 'dir':
                olddir = dirs
                newdirs = olddir + '/' + k
                if os.path.isdir(newdirs) is False:
                    print('Will be create a Directory: %s' % (newdirs))
                    try:
                        os.makedirs(newdirs)
                    except Exception as e:
                        print('make a directory: %s is fail!' % (newdirs))
                        sys.stdout.errors(e)
                        return False

                items = self.CreateProject(v['sub'], newdirs)
                if items is not None:
                    return items


def OptionParser(args):
    from optparse import OptionParser
    optpsr = OptionParser(usage="Usage: %prog [options] arg1",
                          version="%s.%s" % (__version__, __release__),
                          description="Create a project for the Flask.")
    optpsr.add_option("-p", "--project", action="store",
                      type="string", metavar="name",
                      help="Create a project")

    (options, args) = optpsr.parse_args(args)
    return options


if __name__ == '__main__':
    optpsr = OptionParser(sys.argv[1:])

    if optpsr.project is not None:
        ox = foo(optpsr.project)

        if os.path.isdir(optpsr.project) is False:
            os.makedirs(optpsr.project)

        print('current-path: %s' % (os.getcwd()))
        res = ox.CreateProject(ox.makeprj, optpsr.project)
        print(res)

    print("Today is %s." % (__startdt__))
