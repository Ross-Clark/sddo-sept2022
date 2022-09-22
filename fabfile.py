import os
import subprocess

from invoke import run
from invoke.tasks import task

# load .env file
if os.path.exists(".env"):
    with open(".env", "r") as f:
        for line in f.readlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            var, value = line.split("=", 1)
            os.environ.setdefault(var, value)


@task
def build(c):
    """
    Build the development environment (call this first)
    """
    #insert build processes

    run("docker-compose up -d --build web")

    run("docker-compose stop")
    print("Project built: now run 'fab start'")


@task
def start(c):
    """
    Start the development environment
    """
    run("docker-compose up -d")

    print("Use `fab sh` to enter the web container and run `djrun`")



@task
def stop(c):
    """
    Stop the development environment
    """
    run("docker-compose stop")


@task
def restart(c):
    """
    Restart the development environment
    """
    stop(c)
    start(c)


@task
def sh(c):
    """
    Run bash in the local web container
    """
    subprocess.run(["docker-compose", "exec", "web", "bash"])


@task
def sh_root(c):
    """
    Run bash as root in the local web container
    """
    subprocess.run(["docker-compose", "exec", "--user=root", "web", "bash"])
