        
import beringia.region as reg
import beringia.interface.parser as parser
import Levenshtein

class Parser:
    valid_commands = ['help', 'h', 'parameters', 'reset', 'exit', 'run', 'r', 'elevation', 'elev', 'slow', 'flora']
    max_distance = 3  # Adjust this threshold as needed
    command_method_mapping = {
        'h': 'help',
        'help': 'help',
        'parameters': 'set_parameters',
        'reset': 'reset',
        'exit': 'exit',
        'run': 'run_simulation',
        'r': 'run_simulation',
        'elevation': 'show_elevation',
        'elev': 'show_elevation',
        'slow': 'toggle_burn',
        'flora': 'set_flora_system'
    }


    def __init__(self, session):
        # Initialize any instance-specific variables here
        self.inputLog = []
        self.session = session

        

    def parse_input(self, inp):
        self.inputLog.append(inp)
        inp = self.clean_input(inp)
        if inp in self.valid_commands:
            method_name = self.command_method_mapping.get(inp)
            method = getattr(self.session, method_name)
            #method()
            print('found method!')
            print(method_name)
            print(method)
        else:
            suggestion = self.suggest_closest_command(inp)
            if suggestion:
                verification = input(f"Did you mean '{suggestion}'? (yes/no): ").strip().lower()
                if verification == 'yes' or verification == 'y':
                    method_name = self.command_method_mapping.get(suggestion, None)
                    if method_name:
                        #method = getattr(self.session, method_name)
                        #method()
                        print (method_name)

    def clean_input(self, inp):
        temp_input = str(inp).lower().strip()
        return temp_input

    def find_closest_command(self, inp):
        closest_command = None
        min_distance = float('inf')

        for command in self.valid_commands:
            distance = Levenshtein.distance(inp, command)
            if distance < min_distance:
                min_distance = distance
                closest_command = command

        if min_distance <= self.max_distance:
            return closest_command
        else:
            return None

    def suggest_closest_command(self, inp):
        closest_command = None
        min_distance = float('inf')

        for command in self.valid_commands:
            distance = Levenshtein.distance(inp, command)
            if distance < min_distance:
                min_distance = distance
                closest_command = command

        if min_distance <= self.max_distance:
            return closest_command
        else:
            return None


