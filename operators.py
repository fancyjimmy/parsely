import random
from dataclasses import *
from typing import Callable
from enum import Enum
import re
import functools

STRING_METHODS = {methodName: getattr(str, methodName) for methodName in dir(str) if
                  callable(getattr(str, methodName)) and not methodName.startswith("__")}
REGEX_METHODS = {methodName: getattr(re, methodName) for methodName in dir(re) if
                 callable(getattr(re, methodName)) and not methodName.startswith("__")}
SAVE_BUILTIN = {"abs": abs,
                "all": all,
                "any": any,
                "bin": bin,
                "divmod": divmod,
                "enumerate": enumerate,
                "float": float,
                "int": int,
                "format": format,
                "hex": hex,
                "len": len,
                "list": list,
                "max": max,
                "map": map,
                "min": min,
                "oct": oct,
                "ord": ord,
                "pow": pow,
                "reversed": reversed,
                "round": round,
                "range": range,
                "set": set,
                "slice": slice,
                "sorted": sorted,
                "str": str,
                "sum": sum,
                "tuple": tuple,
                "zip": zip}

OPERATIONS = []

SEPARATOR = [":", ">", " "]


def registerOperation(op):
    OPERATIONS.append(op)


def register(names, function):
    if type(names) is list:
        registerOperation(Operation(names, function))  # list off
    elif type(names) is str:
        registerOperation(Operation([names], function))
    else:
        raise Exception("names has to be a string or a list of strings")


# Decorator
def getPossibleNames(names, separators):
    parsedNames = []
    allNames = []
    if type(names) is list:
        parsedNames.extend(names)
        allNames.extend(names)
    elif type(names) is str:
        parsedNames.append(names)
        allNames.append(names)
    else:
        raise Exception("Not valid")
    allNames.extend([str(name) + separator for name in parsedNames for separator in separators])
    return allNames


def operation(*names):
    def decorate_operate(function):
        register(list(names), function)

    return decorate_operate


def suffixedOperation(names, separator=SEPARATOR):
    def decorate_operate(function):
        register(getPossibleNames(names, separator), function)

    return decorate_operate


def getParameterValue(value):
    if value.startswith('"') and value.endswith('"'):
        try:
            return str(eval_expression(value))
        except:
            return value
    if value.startswith("'") and value.endswith("'"):
        try:
            return str(eval_expression(value))
        except:
            return value
    return value


# Decorator which gets a function that transforms a string to another string
def simpleStringOperation(names):
    def decorate_simple_string_operation(transformation):
        def function(lines: list[str], value: str):
            start = getParameterValue(value)
            new_lines = [transformation(line, index, start) for index, line in enumerate(lines)]
            return new_lines

        register(names, function)

    return decorate_simple_string_operation


def debug(func):
    """Print the function signature and return value"""

    @functools.wraps(func)
    def wrapper_debug(*args, **kwargs):
        args_repr = [repr(a) for a in args]  # 1
        kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]  # 2
        signature = ", ".join(args_repr + kwargs_repr)  # 3
        print(f"Calling {func.__name__}({signature})")
        value = func(*args, **kwargs)
        print(f"{func.__name__!r} returned {value!r}")  # 4
        return value

    return wrapper_debug


def eval_expression(input_string, globVar=None, localVar=None):
    # Step 1
    if localVar is None:
        localVar = {}
    if globVar is None:
        globVar = {}

    allowed_names = {"sum": sum, **STRING_METHODS, **SAVE_BUILTIN, **REGEX_METHODS, **localVar}
    # Step 2
    code = compile(input_string, "<string>", "eval")
    # Step 3
    for name in code.co_names:
        if name not in allowed_names:
            # Step 4
            raise NameError(f"Use of {name} not allowed")
    return eval(code, {"__builtins__": {}, **globVar}, allowed_names)


OPERATION_LIST = dict()


@dataclass
class Operation:
    name: list[str]
    transformation: Callable[[list[str], str], list[str]] = lambda lines, criteria: list()

    def fixate(self, op):
        return lambda lines: self.transformation(lines, op)

    def __post_init__(self):
        OPERATION_LIST[self.name[0]] = self.name


class Transformations:
    pass


@suffixedOperation(["filter", 'f'])
def opFilter(lines: list[str], criteria: str):
    new_lines = list()

    for index, line in enumerate(lines):
        if eval_expression(criteria, localVar={'line': line, 'index': index}):
            new_lines.append(line)

    return new_lines


