import csv
import random
import numpy as np
from team import Team

class GA():
    def __init__(self):

        # Parameters
        self.population = 3000
        self.mutation_rate = 0.05

        self.GK = []
        self.FOR = []
        self.MID = []
        self.DEF = []
        self.get_data()
        self.total_players = self.GK + self.FOR + self.MID + self.DEF
        self.player_count = len(self.total_players)
    
    def get_data(self):
        """Load in data to class attributes in form [playerName, points, cost, position].
           Different positions are stored in seperate lists. """
        with open("data.csv") as data:
            csv_reader = csv.reader(data)

            # Skip header
            next(csv_reader)
            for line in csv_reader:
                player, points, cost, pos = line[0], int(line[2]), float(line[3]), line[4]
                if line[4] == "GK":
                    self.GK.append([player, points, cost, pos])
                elif line[4] == "FOR":
                    self.FOR.append([player, points, cost, pos])
                elif line[4] == "MID":
                    self.MID.append([player, points, cost, pos])
                elif line[4] == "DEF":
                    self.DEF.append([player, points, cost, pos])
        
    def pick_random_teams(self):
        """ Create initial population of teams by choosing random players"""
        self.teams = set()
        while len(self.teams) <= self.population:
            new_team = self.random_team()

            # Prevent duplications and ensure all teams are valid
            if new_team not in self.teams and new_team.under_limit():
                self.teams.add(new_team)

        self.teams = list(self.teams)

    def random_team(self):
        team = Team()
        team.add_goalie(self.GK[np.random.randint(len(self.GK))])
        while len(team.defs) < 4:
            team.add_defs(self.DEF[np.random.randint(len(self.DEF))])
        while len(team.mids) < 4:
            team.add_mids(self.MID[np.random.randint(len(self.MID))])
        while len(team.fors) < 2:
            team.add_fors(self.FOR[np.random.randint(len(self.FOR))])
        return team
    
    def filter_teams(self):
        # Filter out bottom half of teams
        cut_off = len(self.teams) // 2
        self.teams = self.teams[:cut_off]

    def rank_teams(self):
        # Teams are sorted by their total points; any team with cost over salary get is assigned 0 points
        self.teams.sort(reverse=True, key= lambda x: x.get_total_points())


    def repopulate(self):
        """ Repopulate teams by choosing two random parents from current generation and crossing their player list."""
        total_teams = len(self.teams)
        for i in range(total_teams//2):
            parent_one = self.teams[np.random.randint(total_teams)]
            parent_two = self.teams[np.random.randint(total_teams)]
            child_one, child_two = parent_one.crossover(parent_two)
            
            # Each child has a chance to mutate to swap a player at random 
            self.mutate(child_one)
            self.mutate(child_two)
            
            self.teams.append(child_one)
            self.teams.append(child_two)

    def mutate(self, team):
        if np.random.uniform() < self.mutation_rate:
            # Loop until player is chosen who is not in original team and swap is successful.
            while True:
                new_player = self.total_players[np.random.randint(self.player_count)]
                if team.mutate(new_player):
                    break


            

