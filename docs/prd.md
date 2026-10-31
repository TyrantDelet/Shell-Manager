# PRD - 001: Shell Manager 

**Author:** Tyrant_Delet

**Date:** 27/10/2026

## Objective

**Problem:** Nowadays there are many new users starting with Linux, and many of them find it difficult to interact with commands in the terminal. This leads many of them to use AI to help them use terminal commands, which may lead users to use incorrect commands and possibly even make them break something important in the system, since AI is not always accurate to guide users to interact with terminal commands.

**Solution:** A program written in python that gives users an easy way to interact with all kinds of commands on a Linux terminal, such as an option menu with all commands explained and provided with their respective acronyms. This will prevent users to type commands they don't understand and will make it much easier for them to interact with a Linux terminal without risking bigger problems in the system due to incorrectly typed commands

## User Stories

**History 1:** As an user i want to make simple navigation commands to learn more about an Linux system, and the app will show me an list of navigation commands and describe what it does and it's options for me, making it easy for me to navigate and manipulate my Linux system.

**History 2:** As an user i want to manipulate directories and files for any type of objective, for example changing the /etc/fstab, cleaning the /tmp/, check the /usr/bin, and the app will show me a list of the correct commands to do this.

**History 3:** As an user i want to see the logs of an determined application on the system to check if an error has occurred, and the application will show me all the ways i can do this with the list of commands.

**History 4**: As an user i want to understand the logic behind Linux CLI using commands and interacting with the terminal in a way it doesn't break anything in the system, understanding that Linux does not have an "undo" command and the system assumes i know exactly what i'm doing, the app will help me out with the correct explanations for each command.

## MVP Scope

What is **STRICTLY** necessary for 1.0:

- Interactive menu framework: a lightweight menu (using python lib or standard input prompts).
- Graceful Navigation (such as "Exit", "Back" and "Next").
- Command Book: A structured format containing 20-30 foundational commands across Navigation, File Management and Logs.
- Exploded Command View: For each command display:
    - Purpose & plain-English explanation.
    - Common flags (such as -l, -h, -a).
    - Safety level (Read-only vs. Destructive/Requires sudo).
- Safe Execution / Copy-to-Clipboard Mode: Allow users to preview and confirm before running, or copy the command directly.
- Runtime: Python 3.12 

## Definition of Done

Project will be considered accomplished in 1.0 when:

- [ ] **Command Book Coverage:** At least 20 foundational commands are cataloged across the 3 core categories (Navigation, File Manipulation and System logs), with all the methods implemented. 

- [ ] **Exploded View & Safety Warnings:** Every command screen presents a plain-English explanation, breakdown of common flags (e.g., `-l`, `-h`, `-a`), and a clear visual warning if a command is destructive or requires `sudo` privileges.

- [ ] **Execution Safety Guardrail:** The user is always shown a full preview of the command before running it, and destructive/sudo commands require explicit confirmation (e.g., `[y/N]`) prior to execution.

- [ ] **Graceful Navigation & Exception Handling:** Users can navigate forward, return to previous menus ("Back"), and quit ("Exit" or `Ctrl+C`) from any screen without exposing raw Python tracebacks or crashing the session.

- [ ] **Environment Compatibility & Verification:** The application runs on Python 3.12 in a standard Linux terminal, successfully executes selected commands with real-time output, and handles invalid inputs gracefully.

## Out of Scope (For now)

To keep the focus and to guarantee the deployment of the project with the defined items above, are excluded from this version:

- GUI or Web Page, everything will be made CLI and with automated scripts.
- No custom command-creation by the user /  saving by the user.
