from setuptools import setup, find_packages


# the URL to find the source code and releases
__url__ = 'https://github.com/Kautenja/nesgym-super-mario-bros'


# open the README to fill the long description key
with open('README.md') as README:
    long_description = README.read()


setup(
    name='nesgym_super_mario_bros',
    setup_requires=[
        'setuptools-git-version'
    ],
    version_format='{tag}',
    description='Super Mario Bros. for Open.ai Gym',
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords=['Open.ai Gym', 'NES', 'Super Mario Bros.'],
    url=__url__,
    author='Christian Kauten',
    author_email='kautencreations@gmail.com',
    license='MIT License',
    packages=['nesgym_super_mario_bros'],
    zip_safe=False,
    install_requires=[
        'gym>=0.10.5',
        'Pillow>=5.0.0',
        'numpy>=1.14.2'
    ],
)
