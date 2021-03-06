# Arduino Introduction

#### Schéma carte Arduino UNO Rev3

<img src="https://github.com/sirbrowser/astroworld/blob/master/images/Arduino1.png"><br>
Les 4 composants ici sont les Leds (Light-Emitting Diode) de l'Arduino.<br>

- La LED "ON" est verte quand l'Arduino est sous tension.
- Les LEDs "TX" et "RX" clignotent quand l'Arduino reçoit ou envoie de informations.
- La LED "L" clignote si on appuie sur le bouton reset

Une diode s'allume quand elle est parcourue par le BON courant dans le BON sens.

L'Arduino envoie du courant, ou non, par les connexions numétotées de 1 à 13 :<br>
<img src="https://github.com/sirbrowser/astroworld/blob/master/images/Arduino2.png"><br>

La LED "L" s'allume quand on dit à l'Arduino d'envoyer du courant dans la connexion 13.

Le langage Arduino  est basé sur le C.<br>
Le code est toujours de la forme suivante :<br>
```C
void setup() {
  // put your setup code here, to run once:

}

void loop() {
  // put your main code here, to run repeatedly:

}
```

Pour allumer la diode L continuellement on code :<br>
```C
void setup() {

  pinMode(13,OUTPUT);  // on dit a la connexion 13 qu'elle peut ENVOYER du courant
  digitalWrite(13,HIGH); //HIGH=1 et LOW=0 ou HIGH=+5V et LOW=0V

}

void loop() {
  // put your main code here, to run repeatedly:

}
```

Pour allumer la led 1 seconde et l'éteindre 1 seconde à l'infini :<br>
```C
void setup() {
  pinMode(13,OUTPUT);

}

void loop() {
  digitalWrite(13,HIGH);
  delay(1000);  //en ms
  digitalWrite(13,LOW);
  delay(1000);  // en ms

}
```

Un programme pour afficher des choses dans la console Arduino (la petite loupe en haut a gauche) :<br>
```C
void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);  
  Serial.println("Communication initialisée");
}

void loop() {
  // put your main code here, to run repeatedly:
  Serial.println("Je suis dans la boucle!");
}
```
Le 9600 dans les parenthèses de l'initialisation correspond à un nombre de caractères par seconde qu'on appelle des bauds. L'Arduino peut donc envoyer un maximum de 9600 caractères par seconde à l'ordinateur dans cette configuration.<br>
A ne pas confondre avec l'unité bps qui signifie bits par seconde. Un caractère pour l'Arduino c'est 8 bits.<br>

REMARQUE : <br>
Le moniteur série (console) utilise les connexions 0 et 1 de l'Arduino (0 pour la diode RX et 1 pour TX lors de l'utilisation en communication). Si on utilise le port série, il ne faut pas utiliser les connexions 0 et 1 pour d'autres choses dans le projet.<br>

connexion = pin !!

#### Electricité

