from pyramid.response import Response 
from ansible.playbook import PlayBook
from ansible.inventory import Inventory
import ansible.callbacks as callbacks
import ansible.utils as utils 
import json
from os import path
import subprocess

def _playbookdir(request):
    return request.registry.settings.playbookdir

def _inventory(request):
    return Inventory(request.registry.settings.hosts)


def install(request):
    """
    Install new playbooks using `git clone`.

    matchdict
    ---------
    playbooks
    """
    playbookdir = _playbookdir(request)
    playbooks = request.matchdict.get('playbooks')
    source = request.params.get('source')
    dest = path.join(playbookdir, playbooks)

    if path.isdir(dest):
        return Response(None, status=201)

    process = subprocess.Popen(
            ['git', 'clone', source, dest],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)

    (stdout, stderr) = process.communicate(None)
    return Response(stdout, status=201)


def update(request):
    """
    Update playbooks git repo using `git -C {dir} pull`.

    matchdict
    ---------
    playbooks
    """
    playbookdir = _playbookdir(request)
    playbooks = request.matchdict.get('playbooks')
    dest = path.join(playbookdir, playbooks)
    process = subprocess.Popen(
            ['git', '-C', dest, 'pull'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)

    (stdout, stderr) = process.communicate(None)
    return Response(stdout, status=200)



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
    playbookdir = _playbookdir(request)
    inventory = _inventory(request)

    # Instantiate other parameters which PlayBook requires.
    stats = callbacks.AggregateStats()
    playbook_cb = callbacks.PlaybookCallbacks(verbose=utils.VERBOSITY)
    runner_cb = callbacks.PlaybookRunnerCallbacks(
            stats,
            verbose=utils.VERBOSITY)

    repos = path.join(playbookdir, request.matchdict.get('playbooks'))
    yml = path.join(repos, request.matchdict.get('playbook'))

    results = PlayBook(
                playbook=yml,
                inventory=inventory,
                callbacks=playbook_cb,
                runner_callbacks=runner_cb,
                stats=stats,
                forks=10
                ).run()
    return Response(json.dumps(results))


