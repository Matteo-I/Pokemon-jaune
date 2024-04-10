from setuptools import setup

setup(
    name='Pokemon_Jaune',
    version='1',
    description='Une reproduction du jeu pokemon jaune avec python',
    author='Matteo Imbert',

    install_requires=[
        "sqlalchemy",
        "pandas",
        "requests"
        ],
    zip_safe=False,
)