L'arduino UNO propose à ses bornes (pin 0 à 13) une tension de +5V qui sort. Il utilise un courant continue (c'est toujours du +5V qui sort).<br>
On peut fournir à l'Arduino son alimentation de 3 façcons principales :
- via le cable USB car l'ordinateur fournit un courant de +5V par ce câble.
- via une pile 9V (entre 7V et 12v en réalité) via la prise ronde de l'arduino. Arduino transforme ensuite ces 9V en 5V.
- via un transformateur à la prise ronde (attention il faut que la connectique du transformateur soit correcte et qu'il fournisse bien la tension demandée (9V).

Le transformateur se branche sur du 220V, mais à l'intérieur du boitier il y a deux bobines qui transforment ces 220V en 9V, puis un redresseur de courant qui permet de transformer l'alternatif en courant continu.<br>
Rappel : pour la tension on a la [loi des mailles](https://fr.wikiversity.org/wiki/Loi_de_Kirchhoff/Loi_des_mailles) qui s'applique.<br>

L'intensité est la quantité de courant qui passe dans un endroit du circuit. elle est mesurée en Ampère (A).<br>
Rappel : pour l'intensité on a la [loi des noeuds](https://fr.wikipedia.org/wiki/Lois_de_Kirchhoff) qui s'applique.<br>

Rappel : la loi d'ohm --> U = R * I <br>

Une LED est un dipôle qui ne laisse passer le courant que dans **un seul sens**. C'est appelé un semi-conducteur.<br>
<img src=https://github.com/sirbrowser/astroworld/blob/master/images/LED.PNG><br>
Pour brancher la LED on doit brancher la patte la plus longue (anode ou +) du coté du 5V et la patte la plus courte (cathode ou -) du coté du 0V ou *ground*.<br>
Symboles représentant le ground et le +5V :<br>
<img src=https://github.com/sirbrowser/astroworld/blob/master/images/ground.PNG><br>

Sur l'arduino il y a 3 pins gnd, 1 pin 3.3V et 1 pin 5V :<br>
<img src=https://github.com/sirbrowser/astroworld/blob/master/images/pins.PNG><br>
Connecter directement la LED du 3.3V ou du 5V vers le ground sans résistance reste un risque pour la LED.<br>
Schéma de branchement de la LED :<br>
<img src=https://github.com/sirbrowser/astroworld/blob/master/images/LED2.PNG><br>

Schéma de la breadboard:<br>
<img src=https://github.com/sirbrowser/astroworld/blob/master/images/breadboard.PNG><br>
Les trous colorés sont connectés entre eux.<br>
Les deux grandes lignes servent souvent à relier les Vin(+5V) et les grounds (Gnd) entre eux :<br>
<img src=https://github.com/sirbrowser/astroworld/blob/master/images/breadboard2.PNG><br>

#### Calcul de la bonne valeur de résistance pour une LED
Tout matériel électronique est accompagné d'une fiche de spécifications techniques (datasheet).<br>
En lisant celle de la LED il faut retenir qu'une LED produit une chute de tension entre 1V et 4V (ca dépend des couleurs).<br>
Appelons la tensionde la LED "Uled" et la fixer à 1,8V par exemple. La tension fournie par l'arduino est de 5V, nous l'appelerons Ugen. La tension aux bornes de la resistance sera Ures. :<br>
<img src=https://github.com/sirbrowser/astroworld/blob/master/images/LED3.PNG><br>
D'après la loi des mailles on a : Ugen = Uled+Ures <==> Ures = Ugen - Uled = 5-1.8 = 3.2V --> la tension aux bornes de la résistance.<br>
Dans le datasheet on a aussi "l'intesité qui traverse la LED doit etre aux environs de 20mA soit 0.02A.<br>

Sur l'arduino la sortie 5V délivre un courant de 0.5A (500mA) et les pins de 0 à 13 produisent du 0.04A (40mA) et un max de 0.2A pour les 13 pins cumulés.<br>

Avec la loi d'Ohm : U=R*I <==> R=U/I =3.2/0.02 = 160ohm (en réalité on peut utiliser des résistances entre 100 et 1000ohms).<br>

!!!! [**Le code couleurs des résistances**](https://www.apprendre-en-ligne.net/crypto/passecret/resistances.pdf)!!!<br>
<img src=https://github.com/sirbrowser/astroworld/blob/master/images/LED4.PNG><br>

------------------------------------------------
La sortie 5V fournit du courant continuellement tandis que les pins de 1 à 13 ne fournissent du courant que par programmation.<br>

Connecter une LED sur un pin :<br>
<img src=https://github.com/sirbrowser/astroworld/blob/master/images/LED5.PNG><br>
```C
int pinLed=13; //variable pour le numéro de pin utilisé
void setup() {
  pinMode(pinLed,OUTPUT); //pin 13 en mode sortie de courant
}

void loop() {
  digitalWrite(pinLed,HIGH); //on passe le pin à +5V
  delay(1000);
  digitalWrite(pinLed,LOW); //on passe le pin à 0V
  delay(1000);

}
```
Autre méthode pour ménager la carte arduino :
L'exemple précédent utilise le pin 13 pour fournir du courant qui s'enfuit ensuite vers le Gnd. Cette méthode de branchement est correcte, mais elle demande de l'énergie à l'arduino, elle préfère absorber du courant qu'en fournir.<br>
Il faut donc monter le circuit à l'envers : on part du +5V de l'arduino puis on connecte la résistance et la LED puis on relie le tout au pin 13 (sans oublier la patte + de la LED vers le 5V)<br>
<img src=https://github.com/sirbrowser/astroworld/blob/master/images/LED6.PNG><br>

##### Objcetif : projet "Blink a trois"

description du programme :
- les trois LED sont étieintes
- les trois LED s'allument une seconde
- après une brève extinction de toutes les LED, les deux premières restent éteintes et la troisième s'allume une seconde
- extinction brève, puis LED 1 et LED3 éteintes, LED 2 allumée une seconde
- extinction brève, LED 1 allumée et LED 2 et LED 3 éteintes une seconde
- on retourne au début, mais le programme recommence avec un temps d'allumage de 0.8s puis 0.6s puis 0.4s puis 0.2
- le programme recommence au début

Le montage ressemble a ceci :<br>
<img src=https://github.com/sirbrowser/astroworld/blob/master/images/blink.PNG><br>
```C
int pled1, pled2, pled3;
void setup() {
  pled1=6;
  pled2=5;
  pled3=4;

  pinMode(pled1,OUTPUT);
  pinMode(pled2,OUTPUT);
  pinMode(pled3,OUTPUT);

  digitalWrite(pled1,LOW);
  digitalWrite(pled2,LOW);
  digitalWrite(pled3,LOW);
}

void loop() {
  digitalWrite(pled1,HIGH);
  digitalWrite(pled2,HIGH); 
  digitalWrite(pled3,HIGH);
  delay(1000);

  digitalWrite(pled1,LOW);
  digitalWrite(pled2,LOW);
  digitalWrite(pled3,LOW);
  delay(100);

  for(int i=1000;i>=200;i=i-200){
    digitalWrite(pled1,HIGH);
    delay(i);
    digitalWrite(pled1,LOW);
    delay(100);
    digitalWrite(pled2,HIGH);
    delay(i);
    digitalWrite(pled2,LOW);
    delay(100);
    digitalWrite(pled3,HIGH);
    delay(i);
    digitalWrite(pled3,LOW);
    delay(100);
  }
}
```

Un pin est soit en sortie (`digitalWrite(pin,état)`) soit en entrée (`digitalRead(pin)`) mais pas les deux.<br>
Il est donc important de bien définir si le pin va se comporter en entrée ou en sortie :<br>
- `pinMode(pin,OUTPUT)` --> pour indiquer à la carte que le pin doit être en mode écriture, cad qu'il peut envoyer ou non du courant. C'est donc une sortie.<br>
- `pinMode(pin,INPUT)` --> pour indiquer que le pin est en mode lecture. Il ne pilote pas le courant mais il va être à l'écoutedu courant qui va lui arriver.<br>

Avec la commande `digitalRead(pin)` on récupère ce que le pin entend en terme de courant.<br>

##### Le bouton poussoir
Le principe du bouton poussoir est que lorsque l'on appuie, le courant passe, et lorsque l'on relache le courant ne passe plus.<br>
Contrairement à un interrupteur, il ne garde pas la position (il faut garder le doigt dessus pour qu'il fasse contact).<br>

<img src=https://github.com/sirbrowser/astroworld/blob/master/images/poussoir.PNG><br>
<img src=https://github.com/sirbrowser/astroworld/blob/master/images/poussoir2.PNG><br>

Comment utiliser un bouton par programmation?
Tout simplement en le reliant à un pin qui est en mode lecture.<br>
L'arduino va pouvoir lire une valeur de +5V ou de 0V. Donc en théorie si on envoie le +5V sur un poussoir, quand il est baissé, il laisse passer le courant et l'Arduino reçoit +5V, il indique donc HIGH. Si le poussoir est ouvert, l'Arduino devrait ne rien recevoir, donc être à 0V et indiquer LOW.<br>
<img src=https://github.com/sirbrowser/astroworld/blob/master/images/poussoir3.PNG><br>
```C
int pinBouton;
void setup()
{
    Serial.begin(9600);
    pinBouton=10;
    pinMode(pinBouton,INPUT);
}
void loop()
{
    boolean etatBouton=digitalRead(pinBouton);
    Serial.println(etatBouton);
}
```
Ce programme ne marche pas. On voit bien s'afficher des 0, puis lorsque l'on appuie sur le bouton, on voit des 1 et en rela^chant ca reste à 1.<br>
Si on observe bien, le pin 10, quand le bouton est levé, n'est finalement connecté à rien. Le résultat lu par l'Arduino est donc peu interprétable. Il existe un moyen de forcer l'Arduino à lire quelque chose, tout simplement avec l'ajout d'une résistance...<br>

##### Résistance pull-down
L'éléctricité est paresseuse : elle va toujours choisir le chemin qui lui résiste le moins, mais si ellen'a pas le choix, elle passe tout de même la ou ça résiste.<br>
Nous allons donc ajouter une résistance à notre circuit. Une assez forte pour que le courant ne passe que s'il y est obligé (souvent de l'ordre de 10kΩ).<br>
<img src=https://github.com/sirbrowser/astroworld/blob/master/images/pull-down.PNG><br>
Que se passe-t-il dans ce circuit?<br>
Si le poussoir est baissé, le courant va du +5V au pin de l'Arduino. Il ne prendra pas le chemin du ground car la résistance lui demande un effort. Le pin de l'Arduino recevra du +5V et indiquera HIGH.<br>
Si le poussoir est levé le très faible courant résiduel qui sortira du pin de l'Arduinosera absorb par le Gnd, le pin sera donc bien en LOW.<br>
Ce montage est à connaître car quel que soit le type de contacteur (i.e poussoir) que vous placerez en lecture sur le pin, il vous faudra prévor ce comportement erratique.<br>
<img src=https://github.com/sirbrowser/astroworld/blob/master/images/pull-down2.PNG><br>

##### Résistance pull-up
Il est possible dans d'autres cas de monter la résistance, non pas vers le ground, mais vers le +5V. Il faut penser à connecter le poussoir au ground (et non plus au +5V) pour que tout fonctionne.<br>
<img src=https://github.com/sirbrowser/astroworld/blob/master/images/pull-up.PNG><br>
Quand le poussoir est ouvert, le +5V nourrit le pin de l'Arduino, qui donnera HIGH.<br>
Quand le poussoir est fermé, le +5V et le pin sont absorbés par le ground, le pin donnera LOW.<br>
Le fonctionnement en pull-up donne en lecture l'opposé du fonctionnement en pull-do<n.<br>

##### Le mode INPUT_PULLUP
La carte Arduino propose par défaut un mode qui permet d'activer une résistance de 20KΩ qui est dans la carte pour en faire une résistance pull-up. Pas besoin de se prendre la tête avec une résistance en plus, il suffit de connecter correctement le bouton poussoir en mode pull-up.<br>
<img src=https://github.com/sirbrowser/astroworld/blob/master/images/input_pull-up.PNG><br>
Pour activer la résistance : `pinMode(pin,INPUT_PULLUP)`<br>

**!!!** Attention, pour le pin 13, il est déconseillé d'utiliser le mode INPUT_PUULUP. Si vous devez vous servir du pin 13 comme pin de lecture, préférez un montage avec une résistance externe en pull-up ou pull-do<n. L'explication se trouve dans le fait que le pin 13 est aussi lié à une LED et une résistance. Il ne fournira donc pas du +5V, mais du +1.7V à cause de la LED et de la résistance en série qui baissent la tension. De ce fait la lecture sera toujoursà LOW. **!!!**<br>

##### Programme jour/nuit
- le montage contient un poussoir connecté au pin 2 avec une résistance montée en pull-down.
- Une LED (LED1) connecté au pin 4 (pensez à la résistance).
- Une LED (LED2) connectée au pin 6 
- Lorsque le bouton est levé, la LED1 est allumé, la LED2 est éteinte
- Lorsque le bouton est appuyé, la LED1 est éteinte et la LED2 allumée.

<img src=https://github.com/sirbrowser/astroworld/blob/master/images/jour-nuit.PNG><br>
```C
int pinBouton;
int pled1, pled2;

void setup() {
  pinBouton=2;
  pled1=4;
  pled2=6;

  pinMode(pinBouton,INPUT);
  pinMode(pled1,OUTPUT);
  pinMode(pled2,OUTPUT);

}

void loop() {
  boolean etatBouton = digitalRead(pinBouton);

  if(etatBouton==HIGH){
    digitalWrite(pled1,LOW);
    digitalWrite(pled2,HIGH);
  } else {
    digitalWrite(pled1,HIGH);
    digitalWrite(pled2,LOW);
  }
  delay(100);

}
```

##### Programme interrupteur
- Le bouton poussoir est connecté au pin 2 en mode INPUT_PULLUP ;
- Une LED est connectée au pin 4 ;
- Quand on appuie une fois sur le bouton, la LED s'allume (et reste allumée) ;
- Lorsqu'on appuie à nouveau, la LED s'éteint (et reste éteinte).

<img src=https://github.com/sirbrowser/astroworld/blob/master/images/interrupteur.PNG><br>
```C
int pinBouton;
int pled;
boolean etatBouton;

void setup() {
  pinBouton=2;
  pled=4;

  pinMode(pinBouton,INPUT_PULLUP);
  pinMode(pled,OUTPUT);
  etatBouton=0;
}

void loop() {
  if (etatBouton){
    digitalWrite(pled,HIGH);
  } else {
    digitalWrite(pled,LOW);
  }

  boolean etatPinBouton = digitalRead(pinBouton);
  if(!etatPinBouton){
    if (etatBouton){
      etatBouton=0;
    } else {
      etatBouton=1;
    }
  }
  delay(200);

}
```
