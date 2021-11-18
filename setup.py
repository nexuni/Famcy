import setuptools
import os
from setup_utils import *

with open("README.md", "r") as fh:
    long_description = fh.read()

with open(os.path.join(os.path.dirname(__file__), "requirements.txt"), "r") as f:
    requirements = f.read().split("\n")

setuptools.setup(
    name="Famcy", # Replace with your own username
    version="0.2.39",
    author="Nexuni Co Ltd. Develop Team",
    author_email="developers@nexuni.com",
    description="Nexuni Co Ltd. Famcy management console framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nexuni/Famcy.git",
    license="Apache-2.0",
    packages=setuptools.find_packages(),
    entry_points={
        "console_scripts": ["famcy = Famcy.main:command_line_interface"]
    },
    install_requires=requirements,
    package_dir={"Famcy": "Famcy"},
    package_data=package_data_with_recursive_dirs({"Famcy":["bower_components", "node_modules", "templates", "static", "scripts", "famcy.ini", "_style_", "_responses_", "_items_", "_elements_"]}),
    test_suite="Famcy.tests",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries ",
    ],
    python_requires='>=3.6',
)