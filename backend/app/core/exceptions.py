class InvalidTransitionError(Exception):
    def __init__(self, current: str, target: str):
        super().__init__(f"Cannot transition from {current} to {target}")