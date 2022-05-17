from dateutil.relativedelta import relativedelta

from Integration.RelativeDelta.IRelativeDeltaFactory import IRelativeDeltaFactory


class YearRelativeDeltaFactory(IRelativeDeltaFactory):
    def create_time_delta(self, position: int) -> relativedelta:
        return relativedelta(years=position - 1)
