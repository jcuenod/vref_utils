from setuptools import find_packages, setup

setup(
    name="vref_util",
    version="0.0.5",
    packages=find_packages(),
    author="James Cuénod",
    author_email="j3frea+github@gmail.com",
    description="Tools to work with vref files (e.g., in the ebible corpus)",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/jcuenod/vref_util",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    package_data={"": ["vref.txt"]},
    include_package_data=True,
)
