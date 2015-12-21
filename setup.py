from setuptools import setup

setup(name = 'virtualias',
      version = '0.1',
      description = 'Wraps virtualenv command adding aliases for the environments. Similar to virtualenvwrapper, but without the WORKING_HOME variable.',
      url = 'https://github.com/fievelk/virtualias',
      author = 'fievelk',
      author_email = '',
      license = 'MIT',
      packages = ['virtualias'],
      entry_points = {
          'console_scripts': ['virtualias = virtualias.virtualias:main']
      },
      zip_safe=False)

