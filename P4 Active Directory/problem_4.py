# Udacity Data Structures and Algorithms
# Part 2 - Data Structures
# Project 2 - Problem #4 - Active Directory

class Group(object):
    def __init__(self, _name):
        self.name = _name
        self.groups = []
        self.users = []

    def add_group(self, group):
        self.groups.append(group)

    def add_user(self, user):
        self.users.append(user)

    def get_groups(self):
        return self.groups

    def get_users(self):
        return self.users

    def get_name(self):
        return self.name


def is_user_in_group(user, group):
    """
    Return True if user is in the group, False otherwise.

    Args:
      user(str): user name/id
      group(class:Group): group to check user membership against
    """
    # Edge cases - Invalid group name
    if group == "":
        return False

    # Traverses the list of users
    users = group.get_users()
    for current_user in users:
        if current_user == user:
            return True

    # Recursively traverses the list of groups 
    groups = group.get_groups()
    for current_group in groups:
        if is_user_in_group(user, current_group) is True:
            return True

    return False


print("\n# Test Case #1 - Problem statement groups and users")
parent = Group("parent")
child = Group("child")
sub_child = Group("subchild")
sub_child_user = "sub_child_user"
sub_child.add_user(sub_child_user)
child.add_group(sub_child)
parent.add_group(child)

print(is_user_in_group("sub_child_user", parent))
# Expected result: True
print(is_user_in_group("sub_child_user2", parent))
# Expected result: False


print("\n# Test Case #2 - Other group/users example")
my_company = Group("my_company")

egineering = Group("egineering")
sales = Group("sales")
management = Group("management")
procurement = Group("procurement")

my_company.add_group(egineering)
my_company.add_group(sales)
my_company.add_group(management)
my_company.add_group(procurement)

other_users = ["Roberto", "Carlos", "Alysson", "Michelle"]
for u in other_users : egineering.add_user(u)

more_users = ["Hernani", "Djalma", "Rayeck", "Eduardo"]
for u in more_users : sales.add_user(u)

more_users = ["Ana", "Rogerio", "Vivian", "Henrique"]
for u in more_users : management.add_user(u)

more_users = ["Fernanda", "Vivian", "Sandra", "Rafael"]
for u in more_users : procurement.add_user(u)

print(is_user_in_group("Vivian", my_company))
print(is_user_in_group("Vivian", egineering))
print(is_user_in_group("Vivian", sales))
print(is_user_in_group("Vivian", management))
print(is_user_in_group("Vivian", procurement))
# Expected result: True, False, False, True, True


print("\n# Test Case #3 - Groups and user that does not belong to the company")
operations = Group("operations")
another_user = "Ted"
print(is_user_in_group("Ted", operations))
print(is_user_in_group("Ted", my_company))
# Expected result: False, False


print("\n# Test Case #4 - Edge case - Invalid user name")
print(is_user_in_group("", my_company))
# Expected result: False


print("\n# Test Case #5 - Edge case - Invalid group name")
print(is_user_in_group("my_friend", ""))
# Expected result: False



