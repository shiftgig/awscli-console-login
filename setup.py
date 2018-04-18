from setuptools import setup, find_packages


def read_readme():
    """Attempt to read some README file"""
    try:
        import pypandoc
        long_description = pypandoc.convert_file('README.md', 'rst')
    except ImportError:
        long_description = open('README.md').read()
    return long_description


setup(
    name='awscli-console-login',
    version='0.1.0',
    url='https://github.com/shiftgig/awscli-console-login',
    author='Lamar Meigs, Jacob Dougherty, Shiftgig, Inc',
    author_email='lmeigs@shiftgig.com, jacob@shiftgig.com',
    description=(
        'An AWS CLI plugin to convert configured roles into active AWS '
        'Console sessions'
    ),
    long_description=read_readme(),
    packages=find_packages(exclude=['tests', 'tests.*']),
    install_requires=['awscli', 'requests'],
    zip_safe=True,
    test_suite='tests',
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Topic :: System :: Distributed Computing',
    ]
)
