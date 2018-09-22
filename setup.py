from setuptools import setup

# TODO Write README
with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='evernote_dump',
    version='0.1',
    description='Short Description',
    license="MIT",
    long_description=long_description,
    author='Seth Van Roekel',
    url='https://www.github.com/exomut',
    packages=['evernote_dump'],
    install_requires=['html2text']
)
