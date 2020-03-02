# LOLCODE Specification 1.450

WORKING DRAFT Fall 2018

This is a working specification for LOLCODE version 1.450 and is based on the
original version 1.2 specification (a work of genius)
with elements from 2.0.  The changes include: static typing, 
add proper support for arrays and chars, and global scope.

It is only intended for use in MSU's CSE 450 
(Translation of Programming Languages).

---

## Formatting

### Whitespace

* Spaces are used to demarcate tokens in the language, although some keyword
  constructs may include spaces.

* Multiple spaces and tabs are treated as single spaces and are otherwise
  irrelevant.

* Indentation is irrelevant.

* A command starts at the beginning of a line and a newline indicates the end
  of a command, except in special cases.

* A newline will be Carriage Return (`/r`), a Line Feed (`/n`) or both (`/r/n`)
  depending on the implementing system. This is only in regards to LOLCODE 
  code itself, and does not indicate how these should be treated in strings or 
  files during execution.

* Multiple commands can be put on a single line if they are separated by a 
  comma (`,`). In this case, the comma acts as a virtual newline.

* Multiple lines can be combined into a single command by including three 
  periods (`...`) at the end of the line. This is called line continuation.
  This causes the contents of the next line to be evaluated as 
  if it were on the same line.

  * Lines with line continuation can be strung together, many in a row, to allow 
    a single command to stretch over more than one or two lines. As long as each 
    line is ended with three periods, the next line is included, until a line 
    without three periods is reached, at which point, the entire command may be 
    processed.

  * A line with line continuation may not be followed by an empty line.
    Three periods may be by themselves on a single line, in which case, the empty
    line is "included" in the command (doing nothing), and the next line is
    included as well.

* A single-line comment is always terminated by a newline. Line continuation 
  (`...`) and virtual newlines (`,`) after the comment (`BTW`) are ignored.

* Line continuation and soft-command-breaks are ignored inside quoted strings.
  An unterminated string literal (no closing quote) will cause an error.

### Comments

Single line comments are begun by `BTW`, and may occur either after a line of
code or on a separate line.

All of these are valid single line comments:

```
I HAS A VAR ITZ A NUMBAR AN ITZ 12          BTW VAR = 12

I HAS A VAR ITZ A NUMBAR AN ITZ 12
                BTW VAR = 12
```

Multi-line comments are begun by `OBTW` and ended with `TLDR`. 
They should be ignored. Do note that line continuation is needed
if the multi-line comment contains the newline needed 
to separate statements. Multi-line comments cannot nest 
(be used within other multi-line comments).

These are valid multi-line comments:

```
I HAS A VAR ITZ A NUMBAR AN ITZ 12
            OBTW this is a long comment block
                 see, i have more comments here
                 and here
            TLDR
I HAS A FISH ITZ A NUMBAR AN ITZ VAR
```

```
I HAS A VAR ITZ A NUMBR AN ITZ 12 OBTW this is a long comment block
      see, i have more comments here
      and here
TLDR 
I HAS A FISH ITZ A NUMBR AN ITZ VAR
```

### File Creation

All LOLCODE programs must be opened with the command `HAI`. `HAI` should then
be followed with the current LOLCODE language version number (1.450, in this
case). There is no current standard behavior for implementations to use the
version number, though.

A LOLCODE program is closed by the keyword `KTHXBYE`.
Note: the open and closing lines must exist on their own.

---

## Variables

### Scope

All variable have a scope local to the enclosing block in which it was declared 
(global if the variable was declared outside of any code block). Variables are only 
accessible after declaration.

### Naming

Variable identifiers may be in all lowercase or uppercase letters (or a mixture of the two). 
They must begin with a letter and may be followed only by other letters, numbers, and underscores. 
No spaces, dashes, or other symbols are allowed. 
Variable identifiers are CASE SENSITIVE – "cheezburger", "CheezBurger" and "CHEEZBURGER" 
would all be different variables.

### Declaration and Initialization

Variables must be declared prior to use.  Variable declarations take the form, 
`I HAS A <variable> ITZ A <type>`.  This maybe followed by `[AN] ITZ <value>` 
to provide initialization. Note, the square brackets around the `AN` indicate that its 
presence is optional. Variables must be assigned prior to their first use/read.
The following are examples of variable declarations.  
(Types are discussed more fully in the next section.)

```
I HAS A x ITZ A NUMBR
	BTW declares x as integer
I HAS A y ITZ A NUMBAR AN ITZ 5.6     
	BTW declares y as float with initial value of 5.6
```

