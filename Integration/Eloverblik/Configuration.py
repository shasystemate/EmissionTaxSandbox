import os
from dotenv import load_dotenv


class Configuration:

    @property
    def customer_key(self):
        return self.__customer_key

    @customer_key.setter
    def customer_key(self, value: str):
        self.__customer_key = value

    @property
    def data_access_token(self):
        return self.__data_access_token

    @data_access_token.setter
    def data_access_token(self, value: str):
        self.__data_access_token = value

    @property
    def refresh_token(self) -> str:
        return self.__refresh_token


    @refresh_token.setter
    def refresh_token(self, value: str):
        self.__refresh_token = value


    def __init__(self):
        self.__refresh_token = None
        self.__data_access_token = None
        self.__customer_key = None
