from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from ahlquist.cli import create_parser 
from ahlquist.api import *

def make_setting(hosts, playbookdir):
    """
    Build setting options with given parameters.
    """
    settings = {
                'hosts': hosts,
                'playbookdir': playbookdir
               }
    return settings

def configure(settings):
    """
    Create Configurator and define route configurations.
    """
    config = Configurator(settings=settings)

    config.add_route('play', '/playbooks/{playbooks}/play/{playbook}')
    config.add_view(playbooks.play, route_name='play', request_method='POST')

    config.add_route('install', '/playbooks/{playbooks}')
    config.add_view(playbooks.install, route_name='install', request_method='POST')

    config.add_route('update', '/playbooks/{playbooks}/update')
    config.add_view(playbooks.update, route_name='update', request_method='POST')

    return config

def main(args):
    parser = create_parser()
    options = parser.parse_args(args)
    settings = make_setting(options.inventory, options.playbooksdir)
    config = configure(settings)
    app = config.make_wsgi_app()
    server = make_server('0.0.0.0', int(options.port), app)
    server.serve_forever()  
