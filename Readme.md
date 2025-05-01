# Membership_UNOB_ws

Repository pro školní projekt webového scrappingu UNOB IS.

---

## Úkol

### 3. Vyplnění údajů o členství

Využijte zdroje dat k získání informací o členství jednotlivců ve skupinách (GQL_UG). Vytvořte datovou strukturu JSON (kompatibilní se `systemdata.json`). Vypracujte program pro import těchto dat do GQL endpointů (pomocí mutací). Zajistěte existenci propojení (ExternalIDs) se zdrojovým IS.

### Společné požadavky

- Testujte na **duplicitní data**, a to jak pomocí `externalid`, tak, kde je to možné, podle jmen nebo jiných identifikátorů.
- Použijte knihovnu **Selenium** (v režimu headless) pro práci s HTML daty (stahování HTML stránek).
- Vytvořte a publikujte **PyPI balíček**. GitHub repozitář (zdroj balíčku) by měl obsahovat Jupyter notebook (`.ipynb`) demonstrující jeho použití (import balíčku a spuštění hlavního kódu). Balíček by měl umožnit import funkce `gather` z kořenového balíčku.

### Hlavní funkce: `main()`

Funkce `main()` by měla pracovat s následujícími parametry:

- `username`: Přihlašovací jméno.
- `password`: Přihlašovací heslo.
- `config`: Slovník s cestami pro uživatele, skupiny, členství atd. (výchozí hodnota je poskytnuta).
- `output`: Možnosti výstupu (`systemdata.json`, `writetogql`).
- `extras`: Další parametry (např. `token`).

Vyplňte všechny atributy pro entity. Pokud některé atributy ve zdroji chybí, dohodněte se na výchozích hodnotách. Pokud jsou k dispozici další atributy, navrhněte rozšíření GQL endpointu.

---

## Požadavky na JSON

### Před spuštěním `main.py`

Vytvořte soubor `credentials.json` s následujícím formátem:

```json
{
  "username": "vaše unob email",
  "password": "vaše heslo"
}
```

---

## Proces inicializace

### Instalace balíčku

Balíček můžete nainstalovat přímo pomocí následujícího příkazu:

#### Pro verzi 2.0.1:

```bash
pip install membershipUNOB
```

### Zdroj

[PyPI: membershipUNOB](https://pypi.org/project/membershipUNOB/)

---

### Použití balíčku ve vašem projektu

Projekt je publikován jako PyPI balíček. Pro jeho použití přidejte `membershipUNOB` do vašeho souboru `requirements.txt`. Tím se automaticky nainstalují všechny potřebné knihovny a závislosti.

Poté vytvořte soubor `main.py` a importujte `membershipUNOB` následujícím způsobem:

```python
from membershipUNOB import main
```

Po dokončení těchto kroků spusťte soubor `main.py`. Vygeneruje se soubor `config.ini`, podobný příkladu níže:

![Config Example](https://github.com/Getbricked/MembershipUNOB/assets/115787629/1295c47c-7777-4d58-ac8a-9efd577d849e)

V souboru `config.ini` můžete upravit nastavení pro získávání dat z univerzitního webu nebo import dat do GQL endpointu podle vašich požadavků.

---

### Vysvětlení `config.ini`

Výchozí hodnota všech konfigurací je `true`. Níže jsou uvedeny dostupné možnosti:

#### Web scraping a extrakce dat

1. `get_data`: Provádí web scraping pro aktualizaci aktuálních dat při změnách.
2. `extract_data`: Extrahuje data o členství a externích ID uživatelů a skupin.

#### Import dat

3. `users`: Importuje data uživatelů do GQL endpointu.
4. `groups`: Importuje data skupin do GQL endpointu.
5. `memberships`: Importuje data o členství do GQL endpointu.
