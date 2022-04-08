class KeyboardEvent:
    def __init__(self, event_type, scan_code, name, time):
        """Used as a substitue on mac, simple class replicating the keyboard class

        Args:
            event_type (string): Whether the action is up or down
            scan_code (string): Not really used, the id of the key
            name (string): The key, e.g. 'i', 'f'
            time (float): The time since the action occured
        """
        self.event_type = event_type
        self.scan_code = scan_code
        self.name = name
        self.time = time
        