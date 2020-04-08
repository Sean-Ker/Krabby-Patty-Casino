from grid_world import Grid
import matplotlib.pyplot as plt
from statistics import stdev, pstdev
import numpy as np
import random
import time
from tqdm import tqdm
import pickle

plt.style.use('ggplot')

x_grid = 4
y_grid = 4
LIVES = 1

# Only supports a 4 by 4 grid and 1 live!
SHOW_EVERY = 50
show_live = False

N = 50000
cost_per_game = 10
expected_revenue = N*cost_per_game

current_balance = 0  # Set the starting balance
games_log = []

rewards_table = {0: 0, 1: 0, 2: 10, 3: 20, 4: 30, 6: 100}
f, (ax1, ax2) = plt.subplots(2, 1, sharex=True)


def plot_graph(show_live):
    all_round_rewards, all_current_balances = list(zip(*games_log))
    x = range(len(games_log))
    # print(all_round_rewards,all_current_balances)
    # print(x)
    ax1.plot(x, all_current_balances)
    ax1.plot(x, [cost_per_game*r for r in range(len(games_log))])
    ax1.set_title('Sharing Y axis')
    ax2.bar(x, all_round_rewards)

    if show_live:
        plt.pause(0.05)
    else:
        plt.show()


def run_simulation():
    for i in tqdm(range(N)):
        grid = Grid(x_grid, y_grid, LIVES, True)
        while not grid.done:
            state = grid.current_state()  # The current position in the env
            action = random.choice(grid.actions[state])  # Choose a random valid action
            grid.move(*action)

        round_reward = cost_per_game-rewards_table[grid.score]
        global current_balance
        current_balance += round_reward

        # Append round profit and accumulated profit
        games_log.append([round_reward, current_balance])

        if show_live and not i % SHOW_EVERY:
            plot_graph(True)


t = time.time()
run_simulation()
print(f'\nTime to run {N} games: {round(time.time()-t,3)} sec')

all_round_rewards, all_current_balances = list(zip(*games_log))

expected_return = np.mean(all_round_rewards)
theoretical_expected_return = 2.06

print(f'\nStats')
print(f'Games Played: {N}')
print(f'Total Revenue: ${expected_revenue}')
print(f'Total Expenses: ${current_balance-expected_revenue}')

print(f'Total P&L: #{games_log[-1][1]}')
print(f'Average Return per Round: ${round(expected_return,2)}')

print(f'σ(SD): {stdev(all_round_rewards)}')
print(f'% Deviations From Theoretical Expected Return(${theoretical_expected_return}): {(abs(expected_return-theoretical_expected_return)*100/theoretical_expected_return)}%')

print('\nOccurrences')
for i in list(sorted(set(all_round_rewards))):
    c = all_round_rewards.count(i)
    print(f'${i}: {c} Occurrences, Prob({c/N}) ')

with open(f'data\\games_log_{N}_{int(time.time())}.pkl','wb') as f:
    pickle.dump(games_log,f)

plot_graph(False)
