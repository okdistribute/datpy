from distutils.core import setup

setup(
    name='datpy',
    version='1.0.0',
    py_modules=['datpy'],
    description='Python dough for making Dat-flavored pies',
    author='Karissa McKelvey',
    author_email='krmckelv@gmail.com',
    url='http://dat-data.com',
    download_url='https://github.com/karissa/datpy/tarball/0.7.0',
    keywords=['dat', 'python', 'analytics', 'data', 'data science', 'data sharing'],
    classifiers=(
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7'
    ),
    test_suite="test.py"
)
