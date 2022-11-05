import dataclasses


class Operator:
    MATCH = 'match'
    NEGATE_MATCH = 'negate_match'
    INCLUDE = 'include' #separate values with comma ,
    EXCLUDE = 'exclude' #separate values with comma ,
    REGEX_MATCH = 'regex_match'
    REGEX_NOT_MATCH = 'regex_not_match'
    LESS_THAN = 'less_than'
    GREATER_THAN = 'greater_than'
    GREATER_THAN_OR_EQUAL_TO = 'greater_than_or_equal_to'
    EXISTS = 'exists'
    NOT_EXISTS = 'not_exists'

operator_lookup = {
    Operator.MATCH: '=',
    Operator.NEGATE_MATCH: '!=',
    Operator.INCLUDE: '=',  # separate values with comma ,
    Operator.EXCLUDE: '!=',  # separate values with comma ,
    Operator.REGEX_MATCH: '=',
    Operator.REGEX_NOT_MATCH: '!=',
    Operator.LESS_THAN: '<',
    Operator.GREATER_THAN: '>',
    Operator.GREATER_THAN_OR_EQUAL_TO: '>=',
    Operator.EXISTS: None,
    Operator.NOT_EXISTS:  None
}

@dataclasses.dataclass
class Filter:
    field: str
    operator: Operator
    value: str
