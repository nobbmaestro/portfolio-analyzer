def find(data, target, low, high, force=True):
    """Searches for the index of the target in the data by using binary search. Assumes sorted data.

    Args:
        data (list): target data.
        target (any): target to be found.
        low (int): low-end initial guess index, set to '0' if unknown.
        high (int): high-end initital guess index, set to 'len(data) - 1' if unknown.
        force (boolean): If true, target must be inside data. If False, returns index to closest but smaller element.

    Raises:
        ValueError: target out-of-bounds
        ValueError: target not in data

    Returns:
        int: index of the target or closest smallest index 

    """
    if target < data[0]:
        raise ValueError('target out-of-bounds')

    elif target > data[len(data) - 1] and force == True:
        raise ValueError('target out-of-bounds')

    else:
        if high >= low:
            mid = (low + high) // 2

            if data[mid] == target:
                return mid

            elif data[mid] > target:
                return find(data= data, target= target, low= low, high= mid - 1, force = force)

            else:
                return find(data= data, target= target, low= mid + 1, high= high, force= force)
        else:
            if force:
                raise ValueError('target not in data')

            else:
                return high

def main():
    import random
    random.seed(0)

    random_data = [random.randint(-10000000, 10000000) for i in range(random.randint(1, 10000))]
    random_data.sort()

    target_index = random.randint(0, len(random_data) - 1)
    target = random_data[target_index]

    index = find(data=random_data, target= target, low=0, high=len(random_data) - 1, force=True)
    print(target_index, index)


if __name__ == '__main__':
    main()