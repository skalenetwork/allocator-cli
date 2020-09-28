import copy
from datetime import datetime

from utils.helper import from_wei, permille_to_percent


def check_validator_fields(expected, actual, fields):
    for i, field in enumerate(fields):
        assert str(actual[i]) == str(expected[field])


def convert_validators_info(validator_info):
    result = []
    for data in validator_info:
        info = copy.deepcopy(data)
        info['fee_rate'] = permille_to_percent(info['fee_rate'])
        info['minimum_delegation_amount'] = from_wei(
            info['minimum_delegation_amount']
        )
        info['status'] = 'Trusted' if info['trusted'] else 'Registered'
        info['registration_time'] = datetime.fromtimestamp(
            info['registration_time']
        ).strftime('%d.%m.%Y-%H:%M:%S')
        result.append(info)
    return result


def str_contains(string, values):
    return all(x in string for x in values)
