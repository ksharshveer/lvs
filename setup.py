from setuptools import find_packages, setup

setup(
    name='lvs',
    version='1.0',
    packages=find_packages(exclude=("tests",)),
    include_package_data=True,
    install_requires=['opencv-python', 'click', 'toml', 'flask'],
    entry_points='''
            [console_scripts]
            lvs=lvs.cli:cli
        ''',
    url='https://github.com/ksharshveer/lvs',
    license='MIT',
    author='Harshveer Singh',
    author_email='ksharshveer@gmail.com',
    description='Stream video from camera or video file to devices on your local network'
)
