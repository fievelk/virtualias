from setuptools import setup
from os import path

cur_dir = path.abspath(path.dirname(__file__))
print(cur_dir)

with open(path.join(cur_dir,'DESCRIPTION.txt'), 'r') as desc_file:
      long_description = desc_file.read()

setup(name = 'virtualias',
      version = '0.1',
      description = 'VirtuAlias, minimal virtualenv wrapper.',
      # long_description = """Wraps virtualenv command adding aliases for the environments. \
      # Similar to virtualenvwrapper, but without the WORKING_HOME variable.""",
      long_description = long_description,
      url = 'https://github.com/fievelk/virtualias',
      author = 'fievelk',
      author_email = '',
      license = 'MIT',
      packages = ['virtualias'],
      entry_points = {
          'console_scripts': ['virtualias = virtualias.virtualias:main']
      },
      classifiers = [
            'Intended Audience :: Developers',
            'Programming Language :: Python :: 3.4',
            'Programming Language :: Python :: 3.5',
            'Development Status :: 3 - Alpha'
            ],
      zip_safe=False)

