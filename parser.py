import json
import shlex

def parse_input_client(input):
    input_parsed = shlex.split(input)
    print("In parser", input_parsed)
    return input_parsed


def parse_input_api(output):
    return output