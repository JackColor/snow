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

user = "kkk"

password = 123

account_list = [("jack", 123), ("bob", 123), ()]

user_pwd = (user, password)

print(user_pwd in account_list)
