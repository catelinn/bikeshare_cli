from pkg_resources import resource_stream

import click
import numpy as np
import pandas as pd

from .helpfunc import validate_days, validate_months, show_data, station_stats,\
    trip_duration_stats, time_stats, user_stats, restart_program

CITY_DATA = { 'Chicago': 'data/chicago.csv',
              'New York': 'data/new_york_city.csv',
              'Washington': 'data/washington.csv' }

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

class Config:
    def __init__(self):
        self.city=''


pass_config = click.make_pass_decorator(Config, ensure=True)

@click.group(context_settings=CONTEXT_SETTINGS)
@click.argument('city', type=click.Choice(['chicago', 'new york', 'washington']))
@pass_config
def main(config, city):
    """
    Usage: 
    bikeshare city filter -m 23 -d 67 --s summary -time -station -trip -user

    This script explore bikeshare data for a specific city.
    """
    click.clear()
    click.echo(f'Hello! Let\'s explore some US bikeshare data for {city}!\n')
    config.city = city
    
    
@main.command('filter')
@click.option('-month', '-m', type=click.INT,callback=validate_months, prompt=True,
             help="Enter 0 for all months, 1 for January and so on, maximum is 6 (up to June).")
@click.option('-day', '-d', type=click.INT, callback=validate_days, prompt=True,
             help="Enter 0 for all days of a week, 1 for Monday and so on, maximum is 7 (up to Sunday).")
@click.option('--show', '--s', default=True, is_flag=True,
              help='Show data table, 5 lines each time, if flagged')
@click.option('--line', '--l', type=click.INT, default=5, help="Number of lines of data to show")
@pass_config
def filter(config, month, day, show, line):
    """
    Filter city data by month and day.
    """
    stream = resource_stream(__name__, CITY_DATA[config.city.title()])
    df = pd.read_csv(stream)

    # all column names having the first letter of each work capitalized 
    df.rename(str.title, axis=1)

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    df_copy = df.copy()

    # filter by month(s) 
    if 0 not in month:
        # filter by month(s) to create the new dataframe
        df_copy = df_copy[df_copy['month'].isin(month)]

    # filter by day of week
    if 0 not in day:
        days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        filters = [days[i-1] for i in day]
        # filter by day of week to create the new dataframe
        df_copy = df_copy[df_copy['day_of_week'].str.lower().isin(filters)]
    
    # Show dataframe information
    click.echo(f"{df_copy.info()}\n")

    # Show data (default True and Line number as 10)
    if show:
        show_data(df_copy, line)


    # Show stats
    time_stats(df_copy)
    station_stats(df_copy)
    trip_duration_stats(df_copy)
    user_stats(df_copy)

    if click.confirm(f"Restart to select different month(s) or day(s) for {config.city.title()}?") is not False:
        restart_program()
        
