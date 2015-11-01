from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response 
from ansible.runner import Runner
from ansible.playbook import PlayBook
from ansible.inventory import Inventory
import ansible.utils as utils 
import ansible.callbacks as callbacks
from os import path
import json
import functools

def play(request):
    """
    This function executes ansible-playbook with specified playbook file.
    A path parameter `playbook` is required.
    `playbook` is exepected file path to existing playbook yaml file.
    
    This `play` function tries to find `playbook` file in directory that is paramer passed as `playbook` in settins.

    The Inventory file is also expected passed by `setttings`.

    Ansible PlayBook seems to require parameters below.
      - callbacks
      - runner_callbacks
      - stats

    """
    # Build parameters from settings.
    playbookhome = request.registry.settings.playbook 
    inventory = Inventory(request.registry.settings.hosts)

    # Instantiate other parameters which PlayBook requires.
    stats = callbacks.AggregateStats()
    playbook_cb = callbacks.PlaybookCallbacks(verbose=utils.VERBOSITY)
    runner_cb = callbacks.PlaybookRunnerCallbacks(
            stats,
            verbose=utils.VERBOSITY)

    results = PlayBook(
                playbook=path.join(playbookhome, request.matchdict.get('playbook')),
                inventory=inventory,
                callbacks=playbook_cb,
                runner_callbacks=runner_cb,
                stats=stats,
                forks=10
                ).run()
    return Response(json.dumps(results))

def main(args):
    if len(args) < 3:
        print 'Usage: hosts playbook'
        return 1
    (hosts, playbook) = args[1:]
    settings = {
                'hosts': hosts,
                'playbook': playbook
               }
    config = Configurator(settings=settings)
    config.add_route('play', '/play/{playbook}')
    config.add_view(play, route_name='play')
    app = config.make_wsgi_app()
    server = make_server('0.0.0.0', 8080, app)
    server.serve_forever()  
