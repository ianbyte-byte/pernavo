import json
import math
from typing import Dict, List, Tuple, Union

from agentctl_types import DataError, JsonValue, Problem


class DuplicateJsonKeyError(ValueError):
    pass


class NonFiniteJsonNumberError(ValueError):
    pass


def duplicate_free_object(pairs: List[Tuple[str, JsonValue]]) -> Dict[str, JsonValue]:
    result: Dict[str, JsonValue] = {}
    for key, value in pairs:
        if key in result:
            raise DuplicateJsonKeyError(key)
        result[key] = value
    return result


def finite_float(value: str) -> float:
    number = float(value)
    if not math.isfinite(number):
        raise NonFiniteJsonNumberError(value)
    return number


def reject_constant(value: str) -> float:
    raise NonFiniteJsonNumberError(value)


def decode_json(source: Union[str, bytes], label: str, invalid_code: str) -> JsonValue:
    try:
        text = source.decode("utf-8") if isinstance(source, bytes) else source
        return json.loads(
            text,
            object_pairs_hook=duplicate_free_object,
            parse_float=finite_float,
            parse_constant=reject_constant,
        )
    except DuplicateJsonKeyError as error:
        raise DataError(Problem("duplicate_json_key", label + " contains duplicate key " + str(error)))
    except NonFiniteJsonNumberError as error:
        raise DataError(Problem("non_finite_number", label + " contains non-finite number " + str(error)))
    except RecursionError:
        raise DataError(Problem("json_recursion", label + " exceeds JSON nesting limit"))
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise DataError(Problem(invalid_code, label + " is not valid JSON: " + str(error)))
