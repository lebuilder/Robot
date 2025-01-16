# Compte Rendu POO2 BENIS Bastien MURY Gurvan

## Introduction

Ce document présente un compte rendu des fonctionnalités développées pour le robot n°13 dans le cadre de la SAÉ 3.02. Nous avons implémenté une application client-serveur en Python permettant de contrôler le robot à distance et de le faire fonctionner en mode autonome.

## Fonctionnalités Implémentées

### Serveur

Le serveur est responsable de la gestion des commandes envoyées par le client et du contrôle des différents composants du robot (moteurs, capteurs, LED RGB, buzzer). Les principales fonctionnalités du serveur incluent :

- **Déplacement du robot** : Le serveur peut recevoir des commandes pour avancer, reculer, tourner à gauche et tourner à droite.
- **Mode autonome** : Le serveur peut activer un mode autonome où le robot utilise ses capteurs pour naviguer de manière autonome.
- **Contrôle des capteurs** : Le serveur peut envoyer les valeurs des capteurs au client.
- **Contrôle de la batterie** : Le serveur peut envoyer le niveau de la batterie au client.
- **Mode police** : Le serveur peut activer un mode où la LED RGB change de couleur et le buzzer joue une mélodie.

### Client

Le client est une interface graphique développée en Python utilisant Tkinter. Il permet à l'utilisateur de se connecter au serveur et de contrôler le robot. Les principales fonctionnalités du client incluent :

- **Connexion au serveur** : L'utilisateur peut entrer l'adresse IP et le port du serveur pour se connecter.
- **Contrôle manuel** : L'utilisateur peut envoyer des commandes pour avancer, reculer, tourner à gauche et tourner à droite.
- **Mode autonome** : L'utilisateur peut activer ou désactiver le mode autonome.
- **Affichage des capteurs** : L'utilisateur peut demander les valeurs des capteurs et les afficher en continu.
- **Affichage de la batterie** : L'utilisateur peut demander le niveau de la batterie et l'afficher en continu.
- **Mode police** : L'utilisateur peut activer ou désactiver le mode police.
- **Logs** : Les actions et messages sont enregistrés dans un fichier de log au format JSON.

## Conformité avec le Cahier des Charges

### Objectifs Réalisés

- **Suivi de ligne et gestion des angles** : Le mode autonome utilise les capteurs pour détecter les obstacles et ajuster la direction du robot.
- **Application client-serveur** : Nous avons développé une application client-serveur en Python utilisant le protocole TCP.
- **Interface graphique** : Le client dispose d'une interface graphique permettant de configurer les paramètres réseau et de contrôler le robot.
- **Sauvegarde des données** : Les logs des actions et messages sont sauvegardés dans un fichier JSON.

### Objectifs Non Réalisés

- **Base de données** : Nous avons implémenter la sauvegarde de donné grace à un json que nous pouvons récupéré sur demmande avec le boutton Logs

## Diagramme de Gantt

Le diagramme de Gantt ci-dessous montre les différentes étapes du projet en fonction de l'avancement sur le Projet.

| Tâche                          | Début       | Fin         | Durée (jours) |
|--------------------------------|-------------|-------------|---------------|
| Initialisation du projet       | 12/11/2024  | 16/11/2024  | 5             |
| Développement du serveur       | 12/11/2024  | 12/01/2025  | 62            |
| Développement du client        | 12/11/2024  | 12/01/2025  | 62            |
| Intégration des capteurs       | 13/12/2024  | 12/01/2025  | 31            |
| Implémentation du mode autonome| 13/12/2024  | 12/01/2025  | 31            |
| Tests et débogage              | 12/11/2024  | 16/01/2025  | 66            |
| Documentation                  | 16/01/2025  | 16/01/2025  | 1             |

## Conclusion

Nous avons réussi à implémenter la majorité des fonctionnalités décrites dans le cahier des charges. Le robot peut être contrôlé manuellement ou fonctionner en mode autonome, et les données des capteurs et de la batterie peuvent être affichées en temps réel. Les logs des actions sont sauvegardés dans un fichier JSON, permettant de suivre l'historique des interactions avec le robot.
