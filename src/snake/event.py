EVENT_INPUT = 'event-input'
EVENT_TICK = 'event-tick'

class Event:

    def __init__(self, event_type, event_data):
        self.event_type = event_type
        self.event_data = event_data

    def type(self):
        return self.event_type


    def data(self):
        return self.event_data

