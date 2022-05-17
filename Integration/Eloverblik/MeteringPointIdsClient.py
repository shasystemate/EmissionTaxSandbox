import requests

from Integration.Eloverblik.Configuration import Configuration


class MeteringPointIdsClient:

    def __init__(self, configuration: Configuration):
        self.__base_url = 'https://api.eloverblik.dk/thirdpartyapi/api/1.0/authorization/authorization/meteringpoints/customerKey'
        self.__configuration = configuration


    def find_metering_points_ids(self) -> [str]:
        url = f'{self.__base_url}/{self.__configuration.customer_key}'
        headers = {'Authorization': 'Bearer ' + self.__configuration.data_access_token}
        response = requests.get(url, headers=headers)
        if not response.ok:
            raise AssertionError('Request was not successful')
        metering_point_ids = []
        for result in response.json()['result']:
            metering_point_ids.append(result['meteringPointId'])
        return metering_point_ids
