import requests

from Integration.Eloverblik.Configuration import Configuration


class DataAccessTokenClient:

    def __init__(self, configuration: Configuration):
        self.__base_url = 'https://api.eloverblik.dk/thirdpartyapi/api/1.0/token'
        self.__configuration = configuration


    def get_token(self) -> str:
        headers = {'Authorization': 'Bearer ' + self.__configuration.refresh_token}
        response = requests.get(self.__base_url, headers=headers)
        if not response.ok:
            raise AssertionError('Request was not successful')
        return response.json()['result']