The declared type of the variable is static and cannot be changed.

---

## Types

The intrinsic variable types are: booleans (TROOF), integers (NUMBR), floats
(NUMBAR), chars (LETTR), arrays (LOTZ), and strings (YARN).

Variables are statically typed and the type of a variable cannot change.  (An
exception to this is the implied `IT` variable used with
expression-statements.)
 
### Booleans

The two boolean (TROOF) values are WIN (true) and FAIL (false). 

### Numerical Types

A NUMBR is an integer (of unfixed width). Any
contiguous sequence of digits outside of a quoted YARN and not containing a
decimal point (`.`) is considered a NUMBR. A NUMBR may have a leading hyphen (`-`)
to signify a negative number.

A NUMBAR is a float (of fixed width, likely 64-bit). It is
represented as a contiguous string of digits containing exactly one decimal
point. (There need not be digits after the decimal point.) 
A NUMBAR may have a leading hyphen (`-`) to signify a
negative number.


### Chars

Char literals (LETTR) are demarked with single quotation marks (`'`).
For example, the char `a` is represented by `'a'`.

Within a char literal, all characters represent their literal value except the colon
(`:`), which is the escape character. Characters immediately following the colon
also take on a special meaning.

* `:)` represents a newline (`\n`)
* `:>` represents a tab (`\t`)
* `:'` represents a literal single quote (`'`)
* `::` represents a single literal colon (`:`)

So an apostrophe is represented as `':''`.


### Arrays

Arrays may be declared using the typing clause `ITZ LOTZ A
<type>S` and size allocation clause `AN THAR IZ <size>`. 
The type must be one of the previously described types.
Size musy be a NUMBR expression.

For example,

```
I HAS A x ITZ LOTZ A NUMBRS AN THAR IZ 500
I HAS A y ITZ LOTZ A NUMBARS AN THAR IZ n
```

Here x is declared as an array of 500 integers, and y is declared an array
of floats of size n.

Array elements are accessed with the `'Z` operator that takes the form
`<array>'Z <index>`.  Array indexing begins with 0 like a proper programming
language.  Assignment to elements of a array use `IN` and `PUT`. For example,

```
I HAS A x ITZ LOTZ A NUMBRS AN THAR IZ 20
IN x'Z 5 PUT 6         BTW assign array element 5 the value 6
IN x'Z n PUT y         BTW assign array element n the value y
VISIBLE x'Z 5          BTW prints of element 5 (the value 6)
```

Assignment between arrays makes a copy of the right hand-side.  For
example,

```
I HAS A x ITZ LOTZ A NUMBRS AN THAR IZ 20
I HAS A y ITZ LOTZ A NUMBRS AN THAR IZ 10
x R y      BTW assign all elements of y to x
```




### Strings

String literals (YARN) are demarked with double quotation marks (`"`). Line
continuation and virtual newlines are ignored inside quoted strings. String literals
must be terminated on the same line it was begun.

String literals use the same escaping as char literals, except that single quotes
don't require escaping, but double quotes do (with `:"`).

For example, `"Josh's ferret is named :"CrashDown:""` represents the string 
`Josh's ferret is named "CrashDown"`.

Strings are synoymous with arrays of LETTRs. 
```

I HAS A x ITZ LOTZ A LETTRS AN THAR IZ 3
IN x'Z 0 PUT 'a'
IN x'Z 1 PUT 'b'
IN x'Z 2 PUT 'c'
I HAS A y ITZ A YARN AN THAR IZ 99
y R x

BTW x and y have the same type and value
```


---

## Operators

### Calling Syntax and Precedence

Mathematical operators and functions in general rely on prefix notation. By
doing this, it is possible to call and compose operations with a minimum of
explicit grouping. When all operators and functions have known arity, no
grouping markers are necessary. In cases where operators have variable arity,
the operation is closed with `MKAY`. 

Calling unary operators then has the following syntax:

```
<operator> <expression1>
```

The `AN` keyword can optionally be used to separate arguments, 
so a binary operator expression has the following syntax:

```
<operator> <expression1> [AN] <expression2>
```

An expression containing an operator with infinite arity can then be expressed
with the following syntax:

```
<operator> <expr1> [[[AN] <expr2>] [AN] <expr3> ...] MKAY
```

Note: none of the operators change any of their arguments, there only effect is what they yield/return. 

### Math Operators

The basic math operators are unary or binary prefix operators.

