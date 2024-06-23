def reverse_digits(num):
    return int(str(num)[::-1])

def max_difference():
    max_diff = float('-inf')
    for num1 in range(10, 100):
        for num2 in range(10, 100):
            if num1 != num2:  # Ensure distinct numbers
                sum_original = num1 + num2
                sum_reversed = reverse_digits(num1) + reverse_digits(num2)
                diff = abs(sum_original - sum_reversed)
                max_diff = max(max_diff, diff)
    return max_diff

max_diff = max_difference()
print("Maximum difference in the sum of reversed two-digit numbers:", max_diff)
