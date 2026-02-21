import os.path
import yaml

from invoke import task

import ports
import utils

@task
def project(ctx, project_file, sections=None):
    """ Install a Project from a YML File """
    data = None
    with open(project_file, "r") as fptr:
        data = yaml.safe_load(fptr)

    # Exclude 'requirements' from defs b/c they don't change very often
    # will need to explicitly include them
    sections = ("package", "main", "boot", "libs") if sections is None else sections.split(",")

    # package
    if "package" in sections:
        pkg_name = data.get("package")
        if pkg_name:
            print(f"=> Install '{pkg_name}' Package...")
            ctx.run(f"mpremote fs cp -r {pkg_name}/ :.")

    # main & boot
    if "main" in sections:
        fname = data.get("main")
        if fname:
            print("=> Install main.py...")
            main(ctx, fname)

    if "boot" in sections:
        fname = data.get("boot")
        if fname:
            print("=> Install boot.py...")
            boot(ctx, fname)

    # libs
    if "libs" in sections:
        libs = data.get("libs", [])
        if libs:
            print("=> Installing libs...")
            # Create lib/ on device
            ctx.run("mpremote fs mkdir :lib", warn=True)

            for fname in libs:
                file(ctx, f"lib/{fname}")

    # requirements
    if "requirements" in sections:
        reqs = data.get("requirements", [])
        if reqs:
            print("=> Installing Requirements...")
            for pkg in reqs:
                ctx.run(f"mpremote mip install {pkg}")

    ctx.run("mpremote fs tree")


@task
def file(ctx, src_file, dst_file=None, no_compile=False):
    """ Install a file on a device """
    port = ports.find_port()
    local_file = None
    remote_file = None

    (src_name, src_ext) = os.path.splitext(src_file)

    dst_name = None
    if dst_file:
        (dst_name, _) = os.path.splitext(dst_file)
        remote_file = dst_file

    if src_ext == ".py" and not no_compile:
        # compile first
        # file.py => file.mpy
        local_file = f"{src_name}.mpy"
        remote_file = f"{dst_name}.mpy" if dst_name else local_file

        if not os.path.exists(local_file) or utils.is_newer(src_file, local_file):
            compile(ctx, src_file)
    else:
        local_file = src_file
        remote_file = dst_file

    # ctx.run(f"ampy --port {port} put {local_file} {remote_file}")
    ctx.run(f"mpremote fs cp {local_file} :{remote_file}")


@task
def boot(ctx, src_file):
    """ Install source file as `boot.py` """
    file(ctx, src_file, dst_file="boot.py", no_compile=True)


@task
def main(ctx, src_file):
    """ Install source file as `main.py` """
    file(ctx, src_file, dst_file="main.py", no_compile=True)


@task
def compile(ctx, filename):
    """ Compile a .py source file to .mpy"""
    ctx.run(f"mpy-cross {filename}")
