from setuptools import find_packages, setup

setup(
    name="nexus-cli",
    version="0.1.0",
    packages=find_packages(),
    install_requires=["click", "rich", "google-genai", "httpx", "pydantic"],
    entry_points={"console_scripts": ["nexus=nexus_cli.cli:cli"]},
)
