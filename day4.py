range_low = 165432
range_high = 707912
#range_low = 111111
#range_high = 133333
pw_range = range(range_low, range_high, 1)

def is_valid_password(pw):
    pw_list = [int(i) for i in str(pw)]

    rising_digits_count = 0
    double_digits_count = 0
    triple_digits_count = 0
    triples = []
    doubles = []

    for prev, cur, next in zip([None]+pw_list[:-1], pw_list, pw_list[1:]+[None]):
        if next == None:
            continue

        if prev == cur and cur == next:
            triple_digits_count += 1
            rising_digits_count += 1
            triples.append(cur)
        elif next == cur and cur not in triples:
            double_digits_count += 1
            rising_digits_count += 1
            doubles.append(cur)
        elif next > cur:
            rising_digits_count += 1

    num_unique = len(set(pw_list))
    num_unique_triples = len(set(triples))

    conditions = \
            rising_digits_count == len(pw_list)-1 \
            and double_digits_count >= 1 \
            and double_digits_count - triple_digits_count >= 0 \
            and num_unique > num_unique_triples \
            and len([value for value in doubles if value not in triples]) > 0
    return conditions

possible_pw = [pw for pw in pw_range if is_valid_password(pw)]
print(len(possible_pw))
print(possible_pw[:50])
