from setuptools import setup, find_packages

setup(
    name="AST",
    version="2025.11.0",
    description="Automated Security Tools - Python CLI tools",
    author="alsulf",
    packages=find_packages(),
    py_modules=["Alsulf"],
    install_requires=[
        "colorama",
    ],
    entry_points={
        "console_scripts": [
            "ast=Alsulf:main_menu",
        ],
    },
)
