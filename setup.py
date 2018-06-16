from setuptools import setup, find_packages

from kees import __version__

#from pipenv.project import Project
#from pipenv.utils import convert_deps_to_pip
#
#pfile = Project(chdir=False).parsed_pipfile
#requirements = convert_deps_to_pip(pfile['packages'], r=False)
#test_requirements = convert_deps_to_pip(pfile['dev-packages'], r=False)

setup(
    name="kees",
    version=__version__,
    url="https://github.com/jmsdnns/kees",
    description="CLI for reading 1Password vaults",
    author="Jms Dnns",
    author_email="jdennis@gmail.com",

    packages=find_packages(),

    install_requires=[
        "M2Crypto",
        "fuzzywuzzy",
        "python-Levenshtein",
    ],

    entry_points={'console_scripts': [
        'kees = kees.commands:run_it',
    ]},
    scripts=['kees.sh'],
)
