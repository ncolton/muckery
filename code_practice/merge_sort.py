import random
l = range(10)
random.shuffle(l)

def merge_sort(a):
	# time complexity is O(n log(n)) for best/avg/worst
	# space complexity is O(n) if done w/o creating new lists, but I am, so no idea as to space other than 'not great'
	if len(a) <= 1:
		return a
	a1 = merge_sort(a[0:len(a)/2])
	a2 = merge_sort(a[len(a)/2:])
	ret = []
	while len(a1) or len(a2):
		if not len(a1):
			while len(a2):
				ret.append(a2.pop(0))
		elif not len(a2):
			while len(a1):
				ret.append(a1.pop(0))
		elif a1[0] < a2[0]:
			ret.append(a1.pop(0))
		else:
			ret.append(a2.pop(0))
	return ret
