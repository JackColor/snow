from django.test import TestCase

# Create your tests here.


lis = [[12, 3, 4], [1, 2, 3]]

# lis2 = lis
#
# lis2[0].append(2)
#
# print(lis)
#
# for i in lis:
#     i.append(2)
#
# print(lis)

import copy

lis3 = []

lis3.append(copy.deepcopy(lis))

lis[0][0] = 10000

print(lis3)
