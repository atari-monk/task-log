from setuptools import setup, find_packages

setup(
    name="task_log",
    version="0.1",
    packages=find_packages(),
    install_requires=[],
    entry_points={
        "console_scripts": [
            "task_log=task_log.main:main"
        ],
    },
    python_requires=">=3.7",
)
