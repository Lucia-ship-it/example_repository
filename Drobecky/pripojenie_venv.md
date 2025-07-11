na pripojenie pymysql
        
        # Open the integrated terminal in VS Code.
        # Run python3 -m venv .venv to create a virtual environment.
        # Activate it with source .venv/bin/activate.
        # Run pip install PyMySQL inside the activated environment.

1. Virtuálne prostredie nie je aktivované pri spustení programu

Keď spúšťaš program, musíš mať aktívne virtuálne prostredie, aby Python vedel používať nainštalované balíčky.

Skús ešte raz aktivovať prostredie pred spustením programu.

source .venv/bin/activate
python <tvoj_program>.py

2. Nainštalovaný balík je v inom prostredí

Skontroluj, že po aktivácii máš nainštalovaný PyMySQL:

pip list

3. Python používa iný interpreter

Vo VS Code sa často stáva, že je nastavený iný Python interpreter, ktorý nemá nainštalované balíčky.

Skontroluj v ľavom dolnom rohu VS Code, ktorý Python interpreter je aktívny (mala by tam byť cesta k .venv).

Ak nie, zmeň interpreter cez Ctrl+Shift+P → Python: Select Interpreter → vyber ten v .venv.