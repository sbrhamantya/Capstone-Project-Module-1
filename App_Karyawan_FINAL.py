import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import seaborn as sns
import numpy as np
print("=== FILE BERJALAN ===")
print("Loading aplikasi...")
# Koneksi ke database
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "qwerty123",
    "database": "employee_management"
}

def connect_db():
    """Fungsi untuk koneksi ke database MySQL"""
    return mysql.connector.connect(**DB_CONFIG)

def format_currency(value):
    """Fungsi untuk format angka dengan separator ribuan"""
    return f"{value:,.0f}".replace(",", ".")

# 1. Read Table
def read_table():
    """Menampilkan tabel data karyawan"""
    conn = connect_db()
    df = pd.read_sql('SELECT * FROM karyawan;', conn)

    df_display = df.copy()
    df_display['gaji'] = df_display['gaji'].apply(lambda x: format_currency(x))

    print("\n" + "="*80)
    print("DATA KARYAWAN".center(80))
    print("="*80)

    with pd.option_context(
        'display.max_rows', None,
        'display.max_columns', None,
        'display.width', 200,
        'display.colheader_justify', 'left'
    ):
        print(df_display.to_string(index=False))

    print("="*80)
    print(f"Total Karyawan: {len(df_display)} orang\n")

    conn.close()

# 2. Show Statistik - Lengkap dengan MEAN, MEDIAN, MIN, MAX, dll
def show_statistik(kolom):
    """Menampilkan statistik deskriptif lengkap untuk kolom numerik"""
    conn = connect_db()
    df = pd.read_sql('SELECT * FROM karyawan;', conn)

    print("\n" + "="*60)
    print(f"STATISTIK DESKRIPTIF - {kolom.upper()}".center(60))
    print("="*60)

    if kolom == 'gaji':
        stats = df[kolom].describe()
        print(f"Jumlah Data    : {int(stats['count'])}")
        print(f"Rata-rata      : Rp {format_currency(stats['mean'])}")
        print(f"Median         : Rp {format_currency(df[kolom].median())}")
        print(f"Std Deviasi    : Rp {format_currency(stats['std'])}")
        print(f"Minimum        : Rp {format_currency(stats['min'])}")
        print(f"Quartile 1     : Rp {format_currency(stats['25%'])}")
        print(f"Quartile 2     : Rp {format_currency(stats['50%'])}")
        print(f"Quartile 3     : Rp {format_currency(stats['75%'])}")
        print(f"Maximum        : Rp {format_currency(stats['max'])}")
    else:
        stats = df[kolom].describe()
        print(f"Jumlah Data    : {int(stats['count'])}")
        print(f"Rata-rata      : {stats['mean']:.2f} tahun")
        print(f"Median         : {df[kolom].median():.2f} tahun")
        print(f"Std Deviasi    : {stats['std']:.2f}")
        print(f"Minimum        : {int(stats['min'])} tahun")
        print(f"Quartile 1     : {stats['25%']:.2f} tahun")
        print(f"Quartile 2     : {stats['50%']:.2f} tahun")
        print(f"Quartile 3     : {stats['75%']:.2f} tahun")
        print(f"Maximum        : {int(stats['max'])} tahun")

    print("="*60 + "\n")
    conn.close()

