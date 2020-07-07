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

Le code est toujours de la forme suivante :<br>
```arduino
void setup() {
  // put your setup code here, to run once:

}

void loop() {
  // put your main code here, to run repeatedly:

}
```