@suffixedOperation(["transform", 't'])
def opTransform(lines: list[str], transformation: str):
    new_lines = [eval_expression(transformation, localVar={'line': line, 'index': index}) for index, line in
                 enumerate(lines)]
    return new_lines


@simpleStringOperation("strip")
def opStrip(line, index, expression):
    return line.strip()


@simpleStringOperation("wrap")
def opWrap(line, index, expression):
    return f'{expression}{line}{expression}'


@simpleStringOperation(["enumerate", 'enum'])
def opEnumerate(line, index, start):
    return f'{index + 1} {line}'


@simpleStringOperation('prefixAll')
def opPrefixAll(line, index, start):
    return f'{start}{line}'


@simpleStringOperation('suffixAll')
def opSuffixAll(line, index, start):
    return f'{line}{start}'


@simpleStringOperation(["html", "HTML"])
def opHTML(line, index, start):
    return f'<{start}>{line}</{start}>'


@suffixedOperation(['split', 's'])
def opSplit(lines: list[str], transformation: str):
    new_lines = list()

    for index, line in enumerate(lines):
        result = eval_expression(transformation, localVar={'line': line, 'index': index})
        if not type(result) is list:
            raise Exception('Result has to be a list')
        new_lines.extend(result)

    return new_lines


@operation('removeEmptyLines', 'rm', 'removeEmpty', "remove Empty", "remove empty", "remove empty lines")
def opRemoveEmptyLines(lines: list[str], transform: str):
    return [line for line in lines if line.strip()]


@operation('shuffle', 'randomize')
def opShuffle(lines: list[str], transform: str):
    seed = hash(transform)
    random.shuffle(lines, random.Random(seed).random)
    return lines


@operation("prefix")
def opPrefix(lines: list[str], transform: str):
    if len(lines) > 0:
        lines[0] = getParameterValue(transform) + lines[0]
    return lines


@operation("reverse")
def opReverse(lines: list[str], transform: str):
    lines.reverse()
    return lines;


@operation("suffix")
def opSuffix(lines: list[str], transform: str):
    if len(lines) > 0:
        lines[-1] = str(lines[-1]) + getParameterValue(transform)
    return lines


@operation("flatten")
def opFlatten(lines: list[str], transform):
    new_lines = []
    for line in lines:
        new_lines.extend(line.split('\n'))
    return new_lines


def getListFormat(stringInput):
    quoteUsed = '"'
    listUsed = '['
    listEndUsed = ']'
    if "'" in stringInput:
        quoteUsed = "'"
    elif '"' in stringInput:
        quoteUsed = '"'
    if '[' in stringInput or ']' in stringInput:
        listUsed = '['
        listEndUsed = "]"
    elif '(' in stringInput or ')' in stringInput:
        listUsed = '('
        listEndUsed = ')'
    elif '{' in stringInput or '}' in stringInput:
        listUsed = '{'
        listEndUsed = '}'
    return listEndUsed, listUsed, quoteUsed


def makeListLine(line, index, lines, listEndUsed, listUsed, quoteUsed):
    new_line = ""
    if index == 0:
        new_line += listUsed
    new_line += f'{quoteUsed}{line}{quoteUsed}'
    if index == len(lines) - 1:
        new_line += listEndUsed
    else:
        new_line += ','
    return new_line


@operation("list", 'toList')
def opList(lines: list[str], transform: str):
    listEndUsed, listUsed, quoteUsed = getListFormat(transform)

    new_line = []
    for index, line in enumerate(lines):
        new_line.append(makeListLine(line, index, lines, listEndUsed, listUsed, quoteUsed))
    return new_line


@operation('start')
def opStart(lines: list[str], transform: str):
    if len(lines) < 1:
        return lines

    startLine = eval_expression(transform, localVar={'line': lines[0]})
    lines[0] = startLine
    return lines


@operation('end')
def opEnd(lines: list[str], transform: str):
    if len(lines) < 1:
        return lines

    startLine = eval_expression(transform, localVar={'line': lines[-1]})
    lines[-1] = startLine
    return lines


@operation("replace")
def opReplace(lines: list[str], transform: str):
    toReplace, replacement = eval_expression(transform)
    return [re.sub(toReplace, replacement, line) for line in lines]


@operation("count")
def opCount(lines: list[str], transform):
    count = 0
    for index, line in enumerate(lines):
        matches = eval_expression(transform, localVar={'line': line, 'index': index})
        if matches:
            count += 1

    return [str(count)]


@suffixedOperation(["joined"])
def opJoined(lines: list[str], transform):
    joined = "\n".join(lines)
    output = eval_expression(transform, localVar={'joined': joined})
    return [str(output)]


