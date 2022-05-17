from dateutil.relativedelta import relativedelta

from Integration.RelativeDelta.IRelativeDeltaFactory import IRelativeDeltaFactory


class MonthRelativeDeltaFactory(IRelativeDeltaFactory):
    def create_time_delta(self, position: int) -> relativedelta:
        return relativedelta(months=position - 1)
