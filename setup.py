from setuptools import setup, find_packages
import sys, os


setup(
    name='nesgym-super-mario-bros',
    version='0.1.0',
    description='Super Mario Bros. for Open.ai Gym',
    keywords=['Open.ai Gym', 'NES', 'Super Mario Bros.'],
    url='https://github.com/Kautenja/nesgym-super-mario-bros',
    download_url='https://github.com/Kautenja/nesgym-super-mario-bros/archive/0.1.0.tar.gz',
    author='Christian Kauten',
    author_email='kautencreations@gmail.com',
    license='MIT License',
    packages=find_packages(),
    package_data=['src/lua/*.lua', 'src/roms/*.nes'],
    zip_safe=False,
    install_requires=[
        'gym>=10.5.0',
        'Pillow>=5.0.0',
        'numpy>=1.14.2'
    ],
)
