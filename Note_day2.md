# Note day2

## set up

```md
cd .\day2\Day2-FunctionsAndProjectOrganization\

# create cell code
> # %%

# use pixi install
pixi add ipykernal
# use (activated) python install
python -m ipykernel install --user
```

##  write a function

1. function composition
   1. create a function `def aa()`
2. how to use function
   1. import from a seperate file `from utils import aa`
3. git commit for every successful code

command line 
1. [Using as a command line tool](https://nbconvert.readthedocs.io/en/latest/usage.html)
2. [paper mill](https://github.com/nteract/papermill)

shortcut:
1. rename vriables:
   1. select variable, use `F2`, enter the replace name. VScode will replace variables within the small scopes with `F2`.

## Suggestions
1. ai assistant coding will benefit from
   1. clear definition 

```python
import pandas as pd
def make_path(psth: pd.DataFrame) -> pd.DataFrame :
```

## weird example and potential bugs
scopeing rule:
- we should not define the variable name inside functions that have been used outside
- used function should not be without undefined function `np` 
  - usually include `import numpy ad np` inside, but using modual is better
- it is not recommended to use repeat variables

```py
def fun():
    return x

x = 10
fun()
```

## module

```text
├── scripts/
|   └── calculate_psths.py
|
├── src/
|   ├── project_name/
|   |   ├── __init__.py
|   |   └── utils.py
|   |
|   └── <module>.py
```




`__init__.py` is essential to identify the package, which is usually put `src/package-name`.

```bash

pixi
install -e
```

pip install the library from local


pip will install packages into `envs/default/lib/site-packages` of a given conda env

