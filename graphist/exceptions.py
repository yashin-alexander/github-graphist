class ConfigFileError(Exception):
    pass


class ConfigFileNotFound(ConfigFileError):
    pass


class InvalidConfigFileStructure(ConfigFileError):
    pass


class AuthSectionNotFound(InvalidConfigFileStructure):
    pass


class AccessTokenParameterNotFound(InvalidConfigFileStructure):
    pass


class UsernameParameterNotFound(InvalidConfigFileStructure):
    pass


class InvalidGraphQLQuery(Exception):
    pass


class InvalidAPIRequest(Exception):
    pass
