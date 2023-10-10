#!/usr/bin/env python3

import requests
from termcolor import colored

from tests import *

# Display name, function pointer, args
TESTS = [
    ("teams/create", teams.create, {"name": "Foobar", "password": "Example"}),
    ("teams/read", teams.read, {})
]

def main():

    print("==[ HTP!m Platform Test ]==")
    print("Remember to run this on an EMPTY database.\n")

    for i,t in enumerate(TESTS):

        if t[1](**t[2]):
            print(f"[{i}] {t[0]} " + colored("passed", "green", attrs=["bold"]))
        else:
            print(f"[{i}] {t[0]} " + colored("failed", "red", attrs=["bold"]))

if __name__ == "__main__":
    main()
