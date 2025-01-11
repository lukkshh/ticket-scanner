# Ticket Scanner

Ticket Scanner is a simple ticket management system that allows event organizers to generate tickets, scan QR codes, and manage access control efficiently. This tool is perfect for real-time ticket verification, ensuring seamless check-ins at your events.

## Features

- **Generate Tickets**: Create unique tickets with a customizable prefix, saved as QR code images.
- **QR Code Scanning**: Verify tickets in real-time using a webcam.
- **SQLite Integration**: Store and manage tickets in a lightweight SQLite database.
- **Ticket Status Management**:
  - Check if a ticket is valid.
  - Identify if a ticket has already been used.
  - Handle invalid or non-existent tickets.
- **Ticket Operations**:
  - View all tickets.
  - Delete tickets by ID or UID.
  - Clear all tickets from the database.

---

## Installation

1. **Clone the Repository**

```bash
git clone https://github.com/yourusername/ticket-scanner.git

cd ticket-scanner
```

2. **Install Dependencies**

```bash
pip install -r requirements.txt
```

3. **Enjoy :)**

```bash
python main.py
```
