import pandas as pd
import numpy as np
import click


def validate_intval(ctx, value, valid, errmsg):
    """
    Validate months/days option integer value
    """
    try:
        value = list(set(str(value)))
        result = [int(x) for x in value if x in list(map(str, valid))]
        click.echo(f"You have entered {value}, accepted value(s) are {result}\n")
    except ValueError:
            raise click.BadParameter(errmsg)
    finally:
        if len(result)==0:
            raise click.BadParameter(errmsg)
        click.pause() # wait for user press key to continue here
        return result

def validate_months(ctx, value):
    valid = [0,1,2,3,4,5,6]
    errmsg ='month can only be from 0 to 6 (0 as for all months available)'
    return validate_intval(ctx, value, valid, errmsg)

def validate_days(ctx, value):
    valid = [0,1,2,3,4,5,6,7]
    errmsg = 'day can only be from 0 to 7 (0 as for all days available)'
    return validate_intval(ctx, value, valid, errmsg)


def check_col(df, col_name):
    if col_name in df.columns:
        return True
    else:
        click.echo("No data on {} for this city. ".format(col_name))
        return False