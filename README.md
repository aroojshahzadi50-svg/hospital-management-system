# Hospital Admission Management System

A command-line Hospital Admission Management System built with **Python** and **MySQL**, developed as a Class XII Informatics Practices (IP) project at Oasis International School, Al Ain.

## Overview

Managing patient details, doctor information, appointments, and treatments manually can be time-consuming and error-prone. This system provides a simple digital solution for hospital staff to register patients, manage doctor profiles, schedule appointments, and maintain medical histories — all from a terminal menu.

## Features

- **Admin / Staff login** (password protected) with full CRUD access
- Add, view, update, and delete **doctor** records
- Add, view, update, and delete **patient** records
- Assign / reassign a doctor to a patient
- Search for a patient by name
- Separate **Patient** menu for viewing doctors and looking up their own record
- Data persisted in a MySQL database with a foreign key link between patients and doctors

## Tech Stack

- Python 3
- MySQL (via `mysql-connector-python`)

## Database Design

**DOCTOR**

| Field | Type | Key |
|---|---|---|
| doctorid | INT | PRIMARY KEY |
| doctorname | VARCHAR(50) | |
| specialization | VARCHAR(50) | |

**PATIENTS**

| Field | Type | Key |
|---|---|---|
| patientid | INT (AUTO_INCREMENT) | PRIMARY KEY |
| patientname | VARCHAR(50) | |
| disease | VARCHAR(50) | |
| bloodtype | VARCHAR(5) | |
| checkup_date | DATE | |
| appointment_date | DATE | |
| doctorid | INT | FOREIGN KEY → DOCTOR(doctorid) |

See [`schema.sql`](./schema.sql) for the full table definitions.

## Setup

1. **Install MySQL** and make sure the server is running locally.
2. **Create the database and tables** — run the schema:
   ```bash
   mysql -u root -p < schema.sql
   ```
3. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Configure the connection** in `main.py` if your MySQL credentials differ from the defaults:
   ```python
   mydb = mysql.connector.connect(
       host="localhost",
       user="root",
       password="tiger",
       database="12b"
   )
   ```
5. **Run the program:**
   ```bash
   python main.py
   ```

## Usage

On launch, choose to log in as **Admin/Staff** (default password: `admin123`) or **Patient**, then follow the on-screen menu.

```
Login as:
1. Admin / Staff
2. Patient
3. Exit Program
```

Admins can manage doctors and patients via the numbered menu (add, view, update, delete, search, reassign doctor). Patients can view the list of doctors and search for their own record.

## Advantages

- Efficient, centralized digital record-keeping
- Reduces manual errors and saves staff time
- Faster access to patient and doctor information
- Improves coordination between doctors and staff
- Scalable as hospital data grows

## Future Enhancements

- Online appointment booking
- Automated billing
- Full electronic medical records
- Role-based access control
- Lab & pharmacy integration
- Appointment/medication reminders and alerts
- Data analytics/reporting dashboard
- Cloud backup
- Telemedicine / mobile support

## Acknowledgment

Developed as an Informatics Practices project 

## License

This project was created for academic purposes.
