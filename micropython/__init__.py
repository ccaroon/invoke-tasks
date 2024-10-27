import os
from invoke import task, Collection

import firmware
import install

import ports

@task
def shell(ctx):
    """ Use picocom to run the REPL """

    port = ports.find_port()
    if port:
        # NOTE: doesn't behave properly with run()...even with pty=True
        # ctx.run(f"picocom {port} -b115200", pty=True)
        os.execlp("picocom",  ".", port, "-b115200")


ns = Collection(
    shell,
    firmware,
    install
)
