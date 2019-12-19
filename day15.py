from intcode import IntcodeParser

parser = IntcodeParser()
intcode = parser.get_intcode_from_file('input-files/day15.csv')

print(intcode)