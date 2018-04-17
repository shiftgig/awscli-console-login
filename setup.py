from setuptools import setup, find_packages


def read_readme():
    """Attempt to read some README file"""
    try:
        return open('README.rst').read()
    except IOError:
        return open('README.md').read()


setup(
    name='awscli-console-login',
    version='0.0.1',
    # url='',
    author='Lamar Meigs, Jacob Dougherty, Shiftgig, Inc',
    author_email='lmeigs@shiftgig.com, jacob@shiftgig.com',
    description='An aws-cli plugin to login to an account via the browser',
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
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: System :: Distributed Computing',
    ]
)
