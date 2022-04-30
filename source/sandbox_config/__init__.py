
class Withable:
    internal_holding: str

    def __enter__(self):
        pass

    def __exit__(self, exception_type, exception_value, traceback):
        pass


onto: Withable = None