```
SUM OF <x> [AN] <y>       BTW +
DIFF OF <x> [AN] <y>      BTW -
PRODUKT OF <x> [AN] <y>   BTW *
QUOSHUNT OF <x> [AN] <y>  BTW /
FLIP OF <x>               BTW 1/x
SQUAR OF <x>              BTW x*x
BIGGR OF <x> [AN] <y>     BTW max
SMALLR OF <x> [AN] <y>    BTW min
```

`<x>` and `<y>` may each be expressions in the above, so mathematical operators
can be nested and grouped indefinitely.

Math operators require that the types on all arguments have the same type and that
type must be numerical (NUMBR or NUMBAR). The expression yield the type of its
arguments.


### Logical Operators

Boolean operators working on TROOFs are as follows:

```
BOTH OF <x> [AN] <y>          BTW and: WIN iff x=WIN, y=WIN
EITHER OF <x> [AN] <y>        BTW or: FAIL iff x=FAIL, y=FAIL
WON OF <x> [AN] <y>           BTW xor: FAIL if x=y
NOT <x>                       BTW unary negation: WIN if x=FAIL
ALL OF <x> [AN] <y> ... MKAY  BTW variable arity AND
ANY OF <x> [AN] <y> ... MKAY  BTW variable arity OR
```

`<x>` and `<y>` in the expression syntax above must be TROOFs.

Short circuited evaluation applies, meaning that the operands are 
lazily evaluated as need to determine the result.

### Comparison Operators

Comparison is done with two binary equality operators:

```
SAEM <x> [AN] <y>   		        BTW WIN if x == y
DIFFRINT <x> [AN] <y>    		BTW WIN if x != y
FURSTSMALLR <x> [AN] <y>		BTW WIN if x < y
FURSTBIGGR  <x> [AN] <y>		BTW WIN if x > y
```

Comparison operators will always yield FAIL if the types of the two operands
do not have the same type. 

### Concatenation Operator ???

An indefinite number of YARNs (zero or more) may be explicitly concatenated with the
`SMOOSH...MKAY` operator. Arguments may optionally be separated with `AN`. As
the `SMOOSH` expects strings as its input arguments, it will implicitly cast
all input values of other types to YARNs.

### Array Operators

You can determine the length of an array at runtime using `LENGTHZ OF <array>` expression, which yields a NUMBR.
```
I HAS A x ITZ LOTZ A LETTRS AN THAR IZ 3
I HAS A y ITZ NUMBR AN ITZ LENGTHZ OF x
BTW y is 3.
```


### Casting ???

An expression's value may be explicitly cast with the binary `MAEK` operator.

```
MAEK <expression> [A] <type>
```

Where `<type>` is one of TROOF, NUMBR, NUMBAR, LETTR, YARN. This is only for
local casting: only the resultant value is cast, not the underlying
variable(s), if any.


#### Casting to TROOF
The an empty array (and empty string), 0, and 0.0 are all cast to FAIL. All other
values evaluate to WIN.

#### Casting to NUMBR
NUMBAR (floats) are truncated when cast to NUMR. 
No other casts to NUMBR are supported.

#### Casting to NUMBAR
NUMBR (ints) are cast to the appropriate NUMBAR. No other casts to NUMBR are supported.

#### Casting to LETTR
No casts to LETTR are supported.

#### Casting to YARN
`7` casts to `"7"`, `-56.40` casts to `"-56.4"`, `WIN` casts to `"WIN"`, `'a'` casts to `"a"`.

An array casts to a YARN where each element is converted to a YARN and 
concatenated (like the `SMASH` operator). So an array with elements, `7`, `-7`, and `4`, 
casts to `"7-74"`.

Note the enclosing double quotes are not part of the YARN, 
they are only used in the literal representation.



### Random Numbers

To generate an integer random number, the keyword
`WHATEVR` is evaluated as an expression. 
For example,

```
<var> R WHATEVR          BTW <var> is assigned a random integer 
```

---

## Input/Output

### Terminal-Based

The print (to STDOUT or the terminal) operator is `VISIBLE`. It has variable
arity and implicitly concatenates all of its arguments after casting them to
YARNs. 
It is terminated by the statement delimiter (line end or comma).
The output is automatically terminated with a carriage return (`:)`),
unless the final token is terminated with an exclamation point (`!`),
in which case the carriage return is suppressed.

```
VISIBLE <expression> [[AN] <expression> ...][!]
```

To accept a character of input from the user, the expression is

```
GIMMEH
```