@suffixedOperation(["resplit"])
def opResplit(lines: list[str], transform):
    joined = "\n".join(lines)
    output = eval_expression(transform, localVar={'joined': joined})
    if type(output) is not list:
        raise Exception('output of resplit has to be a list')
    return [str(line) for line in output]


@suffixedOperation(["reduce"])
def opReduce(lines: list[str], transform):
    previousLine = ""
    for index, line in enumerate(lines):
        previousLine = eval_expression(transform, localVar={'line': line, 'index': index, 'previousLine': previousLine})

    return [previousLine]


@suffixedOperation(["remap"])
def opRemap(lines: list[str], transform):
    output = eval_expression(transform, localVar={'lines': lines})
    if type(output) is not list:
        raise Exception('output of remap has to be a list')
    return [str(line) for line in output]


@suffixedOperation(["compound"])
def opCompound(lines: list[str], transform):
    output = eval_expression(transform, localVar={'lines': lines})

    return [str(output)]


@operation('unique')
def opUnique(lines: list[str], transform: str):
    uniqueLines = []
    for line in lines:
        if line not in uniqueLines:
            uniqueLines.append(line)

    return uniqueLines


@operation('sort')
def opSort(lines: list[str], transform: str):
    isReversed = 'reversed' not in transform
    key = len if 'length' in transform else str
    lines.sort(key=key, reverse=isReversed)
    return lines


@operation('context')
def opContext(lines: list[str], transform: str):
    return [eval_expression(line, localVar={'line': line, 'lines': lines.copy(), 'index': index}) for index, line in
            enumerate(lines)]


@operation('progressiveContext')
def opProgressiveContext(lines: list[str], transform: str):
    new_lines = []

    for index, line in enumerate(lines):
        temp_lines = [*new_lines[0: index], *lines[index:]]
        new_lines.append(eval_expression(line, localVar={'line': line, 'index': index, 'lines': temp_lines}))

    return new_lines


@operation('groupWithKey')
def opGroupWithKey(lines: list[str], transform: str):
    keys = dict()
    for index, line in enumerate(lines):
        val = eval_expression(line, localVar={'line': line, 'index': index})
        key = keys.get(eval_expression('line'), default=[line])
        if val not in keys:
            keys[val] = key
        else:
            key.append(line)

    return [''.join(lineWithKey) for lineWithKey in keys.values()]


@operation('groupUntil')
def opGroupUntil(lines: list[str], transform: str):
    grouped = ''
    new_lines = []
    for index, line in enumerate(lines):
        if eval_expression(transform, localVar={'line': line, 'index': index}) or index == len(lines) - 1:
            new_lines.append(grouped)
            grouped = line
        else:
            grouped += " " + line
    return new_lines


@operation('range')
def opRange(lines: list[str], transform: str):
    start, end = eval_expression(transform)

    start = getRangeValue(start)
    end = getRangeValue(end)
    if start > len(lines):
        start = len(lines)

    if end > len(lines):
        end = len(lines)

    return lines[start:end]


def getRangeValue(value):
    value = int(value) if value.isdigit() else value

    if value == 'start':
        return 0
    elif value == 'end':
        return -1
    elif type(value) is int:
        return value

    raise Exception("has to be an int or start and end")


@suffixedOperation(["transformWhere", 'tw'])
def opTransformWhere(lines: list[str], transform: str):
    condition, mapping = transform.split(';')
    mapping = mapping.strip()
    new_lines = []
    for index, line in enumerate(lines):
        new_line = line
        if eval_expression(condition, localVar={"line": line, 'index': index}):
            new_line = eval_expression(mapping, localVar={'line': line, 'index': index})
        new_lines.append(new_line)

    return new_lines


class Operations(Enum):
    @staticmethod
    def getOperation(rawLine: str):
        """
        returns the function which gets called onto the list and if the operation was found
        TODO list of name for the Operation
        :param rawLine:
        :return: lambda list[string]: list[string, boolean
        """
        for operator in OPERATIONS:
            for name in operator.name:
                if rawLine.startswith(name):
                    # print(operation.value.name, rawLine)
                    return operator.fixate(rawLine[len(name):].strip()), True

        return rawLine, False

    @staticmethod
    def getOperations(lines: list[str]):
        for line in lines:
            yield Operations.getOperation(line)

    @staticmethod
    def getOperationList():
        print(OPERATION_LIST)


if __name__ == '__main__':
    print(OPERATIONS)
    print(OPERATION_LIST)
