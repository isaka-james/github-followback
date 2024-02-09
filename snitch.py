# Open the file
with open('followers.txt', 'r') as file:
    # Initialize an empty array to store names
    followers_names = []
    # Loop through each line in the file
    for line in file:
        # Check if the line starts with '@'
        if line.startswith('@'):
            # Strip any leading or trailing whitespace and append to the names array
            followers_names.append(line.strip())
            



with open('following.txt', 'r') as file:
    # Initialize an empty array to store names
    following_names = []
    # Loop through each line in the file
    for line in file:
        # Check if the line starts with '@'
        if line.startswith('@'):
            # Strip any leading or trailing whitespace and append to the names >
            following_names.append(line.strip())



# Define your two arrays of strings
array1 = list(dict.fromkeys(followers_names))
array2 = list(dict.fromkeys(following_names))

print(f"the number of followers : {len(array1)}")
print(f"the number of following : {len(array2)}")


exclusive_to_array = [string for string in array2 if string not in array1]

# Combine the exclusive strings into a new array
snitch_names = exclusive_to_array

# Print the new array
print(f"the number of snitches: {len(snitch_names)}")
#print(f"The names of followers: {array1}")
#print(f"The names of followinf: {array2}")
#print*f"The names of snitches" {snitch_names}")


for i in snitch_names:
	print(i)
