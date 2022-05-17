from dateutil.relativedelta import relativedelta

from Integration.RelativeDelta.IRelativeDeltaFactory import IRelativeDeltaFactory


class DayRelativeDeltaFactory(IRelativeDeltaFactory):
    def create_time_delta(self, position: int) -> relativedelta:
        return relativedelta(days=position - 1)
