# Udacity Data Structures and Algorithms
# Part 2 - Data Structures
# Project 2 - Problem #2 - File Recursion

import os

def find_files(suffix, path):
    """
    Find all files beneath path with file name suffix.

    Note that a path may contain further subdirectories
    and those subdirectories may also contain further subdirectories.

    There are no limit to the depth of the subdirectories can be.

    Args:
      suffix(str): suffix if the file name to be found
      path(str): path of the file system

    Returns:
       a list of paths
    """
    
    if not os.path.exists(path): # Checks path string
      print("Invalid path.")
      return []
    
    suffix = suffix.strip(".") # Strips out the dot from suffix param
    
    # Initialize a structure to accumulate .c files that are found
    found_dirs = set() 
    # creates a list of entries in current path directory
    current_list = os.listdir(path)

    for entry in current_list:

      # formats a pathname including current directory and entry
      pathname = "{}\\{}".format(path, entry)

      # If the entry is a directory, it calls find_files() recursively
      if os.path.isdir(pathname):
        found_dirs = found_dirs.union(find_files(suffix, pathname))
      
      # If the entry is a file and it has the given suffix, accumulate result
      if os.path.isfile(pathname):
        file_name, file_suffix = entry.rsplit(".", 1)
        if file_suffix == suffix:
          found_dirs.add(pathname)
   
    return found_dirs

# Helper function to print the test results
def print_result(result, description):
  print("\n\n")
  print(description)
  for item in result:
    print(item)


description = "# Test Case 1: Testing the problem giving example"
result = find_files(".c", ".\\2_Project\\P2 File Recursion\\testdir")
print_result(result, description)

description = "# Test Case 2: Other example"
result = find_files(".c", ".\\2_Project\\P2 File Recursion\\testdir2")
print_result(result, description)

description = "# Test Case 2:Very deep file extrucute"
result = find_files(".c", ".\\2_Project\\P2 File Recursion\\testdir3")
print_result(result, description)

description = "# Test Case 4: Empty directory"
result = find_files(".c", ".\\2_Project\\P2 File Recursion\\testdir4")
print_result(result, description)
print("Nothing expected.")
print("\n\n")

print("# Test Case 5: Invalid path string. Directory does not exist.")
result = find_files(".c", ".\\2_Project\\P2 File Recursion\\testdir5")
print("Error message expected.")
print("\n\n")
