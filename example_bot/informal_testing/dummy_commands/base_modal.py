from .base_generic import COMMON_INTERACTION_DUMMY
from functools import wraps

def dummy_modal_submit(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        data = function(*args, **kwargs)
        return {
            "data": data,
            "type": 5,
            **COMMON_INTERACTION_DUMMY,
        }, "RUN_HANDLER"
    return wrapper
