import re

def main():
    text = open('./resources/recettes.txt')
    print_temperatures_in_text(text)
    text.seek(0)
    print_bake_times_in_text(text)

def print_temperatures_in_text(text):
    print("Temperature in text:")
    for line in text:
        temperatures = get_temperatures(line)
        if len(temperatures) != 0:
            print(temperatures)

def print_bake_times_in_text(text):
    print("Bake times in text:")
    for line in text:
        bake_times = get_bake_times(line)
        if len(bake_times) != 0:
            bake_time = ""
            for i in range(len(bake_times[0])):
                bake_time = bake_time + bake_times[0][i]
            print(bake_time)

def get_bake_times(line_of_text):
    bake_times_regex = r'Bake at 350° for (\d+ to \d+ minutes) |Cook until tender, (\d+ to \d+ minutes)|simmer for (\d+ or \d+ minutes)|Bake at 350 degrees for (\d+ to \d+ minutes)|Cook over rapidly boiling water; stirring often, for (\d+ to \d+ minutes)|\b(?:(?:b|B)ake|simmer|Cook|COOK|cook|SIMMER|baking|boiling)\b[\w ;,().°]*\b((?:(?:1 or )?(?:\d+ ?- ?)?\d+|ONE) ?(?:hr|minutes?|min|hours?|(?:MORE )?MINUTES?|MIN))'
    return re.findall(bake_times_regex, line_of_text)

def get_temperatures(line_of_text):
    temperatures_regex = r'((?:\d+ to )?\d+ ?(?:degrees?|deg F.|°|F))'
    return re.findall(temperatures_regex, line_of_text)

if __name__ == "__main__":
   main()