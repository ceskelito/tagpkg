## TagPkg
A simple tool to tag installed packages.
Useful when you need to install dependencies (like libraries, tools, etc.) for your projects, but don’t want to clutter your system with unnecessary stuff afterward.
You can also use it to tag apps for specific tasks, like video editing, virtualization, productivity, or anything else you have on your PC.

### Setup:
```bash
git clone git@github.com:ceskelito/tagpkg.git;
cp tagpkg/tagpkg.py ~/.local/bin/tagpkg;
rm -rf tagpkg
```

*only if the autocompletion don't start automatically*
```bash
activate-global-python-argcomplete --user
```

### Usage:
Install an APT package and assign one or more tags to it:
  ```bash
tagpkg install <package> <tags...>
  ```

Add one or more tags to an already installed package:
```bash  
tagpkg tag <package> <tags...>
```

List all packages tagged with the specified tag:
```bash
tagpkg list <tag>
```

Show all tags assigned to the given package:
```bash
  tagpkg tags <package>
```

Remove a specific tag from a package:
```bash
tagpkg untag <package> <tag>
```

Remove all tags associated with the package:
```bash
  tagpkg remove <package>
```

### Dependencies

- Python 3
- `argcomplete` Python package (for shell autocompletion)
- `dpkg` (Debian package manager, required to check installed packages)
- `apt` (for installing packages via the script)
- Bash (for autocompletion support)

#### Installation of Python dependency

```bash
pip install argcomplete
