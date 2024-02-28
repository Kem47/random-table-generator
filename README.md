# Random Table Generator

This is a weekend project that aims to provide easy-to-create random tables for use in tabletop RPGs. The unique selling point here is that the user is able to create an "instruction" file with some key-words that provide this program instruction on how to randomly fill in the sheet using those instructions.

Here is an example from [TraumaTeamCallout.txt](TraumaTeamCallout.txt):

```
TRAUMA TEAM CALLOUT DETAILS:
Who? @person_generic
How many? #med
TT memberships: #vlo
Injury: @injury
Where? @location_generic
Threat: @threat %0.1.[AND @threat]
Threat still present? $.Yes.No
Modifier: @modifier
```
The @, $, % and # characters are used to provide the program instructions. See Instruction Strings section below.

## Prerequisites

You will need to install 2 libraries:

[pyparsing](https://pypi.org/project/pyparsing/)

[numpy](https://numpy.org)


## Run Instructions

```python
python RTG.py [INSTRUCTION FILE]
```

## Instruction Strings

### Number
\# number

can have 2 inputs separated by .
first input (must have): vlo/lo/med/hi/vhi - what kind of probability curve do you want to generate this number
second input (optional): max value you want it to have

### Table
@ other roll table

must be an exact name of the other file you are referring to (without .txt)

DO NOT use spaces in the names of files for tables.
keep the names of the tables simple
they must be in .txt file format

when using a table reference in a sentence make sure you separate any punctuation from the reference
DON'T: (2 @animal) OR should I bring in @threat?
DO: (2 @animal ) OR should I bring in @threat ?

This choice was either limit the characters that are allowed in the names of tables or maintain discipline while referencing.
This can be changed if overwhelming number of people want it to be the other way around.

When the program is pulling the lines from a table it assigns equal chance to each line. However it is possible to modify the chances for a line. It can either be increased with ^ or decreased with * :

\* lower the chance

leave it empty for the default increase of 0.5 times the equal chance or input your own value right after it. Make sure there is a space between this and the beginning of your actual line.


^ increase the chance

Leave it empty for default increase of 2 times the equal chance or input your own value right after it. Make sure there is a space between this and the beginning of your actual line.


### Option
% option

Chance of coming up with the next thing. If blank the default value is 0.5. If this is used within a larger sentence then enclose what you want to be chance occurence within ```[]```

Examples:

```%@corporation```

```%0.9@animal```

```%@person_generic comes in fight happens```

in the above example "comes in fight happens" will always appear. Do this instead:

```%[@person_generic comes in] fight happens```





### Boolean

$ boolean

Default at 0.5 or input your own success value. Can have 2 optional values - separated by ```.```
First value for success, second for the opposite.

