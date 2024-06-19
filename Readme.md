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

### Initialization process

We already published our project as a Pypi package so in file 'requirement.txt' you just need to add "membershipUNOB", it will automatically install all the libraries and dependencies.<br />
Move on to the next step, please create main.py file and in this file please import "membershipUNOB" just like code below:<br />
![image](https://github.com/Getbricked/MembershipUNOB/assets/115787629/7230b3bc-e0c5-4d9f-b117-8827bd64ef37)<br />

Once you have done all these steps, all you have to do is run the main.py flle and after that a "config.ini" file will pop up just like this.<br />
![image](https://github.com/Getbricked/MembershipUNOB/assets/115787629/1295c47c-7777-4d58-ac8a-9efd577d849e)<br />

In 'config.ini' You can adjust the data retrieval from the website of the university or import data, which you scrape, into the GQL endpoint, depending on how you want






