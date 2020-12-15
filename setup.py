from setuptools import setup

setup(
    name="quizScattererDoc2Vec",
    version='1.0',
    description='doc2vecとクラスタリングでクイズの出題順を最適化したい',
    author='Miyax',
    url='https://github.com/miyax0227/quizScattererDoc2Vec',
    install_requires=open('requirements.txt').read().splitlines(),
)