from setuptools import setup


setup(
    name='networktools', 
    version='0.1',
    description='A set of tools for building/comparing networks (adjacency matrices) from events files, and node pairs files.',
    url='https://github.com/rahuezo/networktools',
    author='Rudy Huezo',
    author_email='rahuezo@ucdavis.edu',
    license='MIT',
    packages=['networktools.files', 'networktools.matrices', 'networktools.events'],
    zip_safe=False
)