which yields a LETTR from standard input.

---

## Assignment Expressions

Assignment of a variable is accomplished with an assignment expression,
`<variable> R <expression>`

```
I HAS A x ITZ A YARN            BTW declare x to be a string
x R "THREE"                     BTW x now equals "THREE"
I HAS A y ITZ A NUMBAR          BTW declare y to be a float
y R 3.14                        BTW y now equals 3.14
```

Additional assignment operators can be used to modify a variable, and take the
form,

```
<operator> <variable> [BY <expression>]
```

The following are examples of assignment operators: `UPPIN` and `NERFIN`.
These operators only work on NUMBRs.

```
UPPIN x          BTW increment x by 1
NERFIN x         BTW decrement x by 1
UPPIN x BY 6     BTW increment x by 6
NERFIN x BY y    BTW decrement x by y
```

Note, all assignments are expressions and yield their newly assigned value:

```
I HAS A x ITZ A NUMBR ITZ 4         BTW x is 4
I HAS A y ITZ A NUMBR ITZ UPPIN x   BTW x and y are 5
I HAS A z ITZ A NUMBR ITZ x R 10    BTW z and x are 10 (y is still 5)
```

---

## Flow Control

### Conditionals

#### If-Then

The traditional if/then construct is a very simple construct operating on the 
previous expression. In the base form, there are four keywords: 
`O RLY?`, `YA RLY`, `NO WAI`, and `OIC`.

`O RLY?` branches to the block begun with `YA RLY` if the expression is WIN, 
and branches to the optional `NO WAI` block if the expression is FAIL. 
The code block introduced with `YA RLY` is implicitly closed when `NO WAI` is reached. 
The `NO WAI` block is closed with `OIC`. The general form is then as follows:

```

O RLY? <expression>
  YA RLY
    <code block>
  NO WAI
    <code block>
OIC
```

while an example showing the ability to put multiple statements on a line 
separated by a comma (virtual newline) would be:

```
O RLY? SAEM ANIMAL AN "CAT"
  YA RLY, VISIBLE "J00 HAV A CAT"
  NO WAI, VISIBLE "J00 SUX"
OIC
```

The elseif construction adds a little bit of complexity. 
Optional `MEBBE <expression>` blocks may appear between the YA RLY and NO WAI blocks. 
If the `<expression>` following `MEBBE` is WIN, then that block is performed; 
if not, the block is skipped until the following `MEBBE`, `NO WAI`, or `OIC`. 
The full expression syntax is then as follows:

```
O RLY? <expression>
  YA RLY
    <code block>
 [MEBBE <expression>
    <code block>
 [MEBBE <expression>
    <code block>
  ...]]
 [NO WAI
    <code block>]
OIC
```

An example of this conditional is then:

```

O RLY? SAEM ANIMAL AN "CAT"
  YA RLY, VISIBLE "J00 HAV A CAT"
  MEBBE SAEM ANIMAL AN "MAUS"
    VISIBLE "NOM NOM NOM. I EATED IT."
OIC
```

#### Case


The LOLCODE keyword for switches is `WTF?`. The `WTF?` operates on the 
expression value for comparison. A comparison block is opened by `OMG` 
and must be a literal, not an expression. Each literal must be unique. 
The `OMG` block can be followed by any number of statements and may be 
terminated by a `GTFO`, which breaks to the end of the the `WTF` statement. 
If an `OMG` block is not terminated by a `GTFO`, then the next `OMG` 
block is executed as is the next until a `GTFO` or the end of the `WTF` 
block is reached. The optional default case, if none of the literals 
evaluate as true, is signified by `OMGWTF`.

As the expression and the literals are compared by equality, their types
must match.

```
WTF? <expression>
 [OMG <value literal>
    <code block> ...]
 [OMGWTF
    <code block>]
OIC
```

```
WTF? COLOR
  OMG "R"
    VISIBLE "RED FISH"
    GTFO
  OMG "Y"
    VISIBLE "YELLOW FISH"
  OMG "G"
  OMG "B"
    VISIBLE "FISH HAS A FLAVOR"
    GTFO
  OMGWTF
    VISIBLE "FISH IS TRANSPARENT"
OIC
```

In this example, the output results of evaluating the variable `COLOR` would be:

"R":

```
RED FISH
```

"Y":

```
YELLOW FISH
FISH HAS A FLAVOR
```

"G":

```
FISH HAS A FLAVOR
```

"B":

```
FISH HAS A FLAVOR
```

none of the above:

