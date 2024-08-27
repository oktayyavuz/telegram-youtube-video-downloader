# 📹 Telegram YouTube Video İndirme Botu

Bu Telegram botu, kullanıcılara YouTube video bağlantısı göndererek videoları indirme ve alma imkanı sunar. Kullanıcılar, video kalitesini seçebilir ve bot, videoyu indirme, büyük dosyaları bölme ve videoyu kullanıcıya gönderme işlemlerini otomatik olarak halleder.

## 🚀 Özellikler 

- YouTube videolarını farklı kalitelerde indirme (1080p, 720p, 480p).
- 2GB'den büyük videoları otomatik olarak daha küçük parçalara böler.
- Video indirme ve yükleme süreçleri için ilerleme durumu bildirimi.
- Videoyu gönderdikten sonra geçici dosyaları temizler.

## 🛠️ Kurulum

1. Repoyu klonlayın:

   ```bash
   git clone https://github.com/oktayyavuz/telegram-youtube-video-downloader.git
   cd telegram-youtube-video-downloader
   ```

2. Gerekli Python paketlerini yükleyin:

   ```bash
   pip install -r requirements.txt
   ```

3. Ortam değişkenlerinizi ayarlayın:

   - `API_ID`: Telegram API ID'niz
   - `API_HASH`: Telegram API Hash'iniz
   - `BOT_TOKEN`: Telegram Bot Token'ınız

4. Botu çalıştırın:

   ```bash
   python main.py
   ```

## 📚 Kullanım

1. Telegram'da botu başlatın.
2. Bota bir YouTube video bağlantısı gönderin.
3. Sağlanan düğmelerden istediğiniz video kalitesini seçin.
4. Botun videoyu indirip, işleyip ve size göndermesini bekleyin.

## 📋 Gereksinimler

- Python 3.7 veya üzeri
- Sisteminizde yüklü olan FFmpeg

## 📦 Bağımlılıklar

- `pyrogram`: Bir Telegram MTProto API İstemci Kütüphanesi ve Framework
- `yt-dlp`: YouTube ve diğer sitelerden video indirmek için bir komut satırı programı
- `moviepy`: Video düzenleme için bir Python modülü

## 📄 Lisans

Bu proje MIT Lisansı altında lisanslanmıştır.

---

## ❓ Telegram Botu Oluşturma ve API Bilgileri Alma

### 1. Telegram Botu Oluşturma

1. **Telegram'ı açın** ve [@BotFather](https://t.me/botfather) ile sohbet başlatın.
2. `/start` komutunu gönderin.
3. `/newbot` komutunu gönderin.
4. Botunuza bir ad ve kullanıcı adı verin.
5. BotFather, size bir API Token verecek. Bu token'ı not edin; botunuzu çalıştırırken ihtiyacınız olacak.

### 2. Telegram API ID ve API Hash Alma

1. **[Telegram Developer Platformu](https://my.telegram.org/auth)** adresine gidin.
2. **Telegram hesabınızla** giriş yapın.
3. **API Development Tools** bölümüne gidin ve **Create new application** seçeneğine tıklayın.
4. Uygulamanız için bir **isim** ve **kısa bir açıklama** girin. 
5. **Create application** butonuna tıklayın.
6. API ID ve API Hash bilgilerinizi göreceksiniz. Bu bilgileri not edin; botunuzun çalışması için gerekecek.

---

Bu adımları takip ederek botunuzu başarıyla oluşturabilir ve yapılandırabilirsiniz. Daha fazla yardım için [Telegram Bot API Dokümantasyonu](https://core.telegram.org/bots/api) ve [Python-telegram-bot Kütüphanesi Dokümantasyonu](https://python-telegram-bot.readthedocs.io/) gibi kaynakları inceleyebilirsiniz.
