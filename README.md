# Password Generator
A secure and user-friendly Password Generator built using Python, offering both Command Line Interface (CLI) and Graphical User Interface (GUI) versions.
The application generates strong, customizable passwords and provides real-time strength analysis.
# Features
- Generate secure passwords with custom length
- Choose character types:
- Lowercase letters
- Uppercase letters
- Digits
- Special characters
- Easy / Medium / Strong password presets
- PIN and passphrase generation
- Password strength analysis (score & feedback)
- Save password history locally
- Copy passwords to clipboard
- Available in CLI and GUI (Tkinter)
# Technologies Used
- Python 3.7+
- Tkinter (for GUI)
- Python Standard Library only
(no external dependencies required)
# How It Works
1. User selects password length and options
2. Application generates a secure random password
3. Password strength is analyzed and displayed
4. User can copy or save the password
5. Saved passwords are stored locally in JSON format
# Data Storage
- Password history is saved automatically in: password_history.json
- File is created only when passwords are saved
- Can be deleted safely to clear history
# Purpose of This Project
### This project demonstrates:
- Secure random password generation
- Python object-oriented programming
- CLI and GUI development
- File handling with JSON
- User input validation
- Basic security best practices
