from dateutil.relativedelta import relativedelta


class IRelativeDeltaFactory:
    def create_time_delta(self, position: int) -> relativedelta:
        pass
