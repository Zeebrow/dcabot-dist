import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dcabot-zeebrow",
    version="0.0.4",
    author="Zeebrow",
    author_email="zeebrow@dcabot-project.com",
    description="A small crypto-buying program for dollar-cost-averaging",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/zeebrow/dcabot",
    project_urls={
        "Bug Tracker": "https://github.com/zeebrow/dcabot"
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",    
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where='src'),
    python_requires=">=3.6",
)

