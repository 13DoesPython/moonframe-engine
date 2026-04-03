from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="moonframe-engine",
    version="1.0.0",
    author="Samin",
    description="A lightweight 2D game engine built on Pyglet",
    long_description=long_description,
    long_description_content_type="text/markdown", # This clears the warning
    url="https://github.com/YourUsername/MoonFrame", # Link to your repo
    packages=find_packages(),
    install_requires=[
        "pyglet",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)