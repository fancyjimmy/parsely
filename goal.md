## TODO

### Functions

parameter as a local variable
line -> input
index -> input
- transform: (string) => string; transforms the string to a new string
- filter: (string) => boolean; and then exclude when not 
- split: (string) => list[string]; flattens the string which gets split
- wrap: (string) => string; like transform, but with html wrap function

### Functions-TODO

- joined: (string) => string; gets a long string joined at \n
- resplit: (string) => list[string]; gets the joined string and resplit to list
- list: (list[string]) => list[string]; transforms list
- reduce (prev: string, current: string) => string; reduces
- compound: (list[string]) => string; returns a single string from list
- emmet: (string) => string; ? as the line
- context: (current: string, lines: list[string], index: number) => string;  
- progressiveContext: (current: string, lines: list[string], index: number) => string; but lines change with every iteration
- sort: (this: string, other: string) => number;

### Quick-Function

- count: unit => void; reduces to one entry with the count of lines
- enumerate: number => string;  puts number before string
- toList unit => [', "]; returns every line as ["hallo", "next"]. parameter ' or ". default "
- prefix: unit => string; puts a string at the start
- suffix: unit => string; puts a string at the end
- end: string => string; only gets called for the last line
- start: string => string; only gets called for the first line
- shuffle: unit; randomizes order
- reverse: unit; reverses the list
- unique: unit; only unique lines
- perLine: unit; one by one line
- strip: unit; removes spaces
  - lstrip
  - rstrip
- xmlParse
- mark: string => string; mark for every string 
  - countSpaces: unit; mark with the amount of spaces
- sortBy: unit => (["alphabet", "length"], ["asc", "desc"]); just a sort
- replace: unit => ("toReplace", "replicant")
- replaceWhere: string => (boolean, "replicant")
- groupingSegments: unit => number; next call gets x lines as one
- groupingBy: string => (string, ["counting", "list"]); counting returns name:0
- groupUntil: string => boolean; until the boolean is set to true, the next operator gets them grouped
- range: unit => ([ number, "start", "end"], [number, "start", "end"], number)
### Table Mode

extra mode for tables and extra mode where you actually work with a dict

### TODO

- copy to clipboard button
- save script function
- load file function
- load from Image function
- save output function
- load and save setup
- Exception Messages
- making custom loadable scripts 
- clear setup
- use str after eval
- implementing Regex
- implementing general purpose emmet
- Multiline snippets
- abbreviated names
- settings activation
- appdata folder
- change app name and icon

### Session 1 TODO 23/10/2022

- ~~copy to clipboard button~~
- ~~load file function~~
- ~~save output function~~
- ~~save script function~~
- ~~Exception Messages~~
- load from Image function
- ~~load and save setup~~
- ~~making custom loadable scripts~~ 
- clear setup
- use str after eval
- implementing Regex
- implementing general purpose emmet
- Multiline snippets
- abbreviated names
- settings activation
- appdata folder
- change app name and icon

### New TODO
- load from Image function
- clear setup
- use str after eval
- implementing Regex
- implementing general purpose emmet
- Multiline snippets
- abbreviated names
- settings activation
- appdata folder
- change app name and icon

### Functions
- **New TODO**
- Functions
- **joined**:  (string) => string
   - gets a long string joined at \n
- **resplit**:  (string) => list[string]
   - gets the joined string and resplit to list
- **list**:  (list[string]) => list[string]
   - transforms list
- **reduce**:  string) => string
   - reduces
- **compound**:  (list[string]) => string
   - returns a single string from list
- **emmet**:  (string) => string
   - ? as the line
- **context**:  number) => string
- **progressiveContext**:  number) => string
   - but lines change with every iteration
- **sort**:  string) => number
- **count**:  unit => void
   - reduces to one entry with the count of lines
- **enumerate**:  number => string
   -  puts number before string
