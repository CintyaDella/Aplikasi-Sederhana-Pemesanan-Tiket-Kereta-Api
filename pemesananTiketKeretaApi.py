import mysql.connector
from prettytable import from_db_cursor
from prettytable import from_csv
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import os

df = pd.read_csv('kereta.csv')

db = mysql.connector.connect(
    host = 'localhost', 
    user = 'root',
    password = '',
    database = 'pemesanan_keretaapi'
    )

def selectMenu () :
    connect = db.cursor()
    with open('kereta.csv') as fp :
        table = from_csv(fp)
        print(table)
        lanjut = True
        while(lanjut) :
            nomor = int(input('Nomor Kereta : '))
            cekNomor = any(df['Nomor Kereta'] == nomor)
            if cekNomor == True :
                namaPemesan = str(input('Nama Pemesan : '))
                jumlahTiket = int(input('Jumlah Tiket : '))
                namaKereta = df.loc[df['Nomor Kereta'] == nomor]['Nama Kereta'].iloc[0]
                kelas = df.loc[df['Nomor Kereta'] == nomor]['Kelas'].iloc[0]
                kotaAsal = df.loc[df['Nomor Kereta'] == nomor]['Kota Asal'].iloc[0]
                kotaTujuan = df.loc[df['Nomor Kereta'] == nomor]['Kota Tujuan'].iloc[0]
                jamBerangkat = df.loc[df['Nomor Kereta'] == nomor]['Jam Berangkat'].iloc[0]
                jamTiba = df.loc[df['Nomor Kereta'] == nomor]['Jam Tiba'].iloc[0]
                harga = int(df.loc[df['Nomor Kereta'] == nomor]['Harga'].iloc[0])
                statusBayar = ('Belum Dibayar')
                tanggalBayar = ('0000-00-00 00:00:00')
                querry = 'INSERT INTO datapemesan (NomorKereta, NamaPemesan,  NamaKereta, Kelas, KotaAsal, KotaTujuan, JamBerangkat, JamTiba, JumlahTiket, Harga, StatusBayar, TanggalPembayaran) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
                data = (nomor, namaPemesan, namaKereta, kelas, kotaAsal, kotaTujuan, jamBerangkat, jamTiba, jumlahTiket, harga, statusBayar, tanggalBayar)
                connect.execute(querry,data)
                db.commit()
                print('Pemesanan Berhasil Dilakukan Silahkan Melanjutkan ke Menu Pembayaran')
            else :
                print('Nomor Kereta Api Tidak Tersedia, Harap Masukan Kembali')
                break
            os.system('pause')

def showAllDataPemesan () :
    connect = db.cursor()
    show = 'SELECT*FROM datapemesan'
    connect.execute(show)
    pt = from_db_cursor(connect)
    print(' ------------------------------------------------------------- DATA BERHASIL DITAMPILKAN -------------------------------------------------------------')
    print(pt)

def showDataPemesan():
    connect = db.cursor()
    id = input('Masukkan ID Pemesan : ')
    data = [id]
    show = 'SELECT*FROM datapemesan WHERE id=%s'
    connect.execute(show, data)
    pt = from_db_cursor(connect)
    print(' DATA BERHASIL DITAMPILKAN ')
    print(pt)

def deleteDataPemesan () :
    connect = db.cursor()
    id = input('Masukkan ID Pemesan : ')
    data = [id]
    show = 'SELECT*FROM datapemesan WHERE id=%s'
    connect.execute(show, data)
    pt = from_db_cursor(connect)
    print(pt)
    delete=str(input('Yakin ingin Melakukan Pembatalan (Y/N) : '))
    if delete == "Y" :
        sql = 'DELETE FROM datapemesan WHERE id=%s'
        val= [id]
        connect.execute(sql,val)
        db.commit()
        print ('Pembatalan Berhasil Dilakukan')
    else: 
        print('Pembatalan Tidak Berhasil')
        
