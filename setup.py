"""The setup script for installing the package."""
from setuptools import setup, find_packages


# read the contents of the README
with open('README.md') as README_md:
    README = README_md.read()


setup(
    name='gym_super_mario_bros',
    version='7.4.0',
    description='Super Mario Bros. for OpenAI Gym',
    long_description=README,
    long_description_content_type='text/markdown',
    keywords=' '.join([
        'OpenAI-Gym',
        'NES',
        'Super-Mario-Bros',
        'Lost-Levels',
        'Reinforcement-Learning-Environment',
    ]),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: Free For Educational Use',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX :: Linux',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.13',
        'Topic :: Games/Entertainment :: Side-Scrolling/Arcade Games',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
    ],
    url='https://github.com/Kautenja/gym-super-mario-bros',
    author='Christian Kauten',
    author_email='kautencreations@gmail.com',
    license='Proprietary',
    python_requires='>=3.13',
    packages=find_packages(exclude=['tests', '*.tests', '*.tests.*']),
    package_data={ 'gym_super_mario_bros': ['_roms/*.nes'] },
    install_requires=[
        'gym>=0.25.2,<0.26',
        'nes-py>=8.2.1',
    ],
    extras_require={
        'release': [
            'twine>=6.1.0',
        ],
    },
    entry_points={
        'console_scripts': [
            'gym_super_mario_bros = gym_super_mario_bros._app.cli:main',
        ],
    },
)
