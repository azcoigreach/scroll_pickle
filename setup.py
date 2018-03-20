from setuptools import setup

setup(
    author="azcoigreach",
    author_email="azcoigreach@gmail.com",
    name = 'scroll_pickle',
    version = '0.1.0',
    py_modules = ['scroll_pickle'],
    install_requires = [
        'click',
        'colorama',
        'coloredlogs',
        'scrollphathd'
    ],
    entry_points = '''
        [console_scripts]
        wordcloud_maker=wordcloud_maker:main
    ''',
)