import json
from datetime import datetime
from prettytable import PrettyTable
import pwinput

admin_username = "admin"
admin_password = "admin123"

'''=================================================================================================================================='''
'''                                                         JSON                                                                     '''
'''=================================================================================================================================='''

def BacaData_bus():
    try:
        with open("bus.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def SimpanData_bus(data):
    with open("bus.json", "w") as file:
        json.dump(data, file, indent=4)

def bacadata_penumpang():
    try:
        with open("user.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def simpandata_penumpang(data):
    with open("user.json", "w") as file:
        json.dump(data, file, indent=4)

def bacadata_booking():
    try:
        with open("booking.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def simpandata_booking(data):
    with open("booking.json", "w") as file:
        json.dump(data, file, indent=4)



'''=================================================================================================================================='''
'''                                                         LOGIN                                                                    '''
'''=================================================================================================================================='''

def login():
    while True:
        print("\n=== SISTEM LOGIN ===")
        print("1. Login sebagai Admin")
        print("2. Login sebagai Penumpang")
        print("3. Keluar")

        pilihan = input("Pilih menu: ")

        if pilihan == "1":
            login_admin()
        elif pilihan == "2":
            login_penumpang()
        elif pilihan == "3":
            print("Terima kasih telah menggunakan sistem ini.")
            break
        else:
            print("Pilihan tidak valid!")


def login_admin():
    percobaan = 0
    while percobaan < 3:
        user = input("Masukkan username admin: ").lower()
        pw = pwinput.pwinput("Masukkan password admin: ")

        if user == admin_username and pw == admin_password:
            print("\nLogin admin berhasil!\n")
            menu_admin()
            return
        else:
            percobaan += 1
            print(f"Username/password salah! Percobaan ke-{percobaan}/3")

    print("Terlalu banyak percobaan gagal. Hubungi atasan untuk bantuan.\n")


def login_penumpang():
    while True:
        print("\n=== LOGIN PENUMPANG ===")
        print("1. Sudah punya akun")
        print("2. Belum punya akun")
        print("3. Kembali")

        pilih = input("Pilih: ")

        if pilih == "1":
            percobaan = 0
            data = bacadata_penumpang()
            while percobaan < 3:
                username = input("Username: ").lower()
                pw = pwinput.pwinput("Password: ")
                for p in data:
                    if p["username"] == username and p["password"] == pw:
                        print(f"\nSelamat datang, {username}!\n")
                        menu_penumpang_user(username)
                        return
                percobaan += 1
                print(f"Username/password salah! Percobaan ke-{percobaan}/3")

            print("Terlalu banyak percobaan gagal. Hubungi admin.\n")
            return

        elif pilih == "2":
            tambah_penumpang()
            print("\nSilakan login kembali...\n")
            continue

        elif pilih == "3":
            return
        else:
            print("Pilihan tidak valid!")


'''=================================================================================================================================='''
'''                                                         MENU ADMIN UTAMA                                                       '''
'''=================================================================================================================================='''

def menu_admin():
    while True:
        print("\n=== MENU ADMIN ===")
        print("1. Manajemen Bus")
        print("2. Manajemen Penumpang")
        print("3. Manajemen Booking Penumpang")
        print("4. Cek Penjualan Tiket")
        print("5. Logout")

        pilih = input("Pilih menu: ")

        if pilih == "1":
            menu_manajemen_bus()
        elif pilih == "2":
            menu_penumpang()
        elif pilih == "3":
            menu_booking()
        elif pilih == "4":
            cek_penjualan_tiket()
        elif pilih == "5":
            print("Logout berhasil.\n")
            break
        else:
            print("Pilihan tidak valid!")


'''=================================================================================================================================='''
'''                                                         MANAJEMEN BUS                                                            '''
'''=================================================================================================================================='''

def tampilkan_bus():
    data_bus = BacaData_bus()
    if not data_bus:
        print("Belum ada data bis.")
        return
    
    table = PrettyTable(["No", "Nomor Bus", "Nama", "Asal", "Tujuan", "Status", "Qty", "Terisi", "Harga"])
    for bus in data_bus:
        table.add_row([bus["no"], bus["nomor_bus"], bus["nama"], bus["asal"], bus["tujuan"], bus["status"], bus["qty"], bus["terisi"], bus["harga"]])
    print(table)

def tambah_bus():
    data_bus = BacaData_bus()
    print("\n=== Tambah Data Bis ===")
    no = len(data_bus) + 1
    nomor_bus = input("Nomor Bus: ")
    nama = input("Nama bis: ")
    asal = input("Asal: ")
    tujuan = input("Tujuan: ")
    status = "tersedia"

    while True:
        try:
            qty = int(input("Jumlah kursi: "))
            if qty > 0:
                break
            else:
                print("Jumlah kursi harus lebih dari 0.")
        except ValueError:
            print("Input tidak valid! Masukkan angka.")

    terisi = 0
    while True:
        try:
            harga = int(input("Harga tiket (10000-100000): "))
            if 10000 <= harga <= 100000:
                break
            else:
                print("Harga harus antara 10.000 - 100.000.")
        except ValueError:
            print("Masukkan angka!")

    data_baru = {
        "no": no,
        "nomor_bus": nomor_bus,
        "nama": nama,
        "asal": asal,
        "tujuan": tujuan,
        "status": status,
        "qty": qty,
        "terisi": terisi,
        "harga": harga
    }

    data_bus.append(data_baru)
    SimpanData_bus(data_bus)
    print("Bis berhasil ditambahkan!")

def update_statusbus(bus=None):
    if bus:
        if bus["terisi"] >= bus["qty"]:
            bus["status"] = "penuh"
            if bus["terisi"] > bus["qty"]:
                print(f"Peringatan: Bus {bus['nama']} kelebihan penumpang! Reset ke kapasitas maksimal.")
                bus["terisi"] = bus["qty"]
        else:
            bus["status"] = "tersedia"

        data_bus = BacaData_bus()
        for b in data_bus:
            if b["no"] == bus["no"]:
                b.update(bus)
        SimpanData_bus(data_bus)

    else:
        data_bus = BacaData_bus()
        for bus in data_bus:
            if bus["terisi"] >= bus["qty"]:
                bus["status"] = "penuh"
                if bus["terisi"] > bus["qty"]:
                    print(f"Peringatan: Bus {bus['nama']} kelebihan penumpang!")
                    bus["terisi"] = bus["qty"]
            else:
                bus["status"] = "tersedia"
        SimpanData_bus(data_bus)


def tambah_penumpangkonvensional(bus):
    tambah_penumpang = input("Apakah ingin menambah penumpang konvensional? (y/n): ").lower()
    if tambah_penumpang == "y":
        try:
            jumlah_tambah = int(input("Jumlah penumpang yang ingin ditambah: "))
            if jumlah_tambah <= 0:
                print("Jumlah penumpang tidak boleh 0 atau negatif.")
                return

            sisa_kursi = bus["qty"] - bus["terisi"]
            if sisa_kursi <= 0:
                print("Bus sudah penuh, tidak bisa menambah penumpang lagi.")
                bus["status"] = "penuh"
                return


            if jumlah_tambah <= sisa_kursi:
                bus["terisi"] += jumlah_tambah
                print(f"{jumlah_tambah} penumpang berhasil ditambahkan. Total terisi: {bus['terisi']}")
            else:
                print(f"Hanya {sisa_kursi} kursi tersisa. Bus akan penuh jika ditambah lebih dari itu.")
                bus["terisi"] = bus["qty"]
                bus["status"] = "penuh"
                print("Bus sekarang penuh.")

        except ValueError:
            print("Input jumlah penumpang tidak valid.")

def hapus_penumpangkonvensional(bus):
    hapus_penumpang = input("Apakah ingin menghapus penumpang konvensional? (y/n): ").lower()
    if hapus_penumpang == "y":
        try:
            jumlah_hapus = int(input("Jumlah penumpang yang ingin dihapus: "))
            if jumlah_hapus <= 0:
                print("Jumlah yang dihapus tidak boleh 0 atau negatif.")
                return

            if jumlah_hapus > bus["terisi"]:
                print(f"Tidak bisa menghapus {jumlah_hapus} penumpang. Bus hanya terisi {bus['terisi']} penumpang.")
                return

            bus["terisi"] -= jumlah_hapus
            print(f"{jumlah_hapus} penumpang berhasil dihapus. Total terisi: {bus['terisi']}")

            if bus["terisi"] < bus["qty"]:
                bus["status"] = "tersedia"
            else:
                bus["status"] = "penuh"

        except ValueError:
            print("Input jumlah penumpang tidak valid.")

def update_bus():
    data_bus = BacaData_bus()
    if not data_bus:
        print("Belum ada data bus untuk diperbarui.")
        return

    tampilkan_bus()
    try:
        no = int(input("Masukkan nomor bis yang ingin diupdate: "))
        for bus in data_bus:
            if bus["no"] == no:
                print(f"\n=== Update Data Bis: {bus['nama']} ===")
                print("Tekan Enter jika tidak ingin mengubah bagian tersebut. \n")

                bus["nama"] = input(f"Nama baru ({bus['nama']}): ") or bus["nama"]
                bus["asal"] = input(f"Asal baru ({bus['asal']}): ") or bus["asal"]
                bus["tujuan"] = input(f"Tujuan baru ({bus['tujuan']}): ") or bus["tujuan"]
                qty_input = input(f"Jumlah kursi baru ({bus['qty']}): ")
                if qty_input:
                    try:
                        bus["qty"] = int(qty_input)
                        if bus["qty"] <= 0:
                            print("Jumlah kursi harus lebih dari 0. Nilai lama tetap digunakan.")
                            bus["qty"] = bus["qty"]
                    except ValueError:
                        print("Input tidak valid. Nilai lama tetap digunakan.")

                try:
                    harga_baru = input(f"Harga baru ({bus['harga']}): ")
                    if harga_baru:
                        harga_baru = int(harga_baru)
                        if 10000 <= harga_baru <= 100000:
                            bus["harga"] = harga_baru
                        else:
                            print("Harga harus antara 10.000 - 100.000. Harga lama tetap digunakan.")
                except ValueError:
                    print("Input harga tidak valid. Harga lama tetap digunakan.")


                tambah_penumpangkonvensional(bus)
                hapus_penumpangkonvensional(bus)
                update_statusbus(bus)
                SimpanData_bus(data_bus)
                print("Data bis berhasil diperbarui!")
                return
            
        print("Nomor bis tidak ditemukan.")
    except ValueError:
        print("Input tidak valid!")

def hapus_bus():
    data_bus = BacaData_bus()
    tampilkan_bus()
    try:
        no = int(input("Masukkan nomor bus yang ingin dihapus: "))
        for i, bus in enumerate(data_bus):
            if bus["no"] == no:
                data_bus.pop(i)
                for j, b in enumerate(data_bus, start=1):
                    b["no"] = j
                SimpanData_bus(data_bus)
                print("Bus berhasil dihapus!")
                return
        print("Nomor bus tidak ditemukan.")
    except ValueError:
        print("Masukkan angka!")

def menu_manajemen_bus():
    while True:
        print("\n=== MANAJEMEN BIS ===")
        print("1. Lihat Data Bis")
        print("2. Tambah Bis")
        print("3. Update Bis")
        print("4. Hapus Bis")
        print("5. Kembali")

        pilih = input("Pilih menu: ")
        if pilih == "1":
            tampilkan_bus()
        elif pilih == "2":
            tambah_bus()
        elif pilih == "3":
            update_bus()
        elif pilih == "4":
            hapus_bus()
        elif pilih == "5":
            break
        else:
            print("Pilihan tidak valid!")



'''=================================================================================================================================='''
'''                                                         MANAJEMEN PENUMPANG                                                      '''
'''=================================================================================================================================='''

def lihat_penumpang():
    data = bacadata_penumpang()
    if not data:
        print("Belum ada data penumpang.")
        return

    tabel = PrettyTable(["No", "Username", "Role", "E-Money"])
    for p in data:
        tabel.add_row([p["no"], p["username"], p["role"], p["emoney"]])
    print(tabel)

def tambah_penumpang():
    data = bacadata_penumpang()
    print("\n=== BUAT AKUN PENUMPANG ===")
    no = max([p["no"] for p in data], default=0) + 1
    username = input("Masukkan username: ").strip().lower()
    if not username or " " in username:
        print("Username tidak boleh kosong atau mengandung spasi.")
        return

    for user in data:
        if user["username"] == username:
            print("Username sudah digunakan.")
            return

    password = input("Masukkan password: ").strip()
    data.append({"no": no, "username": username, "password": password, "role": "penumpang", "emoney": 0})
    simpandata_penumpang(data)
    print("Akun berhasil dibuat!")

def perbarui_penumpang():
    data = bacadata_penumpang()
    lihat_penumpang()
    try:
        no = int(input("Nomor penumpang yang ingin diperbarui: "))
        for p in data:
            if p["no"] == no:
                nama_baru = input("Masukkan username baru (kosongkan jika tidak ingin ubah): ").strip()
                if nama_baru:
                    p["username"] = nama_baru
                simpandata_penumpang(data)
                print("Data penumpang berhasil diperbarui.")
                return
        print("Nomor penumpang tidak ditemukan.")
    except ValueError:
        print("Harus angka!")

def menu_penumpang():
    while True:
        print("\n=== MANAJEMEN PENUMPANG ===")
        print("1. Lihat Penumpang")
        print("2. Tambah Penumpang")
        print("3. Perbarui Penumpang")
        print("4. Kembali")

        pilih = input("Pilih menu: ")
        if pilih == "1":
            lihat_penumpang()
        elif pilih == "2":
            tambah_penumpang()
        elif pilih == "3":
            perbarui_penumpang()
        elif pilih == "4":
            break
        else:
            print("Pilihan tidak valid!")


'''=================================================================================================================================='''
'''                                                         MANAJEMEN BOOKING                                                        '''
'''=================================================================================================================================='''

def tampilkan_booking():
    data = bacadata_booking()
    if not data:
        print("Belum ada data booking.")
        return

    tabel = PrettyTable(["No", "Nama Penumpang", "Nama Bus", "Tanggal", "Harga Tiket"])
    for i, b in enumerate(data, start=1):
        tabel.add_row([i, b["username"], b["nama_bis"], b["tanggal_pembelian"], f"Rp {b['harga_tiket']:,}"])
    print(tabel)

def hapus_booking():
    data = bacadata_booking()
    tampilkan_booking()
    if not data:
        return

    try:
        no = int(input("Nomor booking yang ingin dihapus: "))
        if 1 <= no <= len(data):
            hapus = data.pop(no - 1)
            simpandata_booking(data)
            print(f"Booking atas nama {hapus['username']} berhasil dihapus.")
        else:
            print("Nomor tidak valid.")
    except ValueError:
        print("Masukkan angka!")

def menu_booking():
    while True:
        print("\n=== MANAJEMEN BOOKING ===")
        print("1. Lihat Booking")
        print("2. Hapus Booking")
        print("3. Kembali")

        pilih = input("Pilih menu: ")
        if pilih == "1":
            tampilkan_booking()
        elif pilih == "2":
            hapus_booking()
        elif pilih == "3":
            break
        else:
            print("Pilihan tidak valid!")


'''=================================================================================================================================='''
'''                                                         CEK PENJUALAN TIKET                                                       '''
'''=================================================================================================================================='''

def cek_penjualan_tiket():
    data = bacadata_booking()
    if not data:
        print("Belum ada penjualan tiket.")
        return

    tabel = PrettyTable(["No", "Nama Penumpang", "Nama Bus", "Tanggal", "Harga Tiket"])
    total = 0
    for i, b in enumerate(data, start=1):
        tabel.add_row([i, b["username"], b["nama_bis"], b["tanggal_pembelian"], f"Rp {b['harga_tiket']:,}"])
        total += b["harga_tiket"]

    print(tabel)
    print(f"\nTotal Penghasilan: Rp {total:,}")

'''=================================================================================================================================='''
'''                                                         MENU PENUNMPANG                                                          '''
'''=================================================================================================================================='''

def lihat_akun_user(username):
    data = bacadata_penumpang()
    for user in data:
        if user["username"] == username:
            print("\n=== DATA AKUN ANDA ===")
            print(f"Username : {user['username']}")
            print(f"Password : {user['password']}")
            print(f"Emoney : {user['emoney']}")
            return
    print("Akun tidak ditemukan.")

def ganti_password_user(username):
    data = bacadata_penumpang()
    for user in data:
        if user["username"] == username:
            pw_lama = input("Masukkan password lama: ")
            if pw_lama != user["password"]:
                print("Password lama salah.")
                return
            pw_baru = input("Masukkan password baru: ")
            user["password"] = pw_baru
            simpandata_penumpang(data)
            print("Password berhasil diubah.")
            return
    print("Akun tidak ditemukan.")

def hapus_akun_user(username):
    data = bacadata_penumpang()
    for user in data:
        if user["username"] == username:
            print(f"Saldo e-money kamu: Rp {user['emoney']:,}")
            konfirmasi = input("Apakah kamu ingin menarik saldo sebelum hapus akun? (y/n): ").lower()
            if konfirmasi == "y" and user["emoney"] > 0:
                print(f"Saldo Rp {user['emoney']:,} akan ditarik ke rekening kamu.")
                user["emoney"] = 0
        
            konfirmasi = input("Apakah kamu yakin ingin menghapus akun ini? (y/n): ").lower()
            if konfirmasi == "y":
                data.remove(user)
                simpandata_penumpang(data)
                print("Akun berhasil dihapus. Kamu akan logout otomatis.")
                return True
            else:
                print("Penghapusan akun dibatalkan.")
                return False
    print("Akun tidak ditemukan.")
    return False

def booking_tiket(username):
    data_bus = BacaData_bus()
    tampilkan_bus()
    no = int(input("Pilih nomor bus yang ingin dibooking: "))

    for bus in data_bus:
        if bus["no"] == no and bus["status"] == "tersedia":

            data_penumpang = bacadata_penumpang()
            for user in data_penumpang:
                if user["username"] == username:
                    if user["emoney"] < bus["harga"]:
                        print("Saldo e-money kamu tidak cukup untuk membeli tiket ini.")
                        return
                    else:
                        user["emoney"] -= bus["harga"]
                        simpandata_penumpang(data_penumpang)
                        print(f"Pembayaran berhasil! Saldo tersisa: Rp {user['emoney']:,}")
                    break

            bus["terisi"] += 1
            update_statusbus(bus)
            SimpanData_bus(data_bus)

            data_booking = bacadata_booking()
            data_booking.append({
                "username": username,
                "nama_bis": bus["nama"],
                "tanggal_pembelian": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "harga_tiket": bus["harga"]
            })
            simpandata_booking(data_booking)
            print("Tiket berhasil dipesan!")
            return
    print("Bus tidak tersedia atau nomor salah.")

def lihat_booking_user(username):
    data_booking = bacadata_booking()
    table = PrettyTable()
    table.field_names = ["No", "Nama Bus", "Tanggal Pembelian", "Harga Tiket"]

    user_bookings = [b for b in data_booking if b["username"] == username]

    if not user_bookings:
        print("\nKamu belum memiliki booking tiket.\n")
        return

    for i, booking in enumerate(user_bookings, start=1):
        table.add_row([
            i,
            booking["nama_bis"],
            booking["tanggal_pembelian"],
            booking["harga_tiket"]
        ])

    print(f"\n=== DAFTAR BOOKING {username.upper()} ===")
    print(table)

def menu_akun_user(username):
    while True:
        print("\n=== PENGATURAN AKUN ===")
        print("1. Lihat Akun")
        print("2. Ganti Password")
        print("3. Hapus Akun")
        print("4. Kembali")
        pilih = input("Pilih: ")

        if pilih == "1":
            lihat_akun_user(username)
        elif pilih == "2":
            ganti_password_user(username)
        elif pilih == "3":
            if hapus_akun_user(username):
                break
        elif pilih == "4":
            break
        else:
            print("Pilihan tidak valid!")

def topup_emoney(username):
    data_penumpang = bacadata_penumpang()
    user_ditemukan = False

    for user in data_penumpang:
        if user["username"] == username:
            user_ditemukan = True
            print("\n=== MENU TOP UP E-MONEY ===")
            print("1. Rp 20.000")
            print("2. Rp 50.000")
            print("3. Rp 100.000")
            print("4. Rp 500.000")
            
            pilihan = input("Pilih nominal (1-4): ")
            nominal = 0

            if pilihan == "1":
                nominal = 20000
            elif pilihan == "2":
                nominal = 50000
            elif pilihan == "3":
                nominal = 100000
            elif pilihan == "4":
                nominal = 500000
            else:
                print("Pilihan tidak valid.")
                return

            konfirmasi = input(f"Konfirmasi top up Rp {nominal}? (y/n): ").lower()
            if konfirmasi == "y":
                user["emoney"] += nominal
                simpandata_penumpang(data_penumpang)
                print(f"Top up berhasil! Saldo e-money kamu sekarang: Rp {user['emoney']:,}")
            else:
                print("Top up dibatalkan.")
            break

    if not user_ditemukan:
        print("Akun tidak ditemukan.")

def menu_penumpang_user(username):
    while True:
        print(f"\n=== MENU PENUMPANG ({username}) ===")
        print("1. Lihat Bus")
        print("2. Booking Tiket")
        print("3. Lihat Tiket Saya")
        print("4. Lihat / Ganti / Hapus Akun")
        print("5. TOP UP")
        print("6. Logout")

        pilih = input("Pilih menu: ")
        if pilih == "1":
            tampilkan_bus()
        elif pilih == "2":
            booking_tiket(username)
        elif pilih == "3":
            lihat_booking_user(username)
        elif pilih == "4":
            menu_akun_user(username)
        elif pilih == "5":
            topup_emoney(username)
        elif pilih == "6":
            print("Logout berhasil.")
            break
        else:
            print("Pilihan tidak valid!")


'''=================================================================================================================================='''
'''                                                         MULAI                                                                    '''
'''=================================================================================================================================='''


login()
