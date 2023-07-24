import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="medium2md",
    version="1.0.0",
    author="Siddharth Kumar",
    author_email="siddharth123sk@gmail.com",
    description="Download and convert Medium articles to markdown with images",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/siddharthksah/medium2md",
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Text Processing",
        "Topic :: Utilities",
    ],
    python_requires=">=3.8",
    install_requires=[
        "beautifulsoup4==4.12.2",
        "certifi==2023.7.22",
        "chardet==5.1.0",
        "charset-normalizer==3.2.0",
        "colorama==0.4.6",
        "cssselect==1.2.0",
        "greenlet==2.0.2",
        "html2text==2020.1.16",
        "idna==3.4",
        "lxml==4.9.3",
        "playwright==1.36.0",
        "pyee==9.0.4",
        "pyfiglet==0.8.post1",
        "PyInquirer==1.0.3",
        "readability-lxml==0.8.1",
        "requests==2.31.0",
        "setuptools==67.8.0",
        "soupsieve==2.4.1",
        "termcolor==2.3.0",
        "tqdm==4.65.0",
        "typing-extensions==4.7.1",
        "urllib3==2.0.4",
        "wheel==0.38.4",
    ],
    entry_points={
        "console_scripts": [
            "medium2md=src.main:main",
        ],
    },
    project_urls={
        "Bug Tracker": "https://github.com/siddharthksah/medium2md/issues",
        "Documentation": "https://github.com/siddharthksah/medium2md#readme",
        "Source Code": "https://github.com/siddharthksah/medium2md",
    },
)
