import configparser
import requests

from .constants import GITHUB_GRAPHQL_URL, GITHUB_API_URL
from .exceptions import (ConfigFileNotFound, AuthSectionNotFound,
                         AccessTokenParameterNotFound, UsernameParameterNotFound,
                         InvalidGraphQLQuery, InvalidAPIRequest)


class GithubGraphist:
    def __init__(self):
        pass

    @property
    def auth(self):
        return self.username, self._token

    @property
    def username(self):
        auth_data = self._get_auth_data()
        try:
            return auth_data['username']
        except KeyError as err:
            raise UsernameParameterNotFound(err)

    @property
    def _token(self):
        auth_data = self._get_auth_data()
        try:
            return auth_data['token']
        except KeyError as err:
            raise AccessTokenParameterNotFound(err)

    @staticmethod
    def _get_auth_data():
        confparser = configparser.ConfigParser()
        try:
            auth_data = confparser.read('auth.conf')
        except configparser.MissingSectionHeaderError as err:
            raise AuthSectionNotFound(err)
        if not auth_data:
            raise ConfigFileNotFound()
        try:
            return confparser['auth']
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

    @staticmethod
    def generate_api_request(parameters):
        request = GITHUB_API_URL
        for key in parameters.keys():
            if parameters[key]:
                request = '{}/{}/{}'.format(request, key, parameters[key])
            else:
                request = '{}/{}'.format(request, key)

        return request

    @staticmethod
    def perform_api_request(request):
        try:
            response = requests.get(request)
        except requests.exceptions.RequestException as err:
            raise ConnectionError(err)

        if response.status_code != 200:
            raise InvalidAPIRequest()
        return response.text


def main():
    gitgraph = GithubGraphist()
    print(gitgraph.username)
    print(gitgraph.perform_graphql_request("{ viewer { login }}"))
    request_parameters = {'users': 'yashin-alexander', 'repos': ''}
    request_parameters = gitgraph.generate_api_request(request_parameters)
    print(request_parameters)
    print(gitgraph.perform_api_request(request_parameters))


if __name__ == '__main__':
    main()
