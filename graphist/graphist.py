import requests
import configparser

from constants import GITHUB_GRAPHQL_URL, GITHUB_API_URL
from exceptions import (ConfigFileNotFound, AuthSectionNotFound,
                        AccessTokenParameterNotFound, UsernameParameterNotFound,
                        InvalidGraphQLQuery, InvalidAPIRequest)


class GithubGraphist:
    def __init__(self):
        self._config_parser = configparser.ConfigParser()

    @property
    def auth(self):
        return self._username, self._token

    @property
    def _username(self):
        auth_data = self._read_config_file()
        try:
            return auth_data['username']
        except KeyError as err:
            raise UsernameParameterNotFound(err)

    @property
    def _token(self):
        auth_data = self._read_config_file()
        try:
            return auth_data['token']
        except KeyError as err:
            raise AccessTokenParameterNotFound(err)

    def _read_config_file(self):
        try:
            auth_data = self._config_parser.read('auth.conf')
        except configparser.MissingSectionHeaderError as err:
            raise AuthSectionNotFound(err)
        if not auth_data:
            raise ConfigFileNotFound()
        try:
            return self._config_parser['auth']
        except KeyError as err:
            raise AuthSectionNotFound(err)

    def perform_graphql_request(self, graphql_query):
        query = {'query': graphql_query}
        try:
            response = requests.post(GITHUB_GRAPHQL_URL, auth=self.auth, json=query)
        except requests.exceptions.RequestException as err:
            raise ConnectionError(err)

        if response.status_code != 200:
            raise InvalidGraphQLQuery()

        return response.text

    def generate_api_request(self, parameters):
        request = GITHUB_API_URL
        for key in parameters.keys():
            if parameters[key]:
                request = '{}/{}/{}'.format(request, key, parameters[key])
            else:
                request = '{}/{}'.format(request, key)

        return request

    def perform_api_request(self, request):
        try:
            response = requests.get(request)
        except requests.exceptions.RequestException as err:
            raise ConnectionError(err)

        if response.status_code != 200:
            raise InvalidAPIRequest()
        return response.text


if __name__ == '__main__':
    gitgraph = GithubGraphist()
    print(gitgraph._username)
    print(gitgraph._token)
    print(gitgraph.perform_graphql_request("{ viewer { login }}"))
    parameters = {'users': 'yashin-alexander', 'repos': ''}
    parameters = gitgraph.generate_api_request(parameters)
    print(parameters)
    print(gitgraph.perform_api_request(parameters))
