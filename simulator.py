from grid_world import Grid
import matplotlib.pyplot as plt
from statistics import stdev, pstdev
import numpy as np
import random
import time
from tqdm import tqdm
import pickle

plt.style.use('ggplot')
import grid_world

# User constants. Not Adjustable.
# Only supports:
# 4 by 4 grid and 1 live gird OR 
# 5 by 5 grid and 2 lives gird!
X_GRID = 5
Y_GRID = 5
LIVES = 2

# Play with me!
SHOW_EVERY = 1           # Show every how many rounds?
show_live = True        # Should update the graph live?
N = 20                   # How many total rounds? 

# It takes approximatelly 30 seconds per 1000 itterations for a (4,4,1) and 
# approximatelly XXXXXX seconds per 1000 itterations for a (5,5,2)

current_balance = 0     # This is not the starting balance! Starting balance is always 0.
games_log = [] 

cost_per_game = 10                                              # The cost to play every game.
expected_revenue = N * cost_per_game

# Custom tables. See the report.
rewards_table_441 = {0: 0, 1: 0, 2: 10, 3: 20, 4: 30, 6: 100}   # The custom made rewards table for (4,4,1)
rewards_table_552 = {(2,8):150,(1,8):50,(0,6):30,(0,5):10}      # The custom made rewards table for (5,5,2)

# Theoretical returns
theoretical_expected_return_441 = 2.06
theoretical_expected_return_552 = 2.23

# Create subplots
fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)

# Function to plot the graphs
def plot_graph(show_live, games_log):
    all_round_rewards, all_current_balances = list(zip(*games_log))
    x = range(len(games_log))
    # print(all_round_rewards,all_current_balances)
    # print(x)
    ax1.plot(x, all_current_balances, label='Accumulated P&L')
    ax1.plot(x, [cost_per_game*(r+1) for r in range(len(games_log))], label = 'Revenue')
    ax2.bar(x, all_round_rewards, label='Profit and Loss')

    # Set titles and labels
    ax1.set_title('Revenue and Profit Over Time')
    ax2.set_xlabel('Time (rounds)')
    ax1.set_ylabel('Price ($)')
    ax2.set_ylabel('Price ($)')

    # Add legend
    handles, labels = ax1.get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    ax1.legend(by_label.values(), by_label.keys(), loc='upper left', fancybox=True,shadow=True)

    handles, labels = ax2.get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    ax2.legend(by_label.values(), by_label.keys(), loc='best', fancybox=True,shadow=True)

    # Show final or live graph
    if show_live:
        plt.pause(0.05)
    else:
        plt.show()

# A function that runs the main simulation
def run_simulation_441():
    for i in tqdm(range(N)):
        grid = Grid(X_GRID, Y_GRID, LIVES, True)
        while not grid.done:
            state = grid.current_state()  # The current position in the env
            action = random.choice(grid.actions[state])  # Choose a random valid action
            grid.move(*action)

        round_reward = cost_per_game-rewards_table_441[grid.score]
        global current_balance
        current_balance += round_reward

        # Append round profit and accumulated profit
        games_log.append([round_reward, current_balance])

        if show_live and not i % SHOW_EVERY:
            plot_graph(True, games_log)

def run_simulation_552():
    for i in tqdm(range(N)):
        grid = Grid(X_GRID, Y_GRID, LIVES, True)
        while not grid.done:
            state = grid.current_state()  # The current position in the env
            action = random.choice(grid.actions[state])  # Choose a random valid action
            grid.move(*action)

        round_reward = cost_per_game-rewards_table_552.get((grid.lives,grid.score),0)
        global current_balance
        current_balance += round_reward

        # Append round profit and accumulated profit
        games_log.append([round_reward, current_balance])

        if show_live and not i % SHOW_EVERY:
            plot_graph(True, games_log)

# Print all stats
def print_stats():
    # Theoretical return
    all_round_rewards, all_current_balances = list(zip(*games_log))
    expected_return = np.mean(all_round_rewards)

    print(f'\nStats')
    print(f'Games Played: {N}')
    print(f'Total Revenue: ${expected_revenue}')
    print(f'Total Expenses: ${current_balance-expected_revenue}')

    print(f'Total P&L: ${games_log[-1][1]}')
    print(f'Average Return per Round: ${round(expected_return,2)}')

    print(f'σ(SD): {round(stdev(all_round_rewards),2)}')
    if X_GRID == 4 and Y_GRID == 4 and LIVES==1:
        print(f'% Deviations From Theoretical Expected Return(${theoretical_expected_return_441}): {round(abs(expected_return-theoretical_expected_return_441)*100/theoretical_expected_return_441,2)}%')
    else:
        print(f'% Deviations From Theoretical Expected Return(${theoretical_expected_return_552}): {round(abs(expected_return-theoretical_expected_return_552)*100/theoretical_expected_return_552,2)}%')

    # print probabilites to compare with the math
    print('\nOccurrences')
    for i in list(sorted(set(all_round_rewards))):
        c = all_round_rewards.count(i)
        print(f'${i}: {c} Occurrences, Prob({c/N}) ')

    with open(f'data\\games_log_{N}_{int(time.time())}.pkl','wb') as f:
        pickle.dump(games_log,f)

# Mard beginning time for stats
t = time.time()
if X_GRID == 4 and Y_GRID == 4 and LIVES==1:
    run_simulation_441()
elif X_GRID == 5 and Y_GRID == 5 and LIVES==2:
    run_simulation_552()
else:
    print('Please run with (X_GRID,Y_GRID,LIVES) as (4,4,1) or (5,5,2)')
    exit()
print(f'\nTime to run {N} games: {round(time.time()-t,3)} sec')

# Plot final graph and stats!
print_stats()
plot_graph(False, games_log)