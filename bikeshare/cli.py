import time

from pkg_resources import resource_stream
import click
import numpy as np
import pandas as pd
from .helpfunc import check_col, validate_months, validate_days


CITY_DATA = { 'Chicago': 'data/chicago.csv',
              'New York': 'data/new_york_city.csv',
              'Washington': 'data/washington.csv' }

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.
    pd.read_csv(city)

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    stream = resource_stream(__name__, CITY_DATA[city.title()])
    df = pd.read_csv(stream)

    # all column names having the first letter of each work capitalized 
    df.rename(str.title, axis=1)
    
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()


    # filter by month(s) if applicable
    if 0 not in month:
        # filter by month(s) to create the new dataframe
        df = df[df['month'].isin(month)]

    # filter by day of week if applicable
    if 0 not in day:
        days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        filters = [days[i-1] for i in day]
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'].str.lower().isin(filters)]
    
    return df



def show_data(df):
    """
    After filtering the data, prompt user if to display 5 lines of raw data each time,
    show the data if the answer is 'yes'; continue the prompt until the user says no.

    Args:
        (DataFrame) df - the filtered dataset available for user to view and explore
    Return:
        Null
    """
    # reset df index to start from 0
    df = df.reset_index()

    # use generator to get indices which are multiple of 5 and 
    # stops at the total number of df rows
    index_gen = (x for x in range(0, df.shape[0], 5))

    while True:
        try:
            i = next(index_gen)
            if i >=5:
                if click.confirm('Do you want to continue viewing data?') is False:
                    break
            click.echo(df[i:i+5])
        except StopIteration:
            break

        
def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    click.echo('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    if check_col(df, 'Start Time'):
        # TO DO: display the most common month
        click.echo(f"The most common month is:{df['month'].mode()[0]}")

        # TO DO: display the most common day of week
        click.echo(f"The most common day of week is:{df['day_of_week'].mode()[0]}")

        # TO DO: display the most common start hour
        click.echo(f"The most common start hour is:{df['Start Time'].dt.hour.mode()[0]}")

    click.echo(f"\nThis took {time.time() - start_time} seconds")
    click.echo('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    click.echo('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    if check_col(df, 'Start Station'):
        # TO DO: display most commonly used start station
        click.echo(f"The most commonly used start station:{df['Start Station'].mode()[0]}")

    if check_col(df, 'End Station'):
        # TO DO: display most commonly used end station
        click.echo(f"The most commonly used end station:{df['End Station'].mode()[0]}")

    # TO DO: display most frequent combination of start station and end station trip
    if check_col(df, 'Start Station') and check_col(df, 'End Station') :
        click.echo("The most frequent combination of start station and end station trip:{}".format((df['Start Station']+' | '+df['End Station']).mode()[0]))

    click.echo(f"\nThis took {time.time() - start_time} seconds")
    click.echo('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    click.echo('\nCalculating Trip Duration...\n')
    start_time = time.time()

    if check_col(df, 'Trip Duration'):
        # TO DO: display total travel time
        click.echo(f"Total travel time:{df['Trip Duration'].sum()}" )

        # TO DO: display mean travel time
        click.echo(f"The average travel time: {df['Trip Duration'].mean()}")

    click.echo(f"\nThis took {time.time() - start_time} seconds")
    click.echo('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    click.echo('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    if check_col(df, 'User Type'): 
        click.echo(f"{pd.DataFrame(df['User Type'].value_counts())}\n")

    # TO DO: Display counts of gender
    if check_col(df, 'Gender'):
        click.echo(f"{pd.DataFrame(df['Gender'].value_counts())}\n")

    # TO DO: Display earliest, most recent, and most common year of birth
    if check_col(df, 'Birth Year'):
        click.echo(f"The birth year of the oldest user is: {df['Birth Year'].min()}")
        click.echo(f"The birth year of the youngest user is: {df['Birth Year'].max()}")
        click.echo(f"The most common birth year of users is: {df['Birth Year'].mode()[0]}")
    

    click.echo(f"\nThis took {time.time() - start_time} seconds")
    click.echo('-'*40)


@click.command()
@click.argument('city', type=click.Choice(['chicago', 'new york', 'washington']))
@click.option('-month', '-m', type=click.INT,callback=validate_months, prompt=True,
             help="Enter 0 for all months, 1 for January and so on, maximum is 6 (up to June).")
@click.option('-day', '-d', type=click.INT, callback=validate_days, prompt=True,
             help="Enter 0 for all days of a week, 1 for Monday and so on, maximum is 7 (up to Sunday).")
@click.option('--show/--no-show', '--s/--no-s', default=True,
              help='Show data table, 5 lines each time, if flagged')
def main(city, month, day, show):
    """
    This script explore bikeshare data for a specific city.

    Usage: bikeshare [-md][--s] city
    """
    click.clear()
    click.echo('Hello! Let\'s explore some US bikeshare data!\n')

    while True:
        df = load_data(city, month, day)
        click.echo(f"{df.info()}\n")
        click.pause()

        if show:
            show_data(df)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break
