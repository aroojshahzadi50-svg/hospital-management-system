import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="tiger",
    database="12b"
)

mycursor = mydb.cursor()

# Create tables
mycursor.execute("""
CREATE TABLE IF NOT EXISTS DOCTOR (
    doctorid INT PRIMARY KEY,
    doctorname VARCHAR(50),
    specialization VARCHAR(50)
)
""")

mycursor.execute("""
CREATE TABLE IF NOT EXISTS PATIENTS (
    patientid INT AUTO_INCREMENT PRIMARY KEY,
    patientname VARCHAR(50),
    disease VARCHAR(50),
    bloodtype VARCHAR(5),
    checkup_date DATE,
    appointment_date DATE,
    doctorid INT,
    FOREIGN KEY (doctorid) REFERENCES DOCTOR(doctorid)
        ON DELETE SET NULL ON UPDATE CASCADE
)
""")


# --- Doctor functions ---
def add_doctor():
    doctorname = input("Enter Doctor Name: ")
    specialization = input("Enter Specialization: ")
    sql = "INSERT INTO DOCTOR (doctorname, specialization) VALUES (%s, %s)"
    val = (doctorname, specialization)
    mycursor.execute(sql, val)
    mydb.commit()
    print("Doctor added successfully!\n")


def view_doctors():
    mycursor.execute("SELECT * FROM DOCTOR")
    result = mycursor.fetchall()
    print("\n--- DOCTOR RECORDS ---")
    if not result:
        print("No doctors found.")
    else:
        print(f"{'Doctor ID':<30} | {'Name':<30} | {'Specialization':<30}")
        print("-" * 100)
        for row in result:
            print(f"{str(row[0]):<30} | {str(row[1]):<30} | {str(row[2]):<30}")
        print("-" * 100)


def update_doctor():
    doctorid = int(input("Enter Doctor ID to update: "))
    new_specialization = input("Enter new specialization: ")
    sql = "UPDATE DOCTOR SET specialization = %s WHERE doctorid = %s"
    val = (new_specialization, doctorid)
    mycursor.execute(sql, val)
    mydb.commit()
    if mycursor.rowcount > 0:
        print("Doctor updated successfully!\n")
    else:
        print("No doctor found with that ID.\n")


def delete_doctor():
    doctorid = int(input("Enter Doctor ID to delete: "))
    sql = "DELETE FROM DOCTOR WHERE doctorid = %s"
    mycursor.execute(sql, (doctorid,))
    mydb.commit()
    if mycursor.rowcount > 0:
        print("Doctor deleted successfully!\n")
    else:
        print("No doctor found with that ID.\n")


# --- Patient functions ---
def add_patient():
    patientname = input("Enter Patient Name: ")
    disease = input("Enter Disease: ")
    bloodtype = input("Enter Blood Type (e.g. A+, O-): ")
    checkup_date = input("Enter Checkup Date (YYYY-MM-DD): ")
    appointment_date = input("Enter Appointment Date (YYYY-MM-DD): ")
    view_doctors()
    doctorid = int(input("Enter Doctor ID assigned to this patient (or 0 if none): "))
    if doctorid == 0:
        doctorid = None
    sql = """INSERT INTO PATIENTS
              (patientname, disease, bloodtype, checkup_date, appointment_date, doctorid)
              VALUES (%s, %s, %s, %s, %s, %s)"""
    val = (patientname, disease, bloodtype, checkup_date, appointment_date, doctorid)
    mycursor.execute(sql, val)
    mydb.commit()
    print("Patient added successfully!\n")


def view_patients():
    mycursor.execute("""
        SELECT
            p.patientid,
            p.patientname,
            p.disease,
            p.bloodtype,
            p.checkup_date,
            p.appointment_date,
            d.doctorname
        FROM PATIENTS p
        LEFT JOIN DOCTOR d ON p.doctorid = d.doctorid;
    """)
    result = mycursor.fetchall()
    print("\n--- PATIENT RECORDS ---")
    if not result:
        print("No patient records found.")
    else:
        header = (
            f"{'Patient ID':<30}|"
            f"{'Name':<30}|"
            f"{'Disease':<30}|"
            f"{'Blood Type':<30}|"
            f"{'Checkup Date':<30}|"
            f"{'Appointment Date':<30}|"
            f"{'Doctor':<30}"
        )
        print(header)
        print("-" * len(header))
        for row in result:
            print(
                f"{str(row[0]):<30}|"
                f"{str(row[1]):<30}|"
                f"{str(row[2]):<30}|"
                f"{str(row[3]):<30}|"
                f"{str(row[4]):<30}|"
                f"{str(row[5]):<30}|"
                f"{str(row[6] if row[6] else 'N/A'):<30}"
            )
        print("-" * len(header))


