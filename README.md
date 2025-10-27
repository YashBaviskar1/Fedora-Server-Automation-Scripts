#  Automated DNF Local Repository Creator

This Python script automates the creation of a **local DNF repository** on RHEL/CentOS/Fedora systems.
It downloads selected packages (and dependencies), builds repository metadata, and optionally serves it via Apache or transfers it to another server.

---

##  Features
- Automatically downloads packages and dependencies using `dnf`.
- Builds metadata with `createrepo_c`.
- Detects local machine IP for serving via Apache.
- Generates `.repo` file automatically.
- Optional SCP transfer to another host.

---

##  Prerequisites
- Python 3
- `dnf-utils` and `createrepo_c` installed
- Apache web server running (`/var/www/html` as default path)
- Sudo privileges
- Internet access (for package download)

---

## Usage

```bash
sudo python3 automate_dnf_repo.py