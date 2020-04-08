# from game_combinatorics import get_random_path
# dic = {(0, 0): ('U', 'R'),
#        (0, 1): ('L', 'U'),
#        (0, 2): ('D', 'L')}

# dic.update({(0,0):'L',(1,1):'L'})
# dic.update({(1,0): dic.get((1,0),()) + tuple('L')})
# print(list(zip(*dic.values())))

# for i in range(10):
#     if dic.get((1, 0)) is None:
#         dic[(1, 0)] = tuple('R')
#     else:
#         dic[(1, 0)] += tuple('L')
# print(dic)
# # print(dic)

# import numpy as np
# import matplotlib.pyplot as plt

# # print(get_random_path(4,4))
# x = np.linspace(0, 2*np.pi, 400)
# y = np.sin(x**2)

# # Create just a figure and only one subplot
# fig, ax = plt.subplots()
# ax.plot(x, y)
# ax.set_title('Simple plot')

# # Create two subplots and unpack the output array immediately
# f, (ax1, ax2) = plt.subplots(1, 2, sharey=True)
# ax1.plot(x, y)
# ax1.set_title('Sharing Y axis')
# ax2.scatter(x, y)

# # Create four polar axes and access them through the returned array
# fig, axs = plt.subplots(2, 2, subplot_kw=dict(polar=True))
# axs[0, 0].plot(x, y)
# axs[1, 1].scatter(x, y)

# # Share a X axis with each column of subplots
# plt.subplots(2, 2, sharex='col')

# # Share a Y axis with each row of subplots
# plt.subplots(2, 2, sharey='row')

# # Share both X and Y axes with all subplots
# plt.subplots(2, 2, sharex='all', sharey='all')

# # Note that this is the same as
# plt.subplots(2, 2, sharex=True, sharey=True)

# # Create figure number 10 with a single subplot
# # and clears it if it already exists.
# fig, ax = plt.subplots(num=10, clear=True)
# plt.show()

# v = 5
# class Test:
#     def __init__(self,v):
#         self.v = v

#     def __str__(self):
#         return f'V: {self.v}'

# my_test = Test(v)
# print(my_test)
# v+=2
# print(my_test)

# from PIL import Image

# im = Image.open('assets/spongebob.png')
# print(im)
# im.show()
cost_per_game =10
i =5
yes = [cost_per_game*r for r in range(1, i+1)]
print(yes)
