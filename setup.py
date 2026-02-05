from pathlib import Path

from setuptools import setup, find_packages

this_dir = Path(__file__).parent
readme = (this_dir / "README.md").read_text(encoding="utf-8")

setup(
    name="basic4web",
    version="v0.0.3",
    author="Gustavo Liberatti",
    author_email="liberatti.gustavo@gmail.com",
    description="Biblioteca interna para uso em projetos privados.",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/liberatti/basic4web",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "requests>=2.32.5",
        "pytz>=2025.1",
        "flask>=3.1.2",
        "PyJWT>=2.11.0",
        "marshmallow>=3.26.1",
    ],
    extras_require={
        "web": [
            "flask-socketio>=5.6.0",
            "eventlet>=0.40.4",
        ],
        "oracle": ["cx_Oracle~=8.3.0"],
        "mongo": ["pymongo>=4.5.0"],
        "sqlite": [],
        "redis": ["redis"],
        "rabbitmq": ["pika>=1.3.0"],
        "minio": ["minio>=7.2.0"],
        "image": [
            "numpy>=1.24.0",
            "opencv-python>=4.8.0",
        ],
    },
    python_requires=">=3.10",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
