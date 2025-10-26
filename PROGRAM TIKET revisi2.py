import json
from datetime import datetime
from prettytable import PrettyTable
import pwinput
import os
os.system('cls')

'''=================================================================================================================================='''
'''                                                         JSON                                                                     '''
'''=================================================================================================================================='''

admin_username = "admin"
admin_password = "admin123"

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
'''                                                         LOGIN                                                                   '''
'''=================================================================================================================================='''

def login():
    os.system("cls")
    while True:
        print("\n" + "="*50)
        print("                   SISTEM LOGIN")
        print("="*50)
        print("1. Login sebagai Admin")
        print("2. Login sebagai Penumpang")
        print("3. Keluar")
        print("="*50)

        pilihan = input("Pilih menu: ")
        os.system("cls")

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
    os.system("cls")
    percobaan = 0
    while percobaan < 3:
        user = input("Masukkan username admin: ").lower()
        pw = pwinput.pwinput("Masukkan password admin: ")
        os.system("cls")

        if user == admin_username and pw == admin_password:
            print("\nLogin admin berhasil!\n")
            menu_admin()
            return
        else:
            percobaan += 1
            if percobaan < 3:
                print(f"Username/password salah! Percobaan ke-{percobaan}/3")
            else:
                print(f"Username/password salah! Percobaan ke-{percobaan}/3")
                print("Terlalu banyak percobaan gagal. Hubungi atasan untuk bantuan.\n")
                exit()



def login_penumpang():
    os.system("cls")
    while True:
        print("\n"+"="*50)
        print("                LOGIN PENUMPANG")
        print("="*50)
        print("1. Sudah punya akun")
        print("2. Belum punya akun")
        print("3. Kembali")
        print("="*50)

        pilih = input("Pilih: ")
        os.system("cls")

        if pilih == "1":
            percobaan = 0
            data = bacadata_penumpang()
            while percobaan < 3:
                username = input("Username: ").lower()
                pw = pwinput.pwinput("Password: ")
                os.system("cls")
                for p in data:
                    if p["username"] == username and p["password"] == pw:
                        print(f"\nSelamat datang, {username}!\n")
                        menu_penumpang_user(username)
                        return
                percobaan += 1
                if percobaan < 3:
                    print(f"Username/password salah! Percobaan ke-{percobaan}/3")
                else:
                    print(f"Username/password salah! Percobaan ke-{percobaan}/3")
                    print("Terlalu banyak percobaan gagal. Hubungi admin.\n")
                    exit()

        elif pilih == "2":
            tambah_penumpang()
            print("\nSilakan login atau sign in kembali...\n")
            continue

        elif pilih == "3":
            return
        else:
            print("Pilihan tidak valid!")

def tambah_penumpang():
    os.system("cls")
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
    os.system("cls")
    if not password or len(password) < 3:
        print("Password harus minimal 3 karakter.")
        return

    data.append({"no": no, "username": username, "password": password, "role": "penumpang", "emoney": 0})
    simpandata_penumpang(data)
    print("Akun berhasil dibuat!")



'''=================================================================================================================================='''
'''                                                         MANAJEMEN BUS                                                            '''
'''=================================================================================================================================='''

def tampilkan_bus():
    os.system("cls")
    data_bus = BacaData_bus()
    if not data_bus:
        print("Belum ada data bis.")
        return
    
    table = PrettyTable(["No", "Nama", "Asal", "Tujuan", "Status", "Qty", "Terisi", "Harga"])
    for bus in data_bus:
        table.add_row([bus["no"], bus["nama"], bus["asal"], bus["tujuan"], bus["status"], bus["qty"], bus["terisi"], bus["harga"]])
    print(table)

