import argparse
import getpass
import os
import sys

from . import __version__
from .keychain import Keychain, UnlockException


DEFAULT_KEYCHAIN_PATH = "~/Dropbox/1Password.agilekeychain"
KEYCHAIN_ENV_VAR = "ONEPASSWORD_KEYCHAIN"


def open_keychain(keychain_path, stdin=False):
    keychain = Keychain(keychain_path)

    if stdin:
        password = sys.stdin.buffer.read().strip()
        password = bytes(password)
        keychain.unlock(password)
    else:
        while keychain.locked():
            try:
                password = getpass.getpass("Password: ")
                password = bytes(password.encode())
                keychain.unlock(password)
            except UnlockException as ue:
                print(ue)
            except KeyboardInterrupt:
                sys.exit(0)
    
    return keychain


def init_arg_parser():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.set_defaults(func=lambda x: parser.print_usage())

    parser.add_argument("item", help="The name of the password to decrypt")

    parser.add_argument('--version', action='version', version=__version__)

    parser.add_argument(
        "--path",
        default=os.environ.get(KEYCHAIN_ENV_VAR, DEFAULT_KEYCHAIN_PATH),
        help="Path to 1Password.agilekeychain file",
    )

    parser.add_argument(
        "--fuzzy",
        action="store_true",
        help="enable fuzzy matching",
    )

    parser.add_argument(
        "--stdin",
        action="store_true",
        help="read from STDIN",
    )

    return parser


def run_it():
    arg_parser = init_arg_parser()
    args = arg_parser.parse_args()

    if args.fuzzy:
        fuzzy_threshold = 70
    else:
        fuzzy_threshold = 100

    keychain = open_keychain(args.path, stdin=args.stdin)
    matches = keychain.find_matches(args.item, fuzzy_threshold)

    if matches:
        if matches[0][1] == 100:
            exact_name = matches[0][0]
            item = keychain._items[exact_name]
            item.decrypt_with(keychain)
            print(item.password)
        else:
            print("Possible matches:")
            for match in matches:
                print('-', match[0])
    else:
        err_msg = "Unmatched identifier: %s" % args.item
        sys.stderr.write(err_msg)
        sys.exit(os.EX_DATAERR)