def update_disease():
    patientid = int(input("Enter Patient ID to update: "))
    new_disease = input("Enter new disease: ")
    sql = "UPDATE PATIENTS SET disease = %s WHERE patientid = %s"
    val = (new_disease, patientid)
    mycursor.execute(sql, val)
    mydb.commit()
    if mycursor.rowcount > 0:
        print("Disease updated successfully!\n")
    else:
        print("No patient found with that ID.\n")


def delete_patient():
    patientid = int(input("Enter Patient ID to delete: "))
    sql = "DELETE FROM PATIENTS WHERE patientid = %s"
    mycursor.execute(sql, (patientid,))
    mydb.commit()
    if mycursor.rowcount > 0:
        print("Patient deleted successfully!\n")
    else:
        print("No patient found with that ID.\n")


def search_patient():
    patientname = input("Enter patient name to search: ").strip()
    if not patientname:
        print("Patient name cannot be empty.\n")
        return
    sql = """
        SELECT p.patientid, p.patientname, p.disease,
               p.bloodtype, p.checkup_date, p.appointment_date,
               d.doctorname
        FROM patients p
        LEFT JOIN doctor d ON p.doctorid = d.doctorid
        WHERE LOWER(p.patientname) LIKE LOWER(%s)
    """
    val = (f"%{patientname}%",)
    mycursor.execute(sql, val)
    results = mycursor.fetchall()
    if results:
        print("\n--- Patient Search Results ---")
        for row in results:
            print(f"""
Patient ID        : {row[0]}
Name               : {row[1]}
Disease            : {row[2]}
Blood Type         : {row[3]}
Checkup Date       : {row[4]}
Appointment Date   : {row[5]}
Doctor             : {row[6] if row[6] else 'N/A'}
""")
    else:
        print("No patient found with that name.\n")


def update_patient_doctor():
    patientid = int(input("Enter Patient ID to update doctor for: "))
    view_doctors()
    doctorid = int(input("Enter new Doctor ID assigned to this patient (or 0 if none): "))
    if doctorid == 0:
        doctorid = None
    sql = "UPDATE PATIENTS SET doctorid = %s WHERE patientid = %s"
    val = (doctorid, patientid)
    mycursor.execute(sql, val)
    mydb.commit()
    if mycursor.rowcount > 0:
        print("Patient's doctor updated successfully!\n")
    else:
        print("No patient found with that ID.\n")


# --- Menus ---
def admin_menu():
    while True:
        print("""
--- ADMIN / STAFF MENU ---
1. Add Doctor
2. View All Doctors
3. Update Doctor Specialization
4. Delete Doctor
5. Add Patient
6. View All Patients
7. Update Patient Disease
8. Delete Patient
9. Search Patient by Name
10. Logout
11. Update Patient's Doctor
""")
        choice = input("Enter choice (1-11): ")
        if choice == '1':
            add_doctor()
        elif choice == '2':
            view_doctors()
        elif choice == '3':
            update_doctor()
        elif choice == '4':
            delete_doctor()
        elif choice == '5':
            add_patient()
        elif choice == '6':
            view_patients()
        elif choice == '7':
            update_disease()
        elif choice == '8':
            delete_patient()
        elif choice == '9':
            search_patient()
        elif choice == '10':
            print("Logging out of Admin Menu...")
            break
        elif choice == '11':
            update_patient_doctor()
        else:
            print("Invalid choice! Please enter 1-11.\n")


def patient_menu():
    while True:
        print("""
--- PATIENT MENU ---
1. View All Doctors
2. Search for Your Record
3. Exit
""")
        choice = input("Enter choice (1-3): ")
        if choice == '1':
            view_doctors()
        elif choice == '2':
            search_patient()
        elif choice == '3':
            print("Exiting Patient Menu...")
            break
        else:
            print("Invalid choice! Please enter 1-3.\n")


def main():
    print("--- Welcome to the Hospital Management System ---")
    while True:
        print("\nLogin as:")
        print("1. Admin / Staff")
        print("2. Patient")
        print("3. Exit Program")
        role = input("Enter your choice (1-3): ")
        if role == '1':
            password = input("Enter admin password: ")
            if password == "admin123":
                print("Login successful! Welcome, Admin.\n")
                admin_menu()
            else:
                print("Incorrect password. Access denied.\n")
        elif role == '2':
            print("Welcome, Patient!\n")
            patient_menu()
        elif role == '3':
            print("Exiting system... Goodbye!")
            break
        else:
            print("Invalid choice! Please enter 1-3.\n")


if __name__ == "__main__":
    main()
