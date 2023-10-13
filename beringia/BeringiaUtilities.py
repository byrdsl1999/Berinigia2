import random
import string
from collections import Counter
from math import floor


def generate_id(length=6, prefix='00'):
    characters = string.ascii_letters + string.digits  # Includes both letters (upper and lower) and digits
    return prefix + ''.join(random.choice(characters) for _ in range(length))



def split_counter(counter, n):
    sub_counters = [Counter() for _ in range(n)]  # Create empty sub-counters
    total_count = sum(counter.values())  # Calculate the total count

    while total_count > 0:
        elements, weights = zip(*counter.items())
        selected_element = random.choices(elements, weights=weights, k=1)[0]
        selected_counter = Counter({selected_element: 1})

        # Add the selected element to one of the sub-counters
        random_sub_counter = random.choice(sub_counters)
        random_sub_counter += selected_counter

        # Remove the selected element from the original counter
        counter.subtract(selected_counter)

        total_count -= 1

    return sub_counters

def stochastic_round(number):
    '''
    Perform stochastic rounding of a floating-point number.

    This method probabilistically rounds a floating-point number to the nearest integer.
    The rounding decision is based on the fractional part of the number and a randomly
    generated probability.

    Args:
        number (float): The input floating-point number to be rounded.

    Returns:
        int: The stochastically rounded integer result.

    Example:
        >>> stochastic_round(2.7)
        3  # Rounding up with a probability of 0.7 (if random value < 0.7)
        >>> stochastic_round(2.3)
        2  # Rounding down with a probability of 0.3 (if random value < 0.3)
    '''
    
    is_negative = (number < 0)
    number = abs(number)
    fractional_part = number - floor(number)
    probability = random.random()
    if probability > fractional_part:
        rounded = int(number)
    else:
        rounded = int(number) + 1
    if is_negative:
        return rounded * -1
    else:
        return rounded