def pembayaranPesanan () :    
    connect = db.cursor()
    connect.execute('SELECT*FROM datapemesan')
    result = connect.fetchall() 
    id = int(input('Masukkan ID Pemesan : '))
    for i in result:
        if id == i[0] :
            data = [id]
            show = 'SELECT*FROM datapemesan WHERE id=%s'
            connect.execute(show, data)
            pt = from_db_cursor(connect)
            print(pt)
            konfirm = str (input('Apakah Data Sudah Benar (Y/N) : '))
            if konfirm == 'Y' :
                print(f'Jumlah yang Harus Dibayar : Rp. {i[10]}')
                uang = int(input('Masukkan Uang Pembayaran  : Rp. '))
                hasil = uang - int(i[10])
                if uang >= int(i[10]) :
                    status = ('Sudah Dibayar')   
                    querry = f'UPDATE datapemesan SET StatusBayar="{status}" WHERE id="{id}"'
                    connect.execute(querry)
                    db.commit()
                    dt = datetime.datetime.now()
                    print("Tanggal : ",dt.strftime("%d %m %Y,pukul%H:%M"))
                    querry = f'UPDATE datapemesan SET TanggalPembayaran="{dt}" WHERE id="{id}"'
                    connect.execute(querry)
                    db.commit()

                    print('------------ BUKTI PEMBAYARAN ------------')
                    print(     f'ID Pemesan           :   {i[0]}     ')
                    print(     f'Nama Pemesan         :   {i[2]}     ')
                    print(     f'Nomor Kereta         :   {i[1]}     ')
                    print(     f'Nama Kereta          :   {i[3]}     ')
                    print(     f'Kelas                :   {i[4]}     ')
                    print(     f'Kota Asal            :   {i[5]}     ')
                    print(     f'Kota Tujuan          :   {i[6]}     ')
                    print(     f'Jam Berangkat        :   {i[7]}     ')
                    print(     f'Jam Tiba             :   {i[8]}     ')
                    print(     f'Jumlah Tiket         :   {i[9]}     ')
                    print(     f'Harga                :   Rp. {i[10]}')
                    print('Tunai                :   Rp.',uang        )
                    print('Kembalian            :   Rp.',hasil       )
                    print(     f'Tanggal Pembayaran   :   {dt}    ')
                    print('----- PEMBAYARAN BERHASIL DILAKUKAN ------')
                elif uang < int(i[10]) :
                    print ('Uang Pembayaran Kurang')
            else:
                break

def cetakUlangStruk () :
    connect = db.cursor()
    connect.execute('SELECT*FROM datapemesan')
    result = connect.fetchall() 
    id = int(input('Masukkan ID Pemesan : '))
    nama = str(input('Masukan Nama Pemesan : '))
    for i in result:
        if id == i[0] and nama == i[2] :
            print('------------ BUKTI PEMBAYARAN ------------')
            print(     f'ID Pemesan           :   {i[0]}     ')
            print(     f'Nama Pemesan         :   {i[2]}     ')
            print(     f'Nomor Kereta         :   {i[1]}     ')
            print(     f'Nama Kereta          :   {i[3]}     ')
            print(     f'Kelas                :   {i[4]}     ')
            print(     f'Kota Asal            :   {i[5]}     ')
            print(     f'Kota Tujuan          :   {i[6]}     ')
            print(     f'Jam Berangkat        :   {i[7]}     ')
            print(     f'Jam Tiba             :   {i[8]}     ')
            print(     f'Jumlah Tiket         :   {i[9]}     ')
            print(     f'Harga                :   Rp. {i[10]}')
            print(     f'Status Pembayaran    :   {i[11]}    ')
            print(     f'Tanggal Pembayaran   :   {i[12]}    ')
            print('----- PEMBAYARAN BERHASIL DILAKUKAN ------')
        else :
            print('ID atau Nama Pengguna Tidak Ditemukan')


