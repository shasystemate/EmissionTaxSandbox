import pandas as pd
import requests
from datetime import datetime

from Integration.Elspotprices import ElspotpricesRecordNames, ElspotpricesAttributeNames


class ElspotpricesClient:
    __base_url = 'https://api.energidataservice.dk/datastore_search_sql'

    def find_elspotprices(self, price_area: str, datetime_utc_from: datetime,
                          datetime_utc_to: datetime) -> pd.Series:
        params = {'sql': self.create_elspotprices_query(price_area, datetime_utc_from, datetime_utc_to)}
        response = requests.get(self.__base_url, params=params).json()
        if not bool(response['success']):
            raise AssertionError('Request was not successful')
        result = response['result']
        period_start = []
        quantity = []
        for record in result['records']:
            period_start.append(record[ElspotpricesRecordNames.PERIOD_START])
            quantity.append(record[ElspotpricesRecordNames.SPOT_PRICE_DKK])
        series = pd.Series(quantity, index=pd.DatetimeIndex(period_start))
        series.name = 'elspotprice'
        return series

    def create_elspotprices_query(self, price_area: str, datetime_utc_from: datetime,
                                  datetime_utc_to: datetime) -> str:
        return \
            f'SELECT ' \
            f'"{ElspotpricesAttributeNames.SPOT_PRICE_DKK}" AS {ElspotpricesRecordNames.SPOT_PRICE_DKK}, ' \
            f'"{ElspotpricesAttributeNames.PRICE_AREA}" AS {ElspotpricesRecordNames.PRICE_AREA}, ' \
            f'"{ElspotpricesAttributeNames.HOUR_UTC}" as {ElspotpricesRecordNames.PERIOD_START} ' \
            f'FROM ' \
            f'"elspotprices" ' \
            f'WHERE ' \
            f'"{ElspotpricesAttributeNames.PRICE_AREA}" LIKE \'{price_area}\' AND ' \
            f'"{ElspotpricesAttributeNames.HOUR_UTC}" >= \'{self.as_iso_string(datetime_utc_from)}\' ' \
            f'AND "{ElspotpricesAttributeNames.HOUR_UTC}" < \'{self.as_iso_string(datetime_utc_to)}\' ' \
            f'ORDER BY ' \
            f'"{ElspotpricesAttributeNames.HOUR_UTC}"'

    def as_iso_string(self, datetime_utc_to: datetime):
        return datetime_utc_to.strftime('%Y-%m-%dT%H:%M:%S %Z').replace(' UTC', 'Z')