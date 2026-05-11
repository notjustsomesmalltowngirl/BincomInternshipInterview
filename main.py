import math
import random
import psycopg2

worker_colors = {
    'MONDAY': [
        'GREEN', 'YELLOW', 'GREEN', 'BROWN', 'BLUE', 'PINK',
        'BLUE', 'YELLOW', 'ORANGE', 'CREAM', 'ORANGE',
        'RED', 'WHITE', 'BLUE', 'WHITE', 'BLUE',
        'BLUE', 'BLUE', 'GREEN'
    ],

    'TUESDAY': [
        "ARSH", "BROWN", "GREEN", "BROWN", "BLUE", "BLUE",
        "BLEW", "PINK", "PINK", "ORANGE", "ORANGE",
        "RED", "WHITE", "BLUE", "WHITE", "WHITE",
        "BLUE", "BLUE", "BLUE"
    ],

    'WEDNESDAY': [
        "GREEN", "YELLOW", "GREEN", "BROWN", "BLUE", "PINK",
        "RED", "YELLOW", "ORANGE", "RED", "ORANGE",
        "RED", "BLUE", "BLUE", "WHITE", "BLUE",
        "BLUE", "WHITE", "WHITE"
    ],

    'THURSDAY': [
        "BLUE", "BLUE", "GREEN", "WHITE", "BLUE", "BROWN",
        "PINK", "YELLOW", "ORANGE", "CREAM", "ORANGE",
        "RED", "WHITE", "BLUE", "WHITE", "BLUE",
        "BLUE", "BLUE", "GREEN"
    ],

    'FRIDAY': [
        "GREEN", "WHITE", "GREEN", "BROWN", "BLUE", "BLUE",
        "BLACK", "WHITE", "ORANGE", "RED", "RED",
        "RED", "WHITE", "BLUE", "WHITE", "BLUE",
        "BLUE", "BLUE", "WHITE"
    ]
}


# ---------------------------------------------------
# 1. Calculate the mean
# ---------------------------------------------------

ALL_WEEK_COLORS = []

for color_list in worker_colors.values():
    ALL_WEEK_COLORS += color_list

ALL_WEEK_COLORS_COUNT = len(ALL_WEEK_COLORS)

# Remove duplicates
unique_colors = list(set(ALL_WEEK_COLORS))

# Count frequencies
COLOR_FREQ_DICT = {}

for color in unique_colors:
    COLOR_FREQ_DICT[color] = ALL_WEEK_COLORS.count(color)

MEAN = round(
    sum(count for count in COLOR_FREQ_DICT.values()) / len(COLOR_FREQ_DICT),
    2
)

print('Average is', MEAN)


# ---------------------------------------------------
# 2. Which color is mostly worn throughout the week?
# ---------------------------------------------------

highest_number = max(COLOR_FREQ_DICT.values())

freq_colors = [
    color
    for color, freq in COLOR_FREQ_DICT.items()
    if freq == highest_number
]

print(f"The most frequently worn color(s) is/are {', '.join(freq_colors)}")


# ---------------------------------------------------
# 3. Which color is the median?
# ---------------------------------------------------

median_pos = math.floor(ALL_WEEK_COLORS_COUNT / 2)

print(f'Median color is {ALL_WEEK_COLORS[median_pos]}')


# ---------------------------------------------------
# 4. BONUS: Get the variance of the colors
# ---------------------------------------------------

print(COLOR_FREQ_DICT)

variance = 0

for count in COLOR_FREQ_DICT.values():
    variance += pow(count - MEAN, 2)

variance /= len(COLOR_FREQ_DICT)

print(f'The variance of all the color frequencies is {round(variance, 2)}')


# ---------------------------------------------------
# 5. BONUS:
# If a color is chosen at random,
# what is the probability that the color is red?
# ---------------------------------------------------

probability_of_red = (
    COLOR_FREQ_DICT['RED'] / ALL_WEEK_COLORS_COUNT
)

print(
    'If a color is chosen at random, '
    f'the probability of it being red is {round(probability_of_red, 2)}'
)


# ---------------------------------------------------
# 6. Save the colours and their frequencies
# in PostgreSQL database
# ---------------------------------------------------

conn = psycopg2.connect(
    database="colors",
    user='postgres',
    password='root',
    host='localhost',
    port='5432'
)

conn.autocommit = True

cursor = conn.cursor()

sql = '''
CREATE TABLE COLORS(
    color_id SERIAL PRIMARY KEY,
    color_name CHAR(20),
    color_freq INT
);
'''

cursor.execute(sql)

for color_tuple in COLOR_FREQ_DICT.items():

    sql2 = '''
        INSERT INTO DETAILS(
            color_name,
            color_freq
        )
        VALUES (%s, %s);
    '''

    cursor.execute(sql2, color_tuple)

sql3 = '''SELECT * FROM COLORS;'''

cursor.execute(sql3)

for i in cursor.fetchall():
    print(i)

conn.commit()
conn.close()


# ---------------------------------------------------
# 7. BONUS:
# Write a recursive searching algorithm
# ---------------------------------------------------

def binary_search(nums, target, low, high):

    low, high = 0, len(nums) - 1

    if low <= high:

        middle = (low + high) // 2

        if nums[middle] == target:
            return middle

        elif target < nums[middle]:
            return binary_search(nums, target, low, middle - 1)

        elif target > nums[middle]:
            return binary_search(nums, target, middle + 1, high)

    else:
        return


# nums = [2, 3, 4, 5, 6, 7, 8, 9]
# print('The index is ', binary_search(nums, 5, 0, len(nums)-1))


# ---------------------------------------------------
# 8. Generate random 4-digit binary number
# and convert to base 10
# ---------------------------------------------------

bin_str = ''

for i in range(4):
    bin_str += str(random.randint(0, 1))

print(f'The number {bin_str} in decimal is {int(bin_str, 2)}')


# ---------------------------------------------------
# Fibonacci sum
# ---------------------------------------------------

def fibonacci_sum(n):

    sum = 0
    current, next = 0, 1

    for _ in range(n):

        # Add current Fibonacci number
        sum += current

        # Update values
        temp = current
        current = next
        next += temp

    return sum


print(fibonacci_sum(50))