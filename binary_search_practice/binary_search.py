count = -1


def get_count():
    global count
    count += 1
    return count


array = [
    (get_count(), "muelsyse"),
    (get_count(), "eyjafjalla"),
    (get_count(), "schwarz"),
    (get_count(), "bagpipe"),
    (get_count(), "ptilopsis"),
    (get_count(), "irene"),
    (get_count(), "ling"),
    (get_count(), "suzuran"),
    (get_count(), "typhon"),
    (get_count(), "texas"),
    (get_count(), "exusiai"),
]


"""
step 1

- get middle index
- get middle item
"""


def get_middle_index(lower_bound: int, upper_bound: int):
    middle = (lower_bound + upper_bound) // 2

    print("middle:", middle)
    return middle


def binary_search(value: int, arr: list[tuple[int, str]]):
    middle = get_middle_index(0, len(arr))

    middle_value = arr[middle]

    if middle_value[0] == value:
        return middle_value

    else:
        if value < middle:
            print("recurse")
            return binary_search(value, arr[:middle])

        elif value > middle:
            print("recurse")
            return binary_search(value, arr[middle:])


def binary_search_imperative(value: int, arr: list[tuple[int, str]]):
    lower_bound = 0

    upper_bound = len(arr)
    middle = get_middle_index(lower_bound, upper_bound)
    middle_value = arr[middle]

    while len(arr) != 0:
        print(arr)
        if middle_value[0] == value:
            return middle_value

        else:
            if value < middle:
                arr = arr[:middle]

            elif value > middle:
                arr = arr[middle:]

            upper_bound = len(arr)
            middle = get_middle_index(lower_bound, upper_bound)
            middle_value = arr[middle]


# print(binary_search(0, array))
print(binary_search_imperative(10, array))
