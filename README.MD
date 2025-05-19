# 🔢 Centratea – Bulls & Cows Multiplayer TCP Game 🧠

**Centratea** este un joc simplu de tip "Bulls & Cows" (4 cifre diferite) implementat în Python folosind socket-uri TCP.  
Proiectul simulează un joc multiplayer unde mai mulți jucători încearcă să ghicească un număr secret generat de server.  
Primul care ghicește câștigă, iar jocul se resetează automat.

---

## 🚀 Funcționalități

- 🧠 Server TCP concurent (`threading`)
- 👥 Suport pentru mai mulți clienți simultan
- 🔢 Număr generat random (4 cifre diferite)
- 🧪 Verificare și feedback pentru fiecare încercare
- 🏁 Nume unic pentru fiecare jucător
- 📈 Număr de încercări contorizat
- 🏆 Anunț câștigător + restart joc automat

---
## 🧪 Exemplu rulare
python server.py
python client.py

> Trimite un număr: 1234
2 centrate, 1 necentrată

> Trimite un număr: 1987
🎉 Playerc9f1 a ghicit numărul 1987 în 5 încercări!
🔁 Joc nou! Ghiciti noul număr cu 4 cifre diferite.




