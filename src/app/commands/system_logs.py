from __future__ import annotations

from types import MappingProxyType
from typing import Final, Iterable

from app.models import Category, Command, CommandExample, Flag, SafetyLevel

SYSTEM_LOGS_COMMANDS: Final[tuple[Command, ...]] = (
    Command(
        name="journalctl",
        category=Category.SYSTEM_LOGS,
        safety_level=SafetyLevel.READ_ONLY,
        summary="Query and inspect systemd journal logs",
        description=(
            "The primary log inspection tool on modern Linux distributions. \n"
            "Collects kernel logs, system service messages, and boot history into "
            "a unified, searchable journal."
        ),
        syntax="journalctl [options]",
        default_args="-n 50 --no-pager",
        flags=(
            Flag(
                flag="-u",
                name="Service unit filter",
                description="Filters logs to a specific systemd service (e.g., nginx, ssh). ",
                example="journalctl -u ssh.service",
            ),
            Flag(
                flag="-f",
                name="Follow real-time logs",
                description="Streams new logs live as they are generated (press Ctrl+C to stop).",
                example="journalctl -f",
            ),
            Flag(
                flag="-b",
                name="Current boot only",
                description="Shows only messages generated during the current boot cycle.",
                example="journalctl -b",
            ),
            Flag(
                flag="-n",
                name="Line count",
                description="Outputs only the most recent N lines.",
                example="journalctl -n 50",
            ),
            Flag(
                flag="-p",
                name="Priority filter",
                description="Filters by severity: emerg, alert, crit, err, warning, notice, info.",
                example="journalctl -p err -b",
            ),
        ),
        examples=(
            CommandExample(
                command="journalctl -u ssh.service -n 50",
                description="View the last 50 log entries for SSH service",
            ),
            CommandExample(
                command="journalctl -f",
                description="Stream live incoming system logs",
            ),
            CommandExample(
                command="journalctl -p err -b",
                description="View all system error logs generated since current boot",
            ),
        ),
        notes="Safe to run. If full system logs require permissions, run with sudo.",
    ),
    Command(
        name="dmesg",
        category=Category.SYSTEM_LOGS,
        safety_level=SafetyLevel.READ_ONLY,
        summary="Display kernel ring buffer messages",
        description=(
            "Prints low-level kernel log messages. Essential for diagnosing \n"
            "hardware recognition, device drivers, USB connections, and memory errors."
        ),
        syntax="dmesg [options]",
        default_args="-T | tail -n 30",
        flags=(
            Flag(
                flag="-T",
                name="Human-readable timestamps",
                description="Prints readable date/time instead of raw seconds since boot.",
                example="dmesg -T",
            ),
            Flag(
                flag="-l",
                name="Log level filter",
                description="Restricts output to levels: emerg, alert, crit, err, warn, notice, info.",
                example="dmesg -l err,warn",
            ),
            Flag(
                flag="-w",
                name="Follow / watch",
                description="Waits for and prints new kernel messages in real time.",
                example="dmesg -w",
            ),
        ),
        examples=(
            CommandExample(
                command="dmesg -T | tail -n 30",
                description="View the 30 most recent kernel messages with timestamps",
            ),
            CommandExample(
                command="dmesg -l err",
                description="Show only kernel error messages",
            ),
        ),
        notes="Helpful when inserting USB devices or investigating kernel driver crashes.",
    ),
    Command(
        name="tail",
        category=Category.SYSTEM_LOGS,
        safety_level=SafetyLevel.READ_ONLY,
        summary="Output the last part of files",
        description=(
            "Displays the ending lines of files (default 10 lines). Commonly used \n"
            "with '-f' to monitor active log files in real time as events occur."
        ),
        syntax="tail [options] [file...]",
        default_args="-n 20 /var/log/syslog",
        flags=(
            Flag(
                flag="-n",
                name="Line count",
                description="Outputs the last N lines instead of the default 10.",
                example="tail -n 50 app.log",
            ),
            Flag(
                flag="-f",
                name="Follow (live updates)",
                description="Continues outputting new lines appended to file (Ctrl+C to stop).",
                example="tail -f /var/log/syslog",
            ),
        ),
        examples=(
            CommandExample(
                command="tail -n 50 /var/log/syslog",
                description="View last 50 lines of system log",
            ),
            CommandExample(
                command="tail -f /var/log/syslog",
                description="Stream system log live as new entries are written",
            ),
        ),
        notes="Combine with grep using pipes: tail -f app.log | grep -i 'error'.",
    ),
    Command(
        name="head",
        category=Category.SYSTEM_LOGS,
        safety_level=SafetyLevel.READ_ONLY,
        summary="Output the first part of files",
        description=(
            "Displays the beginning lines of files (default 10 lines). Helpful \n"
            "for inspecting data headers, CSV column titles, or file formats."
        ),
        syntax="head [options] [file...]",
        default_args="-n 15 /etc/passwd",
        flags=(
            Flag(
                flag="-n",
                name="Line count",
                description="Outputs the first N lines instead of default 10.",
                example="head -n 25 file.txt",
            ),
            Flag(
                flag="-c",
                name="Byte count",
                description="Outputs the first N bytes of the file.",
                example="head -c 100 data.bin",
            ),
        ),
        examples=(
            CommandExample(
                command="head -n 15 /etc/passwd",
                description="View the first 15 system user accounts",
            ),
            CommandExample(
                command="head -n 1 data.csv",
                description="Quickly inspect CSV header column names",
            ),
        ),
        notes="Fast way to examine file headers without loading large files into memory.",
    ),
    Command(
        name="grep",
        category=Category.SYSTEM_LOGS,
        safety_level=SafetyLevel.READ_ONLY,
        summary="Search text using patterns or keywords",
        description=(
            "Searches input files or piped terminal output for lines matching a pattern. \n"
            "One of the most versatile diagnostic and filtering tools in Linux."
        ),
        syntax="grep [options] <pattern> [file...]",
        default_args="-in 'error' /var/log/syslog",
        flags=(
            Flag(
                flag="-i",
                name="Ignore case",
                description="Case-insensitive match ('error', 'Error', 'ERROR' all match).",
                example="grep -i 'failed' auth.log",
            ),
            Flag(
                flag="-r",
                name="Recursive",
                description="Searches all files under each directory recursively.",
                example="grep -r 'PORT' src/",
            ),
            Flag(
                flag="-n",
                name="Line number",
                description="Prefixes each matching line with its line number in the file.",
                example="grep -n 'def main' script.py",
            ),
            Flag(
                flag="-v",
                name="Invert match",
                description="Outputs lines that do NOT match the specified pattern.",
                example="grep -v '^#' config.conf",
            ),
            Flag(
                flag="-C",
                name="Context lines",
                description="Prints N lines of surrounding context before and after each match.",
                example="grep -C 3 'CRITICAL' app.log",
            ),
        ),
        examples=(
            CommandExample(
                command="grep -in 'error' /var/log/syslog",
                description="Search system log case-insensitively for 'error' with line numbers",
            ),
            CommandExample(
                command="grep -rn 'TODO' ./src",
                description="Find all TODO comments across project source code",
            ),
            CommandExample(
                command="grep -v '^#' /etc/fstab",
                description="View fstab configuration excluding comment lines",
            ),
        ),
        notes="Always enclose search patterns in quotes when searching phrases or regex.",
    ),
    Command(
        name="less",
        category=Category.SYSTEM_LOGS,
        safety_level=SafetyLevel.READ_ONLY,
        summary="Terminal pager for viewing long files",
        description=(
            "Opens text files in an interactive pager allowing smooth forward and backward \n"
            "scrolling. Unlike editors, does not read the entire file before starting."
        ),
        syntax="less [options] [file]",
        default_args="-N /var/log/syslog",
        flags=(
            Flag(
                flag="-N",
                name="Line numbers",
                description="Displays line numbers next to each line.",
                example="less -N large_file.log",
            ),
            Flag(
                flag="-S",
                name="Chop long lines",
                description="Disables line wrapping and enables horizontal arrow scrolling.",
                example="less -S data.tsv",
            ),
            Flag(
                flag="+F",
                name="Follow mode",
                description="Starts in follow mode similar to 'tail -f'. Press Ctrl+C to pause.",
                example="less +F /var/log/syslog",
            ),
        ),
        examples=(
            CommandExample(
                command="less /var/log/syslog",
                description="Interactively browse syslog (press 'q' to quit, '/' to search)",
            ),
            CommandExample(
                command="journalctl | less",
                description="Scroll through system journal output page by page",
            ),
        ),
        notes="Navigation keys: 'Space' (page down), 'b' (page up), '/' (search), 'q' (quit).",
    ),
    Command(
        name="uptime",
        category=Category.SYSTEM_LOGS,
        safety_level=SafetyLevel.READ_ONLY,
        summary="Show system running duration and load averages",
        description=(
            "Displays the current time, how long the system has been continuously \n"
            "running, the count of active logged-in users, and system CPU load averages \n"
            "over the last 1, 5, and 15 minutes."
        ),
        syntax="uptime [options]",
        default_args="-p",
        flags=(
            Flag(
                flag="-p",
                name="Pretty format",
                description="Displays uptime in a friendly format (e.g. 'up 2 hours, 15 minutes').",
                example="uptime -p",
            ),
            Flag(
                flag="-s",
                name="Since date/time",
                description="Displays the exact date and timestamp when the system booted.",
                example="uptime -s",
            ),
        ),
        examples=(
            CommandExample(
                command="uptime",
                description="Show full system status, active users, and 1/5/15 min load averages",
            ),
            CommandExample(
                command="uptime -p",
                description="Show clean human-readable uptime duration",
            ),
        ),
        notes="Safe and fast way to check if a machine was recently rebooted or is under high load.",
    ),
)
