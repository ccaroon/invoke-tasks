from invoke import task


@task
def mpy(ctx):
    """ Delete all local .mpy files """
    ctx.run('find . -name "*.mpy" -exec rm {} \\;')

@task
def device(ctx):
    """ Erase all files on the device """
    ctx.run("mpremote fs rm -r :.")
