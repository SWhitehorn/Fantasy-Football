from team import Team
from genetic_alg import GA
import time
import csv 

start = time.perf_counter()
best_team = None
best_points = 0

# Change to adjust how many outputs are sampled.
samples = 20 
ga = GA()

for i in range(samples):
    # Initialise counters
    counter = 0
    best = 0
    generations = 0

    ga.pick_random_teams()

    # Continue until the best team is the same for twenty generations in a row
    while counter < 20:
        
        # Evaluate fitness of teams based on their points
        ga.rank_teams()
        curr_best = ga.teams[0].get_total_points()
        if curr_best == best:
            counter += 1
        else:
            counter = 0
            best = curr_best
        
        # Filter out weakest teams
        ga.filter_teams()
        
        # Use surviving teams to create next generation
        ga.repopulate()
        generations += 1

    ga.rank_teams()
    curr_best = ga.teams[0]
    curr_points = curr_best.get_total_points() 
    if curr_points > best_points:
        best_team = curr_best
        best_points = curr_points


print(best_points)
for player in best_team.flatten():
    print(player)

# Write team to csv file
with open('team.csv', 'w', newline='') as output:
    csv_writer = csv.writer(output, delimiter=',')
    csv_writer.writerows(best_team.flatten())