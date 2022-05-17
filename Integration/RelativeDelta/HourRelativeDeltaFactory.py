from dateutil.relativedelta import relativedelta

from Integration.RelativeDelta.IRelativeDeltaFactory import IRelativeDeltaFactory


class HourRelativeDeltaFactory(IRelativeDeltaFactory):
    def create_time_delta(self, position: int) -> relativedelta:
        return relativedelta(hours=position - 1)
