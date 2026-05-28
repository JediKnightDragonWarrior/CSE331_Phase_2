# CSE 331 Project Phase 2 - Fair Share Scheduler

Bu dizin, Linux 2.4.27 çekirdeğine eklenen **Fair Share Scheduler (Adil Paylaşımlı Zamanlayıcı)** projesinin Faz 1 ve Faz 2 kaynak kodlarını ve test otomasyon dosyalarını içermektedir.

---

## 📂 Dosya Yapısı ve Eşleşmeleri (File Mappings)

Dosyalar, çekirdek kaynak ağacındaki (kernel source tree) ve sistem kullanıcı alanındaki (user space) klasör yapılarına göre gruplandırılmıştır:

### 1. Çekirdek Kodları (Kernel Space Changes)
*   `kernel/sched.c` ➔ `/usr/src/kernel-source-2.4.27/kernel/sched.c` *(Zamanlayıcı çekirdek mantığı)*
*   `fs/phase2switch.c` ➔ `/usr/src/kernel-source-2.4.27/fs/phase2switch.c` *(Faz 2 sistem çağrısı)*
*   `fs/getProcessInfoS26.c` ➔ `/usr/src/kernel-source-2.4.27/fs/getProcessInfoS26.c` *(Faz 1 sistem çağrısı)*
*   `fs/Makefile` ➔ `/usr/src/kernel-source-2.4.27/fs/Makefile` *(Derleme ayarları)*
*   `arch/entry.S` ➔ `/usr/src/kernel-source-2.4.27/arch/i386/kernel/entry.S` *(Sistem çağrısı vektör eşlemesi)*
*   `include/kernel_unistd.h` ➔ `/usr/src/kernel-source-2.4.27/include/asm-i386/unistd.h` *(Çekirdek tarafındaki sistem çağrısı numaraları)*
*   `include/getProcessInfoS26.h` ➔ `/usr/src/kernel-source-2.4.27/include/linux/getProcessInfoS26.h` *(Faz 1 Çekirdek Header'ı)*

### 2. Kullanıcı Seviyesi Tanımlamaları (User Space Mappings)
Derleyicinin kullanıcı alanında (user space) derleme yaparken sistem çağrısı numaralarını ve yapıları (struct) tanıyabilmesi için bu dosyalar kopyalanmalıdır:
*   `include/user_unistd.h` ➔ `/usr/include/asm/unistd.h` *(Kullanıcı tarafındaki sistem çağrısı numaraları - Derleyicinin hata vermemesi için çok önemlidir!)*
*   `user_space/getProcessInfoS26.h` ➔ `/usr/include/linux/getProcessInfoS26.h` *(Faz 1 Kullanıcı Header'ı)*

### 3. Test ve Analiz Araçları
Tüm bu dosyalar `/home/cse331` (veya testleri koşturacağınız ana kullanıcının ev dizini) altına kopyalanmalıdır:
*   `user_space/test_syscall.c` *(Zamanlayıcı modları arasında geçişi sağlayan kullanıcı programı)*
*   `user_space/infinite.c` *(Testler için CPU-bound sonsuz döngü yük oluşturucu)*
*   `user_space/run_tests.sh` *(Test akışını, top çıktılarını ve MSE analizini otomatize eden Bash betiği)*
*   `user_space/calculate_mse.py` *(Top çıktılarını ayrıştırıp istatistiksel MSE ve RMSE hesaplayan Python kodu)*

---

## 🛠️ Kurulum ve Derleme (Installation & Compilation)

### Adım 1: Çekirdek Kodlarını Kopyalayın
Yukarıdaki eşleşmeler listesine uygun olarak, `kernel`, `fs`, `arch` ve `include` altındaki çekirdek dosyalarını çekirdek kaynak dizininize (`/usr/src/kernel-source-2.4.27/`) kopyalayın.

*Not: Kopyalarken dosya adlarını hedefteki gibi `unistd.h` olarak değiştirmeyi unutmayın:*
```bash
# Örnek:
cp include/kernel_unistd.h /usr/src/kernel-source-2.4.27/include/asm-i386/unistd.h
```

### Adım 2: Kullanıcı Seviyesi Sistem Tanımlamalarını Güncelleyin
Derleyicinizin `test_syscall.c`'yi derlerken `set_fair_share` sistem çağrısı numarasını tanıyabilmesi için aşağıdaki kopyalamayı yapın:
```bash
cp include/user_unistd.h /usr/include/asm/unistd.h
cp user_space/getProcessInfoS26.h /usr/include/linux/getProcessInfoS26.h
```

### Adım 3: Çekirdeği Derleyin ve Kurun
Çekirdek kaynak dizinine gidip yeni çekirdeği derleyin ve sisteme kurun:
```bash
cd /usr/src/kernel-source-2.4.27
make dep && make bzImage && make modules && make modules_install
cp arch/i386/boot/bzImage /boot/vmlinuz-2.4.27-fair
```
Sistem açılış yöneticisine (GRUB veya LILO) yeni çekirdeği ekleyin ve sanal makineyi bu çekirdekle yeniden başlatın.

### Adım 4: Test Programlarını Derleyin
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
3.  Arka planda süreçleri başlatın:
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

Script tamamlandığında hem default çekirdek zamanlayıcısı hem de **Fair Share** zamanlayıcınız için MSE analiz raporu otomatik olarak ekrana yazdırılacaktır.
