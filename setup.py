from setuptools import setup
setup(
    name="Alsulf",
    version="2025.11.0a1",
    py_modules=["Alsulf"],
    entry_points={
        "console_scripts": [
            "Alsulf=Alsulf:main",
        ],
    },
)
