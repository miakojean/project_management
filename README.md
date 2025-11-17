# Application web interne pour la gestion des dossiers du cabinet.

Il est ici question de commencer par mettre en place un MVP, qui va être basiquement prêt en maximum deux semaines. Par ailleurs, l'idée est de rendre l'application maintenable et donc scalable. Le développement et donc l'architecture du MVP devrait repondre à ces besoins et à cette philosophie.

## Fonctionnalités de base
- Ajouter un dossier (avec tous ses détails)
- Voir l'étape de progression du dossier
- Pouvoir rétrouver un dossier avec une barre de recherche

## Technologie utilisée

La stack utilisée pour cette application est vue.js pour le front-end et Django pour le backend. La base de données en développement pendant la première semaine sera SQLITE ensuite on va migrer vers POSTGRES pour plus de rigueur.

- Python (Django)
- Js (vue)
- Css (Tailwind & Daysiui)
- Postgresql
### Devops
- Git (github pour l'hébergement du versionnage). On aura deux branches dans un premier temps la branch principale et une branche secondaire pour le développement.


## Interface simple et intuitive

Comme d'habitude l'idée doit être mis sur l'experience utilisateur de l'app. Le style sera assuré avec tailwind.css et la librairie daysiui. On doit réduire voire éviter les courbes d'apprentissage.

Le dashboard est une interface à laquelle tout le monde peut se connecter. Mais aussi à laquelle tout le monde ne peut effectuer de requêtes.


On va commencer à devs puis prendre les informations au fure et à mesure que les idées se concrétisent.