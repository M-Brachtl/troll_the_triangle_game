# Troll the Triangle
Hra na hrací ploše 28x28, kde hráč sbírá mince a bojuje proti nepřátelům (trojúhelníkům). Na některých levelech může narazit na nepřátele nebo loot, který mu rozšiřuje možnosti.   
Hlavním konceptem hry je nekontaktní bojový systém, kdy hráč vyhrává souboje tím, že sbírá DamageCoiny, které poškozují nepřátele. K tomu mu pomáhá náhodné přemisťování zdí na hrací ploše, když do ní vejde.
Hra je napsána v Pythonu s využitím knihovny Tkinter pro grafické rozhraní

## Ovládání
### Pohyb
- Šipka nahoru: Pohyb nahoru
- Šipka dolů: Pohyb dolů
- Šipka vlevo: Pohyb vlevo
- Šipka vpravo: Pohyb vpravo
### Tlačítka
- Q: Použití schopnosti "Wall Move" (přesune zeď na random pozici)
- W: Použití schopnosti "Wall Destroy" (zničí zeď)
- E: Použití schopnosti "Wall Pass" (projde skrz zeď)

## Herní mechaniky
### Ability Loot
Na hrací ploše se může objevit loot, který hráči poskytne novou schopnost. Schopnosti jsou:
- Wall Destroy: Umožňuje hráči přesunout zničit zeď, do které vejde.
- Wall Pass: Umožňuje hráči projít skrz zeď.
- Exit 75 Percent: Umožňuje hráči opustit level, pokud je zdraví nepřítele pod nebo rovno 75 % jeho původního zdraví.
- Revive: Umožňuje hráči oživit se po smrti s 50 % zdraví.
- Fast HP Recovery: Zvyšuje rychlost regenerace zdraví hráče.
- Slow Enemies: Snižuje rychlost pohybu nepřátel.
- Wall Cheap: Snižuje cenu použití schopnosti Wall Move.

Schopnost Wall Move je dostupná od začátku hry a umožňuje hráči přesunout zeď na náhodnou volnou pozici na hrací ploše.
### Bojový systém
Hráč bojuje proti nepřátelům (trojúhelníkům) tím, že sbírá DamageCoiny. Každý DamageCoin způsobí určité množství poškození nepříteli, když do něj hráč narazí. Nepřátelé mají své vlastní zdraví a mohou být poraženi, pokud jejich zdraví klesne na nulu. Hráč také utrpí poškození při kontaktu s nepřítelem:
- Každý DamageCoin způsobí 5 bodů poškození nepříteli.
- Při kontaktu s nepřítelem hráč ztratí 10 bodů zdraví a nepřítel ztratí 1 bod zdraví, hráč je přesunut zpět na startovní pozici.

### Smrt
Pokud zdraví hráče klesne na nulu, level se resetuje, včetně množství mincí, které měl hráč na začátku levelu.

## Vytvoření vlastního levelu
Levely jsou vytvářeny jako obrázky 28x28 pixelů, kde každý pixel reprezentuje jeden čtverec na hrací ploše. Barvy pixelů určují typ čtverce podle následujícího klíče:
- Černá (0,0,0): Prázdný čtverec
- Bílá (255,255,255): Zeď
- Červená (255,0,0): Neprolomitelná zeď (ve hře světlá šedá)
- Zelená (0,255,0): Místo spawnování nepřítele (trojúhelníka)
- Modrá (0,0,255): Výstup z levelu (ve hře tmavě zelená)
- Žlutá (255,255,0): Vstup do levelu (ve hře světle modrá)
- Azurová (0,255,255): Loot  

Pro vytvoření vlastního levelu můžete použít jakýkoliv grafický editor, který umožňuje přesné nastavení barev pixelů. Po vytvoření obrázku jej uložte do složky `levels` ve formátu PNG a ujistěte se, že má rozměry 28x28 pixelů. Název souboru pak použijte při načítání levelu ve hře. Bitová hloubka obrázku by měla být 24-bitová (True Color), aby byly barvy správně rozpoznány.  
Mapa musí mít vstup a výstup, pro správné fungování hry. Spawner nepřítele je volitelný.
<span style="color:red;">Soubor ukládejte ve formátu "nazev.png", nikoli "nazev.lvl.png"</span>

**<span style="color:red;">Není ještě implementováno vlastní vkládání obrázků</span>**

## Spuštění hry ze zdrojového kódu
### Vytvoření virtuálního prostředí:
```bash
python -m venv venv
```
#### Aktivace virtuálního prostředí:  
Windows:
```cmd
venv\Scripts\activate
```
Linux/Mac:
```bash
source venv/bin/activate
```

#### Instalace závislostí:
```bash
pip install -r requirements.txt
```
### Spuštění hry:
```bash
python main.py
```