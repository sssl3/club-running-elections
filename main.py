import argparse
import json
import sys
from counter import *
from vote_ingestion import *
from offices import OFFICES

valid_sheet_settings = ['public', 'private']

class Voting:
    def __init__(self):
        self.url = ""
        self.candidates_to_drop = []
        self.position = ""
        self.sheet_setting = ""
        self.keyfile = ""

    def vote(self):
        if self.sheet_setting == 'private':
            try:
                df = read_private_sheet(self.url, self.keyfile)
            except FileNotFoundError:
                print(f"Keyfile {self.keyfile} not found.")
                sys.exit(1)
        elif self.sheet_setting == 'public':
            df = read_public_sheet(self.url)
        else:
            return
        candidates, replacements, names = generate_candidates(df, self.candidates_to_drop)
        ballots = drop_candidates(df, replacements, names)
        vote_counter(candidates, ballots, self.position)

    def reading(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('--conf', '-c', action='append')
        args = parser.parse_args()

        if args.conf is not None:
            for conf_fname in args.conf:
                try:
                    with open(conf_fname, 'r') as f:
                        parser.set_defaults(**json.load(f))
                except FileNotFoundError:
                    print(f"Configuration file {conf_fname} not found.")
                    sys.exit(1)
                except json.JSONDecodeError:
                    print(f"Error decoding JSON from the configuration file {conf_fname}.")
                    sys.exit(1)
            args = parser.parse_args()
        else:
            print("Missing config file argument. Use --conf or -c with a JSON file.")
            sys.exit(1)

        if hasattr(args, 'url') and hasattr(args, 'position') and hasattr(args, 'sheet_setting'):
            if args.sheet_setting not in valid_sheet_settings :
                print("Invalid 'sheet_setting'. Choose from:", valid_sheet_settings)
                sys.exit(1)
            if args.position not in OFFICES :
                print("Invalid 'position'. Choose from:", list(OFFICES.keys()))
                sys.exit(1)
            self.url = args.url
            self.position = args.position
            self.sheet_setting = args.sheet_setting
            if self.sheet_setting == 'private':
                if args.keyfile != "":
                    self.keyfile = args.keyfile
                else:
                    print("""Missing keyfile path associated with service account. Please update the config file or select "public" option for "sheet_setting" parameter.""")
                    sys.exit(1)
            if hasattr(args, 'candidates_to_drop'):
                    self.candidates_to_drop = args.candidates_to_drop
            return self
        else:
            print("Missing at least one input argument.")
            sys.exit(1)

if __name__ == "__main__":
    voting = Voting()
    voting = voting.reading()
    voting.vote()
