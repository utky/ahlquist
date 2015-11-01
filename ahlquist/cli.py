import argparse
from os import getenv

def create_parser():
    """
    Create command line arugment parser.
    options below has fallback value from environment variables.
      - inventory
      - port
      - playbookdir
    """
    parser = argparse.ArgumentParser(description='Start ahlquist server.')
    parser.add_argument(
            '-i',
            '--inventory',
            dest='inventory',
            default=getenv('AHLQUIST_INVENTORY'))
    parser.add_argument(
            '-p',
            '--port',
            dest='port',
            default=getenv('AHLQUIST_PORT'))
    parser.add_argument(
            '-d',
            '--playbookdir',
            dest='playbooks',
            default=getenv('AHLQUIST_PLAYBOOKS'))

    return parser
