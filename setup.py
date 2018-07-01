"""The setup script for installing the package."""
from setuptools import setup, find_packages


def long_description() -> str:
    """Return the contents of the read me file for this project."""
    with open('README.md') as readme:
        return readme.read()


setup(
    name='gym_super_mario_bros',
    python_requires='>=3.5',
    setup_requires=[
        'very-good-setuptools-git-version'
    ],
    version_format='{tag}',
    description='Super Mario Bros. for OpenAI Gym',
    long_description=long_description(),
    long_description_content_type='text/markdown',
    keywords=' '.join([
        'OpenAI-Gym',
        'NES',
        'Super-Mario-Bros',
        'Lost-Levels',
        'Reinforcement-Learning-Environment',
    ]),
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Games/Entertainment :: Side-Scrolling/Arcade Games',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    url='https://github.com/Kautenja/gym-super-mario-bros',
    author='Christian Kauten',
    author_email='kautencreations@gmail.com',
    license='MIT',
    packages=find_packages(),
    package_data={
        'gym_super_mario_bros': ['lua/*.lua', 'roms/*.nes']
    },
    install_requires=[
        'gym>=0.10.5',
        'numpy>=1.14.2',
        'opencv-python>=3.4.0.12',
        'pygame>=1.9.3',
        'pyglet>=1.3.2',
        'tqdm>=4.19.5',
    ],
    entry_points={
        'console_scripts': [
            'gym_super_mario_bros = gym_super_mario_bros._app.cli:main',
        ],
    },
)
