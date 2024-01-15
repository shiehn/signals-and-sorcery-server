import json
from typing import List, Any, Union


class FileData:
    def __init__(self, name: str, file_type: str, url: str):
        self.name = name
        self.file_type = file_type
        self.url = url

    @staticmethod
    def from_dict(file_dict: dict) -> 'FileData':
        # Use .get() with a default value for 'type'
        name = file_dict.get('name', '')
        file_type = file_dict.get('type', 'unknown')  # Default type can be 'unknown' or any other placeholder
        url = file_dict.get('url', '')
        return FileData(name, file_type, url)

    def to_dict(self):
        return {
            'name': self.name,
            'type': self.file_type,
            'url': self.url
        }


class ResultsData:
    def __init__(self, message_id: str, files: List[FileData], error: str, logs:str, message: str, status: str):
        self.id = message_id
        self.files = files
        self.error = error
        self.logs = logs
        self.message = message
        self.status = status

    @staticmethod
    def from_dict(data_dict: dict) -> 'ResultsData':
        print("FROM_DICT ----------------------------------")
        print("FULL_DATA_DICT: " + str(data_dict))
        response = data_dict.get('response', {})
        print("response: " + str(response))
        files = [FileData.from_dict(file) for file in response.get('files', [])]
        print("files: " + str(files))
        error = response.get('error', '')
        print("error: " + str(error))
        message = response.get('message', '')
        print("message: " + str(message))
        logs = response.get('logs', '')
        print("logs: " + str(logs))
        message_id = response.get('id', '')
        print("message_id: " + str(message_id))
        status = response.get('status', '')  # Default to empty string if 'status' is not provided
        print("status: " + str(status))
        return ResultsData(
            message_id,
            files,
            error,
            logs,
            message,
            status
        )

    def to_dict(self):
        return {
            'id': self.id,
            'token': 'empty',
            'response': {
                'files': [file.to_dict() for file in self.files],
                'error': self.error,
                'logs': self.logs,
                'message': self.message
            },
            'status': self.status
        }


class ActionData:
    def __init__(self, action: str, response: str, id: str, from_: str, to: str):
        self.action = action
        self.response = response
        self.id = id
        self.from_ = from_
        self.to = to

    @staticmethod
    def from_dict(data_dict: dict) -> 'ActionData':
        return ActionData(
            data_dict['action'], data_dict['response'], data_dict['id'], data_dict['from'], data_dict['to']
        )


class RegisterData:
    def __init__(self, status: int):
        self.status = status

    @staticmethod
    def from_dict(data_dict: dict) -> 'RegisterData':
        return RegisterData(data_dict['status'])


from typing import Union, List

class Param:
    def __init__(self, name: str, type: str, default_value: Union[str, int, float], ui_component: str = None,
                 min: int = None, max: int = None, step: int = None, options: List[Union[str, int, float]] = None):
        self.name = name
        self.type = type
        self.default_value = default_value
        self.ui_component = ui_component
        self.min = min
        self.max = max
        self.step = step
        self.options = options if options is not None else []

    @staticmethod
    def from_dict(param_dict: dict) -> 'Param':
        return Param(
            param_dict['name'],
            param_dict['type'],
            param_dict['default_value'],
            param_dict.get('ui_component', None),
            param_dict.get('min', 0),
            param_dict.get('max', 0),
            param_dict.get('step', 0),
            param_dict.get('options', [])
        )

    def to_dict(self):
        return {
            'name': self.name,
            'type': self.type,
            'default_value': self.default_value,
            'ui_component': self.ui_component,
            'min': self.min,
            'max': self.max,
            'step': self.step,
            'options': self.options
        }



class ContractData:
    def __init__(self, method: str, name: str, description: str, author: str, version: str, params: List[Param]):
        self.method = method
        self.name = name
        self.description = description
        self.author = author
        self.version = version
        self.params = params

    @staticmethod
    def from_dict(data_dict: dict) -> 'ContractData':
        # The following line should use 'method_name', not 'method'
        params = [Param.from_dict(param) for param in data_dict['params']]
        return ContractData(data_dict['method_name'], data_dict['name'], data_dict['description'], data_dict['author'],
                            data_dict['version'], params)  # Use 'method_name' here

    def to_dict(self):
        return {
            'method_name': self.method,
            'name': self.name,
            'description': self.description,
            'author': self.author,
            'version': self.version,

            'params': [param.to_dict() for param in self.params]
        }


class Message:
    def __init__(self, token: str, type: str, data: Any):
        self.token = token
        self.type = type
        self.data = data

    @staticmethod
    def from_dict(msg_dict: dict) -> 'Message':
        if msg_dict['type'] == 'contract':
            return Message(msg_dict['token'], msg_dict['type'], ContractData.from_dict(msg_dict['data']))
        elif msg_dict['type'] == 'action':
            return Message(msg_dict['token'], msg_dict['type'], ActionData.from_dict(msg_dict['data']))
        elif msg_dict['type'] == 'register':
            return Message(msg_dict['token'], msg_dict['type'], RegisterData.from_dict(msg_dict['data']))
        elif msg_dict['type'] == 'results':
            return Message(msg_dict['token'], msg_dict['type'], ResultsData.from_dict(msg_dict['data']))
        else:
            raise ValueError(f"Unknown type: {msg_dict['type']}")

    def to_dict(self):
        return {
            'token': self.token,
            'type': self.type,
            'data': self.data.to_dict() if self.data else None,
        }


def create_message_from_json(msg_json: str) -> Message:
    msg_dict = json.loads(msg_json)
    return Message.from_dict(msg_dict)
