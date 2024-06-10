# Online Konzultacije FIPU

---

Ovaj projekt omogućava studentu upravljanje i praćenje terminima konzultacija na Fakultetu informatike.
Web servis omogućava pregled, dodavanje, uređivanje i brisanje termina konzultacija. Ovaj web servis je osmišljen kao pomoć studentima za lakše praćenje obaveza "konzultacija" na fakultetu.

---
## Use case
![use_case](https://github.com/LukaCatela/Projekt_IS/assets/161040078/465569d2-0731-4cd1-ae9a-639b017126f3)

## O projektu

Projekt je razvijen koristeći Python programski jezik i Flask framework za backend dio aplikacije. Za upravljanje bazom podataka koristi se Pony ORM, dok se frontend sastoji od HTML-a i CSS-a. Aplikacija je osmišljena kako bi bila jednostavna za korištenje, omogućujući korisnicima intuitivno upravljanje terminima konzultacija.
Ključne funkcionalnosti

  **Pregled termina konzultacija**: Korisnici mogu pregledavati sve dostupne termine konzultacija.
  
  **Dodavanje novih termina**: Profesori mogu dodavati nove termine konzultacija putem jednostavnog sučelja.
  
  **Uređivanje postojećih termina**: Profesori mogu ažurirati podatke o postojećim terminima konzultacija.
  
  **Brisanje termina**: Profesori mogu brisati termine koji više nisu aktualni.

Instalacija

Skidanje koda s GitHub-a:

cd ~/Downloads
git clone https://github.com/LukaCatela/Projekt_IS
cd Projekt_IS

Docker tutorial:

docker build -t Projekt_IS .
docker ps
docker run -p 5001:5000 Projekt_IS

