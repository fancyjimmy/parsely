from operators import *

op_metaData = [
    ("transformWhere", "(string) => (boolean, string)", "transforms if the returned boolean is true"),
    ("transform", "(string) => string", "transforms the string to a new string"),
    ("filter", "(string) => boolean", "and then exclude when not"),
    ("split", "(string) => list[string]", "flattens the string which gets split"),
    ("wrap", "(string) => string", "like transform, but with html wrap function"),
    ("joined", "(string) => string", "gets a long string joined at \n"),
    ("resplit", "(string) => list[string]", "gets the joined string and resplit to list"),
    ("list", "(list[string]) => list[string]", "transforms list"),
    ("reduce", "string) => string", "reduces to one line"),
    ("compound", "(list[string]) => string", "returns a single string from list"),
    ("context", "(list[string]) => string", "provides list with each line"),
    ("progressiveContext", "(number) => string", "but lines change with every iteration"),
    ("count", "unit => void", "reduces to one entry with the count of lines"),
    ("enumerate", "number => string", "puts number before string"),
    ("list", "unit => [', \"]", "returns every line as [\"hallo\", \"next\"]. parameter ' or \". default \""),
    ("prefix", "unit => string", "puts a string at the start"),
    ("suffix", "unit => string", "puts a string at the end"),
    ("end", "string => string", "only gets called for the last line"),
    ("start", "string => string", "only gets called for the first line"),
    ("shuffle", "unit", "randomizes order"),
    ("reverse", "unit", "reverses the list"),
    ("unique", "unit", "only unique lines"),
    ("strip", "unit", "removes spaces"),
    ("sort", "unit => ([\"alphabet\", \"length\"], [\"asc\", \"desc\"])", "just a sort"),
    ("replace", "unit => (\"toReplace\", \"replicant\")", "replace: unit => (\"toReplace\", \"replicant\")"),
    ("groupingByKey", "unit => key, string", "next call gets x lines as one"),
    ("groupUntil", "string => boolean", "until the boolean is set to true, the next operator gets them grouped"),
    ("range", "unit => ([ number, \"start\", \"end\"], [number, \"start\", \"end\"])", "limit lines to range")]

"""
missing

prefixAll
suffixAll
html
removeEmptyLines
flatten
remap
groupWithKey
"""

def checkIfAllFunctionsHaveBeenDocumented():
    undocumented = []
    for op in OPERATION_LIST:
        if op not in [line[0] for line in op_metaData]:
            undocumented.append(op)
    if len(undocumented) != 0:
        print(undocumented)
        # raise Exception("Make Descriptions for " + str(undocumented))

if __name__ == '__main__':
    checkIfAllFunctionsHaveBeenDocumented()

