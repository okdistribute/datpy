from setuptools import setup

setup(
    name='datPython',
    version = '1.0',
    description='The Python API for dat',
    author='Portia Burton',
    author_email='plburton@gmail.com',
    package_dir = {'datPython': 'src'},
    packages = ['datPython', 'you.module'],
    test_suite = 'datPython.tests',
    use_2to3 = True,
    convert_2to3_doctests = ['README.txt'],
    use_2to3_fixers = ['your.fixers'],
    use_2to3_exclude_fixers = ['lib2to3.fixes.fix_import'],
)