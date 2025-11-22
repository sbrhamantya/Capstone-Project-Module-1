-- Database: employee_management
-- Dibuat untuk project aplikasi manajemen karyawan

-- Membuat database
CREATE DATABASE IF NOT EXISTS employee_management;
USE employee_management;

-- Membuat tabel karyawan
CREATE TABLE IF NOT EXISTS karyawan (
    id_karyawan VARCHAR(10) PRIMARY KEY,
    nama VARCHAR(100) NOT NULL,
    departemen VARCHAR(50) NOT NULL,
    gaji DECIMAL(12,2) NOT NULL,
    lama_bekerja INT NOT NULL
);

-- Insert data 10 karyawan
INSERT INTO karyawan (id_karyawan, nama, departemen, gaji, lama_bekerja) VALUES
('EMP001', 'Budi Santoso', 'Finance', 8500000.00, 5),
('EMP002', 'Siti Nurhaliza', 'HR', 7500000.00, 3),
('EMP003', 'Ahmad Fauzi', 'Operations', 9200000.00, 7),
('EMP004', 'Dewi Lestari', 'Finance', 8000000.00, 4),
('EMP005', 'Rudi Hartono', 'IT', 10500000.00, 6),
('EMP006', 'Maya Kusuma', 'Marketing', 7800000.00, 2),
('EMP007', 'Eko Prasetyo', 'Operations', 8800000.00, 5),
('EMP008', 'Rina Wati', 'IT', 9500000.00, 4),
('EMP009', 'Andi Wijaya', 'Marketing', 7200000.00, 1),
('EMP010', 'Linda Sari', 'HR', 8200000.00, 3);

-- Verifikasi data
SELECT * FROM karyawan;