def tambah_bus():
    os.system("cls")
    data_bus = BacaData_bus()
    print("\n=== Tambah Data Bis ===")

    no = len(data_bus) + 1

    nama = input("Nama bis: ").strip()
    os.system("cls")
    if not nama:
        print("Nama bis tidak boleh kosong!")
        return

    print("\nPilihan Asal:")
    print("1. samarinda")
    print("2. kutai kartanegara")
    pilihan_asal = input("Pilih asal: ").strip()
    
    if pilihan_asal == "1":
        asal = "samarinda"
    elif pilihan_asal == "2":
        asal = "kutai kartanegara"
    else:
        print("Pilihan asal tidak valid!")
        return

    print("\nPilihan Tujuan:")
    print("1. samarinda") 
    print("2. kutai kartanegara")
    pilihan_tujuan = input("Pilih tujuan: ").strip()
    os.system("cls")
    
    if pilihan_tujuan == "1":
        tujuan = "samarinda"
    elif pilihan_tujuan == "2":
        tujuan = "kutai kartanegara"
    else:
        print("Pilihan tujuan tidak valid!")
        return
    
    if asal == tujuan:
        print("asal dan tujuan tidak boleh sama!")
        return

    status = "tersedia"

    while True:
        try:
            qty = int(input("\nJumlah kursi (1-20): "))
            os.system("cls")
            if 1 <= qty <= 20:
                break
            else:
                print("Jumlah penumpang harus antara 1-20.")
        except ValueError:
            print("Input tidak valid! Masukkan angka.")
        except KeyboardInterrupt:
            print("\n\nProgram dihentikan oleh pengguna (Ctrl+C).")
        except EOFError:
            print("\nInput terhenti secara mendadak (Ctrl+D atau Enter kosong).")
        except Exception as e:
            print(f"\nTerjadi kesalahan tidak terduga: {e}")

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
        except KeyboardInterrupt:
            print("\n\nProgram dihentikan oleh pengguna (Ctrl+C).")
        except EOFError:
            print("\nInput terhenti secara mendadak (Ctrl+D atau Enter kosong).")
        except Exception as e:
            print(f"\nTerjadi kesalahan tidak terduga: {e}")

    data_baru = {
        "no": no,
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
    if not bus:
        return

    if bus["terisi"] >= bus["qty"]:
        bus["status"] = "penuh"
    else:
        bus["status"] = "tersedia"

    data_bus = BacaData_bus()
    for b in data_bus:
        if b["no"] == bus["no"]:
            b.update(bus)
            break

    SimpanData_bus(data_bus)

def update_bus():
    os.system("cls")
    data_bus = BacaData_bus()
    if not data_bus:
        print("Belum ada data bus untuk diperbarui.")
        return

    tampilkan_bus()
    try:
        no = int(input("Masukkan nomor bis yang ingin diupdate: "))
        os.system("cls")
        for bus in data_bus:
            if bus["no"] == no:
                print(f"\n=== Update Data Bis: {bus['nama']} ===")
                print("Tekan Enter jika tidak ingin mengubah bagian tersebut. \n")

                bus["nama"] = input(f"Nama baru ({bus['nama']}): ") or bus["nama"]
                os.system("cls")

                print(f"\nAsal saat ini: {bus['asal']}")
                print("Pilihan Asal:")
                print("1. samarinda")
                print("2. kutai kartanegara")
                pilihan_asal = input("Pilih asal baru (1/2 atau Enter untuk skip): ").strip()
                
                if pilihan_asal == "1":
                    bus["asal"] = "samarinda"
                elif pilihan_asal == "2":
                    bus["asal"] = "kutai kartanegara"
                elif pilihan_asal:
                    print("Pilihan asal tidak valid! Asal tidak diubah.")


                print(f"\nTujuan saat ini: {bus['tujuan']}")
                print("Pilihan Tujuan:")
                print("1. samarinda")
                print("2. kutai kartanegara")
                pilihan_tujuan = input("Pilih tujuan baru (1/2 atau Enter untuk skip): ").strip()
                os.system("cls")
                
                if pilihan_tujuan == "1":
                    bus["tujuan"] = "samarinda"
                elif pilihan_tujuan == "2":
                    bus["tujuan"] = "kutai kartanegara"
                elif pilihan_tujuan:
                    print("Pilihan tujuan tidak valid! Tujuan tidak diubah.")

                if bus["asal"] == bus["tujuan"]:
                    print("Asal dan tujuan tidak boleh sama! Data tidak disimpan.")
                    return


                qty_input = input(f"Jumlah kursi baru ({bus['qty']}): ").strip()
                os.system("cls")
                old_qty = bus["qty"]
                if qty_input:
                    try:
                        new_qty = int(qty_input)

                        if new_qty < bus["terisi"]:
                            print(f"\nTIDAK BISA MENGURANGI KURSI!")
                            print(f"Jumlah kursi baru: {new_qty}")
                            print(f"Penumpang saat ini: {bus['terisi']}")
                            print(f"Kursi tidak cukup untuk menampung penumpang yang sudah ada")
                            print(f"Silahkan hubungi penumpang untuk membatalkan booking")
                            return
                        
                        if 1 <= new_qty <= 20:
                            bus["qty"] = new_qty
                            print(f"Jumlah kursi diubah: dari {old_qty} menjadi {new_qty}")


                        else:
                            print("Jumlah kursi harus 1-20. Nilai lama tetap digunakan.")
                            bus["qty"] = old_qty
                    except ValueError:
                        print("Input tidak valid. Nilai lama tetap digunakan.")
                    except KeyboardInterrupt:
                        print("\n\nProgram dihentikan oleh pengguna (Ctrl+C).")
                    except EOFError:
                        print("\nInput terhenti secara mendadak (Ctrl+D atau Enter kosong).")
                    except Exception as e:
                        print(f"\nTerjadi kesalahan tidak terduga: {e}")

                try:
                    harga_baru = input(f"Harga baru ({bus['harga']}): ")
                    os.system("cls")
                    if harga_baru:
                        harga_baru = int(harga_baru)
                        if 10000 <= harga_baru <= 100000:
                            bus["harga"] = harga_baru
                        else:
                            print("Harga harus antara 10.000 - 100.000. Harga lama tetap digunakan.")
                except ValueError:
                    print("Input harga tidak valid. Harga lama tetap digunakan.")
                except KeyboardInterrupt:
                    print("\n\nProgram dihentikan oleh pengguna (Ctrl+C).")
                except EOFError:
                    print("\nInput terhenti secara mendadak (Ctrl+D atau Enter kosong).")
                except Exception as e:
                    print(f"\nTerjadi kesalahan tidak terduga: {e}")

                update_statusbus(bus)
                SimpanData_bus(data_bus)
                print("Data bis berhasil diperbarui!")
                return
            
        print("Nomor bis tidak ditemukan.")
    except ValueError:
        print("Input tidak valid!")
    except KeyboardInterrupt:
        print("\n\nProgram dihentikan oleh pengguna (Ctrl+C).")
    except EOFError:
        print("\nInput terhenti secara mendadak (Ctrl+D atau Enter kosong).")
    except Exception as e:
        print(f"\nTerjadi kesalahan tidak terduga: {e}")

def hapus_bus():
    os.system("cls")
    data_bus = BacaData_bus()
    if not data_bus:
        print("Belum ada data bus.")
        return
    
    tampilkan_bus()
    try:
        no = int(input("Masukkan nomor bus yang ingin dihapus: "))
        os.system("cls")
        for i, bus in enumerate(data_bus):
            if bus["no"] == no:
                print(f"\n=== KONFIRMASI HAPUS BUS ===")
                print(f"Bus: {bus['nama']}")
                print(f"Rute: {bus['asal']} → {bus['tujuan']}")
                print(f"Status: {bus['status']}")
                print(f"Penumpang: {bus['terisi']}/{bus['qty']}")
                
                if bus["terisi"] > 0:
                    print(f"\nTIDAK BISA DIHAPUS!")
                    print(f"Bus masih memiliki {bus['terisi']} penumpang.")
                    print(f"Minta penumpang membatalkan booking terlebih dahulu")
                    return
                    
                konfirmasi = input(f"\nApakah Anda yakin ingin menghapus bus {bus['nama']}? (y/n): ").lower()
                os.system("cls")
                if konfirmasi == 'y':
                    data_bus.pop(i)

                    for j, b in enumerate(data_bus, start=1):
                        b["no"] = j
                    SimpanData_bus(data_bus)
                    print("Bus berhasil dihapus!")
                else:
                    print("Penghapusan dibatalkan")
                return

        print("Nomor bus tidak ditemukan.")
    except ValueError:
        print("Masukkan angka!")
    except KeyboardInterrupt:
        print("\n\nProgram dihentikan oleh pengguna (Ctrl+C).")
    except EOFError:
        print("\nInput terhenti secara mendadak (Ctrl+D atau Enter kosong).")
    except Exception as e:
        print(f"\nTerjadi kesalahan tidak terduga: {e}")

def menu_manajemen_bus():
    os.system("cls")
    while True:
        print("\n"+"="*50)
        print("                MANAJEMEN BIS")
        print("="*50)
        print("1. Lihat Data Bis")
        print("2. Tambah Bis")
        print("3. Update Bis")
        print("4. Hapus Bis")
        print("5. Kembali")
        print("="*50)

        pilih = input("Pilih menu: ")
        os.system("cls")
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
    os.system("cls")
    data = bacadata_penumpang()
    if not data:
        print("Belum ada data penumpang.")
        return

    tabel = PrettyTable(["No", "Username", "Role"])
    for p in data:
        tabel.add_row([p["no"], p["username"], p["role"]])
    print(tabel)


'''=================================================================================================================================='''
'''                                                         MANAJEMEN BOOKING                                                        '''
'''=================================================================================================================================='''

def tampilkan_booking():
    os.system("cls")
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
'''                                                         MENU ADMIN UTAMA                                                         '''
'''=================================================================================================================================='''

def menu_admin():
    os.system("cls")
    while True:
        print("\n"+"="*50)
        print("                   MENU ADMIN")
        print("="*50)
        print("1. Manajemen Bus")
        print("2. Lihat Penumpang")
        print("3. Lihat Booking Penumpang")
        print("4. Logout")
        print("="*50)

        pilih = input("Pilih menu: ")
        os.system("cls")

        if pilih == "1":
            menu_manajemen_bus()
        elif pilih == "2":
            lihat_penumpang()
        elif pilih == "3":
            tampilkan_booking()
        elif pilih == "4":
            print("Logout berhasil.\n")
            break
        else:
            print("Pilihan tidak valid!")

'''=================================================================================================================================='''
'''                                                         MENU PENUNMPANG                                                          '''
'''=================================================================================================================================='''

def booking_tiket(username):
    os.system("cls")
    data_bus = BacaData_bus()
    if not data_bus:
        print("Belum ada bus tersedia.")
        return

    tampilkan_bus()
    try:
        no = int(input("Pilih nomor bus yang ingin dibooking: "))
        os.system("cls")

        for bus in data_bus:
            if bus["no"] == no:
                if bus["status"] != "tersedia" or bus["terisi"] >= bus["qty"]:
                    print("Maaf, bus sudah penuh atau tidak tersedia!")
                    return
        
                data_penumpang = bacadata_penumpang()
                for user in data_penumpang:
                    if user["username"] == username:
                        if user["emoney"] < bus["harga"]:
                            print("Saldo e-money tidak cukup!")
                            return
                
                        user["emoney"] -= bus["harga"]
                        simpandata_penumpang(data_penumpang)

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
                        print(f"Saldo tersisa: {user['emoney']}")
                        print("Tiket berhasil dipesan!")
                        return

                print("Akun tidak ditemukan.")
                return
        
        print("Nomor bus tidak ditemukan.")
        
    except ValueError:
        print("Masukkan angka yang valid!")
    except KeyboardInterrupt:
        print("\n\nProgram dihentikan oleh pengguna (Ctrl+C).")
    except EOFError:
        print("\nInput terhenti secara mendadak (Ctrl+D atau Enter kosong).")
    except Exception as e:
        print(f"\nTerjadi kesalahan tidak terduga: {e}")



def lihat_akun_user(username):
    os.system("cls")
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
    os.system("cls")
    data = bacadata_penumpang()
    for user in data:
        if user["username"] == username:
            pw_lama = input("Masukkan password lama: ")
            if pw_lama != user["password"]:
                print("Password lama salah.")
                return
            pw_baru = input("Masukkan password baru: ").strip()
            if not pw_baru or len(pw_baru) < 3: 
                print("Password baru harus minimal 3 karakter.")
                return
            
            konfirmasi = input("Konfirmasi password baru: ")
            os.system("cls")
            if pw_baru != konfirmasi:
                print("Konfirmasi password tidak sesuai.")
                return
                
            user["password"] = pw_baru
            simpandata_penumpang(data)
            print("Password berhasil diubah.")
            return
    print("Akun tidak ditemukan.")

def hapus_akun_user(username):
    os.system("cls")
    data = bacadata_penumpang()
    for user in data:
        if user["username"] == username:
            print(f"Saldo e-money kamu: Rp {user['emoney']:,}")
            konfirmasi = input("\nApakah kamu ingin menarik saldo sebelum hapus akun? (y/n): ").lower()
            if konfirmasi == "y" and user["emoney"] > 0:
                print(f"Saldo Rp {user['emoney']:,} akan ditarik ke rekening kamu.")
                user["emoney"] = 0
                simpandata_penumpang(data)
        
            konfirmasi_hapus = input("\nApakah kamu yakin ingin menghapus akun ini? (y/n): ").lower()
            os.system("cls")
            if konfirmasi_hapus == "y":
                data.remove(user)
                simpandata_penumpang(data)
                print("Akun berhasil dihapus. Kamu akan logout otomatis.")
                return True
            else:
                print("Penghapusan akun dibatalkan.")
                return False
    print("Akun tidak ditemukan.")
    return False


def lihat_booking_user(username):
    os.system("cls")
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


def topup_emoney(username):
    os.system("cls")
    data_penumpang = bacadata_penumpang()
    user_ditemukan = False

    for user in data_penumpang:
        if user["username"] == username:
            user_ditemukan = True
            print("\n" + "="*50)
            print("             MENU TOP UP E-MONEY")
            print("="*50)
            print("1. Rp 20.000")
            print("2. Rp 50.000")
            print("3. Rp 100.000")
            print("4. Rp 500.000")
            print("="*50)
            
            pilihan = input("Pilih nominal (1-4): ")
            os.system("cls")
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
            os.system("cls")
            if konfirmasi == "y":
                user["emoney"] += nominal
                simpandata_penumpang(data_penumpang)
                print(f"Top up berhasil! Saldo e-money kamu sekarang: Rp {user['emoney']:,}")
            else:
                print("Top up dibatalkan.")
            break

    if not user_ditemukan:
        print("Akun tidak ditemukan.")

def hapus_booking(username):
    os.system("cls")
    data_booking = bacadata_booking()
    user_bookings = [b for b in data_booking if b["username"] == username]

    if not user_bookings:
        print("\nKamu belum memiliki booking tiket.\n")
        return

    lihat_booking_user(username)

    try:
        no = int(input("Masukkan nomor booking yang ingin dihapus: "))
        if 1 <= no <= len(user_bookings):
            hapus = user_bookings[no - 1]
            nama_bus = hapus["nama_bis"]
            harga_tiket = int(hapus["harga_tiket"])

            konfirmasi = input(f"\nApakah kamu yakin ingin menghapus booking di {nama_bus}? (y/n): ").lower()
            if konfirmasi != "y":
                print("\nPenghapusan booking dibatalkan.\n")
                return

            data_booking.remove(hapus)
            simpandata_booking(data_booking)

            user_data = bacadata_penumpang()
            refund_berhasil = False
            for user in user_data:
                if user["username"].lower() == username.lower():
                    user["emoney"] += harga_tiket
                    refund_berhasil = True
                    print(f"\nRp {harga_tiket:,} telah dikembalikan ke saldo e-money kamu.")
                    break

            if refund_berhasil:
                simpandata_penumpang(user_data)

            data_bus = BacaData_bus()
            for bus in data_bus:
                if bus["nama"].lower() == nama_bus.lower():
                    bus["terisi"] = max(bus["terisi"] - 1, 0)
                    update_statusbus(bus)
                    print(f"Satu kursi di {nama_bus} dikosongkan. Total terisi: {bus['terisi']}")
                    break

            SimpanData_bus(data_bus)
            print(f"\nBooking di {nama_bus} berhasil dihapus!\n")

        else:
            print("Nomor booking tidak valid.")
    
    except ValueError:
        print("Masukkan angka yang valid!")
    except KeyboardInterrupt:
        print("\n\nProgram dihentikan oleh pengguna (Ctrl+C).")
    except EOFError:
        print("\nInput terhenti secara mendadak (Ctrl+D atau Enter kosong).")
    except Exception as e:
        print(f"\nTerjadi kesalahan tidak terduga: {e}")


def menu_penumpang_user(username):
    os.system("cls")
    while True:
        print("\n" + "="*50)
        print(f"              MENU PENUMPANG ({username})")
        print("="*50)
        print("1. Lihat Bus")
        print("2. Booking Tiket")
        print("3. Hapus Booking Tiket")
        print("4. Lihat Tiket Saya")
        print("5. Akun Pengguna")
        print("6. TOP UP")
        print("7. Logout")
        print("="*50)

        pilih = input("Pilih menu: ")
        os.system("cls")
        if pilih == "1":
            tampilkan_bus()
        elif pilih == "2":
            booking_tiket(username)
        elif pilih == "3":
            hapus_booking(username)
        elif pilih == "4":
            lihat_booking_user(username)
        elif pilih == "5":
            menu_akun_user(username)
        elif pilih == "6":
            topup_emoney(username)
        elif pilih == "7":
            print("Logout berhasil.")
            break
        else:
            print("Pilihan tidak valid!")

def menu_akun_user(username):
    os.system("cls")
    while True:
        print("\n"+"="*50)
        print("              PENGATURAN AKUN")
        print("="*50)
        print("1. Lihat Akun")
        print("2. Ganti Password")
        print("3. Hapus Akun")
        print("4. Kembali")
        print("="*50)
        pilih = input("Pilih: ")
        os.system("cls")

        if pilih == "1":
            lihat_akun_user(username)
        elif pilih == "2":
            ganti_password_user(username)
        elif pilih == "3":
            if hapus_akun_user(username):
                print("Akun telah dihapus. Kembali ke menu utama...")
                login() 
                return
        elif pilih == "4":
            break
        else:
            print("Pilihan tidak valid!")

'''=================================================================================================================================='''
'''                                                         MULAI                                                                    '''
'''=================================================================================================================================='''


login()