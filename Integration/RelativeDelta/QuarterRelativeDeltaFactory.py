from dateutil.relativedelta import relativedelta

from Integration.RelativeDelta.IRelativeDeltaFactory import IRelativeDeltaFactory


class QuarterRelativeDeltaFactory(IRelativeDeltaFactory):
    def create_time_delta(self, position: int) -> relativedelta:
        return relativedelta(minutes=(position - 1) * 15)
