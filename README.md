# CSE 331 Project Phase 2 - Fair Share Scheduler

Bu dizin, Linux 2.4.27 çekirdeğine eklenen **Fair Share Scheduler (Adil Paylaşımlı Zamanlayıcı)** projesinin Faz 1 ve Faz 2 kaynak kodlarını ve test otomasyon dosyalarını içermektedir.

---

## 📂 Dosya Yapısı ve Eşleşmeleri (File Mappings)

Dosyalar, çekirdek kaynak ağacındaki (kernel source tree) klasör yapılarına göre gruplandırılmıştır:

### 1. Çekirdek Kodları (Kernel Space Changes)
*   `kernel/sched.c` ➔ `/usr/src/kernel-source-2.4.27/kernel/sched.c` *(Zamanlayıcı çekirdek mantığı)*
*   `fs/phase2switch.c` ➔ `/usr/src/kernel-source-2.4.27/fs/phase2switch.c` *(Faz 2 sistem çağrısı)*
*   `fs/getProcessInfoS26.c` ➔ `/usr/src/kernel-source-2.4.27/fs/getProcessInfoS26.c` *(Faz 1 sistem çağrısı)*
*   `fs/Makefile` ➔ `/usr/src/kernel-source-2.4.27/fs/Makefile` *(Derleme ayarları)*
*   `arch/entry.S` ➔ `/usr/src/kernel-source-2.4.27/arch/i386/kernel/entry.S` *(Sistem çağrısı vektör eşlemesi)*
*   `include/unistd.h` ➔ `/usr/src/kernel-source-2.4.27/include/asm-i386/unistd.h` *(Sistem çağrısı numaraları)*
*   `include/getProcessInfoS26.h` ➔ `/usr/src/kernel-source-2.4.27/include/linux/getProcessInfoS26.h` *(Faz 1 Çekirdek Header'ı)*

### 2. Kullanıcı Seviyesi Araçlar ve Testler (User Space & Tests)
Tüm bu dosyalar `/home/cse331` (veya testleri koşturacağınız ana kullanıcının ev dizini) altına kopyalanmalıdır:
*   `user_space/test_syscall.c` *(Zamanlayıcı modları arasında geçişi sağlayan kullanıcı programı)*
*   `user_space/infinite.c` *(Testler için CPU-bound sonsuz döngü yük oluşturucu)*
*   `user_space/run_tests.sh` *(Test akışını, top çıktılarını ve MSE analizini otomatize eden Bash betiği)*
*   `user_space/calculate_mse.py` *(Top çıktılarını ayrıştırıp istatistiksel MSE ve RMSE hesaplayan Python kodu)*
*   `user_space/getProcessInfoS26.h` ➔ `/usr/include/linux/getProcessInfoS26.h` dizinine kopyalanmalıdır *(Faz 1 Kullanıcı Header'ı)*

---

## 🛠️ Kurulum ve Derleme (Installation & Compilation)

### Adım 1: Dosyaları Kopyalayın
Yukarıdaki eşleşmeler listesine uygun olarak, `kernel`, `fs`, `arch`, `include` dizinlerindeki dosyaları çekirdek kaynak dizininize (`/usr/src/kernel-source-2.4.27/`) kopyalayın. 

Ayrıca `user_space/getProcessInfoS26.h` dosyasını `/usr/include/linux/getProcessInfoS26.h` olarak kopyalayın.

### Adım 2: Çekirdeği Derleyin
Çekirdek kaynak dizinine gidip yeni çekirdeği derleyin ve sisteme kurun:
```bash
cd /usr/src/kernel-source-2.4.27
make dep && make bzImage && make modules && make modules_install
cp arch/i386/boot/bzImage /boot/vmlinuz-2.4.27-fair
```
Sistem açılış yöneticisine (GRUB veya LILO) `/boot/vmlinuz-2.4.27-fair` çekirdeğini ekleyin ve sanal makineyi bu çekirdekle yeniden başlatın.

### Adım 3: Test Programlarını Derleyin
`user_space/` dizinindeki test araçlarını derleyin:
```bash
# Sistem çağrısı değiştiriciyi derleyin
gcc test_syscall.c -o test_syscall

# Yük oluşturucuyu derleyin
gcc infinite.c -o infinite
```

---

## 📊 Testlerin Çalıştırılması (Running Tests)

1.  Sistemde `u1` ve `u2` adında iki adet sıradan (root olmayan) kullanıcı oluşturun:
    ```bash
    useradd -m u1
    useradd -m u2
    ```
2.  `infinite` programını `u1`'in ev dizinine `u1p1` adıyla, `u2`'nin ev dizinine ise `u2p1` ve `u2p2` adıyla kopyalayın.
3.  İlgili kullanıcı terminallerine geçip bu süreçleri arka planda başlatın:
    ```bash
    # u1 kullanıcısında:
    ./u1p1 &
    
    # u2 kullanıcısında:
    ./u2p1 &
    ./u2p2 &
    ```
4.  Ana terminale (veya `cse331` kullanıcısına) dönüp `run_tests.sh` scriptini çalıştırın:
    ```bash
    chmod +x run_tests.sh
    ./run_tests.sh
    ```

Script tamamlandığında hem default (varsayılan) çekirdek zamanlayıcısı hem de sizin özel **Fair Share** zamanlayıcınız için MSE (Mean Squared Error) analiz raporu otomatik olarak terminale yazdırılacaktır.
