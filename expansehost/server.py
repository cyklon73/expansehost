import requests

from exeptions import *
from util import convert_size, convert_millis_to_string, isBlank

API_URL = 'https://cp.expansehost.de/api/v1/'


class ExpireDate:
    def __init__(self, data):
        data = data['expiry_date']
        self.string = str(data['string'])
        self.unix = int(data['unix'])
        self.days = int(data['days'])

    def __repr__(self):
        return self.string


class ServerData:
    def __init__(self, data):
        self.name = str(data['name'])
        self.max_disk = int(data['maxdisk'])
        self.expire_date = ExpireDate(data)

    def __repr__(self):
        return f'Name: {self.name}\n' \
               f'MaxDisk: {convert_size(self.max_disk)}\n' \
               f'Expire at: {self.expire_date}'


class LXCServerData(ServerData):
    def __init__(self, data):
        super().__init__(data)
        self.cpu = int(data['cpu'])
        self.mem = int(data['mem'])
        self.mem_free = int(data['memfree'])
        self.mem_total = self.mem + self.mem_free
        self.net_in = int(data['netin'])
        self.net_out = int(data['netout'])
        self.uptime = int(data['uptime'])
        self.state = str(data['state'])

    def __repr__(self):
        return f'{super().__repr__()}\n' \
               f'CPU: {self.cpu}\n' \
               f'Ram: {convert_size(self.mem)}\n' \
               f'Ram free: {convert_size(self.mem_free)}\n' \
               f'Ram Total: {convert_size(self.mem_total)}\n' \
               f'Network in: {convert_size(self.net_in)}\n' \
               f'Network out: {convert_size(self.net_out)}\n' \
               f'Uptime: {convert_millis_to_string(self.uptime*1000)}\n' \
               f'State: {self.state}'


class KVMServerData(LXCServerData):
    def __init__(self, data):
        super().__init__(data)


class Server:
    def __init__(self, server_id: int, api_token: str):
        if api_token is None:
            raise MissingParameterError(f"api_token cannot be None. this parameter is required.")
        if isBlank(api_token):
            raise MissingParameterError(f"api_token cannot be Blank. this parameter is required.")
        if server_id is None:
            raise MissingParameterError(f"server_id cannot be None. this parameter is required.")
        if server_id < 0:
            raise InvalidParameterError(f"{server_id} is invalid. cause: server id cannot less than 0.")
        self.server_id = server_id
        self.api_token = api_token

    def getApiEndpoint(self):
        return API_URL

    def getServerData(self) -> None:
        return None


class LXCServer(Server):

    def __init__(self, server_id: int, api_token: str):
        super().__init__(server_id, api_token)

    def getApiEndpoint(self):
        return f'{API_URL}lxc/info'

    def getServerData(self) -> LXCServerData:
        response = requests.request('POST', self.getApiEndpoint(), data=f'server_id={self.server_id}', headers={
            'Authorization': f'Bearer {self.api_token}',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Cookie': 'PHPSESSID=cu7tv33sddj4r35t1a4tg3n60u'
        })
        return LXCServerData(response.json()['data'])


class KVMServer(Server):

    def __init__(self, server_id: int, api_token: str):
        super().__init__(server_id, api_token)

    def getApiEndpoint(self):
        return f'{API_URL}kvm/info'

    def getJson(self):
        response = requests.request('POST', self.getApiEndpoint(), data=f'server_id={self.server_id}', headers={
            'Authorization': f'Bearer {self.api_token}',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Cookie': 'PHPSESSID=cu7tv33sddj4r35t1a4tg3n60u'
        })
        return response.json()

    def getServerData(self) -> KVMServerData:
        payload = f'server_id={self.server_id}'
        headers = {
            'Authorization': f'Bearer {self.api_token}',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Cookie': 'PHPSESSID=cu7tv33sddj4r35t1a4tg3n60u'
        }
        requests.packages.urllib3.disable_warnings()
        requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS = 'ALL'
        response = requests.request("POST", self.getApiEndpoint(), headers=headers, data=payload)

        j = response.json()

        error = j['message']['error']
        if error is None:
            return KVMServerData(j['data'])
        elif error == 'Unauthorized':
            raise UnauthorizedError(
                f"you are unauthorized to get the data from the server with the id #{self.server_id}")
