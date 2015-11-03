ahlquist
========

An extremely poor (rather then simple) Web API for Ansible.

Features
--------

### 1. Installing playbook

You can install playbooks which is hosted in Git repo into `PLAYBOOKSDIR`.

    curl -X POST http://localhost:8080/playbooks/my-books?source=https://github.com/utky/docker-playbooks.git

- `my-books` is a name of playbooks.(directory name in `PLAYBOOKSDIR`)
- `source` is a query string parameter to be specified as git repo.

*This API uses `git` executable.*

### 2. Update playbook

You can also update playbooks (*using `git pull`*).

    curl -X POST http://localhost:8080/playbooks/my-books/update

- `my-books` is a name of playbooks.(directory name in `PLAYBOOKSDIR`)

### 3. Run playbook

Finally you can run playbook.

    curl -X POST http://localhost:8080/playbooks/my-books/play/docker-engine.yml

- `my-books` is a name of playbooks.(directory name in `PLAYBOOKSDIR`)
- `docker-engine.yml` is a YAML file name in the playbooks directory.

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
