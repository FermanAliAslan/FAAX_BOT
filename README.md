# Discord Pokémon & Quiz Bot + Project Tracker

Bu proje, Discord üzerinde çalışabilen bir **bot sistemi**, bir **quiz sistemi**, **Pokemon mini oyunları** ve **proje yönetim veritabanı** ile entegre bir şekilde çalışan bir bot geliştirmek amacıyla oluşturulmuştur.

Bot, kullanıcıların Discord üzerinde Pokémon yakalamasına, beslemesine, saldırı yapmasına, evrim geçirmesine ve quiz oynamasına olanak tanır. Ayrıca projelerinizi ve yeteneklerinizi takip etmek için SQLite tabanlı bir **project tracker** içerir.

---

## Özellikler

### 1. Discord Bot
- **Komutlar:**
  - `!start` : Pokémon yakala.
  - `!info` : Pokémon bilgilerini görüntüle.
  - `!attack` : Saldırı yap.
  - `!feed` : Pokémon'u besle.
  - `!status` : Pokémon durum raporu.
  - `!heal` : Pokémon'u tamamen iyileştir.
  - `!evolve` : Pokémon evrim geçirebilir.
  - `!release` : Pokémon'u doğaya sal.
  - `!img` : Pokémon GIF göster.
  - `!startquiz` : Quiz başlat.

- **Quiz Sistemi:**
  - Dinamik butonlar ile interaktif quizler.
  - Doğru/yanlış cevap kontrolü.
  - Puanlama ve quiz bitiş mesajı.

---

### 2. Pokémon Mini Oyunu
- Pokémon sınıfları: **Normal**, **Wizard**, **Fighter**.
- Her Pokémon'un HP ve Power değeri vardır.
- Besleme sistemi ile HP arttırma.
- Saldırı ve evrim mekanizması.
- Async HTTP çağrısı ile Pokémon isimleri ve görselleri API’den alınır.

---

### 3. Project Tracker (SQLite)
- **Tablolar:**
  - `projects`: Kullanıcı projeleri.
  - `skills`: Yetkinlikler.
  - `project_skills`: Proje ve yetenek ilişkisi.
  - `status`: Proje durumları.
- CRUD işlemleri desteklenir:
  - Proje ekleme, güncelleme, silme.
  - Yetkinlik ekleme ve silme.
  - Durum takip sistemi.
- Veritabanı `db_manager.py` ile yönetilir.

---

## Kurulum

1. Projeyi klonlayın:
```bash
git clone https://github.com/kullanici/discord-pokemon-quiz.git
cd discord-pokemon-quiz
