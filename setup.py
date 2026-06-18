from setuptools import setup, find_packages

setup(
    name="ultimate-nuke-engine",
    version="3.0.0",
    author="3ZF",
    description="Ultimate Discord Nuke Tool",
    packages=find_packages(),
    install_requires=[
        "discord.py-self>=2.0.0",
        "aiohttp>=3.9.0",
        "uvloop>=0.19.0",
        "orjson>=3.9.0",
        "colorama>=0.4.6"
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "nuke=nuke:main",
        ],
    },
)
