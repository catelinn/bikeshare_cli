from setuptools import setup, find_packages

with open('requirements.txt') as f: 
    requirements = f.readlines()

setup(name='bikeshare',
      version='0.1',
      description='Exploratory data analysis on bikeshare data',
      long_description='',
      keywords='',
      url='',
      author='Catelinn Xiao',
      author_email='',
      license='',
      packages=['bikeshare'],
      install_requires=requirements,
      entry_points={
          'console_scripts': ['bikeshare=bikeshare.cli:main'], #command=package.module:function
      },
      include_package_data=True, # include non-code files in MANIFEST.in
      zip_safe=False)