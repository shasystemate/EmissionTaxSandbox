from datetime import date, datetime, timedelta

import pandas as p
import pytz
import requests

from Integration.Eloverblik.Configuration import Configuration
from Integration.RelativeDelta.DayRelativeDeltaFactory import DayRelativeDeltaFactory
from Integration.RelativeDelta.HalfHourRelativeDeltaFactory import HalfHourRelativeDeltaFactory
from Integration.RelativeDelta.HourRelativeDeltaFactory import HourRelativeDeltaFactory
from Integration.RelativeDelta.IRelativeDeltaFactory import IRelativeDeltaFactory
from Integration.RelativeDelta.MonthRelativeDeltaFactory import MonthRelativeDeltaFactory
from Integration.RelativeDelta.QuarterRelativeDeltaFactory import QuarterRelativeDeltaFactory
from Integration.RelativeDelta.YearRelativeDeltaFactory import YearRelativeDeltaFactory


class ConsumptionQuantitiesClient:


    def __init__(self, configuration: Configuration):
        self.__base_url = 'https://api.eloverblik.dk/thirdpartyapi/api/1.0/meterdata/gettimeseries'
        self.__configuration = configuration



    def find_consumption_quantities(self, metering_point_ids: [str], from_timestamp: datetime, to_timestamp: datetime) -> p.DataFrame:
        url = f'{self.__base_url}/{from_timestamp.date()}/{(to_timestamp + timedelta(days=1)).date()}/Hour'
        headers = {'Content-Type': 'application/json',
                   'Authorization': f'Bearer  {self.__configuration.data_access_token}'}
        body = {"MeteringPoints": {"MeteringPoint": metering_point_ids}}
        response = requests.post(url, headers=headers, json=body)
        if not response.ok:
            raise AssertionError('Request was not successful')
        consumption_quantities_dict = {}
        for result in response.json()['result']:
            my_energy_data_market_document = result['MyEnergyData_MarketDocument']
            for time_series in my_energy_data_market_document['TimeSeries']:
                if not time_series['businessType'] == 'A04':
                    continue
                metering_point_id = time_series['MarketEvaluationPoint']['mRID']['name']
                result_starts = []
                result_quantities = []
                consumption_quantities_series = p.Series(dtype=float)
                for period in time_series['Period']:
                    resolution = period['resolution']
                    delta_factory = self.__create_relative_delta_factory(resolution)
                    time_interval_start = datetime.strptime((period['timeInterval']['start']), '%Y-%m-%dT%H:%M:%S%z')
                    for point in period['Point']:
                        position = int(point['position'])
                        result_starts.append(time_interval_start + delta_factory.create_time_delta(position))
                        quantity = float(point['out_Quantity.quantity'])
                        result_quantities.append(quantity)
                consumption_quantities_series = p.concat([consumption_quantities_series, p.Series(data=result_quantities, index=result_starts, dtype=float)])
                first_index = datetime.combine(from_timestamp, datetime.min.time(), pytz.UTC)
                last_index = datetime.combine(to_timestamp, datetime.min.time(), pytz.UTC) - timedelta(hours=1)
                consumption_quantities_dict[metering_point_id] = consumption_quantities_series.loc[first_index:last_index, ].resample('H').sum()
        return p.DataFrame.from_dict(consumption_quantities_dict)


    @staticmethod
    def __create_relative_delta_factory(resolution: str) -> IRelativeDeltaFactory:
        match resolution:
            case 'PT15M':
                return QuarterRelativeDeltaFactory()
            case 'PT30M':
                return HalfHourRelativeDeltaFactory()
            case 'PT1H' | 'PT60M':
                return HourRelativeDeltaFactory()
            case 'PT1D':
                return DayRelativeDeltaFactory()
            case 'P1M':
                return MonthRelativeDeltaFactory()
            case 'PT1Y':
                return YearRelativeDeltaFactory()
            case _:
                return IRelativeDeltaFactory()
