from setuptools import setup

setup(
    name='judgment_aggregation',
    version='0.1',
    description='A package for judgment aggregation',
    url='https://github.com/jeroenstalenburg/judgment-aggregation',
    author='Jeroen Stalenburg',
    author_email='jeroenstalenburg@gmail.com',
    license='Apache',
    packages=['judgment_aggregation'],
    install_requires=[],
    zip_safe=False,
    test_suite='nose.collector',
    tests_require=['nose'],
)
