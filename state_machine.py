class state_machine:
    def __init__(self):
        self.handlers = {}
        self.start_state = None
        self.end_states = []
    
    def add_state(self, name, handler, end_state=0):
        name = name.upper()
        self.handlers[name] = handler
        if end_state:
            self.end_states.append(name)
    
    def set_start(self, name):
        self.start_state = name.upper()
    
    def run(self, cargo):
        try:
            handler = self.handlers[self.start_state]
        except:
            raise Exception("Must call .set_start() before run()")
        
        if not self.end_states:
            raise Exception("At least one state must be an end_state")

        while (True):
            (new_state, cargo) = handler(cargo)
            if new_state.upper() in self.end_states:
                print("Reached ", new_state)
                break
            else:
                handler = self.handlers[new_state.upper()]
