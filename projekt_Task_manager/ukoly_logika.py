#čistá logika bez input()/print() → testovateľná

def add_task_overenie_input(nazev_ukolu: str, popis_ukolu: str) -> str: # -> oznacuje, ze funkccia vrati retazec. 
    nazev_ukolu = nazev_ukolu.strip()
    popis_ukolu = popis_ukolu.strip()
    if not nazev_ukolu or not popis_ukolu:
        return ""
    return f"{nazev_ukolu}: {popis_ukolu}" 