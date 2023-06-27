import random
import datetime

def calculate_all(num1, num2, num3, num4):
    sum_of_numbers = num1 + num2 + num3 + num4
    result1 = sum_of_numbers / 10
    result2 = random.randint(0,100)
    result3 = result1 + result2
    current_year = datetime.datetime.now().year
    return [result1, result2, result3, current_year]

