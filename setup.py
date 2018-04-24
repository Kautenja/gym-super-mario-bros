from setuptools import setup, find_packages
from nesgym_super_mario_bros import __version__, __url__


# open the README to fill the long description key
with open('README.md') as README:
    long_description = README.read()


setup(
    name='nesgym_super_mario_bros',
    # version=__version__,
    use_scm_version=True,
    setup_requires=['setuptools_scm'],
    description='Super Mario Bros. for Open.ai Gym',
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords=['Open.ai Gym', 'NES', 'Super Mario Bros.'],
    url=__url__,
    # download_url='{}/archive/{}.tar.gz'.format(__url__, __version__),
    author='Christian Kauten',
    author_email='kautencreations@gmail.com',
    license='MIT License',
    packages=['nesgym_super_mario_bros'],
    zip_safe=False,
    install_requires=[
        'gym>=10.5.0',
        'Pillow>=5.0.0',
        'numpy>=1.14.2'
    ],
)
