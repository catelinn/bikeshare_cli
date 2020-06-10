# `$ bikeshare`

`bikeshare` is a cli program that explores the bikeshare data of Chicago, New York and Washginton cities, which is provided in the embedded data files.

This program is designed for the complention of "Intro to Python" course project under Udacity Nano Degree for Python Programing. 


# Installation

Run this in Linux or MacOS terminal to clone the repo and install the package as CLI command.

`git clone https://github.com/catelinn/bikeshare_cli.git && cd bikeshare_cli && pip install .`



# Usage

- `bikeshare -h`
- `bikeshare filter -h`

### Example:

- View data of Chicago in January, February and March on Wednesday and Friday: 

    `bikeshare filter -c chicago -m 123 -d 35` 

- View data of New York of all months and all days:
   
   `bikeshare filter -c new\ york -m 0 -d 0`

- Enter OPTIONS to filter data in interactive mode: 

    `bikeshare filter`