from setuptools import setup, find_packages

setup(
    name="AppleMusicMP3",
    version="0.1.2",
    author="Aidan Friedsam",
    description="Convert Apple Music songs to MP3.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/afriedsam/AppleMusicMP3",
    packages=find_packages(),
    install_requires=open("req.txt").read().splitlines(),
    python_requires=">=3.7",
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        "console_scripts": [
            "applemusicmp3=AppleMusicMP3.main:main",
        ],
    },
)
