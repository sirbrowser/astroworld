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