# 3. Data Visualization - Lengkap dengan berbagai jenis visualisasi
def data_visualization():
    """Menampilkan berbagai jenis visualisasi data karyawan"""
    conn = connect_db()
    df = pd.read_sql('SELECT * FROM karyawan;', conn)

    print("\n" + "="*60)
    print("VISUALISASI DATA KARYAWAN".center(60))
    print("="*60)
    print("Pilih jenis visualisasi:")
    print("1. Pie Chart - Distribusi Karyawan per Departemen")
    print("2. Bar Chart - Rata-rata Gaji per Departemen")
    print("3. Heatmap - Gaji vs Departemen dan Lama Bekerja")
    print("4. Box Plot - Distribusi Gaji per Departemen")
    print("5. Scatter Plot - Hubungan Gaji dan Lama Bekerja")
    print("="*60)

    tipe_visual = input("Pilih visualisasi (1-5): ")

    if tipe_visual == '1':
        # Pie Chart - Distribusi Karyawan per Departemen
        plt.figure(figsize=(8, 8))
        dept_count = df['departemen'].value_counts()
        colors = plt.cm.Set3(range(len(dept_count)))
        plt.pie(dept_count.values, labels=dept_count.index, autopct='%1.1f%%',
                startangle=90, colors=colors, explode=[0.05]*len(dept_count))
        plt.title('Distribusi Karyawan per Departemen', fontsize=14, fontweight='bold')
        plt.axis('equal')
        plt.tight_layout()
        plt.show()

    elif tipe_visual == '2':
        # Bar Chart - Rata-rata Gaji per Departemen
        plt.figure(figsize=(10, 6))
        avg_salary = df.groupby('departemen')['gaji'].mean().sort_values(ascending=False)
        bars = plt.bar(avg_salary.index, avg_salary.values, color='skyblue', edgecolor='navy')

        plt.xlabel('Departemen', fontsize=12, fontweight='bold')
        plt.ylabel('Rata-rata Gaji (Rp)', fontsize=12, fontweight='bold')
        plt.title('Rata-rata Gaji per Departemen', fontsize=14, fontweight='bold')
        plt.xticks(rotation=45, ha='right')

        # Label di atas bar dalam juta
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height,
                     f'Rp {height:.1f} jt',
                     ha='center', va='bottom', fontsize=10)

        # Format sumbu Y dalam juta
        ax = plt.gca()
        ax.yaxis.set_major_formatter(
            mtick.FuncFormatter(lambda x, pos: f'Rp {x:.1f} jt')
        )

        plt.tight_layout()
        plt.show()

    elif tipe_visual == '3':
        # Heatmap - Gaji vs Departemen dan Lama Bekerja
        plt.figure(figsize=(10, 6))
        pivot_data = df.pivot_table(values='gaji', index='departemen', 
                                     columns='lama_bekerja', aggfunc='mean')
        sns.heatmap(pivot_data, annot=True, fmt='.0f', cmap='YlOrRd', 
                    cbar_kws={'label': 'Gaji (Rp)'})
        plt.title('Heatmap Gaji berdasarkan Departemen dan Lama Bekerja', 
                  fontsize=14, fontweight='bold')
        plt.xlabel('Lama Bekerja (tahun)', fontsize=12, fontweight='bold')
        plt.ylabel('Departemen', fontsize=12, fontweight='bold')
        plt.tight_layout()
        plt.show()

    elif tipe_visual == '4':
        # Box Plot - Distribusi Gaji per Departemen
        plt.figure(figsize=(10, 6))
        df.boxplot(column='gaji', by='departemen', grid=False, patch_artist=True)
        plt.suptitle('')
        plt.title('Distribusi Gaji per Departemen (Box Plot)', fontsize=14, fontweight='bold')
        plt.xlabel('Departemen', fontsize=12, fontweight='bold')
        plt.ylabel('Gaji (Rp)', fontsize=12, fontweight='bold')

        # Format sumbu Y dalam juta rupiah
        ax = plt.gca()
        ax.yaxis.set_major_formatter(
            mtick.FuncFormatter(lambda x, pos: f'Rp {x/1_000_000:.1f} jt')
        )

        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.show()

    elif tipe_visual == '5':
        # Scatter Plot - Hubungan Gaji vs Lama Bekerja
        plt.figure(figsize=(10, 6))

        departments = df['departemen'].unique()
        colors = plt.cm.Set3(range(len(departments)))

        for dept, color in zip(departments, colors):
            dept_data = df[df['departemen'] == dept]
            plt.scatter(
                dept_data['lama_bekerja'],
                dept_data['gaji'],
                label=dept,
                alpha=0.7,
                s=100,
                color=color,
                edgecolors='black'
            )

        plt.xlabel('Lama Bekerja (tahun)', fontsize=12, fontweight='bold')
        plt.ylabel('Gaji (Rp)', fontsize=12, fontweight='bold')
        plt.title('Hubungan antara Lama Bekerja dan Gaji', fontsize=14, fontweight='bold')
        plt.legend(title='Departemen', bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.grid(True, alpha=0.3)

        # Format sumbu Y dalam juta rupiah
        ax = plt.gca()
        ax.yaxis.set_major_formatter(
            mtick.FuncFormatter(lambda x, pos: f'Rp {x:.1f} jt')
        )

        plt.tight_layout()
        plt.show()

    else:
        print("\nPilihan tidak valid!")

    conn.close()

# 4. Add Data - Dengan Validasi Input
def add_data():
    """Menambahkan data karyawan baru dengan validasi input"""
    conn = connect_db()
    cursor = conn.cursor()

    print("\n" + "="*60)
    print("TAMBAH DATA KARYAWAN BARU".center(60))
    print("="*60)

    try:
        id_karyawan = input("ID Karyawan (contoh: EMP011): ").strip()

        # Cek apakah ID sudah ada
        cursor.execute("SELECT id_karyawan FROM karyawan WHERE id_karyawan = %s", (id_karyawan,))
        if cursor.fetchone():
            print("\nError: ID Karyawan sudah ada!")
            conn.close()
            return

        nama = input("Nama: ").strip()
        departemen = input("Departemen (Finance/HR/IT/Marketing/Operations): ").strip()
        gaji_input = input("Gaji: ").strip()
        gaji = float(gaji_input)
        lama_bekerja_input = input("Lama Bekerja (tahun): ").strip()
        lama_bekerja = int(lama_bekerja_input)

        # Validasi input
        if not all([id_karyawan, nama, departemen]):
            print("\nError: Semua field harus diisi!")
            conn.close()
            return

        if gaji <= 0 or lama_bekerja < 0:
            print("\nError: Gaji harus positif dan lama bekerja tidak boleh negatif!")
            conn.close()
            return

        # Insert data
        query = """INSERT INTO karyawan (id_karyawan, nama, departemen, gaji, lama_bekerja) 
                   VALUES (%s, %s, %s, %s, %s)"""
        cursor.execute(query, (id_karyawan, nama, departemen, gaji, lama_bekerja))
        conn.commit()

        print("\n" + "="*60)
        print("Data berhasil ditambahkan!".center(60))
        print("="*60 + "\n")

    except ValueError:
        print("\nError: Format input tidak valid! Gaji dan lama bekerja harus berupa angka.")
    except mysql.connector.Error as err:
        print(f"\nError database: {err}")
    finally:
        cursor.close()
        conn.close()

# 5. Update Data - Dengan Validasi
def update_data():
    """Mengupdate data karyawan dengan validasi"""
    conn = connect_db()
    cursor = conn.cursor()

    print("\n" + "="*60)
    print("UPDATE DATA KARYAWAN".center(60))
    print("="*60)

    id_karyawan = input("Masukkan ID Karyawan yang akan diupdate: ").strip()

    # Cek apakah ID ada
    cursor.execute("SELECT * FROM karyawan WHERE id_karyawan = %s", (id_karyawan,))
    if not cursor.fetchone():
        print("\nError: ID Karyawan tidak ditemukan!")
        conn.close()
        return

    print("\nKolom yang dapat diupdate:")
    print("1. Nama")
    print("2. Departemen")
    print("3. Gaji")
    print("4. Lama Bekerja")

    pilihan = input("Pilih kolom (1-4): ").strip()

    try:
        if pilihan == '1':
            nilai_baru = input("Nama baru: ").strip()
            cursor.execute("UPDATE karyawan SET nama = %s WHERE id_karyawan = %s", 
                          (nilai_baru, id_karyawan))
        elif pilihan == '2':
            nilai_baru = input("Departemen baru: ").strip()
            cursor.execute("UPDATE karyawan SET departemen = %s WHERE id_karyawan = %s", 
                          (nilai_baru, id_karyawan))
        elif pilihan == '3':
            nilai_baru = float(input("Gaji baru: ").strip())
            cursor.execute("UPDATE karyawan SET gaji = %s WHERE id_karyawan = %s", 
                          (nilai_baru, id_karyawan))
        elif pilihan == '4':
            nilai_baru = int(input("Lama Bekerja baru (tahun): ").strip())
            cursor.execute("UPDATE karyawan SET lama_bekerja = %s WHERE id_karyawan = %s", 
                          (nilai_baru, id_karyawan))
        else:
            print("\nPilihan tidak valid!")
            conn.close()
            return

        conn.commit()
        print("\n" + "="*60)
        print("Data berhasil diupdate!".center(60))
        print("="*60 + "\n")

    except ValueError:
        print("\nError: Format input tidak valid!")
    except mysql.connector.Error as err:
        print(f"\nError database: {err}")
    finally:
        cursor.close()
        conn.close()

# 6. Delete Data - Dengan Konfirmasi
def delete_data():
    """Menghapus data karyawan dengan konfirmasi"""
    conn = connect_db()
    cursor = conn.cursor()

    print("\n" + "="*60)
    print("HAPUS DATA KARYAWAN".center(60))
    print("="*60)

    id_karyawan = input("Masukkan ID Karyawan yang akan dihapus: ").strip()

    # Cek apakah ID ada dan tampilkan datanya
    cursor.execute("SELECT * FROM karyawan WHERE id_karyawan = %s", (id_karyawan,))
    data = cursor.fetchone()

    if not data:
        print("\nError: ID Karyawan tidak ditemukan!")
        conn.close()
        return

    print(f"\nData yang akan dihapus:")
    print(f"ID        : {data[0]}")
    print(f"Nama      : {data[1]}")
    print(f"Departemen: {data[2]}")
    print(f"Gaji      : Rp {format_currency(data[3])}")
    print(f"Lama Kerja: {data[4]} tahun")

    konfirmasi = input("\nApakah Anda yakin ingin menghapus data ini? (y/n): ").strip().lower()

    if konfirmasi == 'y':
        try:
            cursor.execute("DELETE FROM karyawan WHERE id_karyawan = %s", (id_karyawan,))
            conn.commit()
            print("\n" + "="*60)
            print("Data berhasil dihapus!".center(60))
            print("="*60 + "\n")
        except mysql.connector.Error as err:
            print(f"\nError database: {err}")
    else:
        print("\nPenghapusan dibatalkan.")

    cursor.close()
    conn.close()

# Menu Utama
def main():
    """Menu utama aplikasi"""
    while True:
        print("\n" + "="*60)
        print("APLIKASI MANAJEMEN DATA KARYAWAN".center(60))
        print("="*60)
        print("1. Tampilkan Data Karyawan")
        print("2. Statistik Deskriptif")
        print("3. Visualisasi Data")
        print("4. Tambah Data Karyawan")
        print("5. Update Data Karyawan")
        print("6. Hapus Data Karyawan")
        print("7. Keluar")
        print("="*60)

        pilihan = input("Pilih menu (1-7): ").strip()

        if pilihan == '1':
            read_table()
        elif pilihan == '2':
            print("\nPilih kolom untuk statistik:")
            print("1. Gaji")
            print("2. Lama Bekerja")
            kolom_pilihan = input("Pilih (1-2): ").strip()
            if kolom_pilihan == '1':
                show_statistik('gaji')
            elif kolom_pilihan == '2':
                show_statistik('lama_bekerja')
            else:
                print("\nPilihan tidak valid!")
        elif pilihan == '3':
            data_visualization()
        elif pilihan == '4':
            add_data()
        elif pilihan == '5':
            update_data()
        elif pilihan == '6':
            delete_data()
        elif pilihan == '7':
            print("\n" + "="*60)
            print("Terima kasih telah menggunakan aplikasi ini!".center(60))
            print("="*60 + "\n")
            break
        else:
            print("\nPilihan tidak valid! Silakan pilih 1-7.")

if __name__ == "__main__":
    main()
