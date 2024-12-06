# <center> SAÉ 3.02 : Développer des applications communicantes ! BUT R&T 2 IUT LANNION </center>

# <center> Bastien Benis Delahaye et Gurvan Mury </center>

# <center> Cahier des charges Robot n°13 </center>

## Contexte

Dans le cadre de notre Saé 3.02, nous avons hériter du robot n°13 qui possède

+ 3 capteurs optique
+ 2 roues
+ 2 moteurs
+ 1 carte raspberry pi V0

### Matériel et capteurs à utiliser

+ Capteurs optiques : Ces capteurs seront probablement utilisés pour détecter les lignes ou les obstacles sur le sol. En général, pour un suivi de ligne, les capteurs optiques sont placés au niveau du sol pour détecter les contrastes (par exemple, une ligne noire sur un fond blanc).
+ Raspberry Pi : Il servira de contrôleur central et d'interface pour les capteurs et les moteurs.

## Objectif

Nous avons décidé de programmer notre robot pour qu’il suivent un parcours avec une partie en autonomie et une partie en guidé par l’être humain via un IHM en python.
Sur la partie en autonomie, le robot doit faire un parcours avec des angles qui peuvent changer et le robot doit s’adapter au circuit.
Sur la partie guidée, on va faire une IHM avec des commandes pour pouvoir le guider, on pourra choisir l’option pour le mettre en mode autonome et reprendre la main. On pourra voir la distance des obstacles sur cette interface sur les différents capteurs.

### Fonctionnement autonome

+ Suivi de ligne : En utilisant les 3 capteurs optiques, vous pouvez faire en sorte que le robot suive une ligne. Par exemple, si les 3 capteurs détectent la ligne, le robot avance droit. Si un des capteurs se trouve à l’extérieur de la ligne (par exemple, le capteur à gauche ou à droite), le robot devra ajuster sa direction en tournant vers le côté où la ligne est détectée.

+ Gestion des angles : Les changements de direction peuvent être gérés en utilisant les informations des capteurs optiques pour ajuster les virages et la vitesse. Si le robot est sur une trajectoire avec des angles serrés, il devra peut-être réduire sa vitesse ou augmenter sa fréquence de correction de trajectoire.

## Contrainte

+ Mise en place d'une application client / serveur basée sur l’un des deux protocoles : TCP ou UDP

+ Notre applications cliente et serveur devront être réalisées en python, en programmation objet (... mise en œuvre de classes).
Si votre application prévoit plusieurs clients, l’application cliente devra être unique.
+ Notre application cliente devra avoir nécessairement une interface graphique qui comportera un espace de configuration des paramètres réseaux.
+ On devra aussi prévoir l’utilisation d’une base de données et/ou de fichiers de sauvegarde et de récupération de données.
+ Les échanges réseaux devront être faits sous la forme de sérialisation dé-sérialisation au format json.
