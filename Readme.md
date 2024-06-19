# Membership_UNOB_ws

repository for school web scraping project of unob IS

## Task

### 3. Naplnění dat o členství

Využijte zdroje dat pro získání informací o členství osob ve skupinách (GQL_UG). Vytvořte JSON datovou strukturu (kompatibilní se systemdata.json). Vytvořte program, který importuje data do GQL endpointů (s využitím mutací). Zabezpečte existenci propojení (ExternalIDs) se zdrojovým IS.<br />

### Společné podmínky

Testujte **duplicitu** dat, jednak přes externalid a jednak, kde je to možné, přes jména či jiné identifikátory.<br />

Pro práci s html daty (získání html stránek) použijte knihovnu **selenium** (headless mode).<br />

Vytvořte a publikujte **pypi package**. Součastí github respository (source for package) je i ipynb notebook s demonstrací využití (import package, run main code). Nechť je možné importovat funkci gather z root balíčku (pypi package).<br />

Hlavní funkce **gather()** pracuje s následujícími parametry:

    - username: Přihlašovací jméno

    - password: Přihlašovací heslo

    - config: {paths: {planovaneudalosti: “”, planovanivyuky_attributy: “”, vav_departments: “”. … }} (defaultni hodnota)

    - output (systemdata.json, writetogql)

    - **extras (token!)

U entit naplňte všechny atributy, pokud ve zdroji některé atributy nejsou, domluvte se na jejich dummy values.<br />

Pokud máte u entit k dispozici atributy navíc, navrhněte rozšíření GQL endpointu.<br />

# JSON requirements

## Before you run main.py please create "credentials.json" with this format:

```json
{
  "username": "your unob email",
  "password": "your password"
}
```

### Requirements

Python 3.10.10 is required to run this program. Additional libraries are listed in "requirements.txt" you can install them with this command:

```bash
pip install -r requirements.txt
```

Or you can create .venv with "requirements.txt".