def updateDataPemesan ():
    connect = db.cursor()
    id = input('Masukkan ID Pemesan : ')
    data = [id]
    show = 'SELECT*FROM datapemesan WHERE id=%s'
    connect.execute(show, data)
    pt = from_db_cursor(connect)
    print(' DATA BERHASIL DITAMPILKAN ')
    print(pt)
    konfirm = str (input('Apakah Anda ingin Mengubah Pesanan (Y/N) : '))
    if konfirm == 'Y' :
        with open('kereta.csv') as fp :
            table = from_csv(fp)
            print(table)
            lanjut = True
            while(lanjut) :
                nomor = int(input('Nomor Kereta : '))
                cekNomor = any(df['Nomor Kereta'] == nomor)
                if cekNomor == True :
                    jumlahTiket = int(input('Jumlah Tiket : '))
                    namaKereta = df.loc[df['Nomor Kereta'] == nomor]['Nama Kereta'].iloc[0]
                    kelas = df.loc[df['Nomor Kereta'] == nomor]['Kelas'].iloc[0]
                    kotaAsal = df.loc[df['Nomor Kereta'] == nomor]['Kota Asal'].iloc[0]
                    kotaTujuan = df.loc[df['Nomor Kereta'] == nomor]['Kota Tujuan'].iloc[0]
                    jamBerangkat = df.loc[df['Nomor Kereta'] == nomor]['Jam Berangkat'].iloc[0]
                    jamTiba = df.loc[df['Nomor Kereta'] == nomor]['Jam Tiba'].iloc[0]
                    harga = int(df.loc[df['Nomor Kereta'] == nomor]['Harga'].iloc[0])
                    statusBayar = ('Belum Dibayar')
                    tanggalBayar = ('0000-00-00 00:00:00')
                    querry = f'UPDATE datapemesan SET NomorKereta="{nomor}", NamaKereta="{namaKereta}", Kelas="{kelas}", KotaAsal="{kotaAsal}", KotaTujuan="{kotaTujuan}", JamBerangkat="{jamBerangkat}", JamTiba="{jamTiba}", JumlahTiket="{jumlahTiket}", Harga="{harga}", StatusBayar="{statusBayar}", TanggalPembayaran="{tanggalBayar}" WHERE id="{id}"'
                    connect.execute(querry)
                    show = 'SELECT*FROM datapemesan WHERE id=%s'
                    connect.execute(show, data)
                    pt = from_db_cursor(connect)
                    print(pt)
                    db.commit()
                    print('Data Pemesanan Berhasil Diubah')
                    break
                else :
                    print('Nomor Kereta yang Anda Masukan Salah')
                    break
                os.system('pause')

def showGrafikPenjualan () :
    connect = db.cursor()
    querry   = "SELECT COUNT(JumlahTiket),NamaKereta FROM datapemesan GROUP BY Namakereta"
    connect.execute(querry)
    result   = connect.fetchall()
    data = []
    for j in result:
        data.append(j[0])
    namaJumlah = []
    for j in result:
        namaJumlah.append(j[1])
    plt.bar(namaJumlah,data)
    plt.show()

while True:
    os.system ('cls')
    print('-----------------------------------')
    print("APLIKASI PEMESANAN TIKET KERETA API")
    print('-----------------------------------')
    print("     1.Login sebagai Admin")
    print("     2.Login sebagai Pemesan")
    print("     3.Keluar")
    print('-----------------------------------')
    login = int(input("Masukkan Pilihan Login [1-3]: "))

    if login == 1 :
        username = input('Masukan Username : ')
        password = input('Masukkan Password : ')
        if username == 'admin1' and password == 'server1' or username =='admin2' and password == 'server2':
            while True :
                os.system ('cls')
                print ('1. Daftar Pemesan')
                print ('2. Cari Data Pemesan')
                print ('3. Grafik Penjualan')
                print ('4. Selesai')
                pilih = int(input('Masukan Pilihan Menu [1-4] : '))

                if pilih == 1 :
                    showAllDataPemesan()
                elif pilih == 2 :
                    showDataPemesan()
                elif pilih == 3 :
                    showGrafikPenjualan()
                elif pilih == 4 :
                    break
                else :
                    print('Menu Tidak Terdaftar')
                os.system ('pause')
        else :
            print('Username atau Password Salah')
        os.system('pause')

    elif login == 2 :
                while True :
                    os.system ('cls')
                    print ('1. Pemesanan Kereta Api')
                    print ('2. Lihat Data Pemesanan')
                    print ('3. Pembayaran')
                    print ('4. Ubah Data Pemesanan')
                    print ('5. Pembatalan ')
                    print ('6. Cetak Ulang Bukti Pembayaran')
                    print ('7. Selesai')
                    pilih = int(input('Masukan Pilihan Menu [1-5] : '))

                    if pilih == 1 :
                        selectMenu()
                    elif pilih == 2 :
                        showDataPemesan()
                    elif pilih == 3 :
                        pembayaranPesanan()
                    elif pilih == 4 :
                        updateDataPemesan()
                    elif pilih == 5 :
                        deleteDataPemesan()
                    elif pilih == 6 :
                        cetakUlangStruk()
                    elif pilih == 7 :
                        break
                    else :
                        print('Menu Tidak Terdaftar')
                    os.system ('pause')
    elif login == 3 :
        break
    else :
        print('Menu Tidak Tersedia')
    os.system('pause')