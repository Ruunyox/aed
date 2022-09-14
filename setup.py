from setuptools import setup, find_packages
from setuptools.command.install import install
import os

NAME = "aed"
VERSION = "1.0"


class InstallScript(install):
    def run(self):
        install.run(self)


with open("requirements.txt") as f:
    install_requires = list(
        filter(lambda x: "#" not in x, (line.strip() for line in f))
    )


def read(filename):
    import os

    BASE_DIR = os.path.dirname(__file__)
    filename = os.path.join(BASE_DIR, filename)
    with open(filename, "r") as fi:
        return fi.read()


def readlist(filename):
    rows = read(filename).split("\n")
    rows = [x.strip() for x in rows if x.strip()]
    return list(rows)


setup(
    name=NAME,
    version=VERSION,
    author="Nick Charron",
    author_email="charron.nicholas.e@gmail.com",
    url="https://github.com/ruunyox/aed",
    license="MIT",
    packages=find_packages(),
    install_requires=install_requires,
    zip_safe=True,
    cmdclass={"install": InstallScript},
    entry_points={
        "console_scripts": ["aed = aed.bin.__main__:main"],
    },
)
