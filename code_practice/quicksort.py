def quicksort(a, low, high):
	if high <= low:
		return
	p = partition(a, low, high)
	quicksort(a, low, p - 1)
	quicksort(a, p + 1, high)

def partition(a, low, high):
	pivot = a[high]
	i = low # swapping location
	for j in range(low, high):
		if a[j] <= pivot:
			a[i], a[j] = a[j], a[i]
			i = i + 1
	a[i], a[high] = a[high], a[i]
	return i

import random
l = range(10)
random.shuffle(l)