```
FISH IS TRANSPARENT
```

#### Loops

Simple loops are demarcated with the keyword `IM IN YR LOOP` and 
`IM OUTTA YR LOOP`. 
Loops defined this way are infinite loops that must be explicitly
exited with a GTFO break.  Below is an example of a simple loop.

```
IM IN YR LOOP
  <code-block>
  O RLY? <expression>
  YA RLY, GTFO
  OIC
NOW IM OUTTA YR LOOP
```

Conditional loops require the clause `TIL <expression>` or `WILE <expression>`
and take the form below,

```
IM IN YR LOOP [TIL|WILE <expression>]
  <code-block>
NOW IM OUTTA YR LOOP
```

Before the code-block is executed, the `TIL <expression>` evaluates the expression 
(which must yield a TROOF): if it evaluates as
FAIL, the code-block executes, if not, then loop execution stops, and
continues after the matching NOW IM OUTTA YR LOOP. The `WILE <expression>` is the
converse: if the expression is WIN, execution continues, otherwise the loop
exits.

Iteration loops include clauses for defining the iteration, and take the form,

```
IM IN YR LOOP <assignment-expression> TIL|WILE <conditional-expression>
  <code-block>
NOW IM OUTTA YR LOOP
```

Where `<assignment-expression>`  is UPPIN (increment) or NERFIN (decrement)
or any other assignment expression. This expression is evaluated after every 
code-block execution (but before the TIL/WILE expression).

As an example, the code below will count backwards from 20 to 10 by 2,
(10, 8, 6, 4)

```
I HAS A i ITZ A NUMBR AN ITZ 10
IM IN YR LOOP NERFIN i BY 2 WILE FURSTBIGGR i AN 10
  VISIBLE i
NOW IM OUTTA YR LOOP
```

---

## Functions

### Definition

A function is demarked with the opening keywords `HOW IZ I` and the closing
keywords `IF U SAY SO`. The syntax is as follows:

```
HOW IZ I <function name> [YR <argument1> <type-declaration> [[AN] YR <argument2> <type-declaration>  ...]] MKAY
  <code block>
IF U SAY SO <return type-declaration>
```

`<type-declaration>` can be either `ITZ A NUMBR/NUMBAR/LETTR/TROOF/YARN` or 
`ITZ LOTZ A NUMBRS/NUMBARS/LETTRS/TROOFS`

The number of arguments in a function can only be defined as a fixed
number. The `<argument>`s are single-word identifiers that act as variables
within the scope of the function's code. The calling parameters' values are
then the initial values for the variables within the function's code block when
the function is called.

Functions can only be defined at the file scope (not function declarations in 
other more nested scopes).

### Returning

Return from the function is accomplished in one of the following ways:

* `FOUND YR <expression>` returns the value of the expression.

The return type of the function is automatically determined by the type of
the expression returned.

### Calling

A function of given arity is called with:

```
I IZ <function name> [YR <expression1> [[AN] YR <expression2> [[AN] YR <expression3> ...]]] MKAY
```

That is, an expression is formed by the function name followed by any
arguments. Those arguments may themselves be expressions. The expressions'
values are obtained before the function is called. The arity of the functions
is determined in the definition.

### Function Example
```
HAI 1.450

OBTW
The sum_of_array function takes an array of NUMBRS and a start_value (NUMBR)and
returns the sum of all the values of the array and the start_value as a NUMBR
TLDR
HOW IZ I sum_of_array YR array ITZ LOTZ A NUMBRS AN YR start_value ITZ A NUMBR MKAY
    I HAS A tally ITZ A NUMBR AN ITZ start_value
    I HAS A index ITZ A NUMBR AN ITZ 0
    IM IN YR LOOP UPPIN index TIL NOT FURSTBIGGR LENGTHZ OF array AN index
	tally R SUM OF tally AN array'Z index
    NOW IM OUTTA YR LOOP
    FOUND YR tally
IF U SAY SO ITZ A NUMBR

BTW The array is [1,10,100,1000]
I HAS A my_array ITZ LOTZ A NUMBRS AN THAR IZ 4
IN my_array'Z 0 PUT 1
IN my_array'Z 1 PUT 10
IN my_array'Z 2 PUT 100
IN my_array'Z 3 PUT 1000

I HAS A result ITZ A NUMBR
result R I IZ sum_of_array YR my_array AN YR 5 MKAY

BTW result should be 5 + 1 + 10 + 100 + 1000 = 1116
VISIBLE result
KTHXBYE
```
