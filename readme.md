# Troll the Triangle
Hra na hrací ploše 28x28, kde hráč sbírá mince a bojuje proti nepřátelům (trojúhelníkům). Na některých levelech může narazit na nepřátele nebo loot, který mu rozšiřuje možnosti.   
Hlavním konceptem hry je nekontaktní bojový systém, kdy hráč vyhrává souboje tím, že je přežije déle než jeho protivník. K tomu mu pomáhá náhodné přemisťování zdí na hrací ploše, když do ní vejde.
Hra je napsána v Pythonu s využitím knihovny Tkinter pro grafické rozhraní

## Ovládání
*Bude doplněno později*

## Vytvoření vlastního levelu
Levely jsou vytvářeny jako obrázky 28x28 pixelů, kde každý pixel reprezentuje jeden čtverec na hrací ploše. Barvy pixelů určují typ čtverce podle následujícího klíče:
- Černá (0,0,0): Prázdný čtverec
- Bílá (255,255,255): Zeď
- Červená (255,0,0): Neprolomitelná zeď
- Zelená (0,255,0): Místo spawnování hráče
- Modrá (0,0,255): Výstup z levelu
- Žlutá (255,255,0): Vstup do levelu
- Azurová (0,255,255): Loot
Pro vytvoření vlastního levelu můžete použít jakýkoliv grafický editor, který umožňuje přesné nastavení barev pixelů. Po vytvoření obrázku jej uložte do složky `levels` ve formátu PNG a ujistěte se, že má rozměry 28x28 pixelů. Název souboru pak použijte při načítání levelu ve hře. Bitová hloubka obrázku by měla být 24-bitová (True Color), aby byly barvy správně rozpoznány.
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