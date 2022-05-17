import pandas as pd
import requests
from datetime import datetime

from Integration.Co2emisprog import Co2emisprogRecordNames, Co2emisprogAttributeNames


class Co2emisprogClient:
    __base_url = 'https://api.energidataservice.dk/datastore_search_sql'

    def find_co2emisprog(self, price_area: str, datetime_utc_from: datetime,
                         datetime_utc_to: datetime) -> pd.Series:
        params = {'sql': self.create_co2emisprog_query(price_area, datetime_utc_from, datetime_utc_to)}
        response = requests.get(self.__base_url, params=params).json()
        if not bool(response['success']):
            raise AssertionError('Request was not successful')
        result = response['result']
        period_start = []
        quantity = []
        for record in result['records']:
            period_start.append(record[Co2emisprogRecordNames.PERIOD_START])
            quantity.append(record[Co2emisprogRecordNames.QUANTITY])
        series = pd.Series(quantity, index=pd.DatetimeIndex(period_start))
        return series

    def create_co2emisprog_query(self, price_area: str, datetime_utc_from: datetime,
                                 datetime_utc_to: datetime) -> str:
        return \
            f'SELECT ' \
            f'"{Co2emisprogAttributeNames.CO2_EMISSION}" AS {Co2emisprogRecordNames.QUANTITY}, ' \
            f'"{Co2emisprogAttributeNames.PRICE_AREA}" AS {Co2emisprogRecordNames.PRICE_AREA}, ' \
            f'"{Co2emisprogAttributeNames.MINUTES_5_UTC}" as {Co2emisprogRecordNames.PERIOD_START} ' \
            f'FROM ' \
            f'"co2emisprog" ' \
            f'WHERE ' \
            f'"{Co2emisprogAttributeNames.PRICE_AREA}" LIKE \'{price_area}\' AND ' \
            f'"{Co2emisprogAttributeNames.MINUTES_5_UTC}" >= \'{self.as_iso_string(datetime_utc_from)}\' ' \
            f'AND "{Co2emisprogAttributeNames.MINUTES_5_UTC}" < \'{self.as_iso_string(datetime_utc_to)}\' ' \
            f'ORDER BY ' \
            f'"{Co2emisprogAttributeNames.MINUTES_5_UTC}"'

    def as_iso_string(self, datetime_utc_to: datetime):
        return datetime_utc_to.strftime('%Y-%m-%dT%H:%M:%S %Z').replace(' UTC', 'Z')
