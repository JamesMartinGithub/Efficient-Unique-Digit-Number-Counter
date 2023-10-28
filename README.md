# Efficient Unique-Digit Number Counter
An efficient way to, given a list of ranges, return a list of counts of numbers that have all-unique digits

- Maximum time complexity of O(n) where n is the number of digits in an input range
- Uses precomputation and recursion to increase efficiency

This solution splits a range into smaller ranges that can be computed using just the digits of the range end-values;
this means very little iteration is used compared to the standard solution of triple-nested for loops.

### Efficiency compared to a simple iterative solution:
The iterative algorithm used is provided in `IterativeSolution.py`. The results are averaged.

#### Test data:
```
a = [[1,20], [50, 900], [1000, 3000], [30, 60], [90, 300], [50, 1000], [600, 70000]]
b = [[1,2235070], [50, 90334680], [166, 30553800], [453236, 257925], [50, 10856800], [6234600, 70077300]]
```
#### Results:
+ Array a
  - Iterative solution:   0.03669s
  - Efficient Solution:   0.00015s
+ Array b
  - Iterative solution: 107.31039s
  - Efficient Solution: 000.00745s

The iterative solution's time increased by 292378%

The efficient solution's time increased by   4866%
