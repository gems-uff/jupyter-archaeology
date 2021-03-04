from setuptools import setup, find_packages

setup(
    name='juparc',
    version='1.0.0',
    url='https://github.com/gems-uff/jupyter-archaeology',
    author='Joao Felipe Pimentel',
    author_email='joaofelipenp@gmail.com',
    description='Jupyter analysis tools',
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "juparc = juparc:main"
        ]
    },
    install_requires=[
        'jupyter',
        'nbformat',
        'nbconvert',
        'mistune',
        'langdetect',
        'nltk',
    ],
)