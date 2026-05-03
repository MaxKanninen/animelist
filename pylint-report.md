# Pylint report

Pylint produces the following report for the application:

```
************* Module app
app.py:1:0: C0114: Missing module docstring (missing-module-docstring)
app.py:16:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:21:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:25:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:30:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:34:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:34:0: R0911: Too many return statements (10/6) (too-many-return-statements)
app.py:79:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:95:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:100:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:100:0: R0911: Too many return statements (10/6) (too-many-return-statements)
app.py:156:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:172:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:187:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:187:0: R0911: Too many return statements (10/6) (too-many-return-statements)
app.py:252:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:267:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:305:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:318:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:327:0: C0116: Missing function or method docstring (missing-function-docstring)
************* Module config
config.py:1:0: C0114: Missing module docstring (missing-module-docstring)
config.py:1:0: C0103: Constant name "secret_key" doesn't conform to UPPER_CASE naming style (invalid-name)
************* Module db
db.py:1:0: C0114: Missing module docstring (missing-module-docstring)
db.py:4:0: C0116: Missing function or method docstring (missing-function-docstring)
db.py:10:0: C0116: Missing function or method docstring (missing-function-docstring)
db.py:19:0: C0116: Missing function or method docstring (missing-function-docstring)
db.py:22:0: C0116: Missing function or method docstring (missing-function-docstring)
************* Module seed
seed.py:1:0: C0114: Missing module docstring (missing-module-docstring)
************* Module series
series.py:1:0: C0114: Missing module docstring (missing-module-docstring)
series.py:3:0: C0116: Missing function or method docstring (missing-function-docstring)
series.py:8:0: C0116: Missing function or method docstring (missing-function-docstring)
series.py:14:0: C0116: Missing function or method docstring (missing-function-docstring)
series.py:21:0: C0116: Missing function or method docstring (missing-function-docstring)
series.py:29:0: C0116: Missing function or method docstring (missing-function-docstring)
series.py:35:0: C0116: Missing function or method docstring (missing-function-docstring)
series.py:42:0: C0116: Missing function or method docstring (missing-function-docstring)
series.py:46:0: C0116: Missing function or method docstring (missing-function-docstring)
series.py:55:0: C0116: Missing function or method docstring (missing-function-docstring)
series.py:62:0: C0116: Missing function or method docstring (missing-function-docstring)
series.py:68:0: C0116: Missing function or method docstring (missing-function-docstring)
series.py:72:0: C0116: Missing function or method docstring (missing-function-docstring)
series.py:77:0: C0116: Missing function or method docstring (missing-function-docstring)
series.py:84:0: C0116: Missing function or method docstring (missing-function-docstring)
series.py:90:0: C0116: Missing function or method docstring (missing-function-docstring)
series.py:94:0: C0116: Missing function or method docstring (missing-function-docstring)
************* Module users
users.py:1:0: C0114: Missing module docstring (missing-module-docstring)
users.py:4:0: C0116: Missing function or method docstring (missing-function-docstring)
users.py:12:0: C0116: Missing function or method docstring (missing-function-docstring)
users.py:17:0: C0116: Missing function or method docstring (missing-function-docstring)
users.py:22:0: C0116: Missing function or method docstring (missing-function-docstring)
users.py:32:0: C0116: Missing function or method docstring (missing-function-docstring)

------------------------------------------------------------------
Your code has been rated at 8.69/10 (previous run: 8.63/10, +0.05)
```

The remaining warnings are grouped by type below, with the reasoning for leaving them in place.

## Missing docstrings

Most of the report consists of warnings of this form:

```
app.py:1:0: C0114: Missing module docstring (missing-module-docstring)
app.py:16:0: C0116: Missing function or method docstring (missing-function-docstring)
```

The application does not use docstrings. The route handlers and the helper functions in `series.py` and `users.py` are short and named after what they do, so a docstring would only restate the function name. The same applies to `seed.py`, whose purpose is evident from its name and contents.

## Too many return statements

The report contains the following warnings about return statements:

```
app.py:34:0: R0911: Too many return statements (10/6) (too-many-return-statements)
app.py:100:0: R0911: Too many return statements (10/6) (too-many-return-statements)
app.py:187:0: R0911: Too many return statements (10/6) (too-many-return-statements)
```

These warnings concern the route handlers `registration`, `add_series`, and `edit_series`. Each handler validates several form fields (title, description, year, episodes, genres) and re-renders the form with a flash message when validation fails. For example, `add_series` looks like this:

```python
if not title:
    return error("No title entered")
if len(title) > 100:
    return error("Title too long (max 100 characters)")
if not description:
    return error("No description entered")
if len(description) > 5000:
    return error("Description too long (max 5000 characters)")
try:
    year = int(year)
except ValueError:
    return error("Invalid release year entered")
...
```

Each `return` reports one specific validation failure to the user. Collapsing them into fewer returns would either lose the per-field error message or push the validation rules into a list, which is harder to read for a handler this size.

## Constant name

The report contains the following warning about a variable name:

```
config.py:1:0: C0103: Constant name "secret_key" doesn't conform to UPPER_CASE naming style (invalid-name)
```

Pylint treats the module-level assignment in `config.py` as a constant and expects an upper-case name. The variable is used like this:

```python
app.secret_key = config.secret_key
```

The lower-case name matches Flask's own `app.secret_key` attribute, so it is kept as is.
