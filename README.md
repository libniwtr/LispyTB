# LispyTB -- A "lisp" to Tinderbox Compiler
This is a TINY "Lisp" (maybe more Scheme) to Tinderbox action code compiler. Which generates Tinderbox action code from lispy style.
## Usage
```bash
python lispytb.py your-lispy-script.lisp
```
If there's syntax error in your-lispy-script.lisp, your script would be rejected.
## Keywords
You're not encouraged to use the keywords listed below as variable or attribute names in your code, because it would cause conflicts.

| Keyword | Stands for | Comments |
| --- | --- | --- |
| set! | = | set value for a variable or attribute  |
| eq | == |  |
| gt | > |  |
| lt | < |  |
| or | | |   |
| lor | |= |   |
| and | & |  |
| land | &= |  |
| neq | != | not eq |
| * | * |  |
| + | + |  |
| - | - |  |
| / | / |  |
| cond | conditional | similar to "if" but more powerful  |
| if | if |   |
| else | else | used in "cond" |
| let | var | creates local variable |
| . | . | chained dot. |
| $ |   | force dollar to a name |
| !$ |   | force (un)dollar to a name |
## Example
Here's an example that demonstrates how this "compiler" works.
The lisp-style code:
```lisp
(let ((myZ (+ "this is note " Name Text))
      (myX (* 1 2 3 (+ 3 4 5)))
      (myY (. "XX;YY;ZZ" (at 2))))
  (set! MyDate (max (list MyDateA, MyDateB)))
  (set! MyDate (. links outbound attended ($ MyDate)))
  (if (> ChildCount 5)
      (begin
       (set! Color "red")
       (set! Width 3.5))
    (set! Color "blue"))
  (cond ((eq Color "red")
         (set! Color2 "blue"))
        ((eq Color "blue")
         (set! Color2 "red"))
        (else
         (begin
          (set! Color2 "green")
          (set! Text "You are lucky!")))))```
Would compile to: (I manually indented them)
```php
var myZ("this is note "+$Name+$Text);
var myX(1*2*3*3+4+5);
var myY("XX;YY;ZZ".at(2));
$MyDate=max(list($MyDateA,,$MyDateB));$MyDate=$links.outbound.attended.$MyDate;
if(!$Text.contains("like")){
    $Color="red";$Width=3.5
} else {
    $Color="blue"
};
if($Color=="red")
{
    $Color2="blue"
} else {
    if($Color=="blue"){
        $Color2="red"
    } else {
        $Color2="green";
        $Text="You are lucky!"
    }
}
```
And that's true.

## Syntax

### let, dollar and undollar
There are attributes constants and variables in Tinderbox action script. LispyTB automatically generates dollars before  attributes if not intentionally undollared (see below), and will not generate dollars before variables (declared by var in tinderbox) or constants (strings and numbers) if not intentionally dollared (see below).

use let to declare variables.
Syntax:
```lisp
(let ((name1 expr1) (name2 expr2) ...)
    exprN
    exprN+1
    ...)
```
Example:
```lisp
(let ((foo "hello")
      (bar "world"))
  (set! Text foo)
  (set! foo bar))
```
compiles to :
```php
var foo("hello");
var bar("world");
$Text=foo;
foo=bar
```
As you see, we generate a dollar before *Text* but do not generate dollar before *foo*, *bar*, *"hello"* or *"world"*.
But you can intentionally *dollar* and *undollar* them:
```lisp
(let ((foo "hello")
      (bar "world"))
  (set! (!$ Text) foo)
  (set! ($ foo) bar))
```
compiles to:
```php
var foo("hello");
var bar("world");
Text=foo;
$foo=bar
```
We permit the use of "dollar" and "undollar" under the presumption that you are aware of what you are doing.
### unary operations
```
(op expr1) -> op expr1
```
for example:
```
(not MyString) -> !MyString
```
See the code for declaration of unary operations.
### binary operations
```
(op expr1 expr2) -> expr1 op expr2
```
for example:
```
(set! MyString "hello") -> MyString = "hello"
```
See the code for declaration of binary operations.

### arbitrary operations
```
(op expr1 expr2 expr3 ...) -> expr1 op expr2 op expr3 op ...
```
for example:
```
(* 1 2 3 4) -> 1*2*3*4
```
See the code for declaration of arbitrary operations.

### code block
use *begin* to begin a code block, which is, a block that contains one or more expressions.
for example:
```
(begin 
    (set! MyString "hello")
    (set! MyString "world")
    (set! MyString "again"))
```
### if and cond
use *if* if there's only one conditional, else you may use *cond*.

syntax:
```lisp
(if [CONDITION]
    [EXPR-THEN]
    [(optional)EXPR-ELSE]) 
(cond ([CONDITION1] [EXPR1])
      ([CONDITION2] [EXPR2])
      ([CONDITION3] [EXPR3])
      ([(optional) else] [EXPR-DEFAULT]))
```
where *CONDITION* and *EXPR* are single expression or code block.

example:
```lisp
(if (not MyString)
    (set! MyString "hello")
    (set! MyString "world"))
(cond ((eq Color "red") (set! Color2 "red"))
      ((eq Color "blue")(set! Color2 "blue"))
      (else (begin
                (set! Color2 "blue")
                (set! Color "red"))))
```
## Shortage
There's no warnings or error reports, and no future developments are planned.
## License 
Public domain.


