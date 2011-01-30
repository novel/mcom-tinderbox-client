from distutils.core import setup

setup(name="tbclient",
        version="0.1",
        description="Command line client for Marcuscom Tinderbox REST service",
        author="Roman Bogorodskiy",
        author_email="novel@FreeBSD.org",
        packages=["tbclient.commands", "tbclient"],
        scripts=["tbc"],
)
