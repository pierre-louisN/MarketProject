# MarketProject

Projet PPC 3TC 

pour lancer la simulation : 
deziper l'archive
chmod u+x simulation.py
sudo ./simulation.py

pour y mettre fin :
attendre le 365 ème jour ou Ctrl+C 

Quelques remarques:

ATTENTION, sans le 'sudo', os.kill() ne se sera pas lancé, et les evenements ne seront jamais modifié
Il arrive parfois que le terminal se gèle, il faut alors appuyez sur ENTRÉE

A propos du code :

Un evenement lié à la météo dure au moins un jour 
Un evemenement politique (guerre) ou économique (crise) dure une durée aléatoire

Il est possible de changer le nombre de maisons dans simulation.py via la varialble 'nb_maisons'
