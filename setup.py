import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="jmeter_cloud_load_test", # Replace with your own username
    version="0.0.1",
    author="k$",
    author_email="kronosme@gmail.com",
    description="Simple package to run .jmx file on ec2",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: Linux",
    ],
    python_requires='>=3.6',
)