- **toList**:  unit => [', "]
   - returns every line as ["hallo", "next"]. parameter ' or ". default "
- **prefix**:  unit => string
   - puts a string at the start
- **suffix**:  unit => string
   - puts a string at the end
- **end**:  string => string
   - only gets called for the last line
- **start**:  string => string
   - only gets called for the first line
- **shuffle**:  unit
   - randomizes order
- **reverse**:  unit
   - reverses the list
- **unique**:  unit
   - only unique lines
- **perLine**:  unit
   - one by one line
- **strip**:  unit
   - removes spaces
- **sortBy**:  unit => (["alphabet", "length"], ["asc", "desc"])
   - just a sort
- **replace**:  unit => ("toReplace", "replicant")
   -replace: unit => ("toReplace", "replicant")
- **replaceWhere**:  string => (boolean, "replicant")
   -replaceWhere: string => (boolean, "replicant")
- **groupingSegments**:  unit => number
   - next call gets x lines as one
- **groupingBy**:  string => (string, ["counting", "list"])
   - counting returns name:0
- **groupUntil**:  string => boolean
   - until the boolean is set to true, the next operator gets them grouped
- **range**:  unit => ([ number, "start", "end"], [number, "start", "end"], number)

### Session 2 TODO (23:17)

- ### New TODO
- load from Image function
- clear setup
- use str after eval
- ~~implementing Regex~~
- implementing general purpose emmet
- Multiline snippets
- ~~abbreviated names~~
- settings activation
- appdata folder
- **compunded statements**
- ~~change app name and icon~~
- ### Functions
- ~~**joined**:  (string) => string~~
   - gets a long string joined at \n
- ~~**resplit**:  (string) => list[string]~~
   - gets the joined string and resplit to list
- **list**:  (list[string]) => list[string]
   - transforms list
- ~~**reduce**:  string) => string~~
   - reduces
- ~~**compound**:  (list[string]) => string~~
   - returns a single string from list
- **emmet**:  (string) => string
   - ? as the line
- **context**:  (number) => string
- **progressiveContext**:  (number) => string
   - but lines change with every iteration
- **sort**:  string) => number
- ~~**count**:  unit => void~~
   - reduces to one entry with the count of lines
- ~~**enumerate**:  number => string~~
   -  puts number before string
- ~~**toList**:  unit => [', "]~~
   - returns every line as ["hallo", "next"]. parameter ' or ". default "
- ~~**prefix**:  unit => string~~
   - puts a string at the start
- ~~**suffix**:  unit => string~~
   - puts a string at the end
- ~~**end**:  string => string~~
   - only gets called for the last line
- ~~**start**:  string => string~~
   - only gets called for the first line
- ~~**shuffle**:  unit~~
   - randomizes order
- ~~**reverse**:  unit~~
   - reverses the list
- **unique**:  unit
   - only unique lines
- **perLine**:  unit
   - one by one line
- ~~**strip**:  unit~~
   - removes spaces
- **sortBy**:  unit => (["alphabet", "length"], ["asc", "desc"])
   - just a sort
- ~~**replace**:  unit => ("toReplace", "replicant")~~
   -replace: unit => ("toReplace", "replicant")
- **replaceWhere**:  string => (boolean, "replicant")
   -replaceWhere: string => (boolean, "replicant")
- **groupingSegments**:  unit => number
   - next call gets x lines as one
- **groupingBy**:  string => (string, ["counting", "list"])
   - counting returns name:0
- **groupUntil**:  string => boolean
   - until the boolean is set to true, the next operator gets them grouped
- **range**:  unit => ([ number, "start", "end"], [number, "start", "end"], number)

### Session 3 TODO(24/10/2022 17:54 - 20:19)
- ### New TODO
- load from Image function
- clear setup
- load setup
- use str after eval
- implementing general purpose emmet
- Multiline snippets
- settings activation
- appdata folder
- saving compounded statements
- **make Dynamic documentation for uses** 
  - new
- **Better Exceptions with Line wrong and Reason**
  - new
- **Styling tkinter**
  - new
- ### Functions
- ~~**list**:  (list[string]) => list[string]~~
- **emmet**:  (string) => string
- ~~**context**:  (number) => string~~
- ~~**progressiveContext**:  (number) => string~~
- ~~**sort**:  string) => number~~
- ~~**unique**:  unit~~
- ~~**sortBy**:  unit => (["alphabet", "length"], ["asc", "desc"])~~
- **groupingSegments**:  unit => number
- ~~**groupWhere**: unit => number~~
- **groupingBy**:  string => (string, ["counting", "list"])
- ~~**groupUntil**:  string => boolean~~
- ~~**range**:  unit => ([ number, "start", "end"], [number, "start", "end"], number)~~

- ~~**replaceWhere**:  string => (boolean, "replicant")~~, replace already enough
_ ~~- **perLine**:  unit~~_ removed, I don't know what it means
