import os
import subprocess
import socket

print("""
This is a Automation Script for dnf packaing and serveing it via a Apache Server
Pre-requisties
1) Apache is installed and enabaled and its deafult /var/www/html path is unchanged
2) Firewall enabled along with permissions
3) appropirate permissions to modify the files
4) create_repo_c and dnf utils is installed


Output : DNF LocalRepo Creation served through server's IP
""")
def get_ip():
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]
    finally:
        s.close()



##### ENTER THE NAME YOU WANT OF YOUR REPO, IT WILL BE BETTER IF YOU WON'T REPEAT IT####
repo_name = input("Enter repository name: ").strip()
packages = input("Enter space-separated package names: ").strip()
print(f"Your Server's IP : {get_ip()}")

repo_base = f"/var/www/html/repos/{repo_name}"
download_dir = f"/tmp/{repo_name}_pkgs"

os.makedirs(download_dir, exist_ok=True)
os.makedirs(repo_base, exist_ok=True)


print(f"\n[+] Downloading packages and dependencies for: {packages}")
subprocess.run(
    ["sudo", "dnf", "download", "--resolve", "--alldeps", "-y"] + packages.split(),
    cwd=download_dir
)

print(f"[+] Moving RPMs to {repo_base}")
subprocess.run(["sudo", "cp", "-r", f"{download_dir}/", f"{repo_base}/"], check=False)

print(f"[+] Creating repo metadata with createrepo_c...")
subprocess.run(["sudo", "createrepo_c", repo_base], check=True)

ip_address = get_ip()
repo_url = f"http://{ip_address}/repos/{repo_name}/"
print(f"\n Local repo created successfully!")
print(f"Repo path: {repo_base}")
print(f"Repo URL:  {repo_url}")

repo_file_path = f"/etc/yum.repos.d/{repo_name}.repo"
repo_content = f"""[{repo_name}]
name={repo_name} local repository
baseurl=http://{ip_address}/repos/{repo_name}/
enabled=1
gpgcheck=0
"""

tmp_repo_path = f"/tmp/{repo_name}.repo"
with open(tmp_repo_path, "w") as f:
    f.write(repo_content)

subprocess.run(["sudo", "mv", tmp_repo_path, repo_file_path], check=True)
print(f"[+] Repo config created at {repo_file_path}")
subprocess.run(["sudo", "dnf", "clean", "all"], check=False)
subprocess.run(["sudo", "dnf", "makecache"], check=False)

print("\nYou can now use it with:")
print(f"sudo dnf config-manager --add-repo {repo_url}")