from .base_generic import COMMON_INTERACTION_DUMMY
from functools import wraps

def dummy_autocomplete(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        data = function(*args, **kwargs)
        return {
            "data": {
                "guild_id": "267624335836053506",
                "id": "1012551414855245884",
                **data,
            },
            "type": 4,
            **COMMON_INTERACTION_DUMMY,
        }, "RUN_AUTOCOMPLETE"
    return wrapper
