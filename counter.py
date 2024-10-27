import pyrankvote
from pyrankvote import Candidate, Ballot
import pandas as pd
import numpy as np
from offices import OFFICES

def generate_candidates(df, candidates_to_drop):
    replacements = {}  # Conversions from 'string' objects from submitted ballot to 'Candidate' object for vote tallying
    candidates = []  # List of candidates up for election (stores 'Candidate' objects)
    names = df.dropna().iloc[0].values # Strip out row with all candidates to be generated
    names = [name for name in names if name not in candidates_to_drop] # Drop any candidates who should be dropped
    for name in names:  # For each candidate eligible for election
        replacements[name] = Candidate(name)  # Create 'Candidate' object for each candidate to use for string replacement
        candidates.append(Candidate(name))  # Add 'Candidate' object for each candidate to list of candidates
    return candidates, replacements, names

def drop_candidates(df, replacements, names):
    ballots = []  # Create list to store ballots for tallying
    for index, row in df.iterrows():  # Using current row
        row = [x for x in row if x in names]  # Drop any candidates that are to be dropped
        row = [replacements.get(item, item) for item in row]  # Generate ballot using 'Candidate' objects
        row = [name for name in row if isinstance(name, Candidate)]
        row = np.array([x for x in row if x is not None and x is not np.nan])
        ballots.append(Ballot(ranked_candidates=row))  # Add processed ballot to list of ballots
    return ballots
    
def vote_counter(candidates, ballots, position):
    try:
        num_seats = OFFICES[position]["num_seats"]
    except KeyError:
        # Raise an error if the position does not exist
        print(f"Position '{position}' does not exist.")
    election_result = pyrankvote.single_transferable_vote(
        candidates, ballots,
        number_of_seats=num_seats
    )  # Calculate results according to number of positions available
    print(election_result)  # Print round-by-round results of election


