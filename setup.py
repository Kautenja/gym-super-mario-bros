from setuptools import setup, find_packages


# open the README to fill the long description key
def README():
    with open('README.md') as README_file:
        return README_file.read()


setup(
    name='nesgym_super_mario_bros',
    setup_requires=[
        'setuptools-git-version'
    ],
    version_format='{tag}',
    description='Super Mario Bros. for Open.ai Gym',
    long_description=README(),
    long_description_content_type='text/markdown',
    keywords='OpenAI-Gym NES Super-Mario-Bros',
    url='https://github.com/Kautenja/nesgym-super-mario-bros',
    author='Christian Kauten',
    author_email='kautencreations@gmail.com',
    license='MIT',
    packages=[
        'nesgym_super_mario_bros'
    ],
    package_data = { '': ['*.lua', '*.nes'] },
    zip_safe=False,
    install_requires=[
        'gym>=0.10.5',
        'Pillow>=5.0.0',
        'numpy>=1.14.2'
    ],
)
