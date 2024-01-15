from setuptools import setup, find_packages

setup(
    name="dawnet_discovery_server",
    version="0.1",
    packages=find_packages(),
    package_data={
        'dawnet_discovery_server': ['../config.ini'],
    },
    install_requires=[
        "websockets",
        "aiohttp",
        "dawnet-client",
    ],
    author="Steve Hiehn",
    author_email="stevehiehn@gmail.com",
    description="The Dawnet Discovery Server",
    keywords="websocket discovery server",
)
