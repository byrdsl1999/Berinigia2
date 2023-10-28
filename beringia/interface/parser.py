'''class Parser:
    def __init__(self, session):
        # Initialize any instance-specific variables here
        self.inputLog = []
        self.session = session

    def parse_input(self, inp):
        self.inputLog.append(inp)
        inp = self.clean_input(inp)
        if inp in ['h', 'help']:
            self.session.help()
        elif inp in ['param', 'parameters']:
            self.session.set_parameters()
        elif inp in ['reset']:
            self.session.reset()
        elif inp in ['e', 'exit']:
            self.session.exit()
        elif inp in ['run']:
            self.session.run_simulation()
        elif inp in ['elev', 'elevation']:
            self.session.show_elevation()
        elif inp in ['slow']:
            self.session.toggle_burn()
        elif inp in ['flora']:
            self.session.set_flora_system()
        else:
            print("Unknown command. Type 'help' for a list of available commands.")
            
    def clean_input(self, input):
        temp_input = str(input).lower().strip()
        return temp_input'''
        
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



        '''
        closest_command = self.find_closest_command(inp)
        
        if closest_command:
            method_name = self.command_method_mapping.get(closest_command, None)
            if method_name:
                method = getattr(self.session, method_name)
                method()
        else:
            # If no exact match found, suggest the closest command and ask for verification
            suggestion = self.suggest_closest_command(inp)
            if suggestion:
                verification = input(f"Did you mean '{suggestion}'? (yes/no): ").strip().lower()
                if verification == 'yes':
                    method_name = self.command_method_mapping.get(suggestion, None)
                    if method_name:
                        #method = getattr(self.session, method_name)
                        #method()
                        print (method_name)
                else:
                    print("Unknown command. Type 'help' for a list of available commands.")
            else:
                print("Unknown command. Type 'help' for a list of available commands.")
            '''

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


