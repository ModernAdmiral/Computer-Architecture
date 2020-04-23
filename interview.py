# in dict loop through keys and check if value is int
# count = 0
# if is integer add value to count

# return count

thing = {
    "cat": "bob",
    "dog": 23,
    19: 18,
    90: "fish"
}


def question(arg):
    count = 0
    for key, value in arg.items():
        # print(thing[key])
        if type(value) == int:
            count += value

    return count


print(question(thing))
