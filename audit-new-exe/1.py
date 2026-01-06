def quick_sort1(arr):
    n = len(arr)
    if n <=1: return arr

    pivot = arr[-1]
    left  = [ x for x in arr[:-1] if x <= pivot]
    right = [ x for x in arr[:-1] if x >  pivot]

    return quick_sort1(left) + [pivot] + quick_sort1(right)

arr = [23,34,45,656,4,2,34]

print(quick_sort1(arr))


def quick_sort2(arr):
    if len(arr) <= 1:
        return arr

    pivot   = arr[-1]  # pivot is the middle value
    left    = [x for x in arr if x < pivot]
    middle  = [x for x in arr if x == pivot] 
    right   = [x for x in arr if x > pivot]

    return quick_sort2(left) + middle + quick_sort2(right)

arr = [23, 34, 45, 656, 4, 2, 34]
print(quick_sort2(arr))
