import ast  # ast is used to evaluate string values into python objects according to their actual type
import pandas as pd  # pandas is used for being able to detect different kinds of datetime formats


# Convert the value into the appropriate data type
def evaluate(value):
    # evaluate booleans
    if value.lower() == "true" or value.lower() == "yes":
        value = "True"
    elif value.lower() == "false" or value.lower() == "no":
        value = "False"

    try:
        # evaluate datetimes
        value = pd.to_datetime(value)
    except:
        try:
            # evaluate other non-string types
            value = ast.literal_eval(value)
        except:
            return value

    return value
