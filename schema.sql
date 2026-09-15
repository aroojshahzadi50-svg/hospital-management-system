-- Hospital Admission Management System
-- Database schema (MySQL)

CREATE DATABASE IF NOT EXISTS `12b`;
USE `12b`;

CREATE TABLE IF NOT EXISTS DOCTOR (
    doctorid INT PRIMARY KEY,
    doctorname VARCHAR(50),
    specialization VARCHAR(50)
);

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
);
