from enum import Enum

class WantedRoleEnum(Enum):
    COFounder = 'Cofounder'
    CTO = 'CTO'
    COO = 'COO'
    CMO = 'CMO'
    CFO = 'CFO'
    CoreEngineer = 'CoreEngineer'
    Consultant = 'Consultant'


class CityEnum(Enum):
    BJ = 'Beijing',
    SH = 'Shanghai',
    SZ = 'Shenzhen',
    EnabledRemote = 'ALl_RemoteCapability'
    OtherCity = 'OtherCities'

def getExcludeCity(city:str):
    cities = []
    for v in CityEnum:
        if str(v.value).lower() != city.lower():
            cities.append(v.value)
    return ",".join(cities)

def getExcludeWantedRole(role:str):
    roles = []
    for v in WantedRoleEnum:
        if v.value.lower() != role.lower():
            roles.append(v.value)
    return ",".join(roles)
