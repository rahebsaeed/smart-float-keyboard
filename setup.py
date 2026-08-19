from setuptools import setup, find_packages

setup(
    name="smart-float-keyboard",
    version="1.0.1",
    author="RAHEB Aref Mahyoub Saeed",
    description="A modern, floating virtual on-screen keyboard for Ubuntu Linux",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/your-username/smart-float-keyboard",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Environment :: X11 Applications :: Qt",
    ],
    install_requires=[
        "PyQt6>=6.6.0",
        "evdev>=1.7.0",
    ],
    python_requires=">=3.10",
)
