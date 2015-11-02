ahlquist
========

An extremely simple Web API for Ansible.

Features
--------

### 1. Installing playbook

You can install playbooks which is hosted in Git repo.

    curl -X POST http://localhost:8080/playbooks/my-books?source=https://github.com/utky/docker-playbooks

*This API uses `git`*

### 2. Update playbook

You can also update playbooks (*using `git pull`*).

    curl -X POST http://localhost:8080/playbooks/my-books/update

### 3. Run playbook

Finally you can run playbook.

    curl -X POST http://localhost:8080/playbooks/my-books/play/docker-engine.yml


Starting ahlquist
-----------------

`main` script in this repository is a bootstrap to start server.

```
usage: main [-h] [-i INVENTORY] [-p PORT] [-d PLAYBOOKSDIR]

Start ahlquist server.

optional arguments:
  -h, --help            show this help message and exit
  -i INVENTORY, --inventory INVENTORY
  -p PORT, --port PORT
  -d PLAYBOOKSDIR, --playbookdir PLAYBOOKSDIR
```

- `INVENTORY` is an inventory file for ansible.
- `PORT` is port number to bound.
- `PLAYBOOKSDIR` is a workspace directory which stores playbook repos.
