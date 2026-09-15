# 🔐 Password Vault

A simple **password management vault built with Python** that securely stores and manages saved passwords using a **Master Password**.

The application requires the user to enter a **Master Password** before accessing the vault.

## ✨ Features

* 🔐 Master Password protection
* 🔑 Store and manage passwords
* 🗄️ Local JSON-based data storage
* 🐍 Built with Python
* 💻 Simple command-line interface
* 🔒 Keeps password data stored locally

## 📁 Project Structure

```text
Password-Generator/
│
├── vault.py
├── master.json
├── database.json
└── README.md
```

### Files

| File            | Purpose                                |
| --------------- | -------------------------------------- |
| `vault.py`      | Main Python application                |
| `master.json`   | Stores the Master Password information |
| `database.json` | Stores saved password data             |
| `README.md`     | Project documentation                  |

## 🚀 How to Run

### 1. Clone the Repository

```bash
git clone https://github.com/SannidhRaj/Password-Generator.git
```

### 2. Open the Project

```bash
cd Password-Generator
```

### 3. Run the Application

```bash
python vault.py
```

## 🔑 Master Password

When the application starts, it asks the user to enter the **Master Password**.

```text
Enter Master Password:
```

The Master Password is required to access the password vault.

### First-Time Setup

If the application is being used for the first time, follow the prompts to create your Master Password.

**Important:** Remember your Master Password. Losing it may prevent access to the stored vault data, depending on how the application handles authentication.

## 🗄️ Data Storage

The application uses JSON files for local storage:

```text
master.json
database.json
```

`master.json` contains the information required for Master Password authentication, while `database.json` contains the stored password data.

> ⚠️ **Security Note:** Do not share or publicly expose `master.json` or `database.json` if they contain real credentials or sensitive information.

For a real-world password manager, sensitive data should be protected using strong cryptographic techniques and secure key management.

## 🖥️ Usage

After entering the correct Master Password, you can access the vault and perform the available password-management operations provided by the application.

Typical workflow:

```text
Run vault.py
     ↓
Enter Master Password
     ↓
Authentication
     ↓
Access Password Vault
     ↓
Manage Stored Passwords
```

## 🛠️ Technologies Used

* **Python**
* **JSON**
* **Command Line Interface (CLI)**

## 🔮 Future Improvements

* [ ] Password encryption
* [ ] Password strength checker
* [ ] Secure password generator
* [ ] Copy password to clipboard
* [ ] Search saved passwords
* [ ] Delete/update stored credentials
* [ ] GUI version
* [ ] Use Python `secrets` module for secure password generation
* [ ] Add stronger authentication and encryption

## 👨‍💻 Author

**Sannidh Raj**

GitHub: [@SannidhRaj](https://github.com/SannidhRaj)

## ⭐ Support

If you find this project useful, consider giving the repository a ⭐ on GitHub.
