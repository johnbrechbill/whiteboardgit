import subprocess

def setup_ssh_agent():
    subprocess.run("eval $(ssh-agent -s)", shell=True)
    subprocess.run("ssh-add ~/.ssh/id_ed25519", shell=True)
