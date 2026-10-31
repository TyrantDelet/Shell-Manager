from __future__ import annotations

from types import MappingProxyType
from typing import Final, Iterable

from app.models import Category, Command, CommandExample, Flag, SafetyLevel

NAVIGATION_COMMANDS: Final[tuple[Command, ...]] = (
    Command(
        name="pwd",
        category=Category.NAVIGATION,
        safety_level=SafetyLevel.READ_ONLY,
        summary="Print current working directory",
        description=(
            "Displays the absolute filesystem path of your current location.\n"
            "Essential whenever you need to confirm which directory you are inside \n"
            "before creating, modifying, or moving files."
        ),
        syntax="pwd [options]",
        default_args="",
        flags=(
            Flag(
                flag="-L",
                name="Logical path",
                description="Displays the environment path, preserving symbolic links.",
                example="pwd -L",
            ),
            Flag(
                flag="-P",
                name="Physical path",
                description="Resolves all symbolic links and displays the physical location.",
                example="pwd -P",
            ),
        ),
        examples=(
            CommandExample(
                command="pwd",
                description="Show current working directory path",
            ),
            CommandExample(
                command="pwd -P",
                description="Show physical path resolving any symbolic links",
            ),
        ),
        notes="Safe to run anytime. Does not modify any system state.",
    ),
    Command(
        name="ls",
        category=Category.NAVIGATION,
        safety_level=SafetyLevel.READ_ONLY,
        summary="List directory contents",
        description=(
            "Lists files and directories inside the target directory. Provides \n"
            "options to view hidden files (dotfiles), detailed permissions, file \n"
            "sizes, and timestamps."
        ),
        syntax="ls [options] [path]",
        default_args="-lh",
        flags=(
            Flag(
                flag="-l",
                name="Long listing format",
                description="Shows permissions, owner, group, file size, and modification date.",
                example="ls -l",
            ),
            Flag(
                flag="-a",
                name="All files (including hidden)",
                description="Shows hidden files and directories that begin with a dot (.).",
                example="ls -a",
            ),
            Flag(
                flag="-h",
                name="Human-readable sizes",
                description="Formats byte sizes into KB, MB, GB (must be used with -l).",
                example="ls -lh",
            ),
            Flag(
                flag="-t",
                name="Sort by modification time",
                description="Sorts items by time, displaying newly modified files first.",
                example="ls -lt",
            ),
            Flag(
                flag="-R",
                name="Recursive",
                description="Lists all subdirectories and their contents recursively.",
                example="ls -R",
            ),
        ),
        examples=(
            CommandExample(
                command="ls -lh",
                description="List files in long format with readable file sizes",
            ),
            CommandExample(
                command="ls -lah",
                description="List all files including hidden dotfiles in long format",
            ),
            CommandExample(
                command="ls -lt",
                description="List files sorted by newest modification date",
            ),
        ),
        notes="Safe to run. Combine -l, -a, and -h (-lah) for the most informative directory view.",
    ),
    Command(
        name="cd",
        category=Category.NAVIGATION,
        safety_level=SafetyLevel.READ_ONLY,
        summary="Change current working directory",
        description=(
            "Switches the terminal's active working directory to a new target path. "
            "Supports relative paths, absolute paths, and standard shortcuts like ~ (home)."
        ),
        syntax="cd [directory]",
        default_args="~",
        flags=(
            Flag(
                flag="~",
                name="Home directory shortcut",
                description="Switches directly to the current user's home folder (/home/<user>).",
                example="cd ~",
            ),
            Flag(
                flag="..",
                name="Parent directory shortcut",
                description="Moves one level up in the directory tree.",
                example="cd ..",
            ),
            Flag(
                flag="-",
                name="Previous directory shortcut",
                description="Switches back to the previous directory you were working in.",
                example="cd -",
            ),
        ),
        examples=(
            CommandExample(
                command="cd /var/log",
                description="Change to system log directory",
            ),
            CommandExample(
                command="cd ..",
                description="Move up one directory level",
            ),
            CommandExample(
                command="cd ~",
                description="Return to user home directory",
            ),
        ),
        notes="In Linux, 'cd' is a shell built-in command that shifts your working context.",
    ),
    Command(
        name="find",
        category=Category.NAVIGATION,
        safety_level=SafetyLevel.READ_ONLY,
        summary="Search for files in a directory hierarchy",
        description=(
            "Recursively scans directory trees to locate files matching names, \n"
            "extensions, types, file sizes, or modification timestamps."
        ),
        syntax="find [path] [expression]",
        default_args=". -name '*.log'",
        flags=(
            Flag(
                flag="-name",
                name="Case-sensitive pattern",
                description="Matches filenames matching a wildcard pattern (e.g. '*.txt').",
                example="find . -name '*.py'",
            ),
            Flag(
                flag="-iname",
                name="Case-insensitive pattern",
                description="Matches filenames ignoring uppercase and lowercase differences.",
                example="find . -iname '*.png'",
            ),
            Flag(
                flag="-type",
                name="File type filter",
                description="Filters by type: 'f' for regular file, 'd' for directory.",
                example="find . -type f",
            ),
            Flag(
                flag="-mtime",
                name="Modified days ago",
                description="Finds files modified N days ago (-mtime -7 means within 7 days).",
                example="find /var/log -mtime -7",
            ),
            Flag(
                flag="-size",
                name="File size filter",
                description="Finds files by size (+100M matches files larger than 100MB).",
                example="find . -size +100M",
            ),
        ),
        examples=(
            CommandExample(
                command="find . -name '*.conf'",
                description="Find all .conf configuration files in current directory",
            ),
            CommandExample(
                command="find /var/log -name '*.log' -type f",
                description="Find all log files under /var/log",
            ),
            CommandExample(
                command="find . -size +50M",
                description="Find all files larger than 50 megabytes",
            ),
        ),
        notes="Surround search patterns with quotes (e.g. '*.log') to prevent the shell from expanding them prematurely.",
    ),
    Command(
        name="tree",
        category=Category.NAVIGATION,
        safety_level=SafetyLevel.READ_ONLY,
        summary="Display visual directory tree structure",
        description=(
            "Draws a graphical tree diagram of directories and files. Makes understanding \n"
            "nested project layouts and hierarchies easy at a glance."
        ),
        syntax="tree [options] [path]",
        default_args="-L 2",
        flags=(
            Flag(
                flag="-L",
                name="Depth level limit",
                description="Restricts the tree display to N directory levels deep.",
                example="tree -L 2",
            ),
            Flag(
                flag="-d",
                name="Directories only",
                description="Hides regular files, displaying only folder structures.",
                example="tree -d",
            ),
            Flag(
                flag="-a",
                name="Show all files",
                description="Includes hidden files in the visual tree.",
                example="tree -a",
            ),
            Flag(
                flag="-I",
                name="Ignore pattern",
                description="Excludes files/folders matching a pattern (e.g., node_modules, .git).",
                example="tree -I '.git|__pycache__'",
            ),
        ),
        examples=(
            CommandExample(
                command="tree -L 2",
                description="Show directory tree limited to 2 levels deep",
            ),
            CommandExample(
                command="tree -d",
                description="Show folder hierarchy without listing files",
            ),
        ),
        notes="If tree is not installed on minimal distributions, 'find' with formatting is an alternative.",
    ),
    Command(
        name="which",
        category=Category.NAVIGATION,
        safety_level=SafetyLevel.READ_ONLY,
        summary="Locate executable binary path",
        description=(
            "Searches the directories listed in your $PATH environment variable \n"
            "and prints the full pathname of the executable command that would be run."
        ),
        syntax="which [command_name]",
        default_args="python3",
        flags=(
            Flag(
                flag="-a",
                name="All matching paths",
                description="Prints all matching executables in $PATH, not just the first one.",
                example="which -a python3",
            ),
        ),
        examples=(
            CommandExample(
                command="which python3",
                description="Locate which python3 binary is active in PATH",
            ),
            CommandExample(
                command="which bash",
                description="Find the absolute path of the bash shell",
            ),
        ),
        notes="Helpful for checking whether a tool is installed and which virtualenv or system version is selected.",
    ),
    Command(
        name="whereis",
        category=Category.NAVIGATION,
        safety_level=SafetyLevel.READ_ONLY,
        summary="Locate binary, source, and manual page files",
        description=(
            "Locates the binary executable, manual documentation page (man page), \n"
            "and source code files for a specified command utility."
        ),
        syntax="whereis [options] [name]",
        default_args="grep",
        flags=(
            Flag(
                flag="-b",
                name="Binary only",
                description="Searches only for executable binary files.",
                example="whereis -b ls",
            ),
            Flag(
                flag="-m",
                name="Manuals only",
                description="Searches only for documentation and man pages.",
                example="whereis -m grep",
            ),
        ),
        examples=(
            CommandExample(
                command="whereis python3",
                description="Find binaries and man page paths for Python 3",
            ),
            CommandExample(
                command="whereis -b nginx",
                description="Find binary location of the nginx web server",
            ),
        ),
        notes="Broader than 'which' because it scans system documentation directories as well.",
    ),
    Command(
        name="realpath",
        category=Category.NAVIGATION,
        safety_level=SafetyLevel.READ_ONLY,
        summary="Resolve and print canonical absolute path",
        description=(
            "Resolves all symbolic links, relative path notations (. and ..), \n"
            "and extra slashes, returning the true physical absolute path."
        ),
        syntax="realpath [options] [path]",
        default_args=".",
        flags=(
            Flag(
                flag="-e",
                name="Existence check",
                description="Requires all path components to exist on disk.",
                example="realpath -e config.ini",
            ),
            Flag(
                flag="-m",
                name="No existence check",
                description="Resolves path canonically even if target files do not exist.",
                example="realpath -m future/path/file.txt",
            ),
        ),
        examples=(
            CommandExample(
                command="realpath .",
                description="Print the canonical path of current directory",
            ),
            CommandExample(
                command="realpath symlink_to_file",
                description="Find the real destination file of a symlink",
            ),
        ),
        notes="Crucial in shell scripts to ensure consistent absolute path references.",
    ),
)

