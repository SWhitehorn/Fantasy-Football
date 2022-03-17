import numpy as np

class Team():
    def __init__(self, flat_team=None):
        self.gk = []
        self.defs = []
        self.mids = []
        self.fors = []
        if flat_team is not None:
            self.create_team_from_list(flat_team)

    def add_goalie(self, player):
        self.gk.append(player)

    def add_defs(self, player):
        if player not in self.defs:
            self.defs.append(player)

    def add_mids(self, player):
        if player not in self.mids:
            self.mids.append(player)

    def add_fors(self, player):
        if player not in self.fors:
            self.fors.append(player)

    def under_limit(self):
        return self.get_total_cost() <= 83.8

    def get_total_cost(self):
        cost = 0
        cost += self.gk[0][2]
        for player in self.defs:
            cost += player[2]
        for player in self.mids:
            cost += player[2]
        for player in self.fors:
            cost += player[2]
        return cost
    
    def get_total_points(self):
        points = 0
        points += self.gk[0][1]
        for player in self.defs:
            points += player[1]
        for player in self.mids:
            points += player[1]
        for player in self.fors:
            points += player[1]
        return points if self.under_limit() else 0

    def flatten(self):
        """Returns a single list containing the team's players"""
        flattened_list = self.gk + self.defs + self.mids + self.fors
        return flattened_list

    def create_team_from_list(self, flat_team):
        """Takes a list of players and assigns them to correct positions"""
        self.gk.append(flat_team[0])
        self.defs.append(flat_team[1])
        self.defs.append(flat_team[2])
        self.defs.append(flat_team[3])
        self.defs.append(flat_team[4])
        self.mids.append(flat_team[5])
        self.mids.append(flat_team[6])
        self.mids.append(flat_team[7])
        self.mids.append(flat_team[8])
        self.fors.append(flat_team[9])
        self.fors.append(flat_team[10])

    def crossover(self, second_team):
        """ Flattens both teams into then chooses a point on which to split the list. New teams are generating by 
            taking a section from each team and joining the sections."""
        team_one = self.flatten()
        team_two = self.flatten()

        crossover_point = np.random.randint(11)

        child_one_list = team_one[:crossover_point] + team_two[crossover_point:]
        child_two_list = team_two[:crossover_point] + team_one[crossover_point:]

        child_one = Team(child_one_list)
        child_two = Team(child_two_list)

        return child_one, child_two
    
    def mutate(self, player):
        if player[3] == "GK" and player not in self.gk:
            self.gk[0] = player
            return True
        elif player[3] == "DEF" and player not in self.defs:
            self.defs[np.random.randint(4)] = player
            return True
        elif player[3] == "MID" and player not in self.mids:
            self.mids[np.random.randint(4)] = player
            return True
        elif player[3] == "FOR" and player not in self.fors:
            self.fors[np.random.randint(2)] = player
            return True
        return False