from __future__ import annotations

from types import MappingProxyType
from typing import Final, Iterable

from app.models import Category, Command, CommandExample, Flag, SafetyLevel

FILE_MANIPULATION_COMMANDS: Final[tuple[Command, ...]] = (
    Command(
        name = "touch",
        category=Category.FILE_MANIPULATION,
        safety_level=SafetyLevel.MODIFICATION,
        summary="Create an empty file or update the timestamp of an existing file.",
        description=(
            "The `touch` command is used to create an empty file or update the access and modification timestamps of an existing file. \n"
            "If the specified file does not exist, it will be created. If it does exist, its timestamps will be updated to the current time."
        ),
        syntax="touch [options] <file_name>",
        default_args=("new_file.txt",),
        flags=(
            Flag(
                flag="-c",
                name="no-create",
                description="Do not create any files; only update the timestamps of existing files.",
                example="touch -c existing_file.txt"
            ),
            Flag(
                flag="-a",
                name="time",
                description="Change only the access time.",
                example="touch -a existing_file.txt"
            ),
            Flag(
                flag="-m",
                name="time",
                description="Change only the modification time.",
                example="touch -m existing_file.txt"
            )
        ),
        examples=(
            CommandExample(
                command="touch new_file.txt",
                description="Create a new empty text file",
            ),
            CommandExample(
                command="touch index.html style.css app.js",
                description="Create multiple files in one command",
            ),
        ),
        notes="Safe file creation utility. Will not overwrite or erase content of existing files.",
    ),
    Command(
        name="mkdir",
        category=Category.FILE_MANIPULATION,
        safety_level=SafetyLevel.MODIFICATION,
        summary="Create new directories",
        description=(
            "Creates one or more new directories (folders) in the target path.\n "
            "If the specified directory already exists, an error will be displayed"
        ),
        syntax="mkdir [options] <directory_name>",
        default_args="-p new_folder/sub_folder",
        flags=(
            Flag(
                flag="-p",
                name="Parents (recursive)",
                description="Creates parent directories as needed without error if they exist.",
                example="mkdir -p documents/important/2026",
            ),
            Flag(
                flag="-v",
                name="Verbose",
                description="Displays a notification message for each directory created.",
                example="mkdir -v my_folder",
            ),
        ),
        examples=(
            CommandExample(
                command="mkdir -p documents/important/2026",
                description="Create deeply nested directories in a single command",
            ),
            CommandExample(
                command="mkdir backups",
                description="Create a simple backups directory in current location",
            ),
        ),
        notes="The -p flag is highly recommended in automated scripts to prevent 'File exists' errors.",
    ),
     Command(
        name="cp",
        category=Category.FILE_MANIPULATION,
        safety_level=SafetyLevel.MODIFICATION,
        summary="Copy files and directories",
        description=(
            "Copies files or whole directories from source to destination.\n"
            "Requires the -r flag when copying directories."
        ),
        syntax="cp [options] <source> <destination>",
        default_args="-i source.txt destination.txt",
        flags=(
            Flag(
                flag="-r",
                name="Recursive",
                description="Copies entire directories and all sub-contents recursively.",
                example="cp -r src/ src_backup/",
            ),
            Flag(
                flag="-i",
                name="Interactive prompt",
                description="Prompts before overwriting an existing destination file.",
                example="cp -i file.txt dest.txt",
            ),
            Flag(
                flag="-v",
                name="Verbose",
                description="Prints details of each file as it is being copied.",
                example="cp -v report.pdf backups/",
            ),
            Flag(
                flag="-p",
                name="Preserve attributes",
                description="Preserves timestamps, file modes, and ownership attributes.",
                example="cp -p data.csv backup_data.csv",
            ),
        ),
        examples=(
            CommandExample(
                command="cp file.txt file_backup.txt",
                description="Create a backup copy of a single file",
            ),
            CommandExample(
                command="cp -r ./src ./src_backup",
                description="Recursively copy an entire project directory",
            ),
            CommandExample(
                command="cp -iv config.env .env",
                description="Copy with overwrite confirmation and progress display",
            ),
        ),
        notes="Always consider using -i to avoid accidentally overwriting important files.",
    ),
    Command(
        name="mv",
        category=Category.FILE_MANIPULATION,
        safety_level=SafetyLevel.MODIFICATION,
        summary="Move or rename files and directories",
        description=(
            "Moves files or directories to a different folder, or renames them \n"
            "if the destination is a new name in the same directory."
        ),
        syntax="mv [options] <source> <destination>",
        default_args="-i old_name.txt new_name.txt",
        flags=(
            Flag(
                flag="-i",
                name="Interactive prompt",
                description="Prompts for confirmation before overwriting an existing destination.",
                example="mv -i source.txt existing.txt",
            ),
            Flag(
                flag="-v",
                name="Verbose",
                description="Prints the source and destination names for every moved file.",
                example="mv -v file.txt /tmp/",
            ),
            Flag(
                flag="-n",
                name="No clobber",
                description="Prevents overwriting any existing file at destination.",
                example="mv -n file.txt backups/",
            ),
        ),
        examples=(
            CommandExample(
                command="mv old_name.txt new_name.txt",
                description="Rename a file in the current directory",
            ),
            CommandExample(
                command="mv report.pdf ~/Documents/",
                description="Move a file into your Documents folder",
            ),
            CommandExample(
                command="mv -i config.json config_backup.json",
                description="Safely rename file with confirmation prompt",
            ),
        ),
        notes="Moving files within the same filesystem is instantaneous as only directory pointers change.",
    ),
    Command(
        name="rm",
        category=Category.FILE_MANIPULATION,
        safety_level=SafetyLevel.DESTRUCTIVE,
        summary="Remove files or directories (PERMANENT DELETION)",
        description=(
            "Permanently deletes files or folders from the filesystem. \n"
            "WARNING: In Linux there is NO Recycle Bin / Trash for CLI commands. \n"
            "Deleted data cannot be undone without specialized forensic recovery."
        ),
        syntax="rm [options] <target_file_or_directory>",
        default_args="-i file_to_delete.txt",
        flags=(
            Flag(
                flag="-i",
                name="Interactive prompt",
                description="Prompts for confirmation before deleting each file (safest option).",
                example="rm -i unwanted.txt",
            ),
            Flag(
                flag="-r",
                name="Recursive",
                description="Removes directories and all of their contents recursively.",
                example="rm -r temp_folder/",
            ),
            Flag(
                flag="-f",
                name="Force",
                description="Ignores nonexistent files and never prompts for confirmation. EXTREME CAUTION.",
                example="rm -f file.tmp",
            ),
            Flag(
                flag="-v",
                name="Verbose",
                description="Outputs a log message for each file removed.",
                example="rm -v *.tmp",
            ),
        ),
        examples=(
            CommandExample(
                command="rm -i old_notes.txt",
                description="Safely remove a file with an interactive confirmation prompt",
            ),
            CommandExample(
                command="rm -rv ./temp_cache",
                description="Recursively remove a cache folder with verbose output",
            ),
        ),
        notes=(
            "NEVER run 'rm -rf /' or 'rm -rf /*'. Destructive commands require explicit "
            "preview and confirmation in Shell Manager."
        ),
    ),
    Command(
        name="cat",
        category=Category.FILE_MANIPULATION,
        safety_level=SafetyLevel.READ_ONLY,
        summary="Concatenate and display file contents",
        description=(
            "Reads files sequentially and writes their contents to standard output. \n"
            "Best suited for small files, configuration reviews, and quick script inspections."
        ),
        syntax="cat [options] [file...]",
        default_args="README.md",
        flags=(
            Flag(
                flag="-n",
                name="Number lines",
                description="Numbers all output lines starting from 1.",
                example="cat -n script.py",
            ),
            Flag(
                flag="-b",
                name="Number non-blank lines",
                description="Numbers only non-empty output lines.",
                example="cat -b notes.txt",
            ),
            Flag(
                flag="-s",
                name="Squeeze blank lines",
                description="Compresses consecutive blank lines into a single blank line.",
                example="cat -s output.log",
            ),
        ),
        examples=(
            CommandExample(
                command="cat /etc/os-release",
                description="Display Linux OS release and distribution details",
            ),
            CommandExample(
                command="cat -n requirements.txt",
                description="Display dependency list with line numbers",
            ),
        ),
        notes="For large log files, prefer 'less', 'tail', or 'head' to prevent flooding the terminal.",
    ),
    Command(
        name="nano",
        category=Category.FILE_MANIPULATION,
        safety_level=SafetyLevel.MODIFICATION,
        summary="Simple beginner-friendly terminal text editor",
        description=(
            "A straightforward text editor inside the terminal. Helpful shortcuts \n"
            "are displayed at the bottom of the screen (e.g. Ctrl+O to save, Ctrl+X to exit)."
        ),
        syntax="nano [options] <file>",
        default_args="notes.txt",
        flags=(
            Flag(
                flag="-l",
                name="Line numbers",
                description="Displays line numbers along the left side of the screen.",
                example="nano -l script.py",
            ),
            Flag(
                flag="-v",
                name="View mode (read-only)",
                description="Opens the file in read-only mode so accidental edits cannot be saved.",
                example="nano -v /etc/fstab",
            ),
            Flag(
                flag="-m",
                name="Mouse support",
                description="Enables mouse clicks to position the cursor.",
                example="nano -m document.txt",
            ),
        ),
        examples=(
            CommandExample(
                command="nano config.ini",
                description="Open or create config.ini in the nano text editor",
            ),
            CommandExample(
                command="nano -l main.py",
                description="Edit Python code with visible line numbers",
            ),
            CommandExample(
                command="nano -v /etc/hosts",
                description="Safely inspect hosts file in read-only view mode",
            ),
        ),
        notes="Press Ctrl+O then Enter to save (WriteOut), and Ctrl+X to exit.",
    ),
    Command(
        name="chmod",
        category=Category.FILE_MANIPULATION,
        safety_level=SafetyLevel.SUDO_REQUIRED,
        summary="Change file access permissions",
        description=(
            "Modifies read (r), write (w), and execute (x) permissions for file owner, \n"
            "group, and others. Misconfiguring permissions on system directories can \n"
            "cause security holes or lockout."
        ),
        syntax="chmod [options] <mode> <file_or_directory>",
        default_args="+x script.sh",
        flags=(
            Flag(
                flag="+x",
                name="Make executable",
                description="Grants execution permission so a script can be run directly.",
                example="chmod +x build.sh",
            ),
            Flag(
                flag="-R",
                name="Recursive",
                description="Changes file permissions across all subdirectories recursively.",
                example="chmod -R 755 public_html/",
            ),
            Flag(
                flag="-v",
                name="Verbose",
                description="Outputs a diagnostic message explaining every file permission changed.",
                example="chmod -v 644 file.txt",
            ),
        ),
        examples=(
            CommandExample(
                command="chmod +x run.sh",
                description="Make a shell script executable",
            ),
            CommandExample(
                command="chmod 600 id_rsa",
                description="Set private key file permissions (read/write only by owner)",
            ),
            CommandExample(
                command="chmod 644 README.md",
                description="Set standard file permissions (owner write, everyone read)",
            ),
        ),
        notes="Common modes: 755 (executables/dirs), 644 (regular files), 600 (secret keys).",
    ),
    Command(
        name="chown",
        category=Category.FILE_MANIPULATION,
        safety_level=SafetyLevel.SUDO_REQUIRED,
        summary="Change file owner and group",
        description=(
            "Changes user ownership and group association of files and directories. \n"
            "Typically requires elevated root / sudo permissions."
        ),
        syntax="chown [options] <user>[:<group>] <target_file_or_directory>",
        default_args="$USER:$USER project_dir",
        flags=(
            Flag(
                flag="-R",
                name="Recursive",
                description="Recursively changes ownership for directories and all sub-contents.",
                example="chown -R www-data:www-data /var/www",
            ),
            Flag(
                flag="-v",
                name="Verbose",
                description="Displays a report for each file whose ownership was altered.",
                example="chown -v user:group file.txt",
            ),
        ),
        examples=(
            CommandExample(
                command="sudo chown $USER:$USER /opt/my_project",
                description="Reassign project folder ownership to current user",
            ),
            CommandExample(
                command="sudo chown -R www-data:www-data /var/www/html",
                description="Recursively assign ownership of web directory to www-data",
            ),
        ),
        notes="Always double check paths when running recursive chown with sudo.",
    ),
    Command(
        name="tar",
        category=Category.FILE_MANIPULATION,
        safety_level=SafetyLevel.MODIFICATION,
        summary="Archive and extract files (Tape Archive)",
        description=(
            "Bundles multiple files and directories into a single archive file (.tar), \n"
            "often compressed with gzip (.tar.gz). Standard format for Linux backups and packages."
        ),
        syntax="tar [options] [archive] [target_file_or_directory]",
        default_args="-czvf archive.tar.gz folder/",
        flags=(
            Flag(
                flag="-c",
                name="Create archive",
                description="Creates a new archive file.",
                example="tar -czvf backup.tar.gz src/",
            ),
            Flag(
                flag="-x",
                name="Extract archive",
                description="Extracts files out of an existing archive.",
                example="tar -xzvf backup.tar.gz",
            ),
            Flag(
                flag="-z",
                name="Gzip compression",
                description="Compresses or uncompresses the archive using gzip algorithm.",
                example="tar -czvf data.tar.gz data/",
            ),
            Flag(
                flag="-v",
                name="Verbose",
                description="Lists all files as they are being packed or unpacked.",
                example="tar -xvf package.tar",
            ),
            Flag(
                flag="-f",
                name="Archive file specification",
                description="Specifies the archive file name. Must be followed immediately by file.",
                example="tar -tf archive.tar.gz",
            ),
            Flag(
                flag="-t",
                name="Table of contents (preview)",
                description="Lists files in archive without extracting them to disk.",
                example="tar -tf backup.tar.gz",
            ),
        ),
        examples=(
            CommandExample(
                command="tar -czvf backup.tar.gz ./src",
                description="Create a compressed .tar.gz archive of the ./src directory",
            ),
            CommandExample(
                command="tar -xzvf backup.tar.gz",
                description="Extract a compressed .tar.gz archive into current directory",
            ),
            CommandExample(
                command="tar -tvf backup.tar.gz",
                description="Preview all files inside an archive without extracting",
            ),
        ),
        notes="Remember the mnemonic: -czvf to Create, -xzvf to eXtract.",
    ),
)