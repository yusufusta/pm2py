from setuptools import setup
import sys

required = ["sh"]
long_description = ""
with open('README.md') as f:
    long_description += f.read()

setup(
    name='pm2py',
    version='1.0.1',
    description='PM2 wrapper for Python',
    long_description=long_description,
    author='Yusuf Usta',
    author_email='yusuf@usta.email',
    maintainer='Yusuf Usta',
    maintainer_email='yusuf@usta.email',
    url='https://github.com/yusufusta/pm2py',
    license='GPL3',
    packages=['pm2py'],
    install_requires=required,
    keywords=['pm2', "node"],
    long_description_content_type="text/markdown",
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10'
    ],
)
