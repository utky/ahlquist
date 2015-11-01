from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from ahlquist.cli import create_parser 
from ahlquist.play import play

    

def make_setting(hosts, playbook):
    """
    Build setting options with given parameters.
    """
    settings = {
                'hosts': hosts,
                'playbook': playbook
               }
    return settings

def configure(settings):
    """
    Create Configurator and define route configurations.
    """
    config = Configurator(settings=settings)
    config.add_route('play', '/play/{playbook}')
    config.add_view(play, route_name='play')
    return config

def main(args):
    parser = create_parser()
    options = parser.parse_args(args)
    settings = make_setting(options.inventory, options.playbooks)
    config = configure(settings)
    app = config.make_wsgi_app()
    server = make_server('0.0.0.0', 8080, app)
    server.serve_forever()  
