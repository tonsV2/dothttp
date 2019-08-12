from setuptools import setup

setup(
    name='dothttp',
    version='1.2.0',
    description='See https://github.com/tonsV2/dothttp',
    python_requires='>=3',
    py_modules=['dothttp'],
    install_requires=[
        'click',
        'pygments',
        'termcolor'
    ],
    entry_points='''
        [console_scripts]
        dothttp=dothttp:cli
    '''
)
