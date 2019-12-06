import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.rst')) as f:
    README = f.read()

requires = [
]

dev_requires = [
    'nose',
    'bumpversion',
]

setup(name='fluent-http-apigen',
      version='0.1.0',
      description="App generate HTTP documentation from fluent-http code",
      long_description=README,
      classifiers=[
          "Programming Language :: Python",
      ],
      keywords='icij, fluent-http, documentation',
      author='Sabrina Sahli, Bruno Thomas',
      author_email='sahli.sabrina@gmail.com, bthomas@icij.org',
      url='https://github.com/ICIJ/fluent-http-apigen',
      license='LICENSE.txt',
      packages=find_packages(exclude=("*.tests", "*.tests.*", "tests.*", "tests", "*.test_utils")),
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      extras_require={
        'dev': dev_requires,
      },
      test_suite="nose.collector",
      entry_points={
        'console_scripts': [
            'apigen = apigen:main',
        ],
      }
      )
