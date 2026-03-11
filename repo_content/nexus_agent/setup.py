from setuptools import find_packages, setup

setup(
    name="nexus-agent",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "google-adk>=1.3.0",
        "mcp>=1.9.0",
        "litellm",
        "pydantic-settings",
        "rich",
        "click",
        "google-genai",
    ],
    entry_points={"console_scripts": ["nexus-agent=nexus_agent.agent:main"]},
)
