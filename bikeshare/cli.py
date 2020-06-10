import click
import numpy as np
import pandas as pd

from .helpfunc import validate_city, validate_days, validate_months, show_data, station_stats,\
    trip_duration_stats, time_stats, user_stats, stream_to_df, CITY_DATA, TEXT

import sys


CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

@click.group(context_settings=CONTEXT_SETTINGS)
@click.pass_context
def main(ctx):
    """
    This program explores the bikeshare data for Chicago, New York and Washington.
    """
    #ctx.ensure_object(dict)
 

@main.command('filter')
@click.option('-city', '-c', callback=validate_city, prompt=TEXT['prompt']['city'], help=TEXT['help']['city'])
@click.option('-month', '-m', callback=validate_months, prompt=TEXT['prompt']['month'],help=TEXT['help']['month'])
@click.option('-day_of_week', '-d', callback=validate_days, prompt=TEXT['prompt']['day_of_week'],help=TEXT['help']['day_of_week'])
@click.option('--show', '--s', default=False, is_flag=True, prompt=TEXT['prompt']['show'],help=TEXT['help']['show'])
@click.option('--line', '--l', type=click.INT, default=5, prompt=TEXT['prompt']['line'], help=TEXT['help']['line'])
@click.pass_context
def filter(ctx, city, month, day_of_week, show, line):
    """
    Filter city data by month, day of week; Show data (optional) and summary statistics. 
    """
    
    if city is None:
        city = validate_city(ctx, click.prompt(TEXT['prompt']['city']))
        month = validate_months(ctx, click.prompt(TEXT['prompt']['month']))
        day_of_week = validate_days(ctx, click.prompt(TEXT['prompt']['day_of_week']))
        show = click.prompt(TEXT['prompt']['show'], default=False, type=click.BOOL)
        line = click.prompt(TEXT['prompt']['line'], default=5, type=click.INT)
        

    df = stream_to_df(CITY_DATA[city])
    
    
    # all column names having the first letter of each work capitalized
    df.rename(str.title, axis=1)

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    df_copy = df.copy()

    # filter by month(s) 
    if '0' not in month:
        # filter by month(s) to create the new dataframe
        df_copy = df_copy[df_copy['month'].isin(list(map(int, month)))]

    # filter by day of week
    if '0' not in day_of_week:
        days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        day_of_week = list(map(int, day_of_week))
        filters = [days[i-1] for i in day_of_week]
        # filter by day of week to create the new dataframe
        df_copy = df_copy[df_copy['day_of_week'].str.lower().isin(filters)]
    
    # Show dataframe information
    click.echo(f"\n{df_copy.info()}\n")

    # Show data (default True and Line number as 10)
    if show:
        show_data(df_copy, line)


    # Show stats
    time_stats(df_copy)
    station_stats(df_copy)
    trip_duration_stats(df_copy)
    user_stats(df_copy)

    # Restart upon user confirmation
    if click.confirm('Restart to explore new dataset?'):
        sys.argv.clear()
        ctx.invoke(filter)


        
        
        
