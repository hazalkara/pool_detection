# CSI Kamera ile Mavi Renk Tespiti ve Görüntü Aktarımı

Bu Python uygulaması, CSI kameradan görüntü alır ve mavi renk tespiti yapar. Görüntü üzerindeki mavi alanı tanır ve bu alanın merkez koordinatlarını ve çapını hesaplar. Ardından görüntüyü bir sunucuya iletir.

## Kullanım

1. Proje dosyalarınızın bulunduğu dizine gidin.

2. `main.py` dosyasını çalıştırarak uygulamayı başlatın.

3. Mavi alanı kameranın önünde tutun ve uygulamanın mavi renk tespiti yapmasını bekleyin.

4. Bulunan mavi alanın merkez koordinatları ve çapı hesaplanır ve sonuçlar bir sunucuya iletilir.

5. Pencere kapatmak için 'q' tuşuna basabilirsiniz.


## Gereksinimler

Bu projeyi çalıştırmak için aşağıdaki kütüphanelere ihtiyacınız vardır:

- OpenCV (`cv2`)
- NumPy
- Pickle
- Socket


