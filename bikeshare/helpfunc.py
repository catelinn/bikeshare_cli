import time
import click
import numpy as np
import pandas as pd

import sys
import os


def restart_program():
    """Restarts the current program.
    Note: this function does not return. Any cleanup action (like
    saving data) must be done before calling this function."""
    python = sys.executable
    os.execl(python, python, * sys.argv)


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
        return result

def validate_months(ctx, value):
    valid = [0,1,2,3,4,5,6]
    errmsg ='month can only be from 0 to 6 (0 as for all months available)'
    return validate_intval(ctx, value, valid, errmsg)

def validate_days(ctx, value):
    # 012 only returns [1,2] only
    valid = [0,1,2,3,4,5,6,7]
    errmsg = 'day can only be from 0 to 7 (0 as for all days available)'
    return validate_intval(ctx, value, valid, errmsg)


def show_data(df, line_num):
    """
    After filtering the data, prompt user if to display 5 lines of raw data each time,
    show the data if the answer is 'yes'; continue the prompt until the user says no.
    """
    # reset df index to start from 0
    df = df.reset_index()

    # use generator to get indices which are multiple of 5 and 
    # stops at the total number of df rows
    index_gen = (x for x in range(0, df.shape[0], line_num))

    while True:
        try:
            i = next(index_gen)
            if i >=line_num:
                if click.confirm('Do you want to continue viewing data?') is False:
                    break
            click.echo(df[i:i+line_num])
        except StopIteration:
            break


def check_col(df, col_name):
    if col_name in df.columns:
        return True
    else:
        click.echo("No data on {} for this city. ".format(col_name))
        return False


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
