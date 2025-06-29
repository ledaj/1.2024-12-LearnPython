import random
number = random.randint(1, 10)

def binarySearch(number, list):
    low = 0
    high = len(list) - 1
    while low <= high:
        mid = (low + high) // 2
        guess = list[mid]
        if guess == number:
            return mid
        if guess > number:
            high = mid - 1
        else:
            low = mid + 1
    return None

print(binarySearch(number, [1, 3, 5, 7, 9]))