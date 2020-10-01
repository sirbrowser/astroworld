# Architecture Azure et garanties de service 

## Centres de données et régions dans Azure

Microsoft Azure se compose de centres de données situés dans le monde entier. Les centres de données spécifiques ne sont pas directement exposés aux utilisateurs finaux, mais sont organisés en régions par Azure.<br>

Une région est une zone géographique sur la planète contenant au moins un centre de données, voire plusieurs centres de données proches les uns des autres et reliés par un réseau à faible latence.<br>
Quand vous déployez une ressource dans Azure, vous devez souvent choisir la région où vous souhaitez qu’elle soit déployée.<br>

Vous utilisez des régions pour identifier l’emplacement de vos ressources, mais vous devez également connaître deux autres termes : `zones géographiques` et `zones de disponibilité`.

## Zones géographiques dans Azure

Azure divise le monde en zones géographiques qui sont définies par des limites géopolitiques ou des frontières de pays. Une zone géographique Azure est un marché distinct contenant généralement deux ou plusieurs régions qui conservent des limites de conformité et de résidence des données.<br>
Chaque région appartient à une zone géographique unique et des règles spécifiques de disponibilité des services, de conformité ainsi que de résidence/souveraineté des données lui sont appliquées.

## Zones de disponibilité dans Azure

Azure rend une application hautement disponible via des zones de disponibilité.<br>
Les zones de disponibilité sont des centres de données physiquement séparés au sein d’une région Azure.<br>
Chaque zone de disponibilité est composée d’un ou de plusieurs centres de données équipés d’une alimentation, d’un refroidissement et d’un réseau indépendants.<br>
Les zones de disponibilité sont connectées via des réseaux en fibre optique privés très rapides.<br>
Vous pouvez utiliser des zones de disponibilité pour exécuter des applications stratégiques et générer la haute disponibilité dans votre architecture d’applications.<br>
Cela engendre un coût lié à la duplication des services et aux transferts de données entre les zones.<br>

## Paires de régions dans Azure

Les zones de disponibilité sont créées avec un ou plusieurs centres de données, et sont au minimum au nombre de trois au sein d’une seule région. Toutefois, il peut arriver qu’un sinistre suffisamment grave entraîne une panne assez importante pour affecter deux centres de données. C’est pourquoi Azure crée également des paires de régions.<br>
Dans la mesure où les deux régions sont directement connectées et suffisamment éloignées pour être isolées de sinistres régionaux, vous pouvez les utiliser pour assurer la redondance des données et la fiabilité des services.<br>

## Contrat de niveau de service pour Azure

Contrat de niveau de service = **SLA**.<br>
Il décrive l'engagement de Microsoft avec les clients selon des normes de performances spécifiques. Il indique aussi les conséquences si il ne respecte pas le SLA.<br>
Il existe trois principales caractéristiques des contrats SLA pour les produits et services Azure :
- Cibles de performances
- Garanties de connectivité et durée de fonctionnement
- Crédits du service

### Cibles de performances

Un contrat SLA définit des cibles de performances pour un produit ou service Azure. Par exemple, pour certains services Azure, les cibles de performances sont exprimées comme garanties de durée de fonctionnement ou taux de connectivité.

### Garanties de connectivité et durée de fonctionnement

Un contrat SLA classique spécifie les engagements en matière de cibles de performances allant de 99,9 % (« trois neuf ») à 99,999 % (« cinq neuf ») pour chaque produit ou service Azure correspondant.

### Crédits du service

Les contrats SLA décrivent également la réponse de Microsoft si un service ou produit Azure ne respecte pas une spécification applicable du contrat. Par exemple, une remise peut être appliquée à la facture Azure des clients comme compensation pour un produit ou service Azure sous-performant

## Résilience

La résilience est la capacité d’un système à récupérer après des défaillances et à continuer de fonctionner. Il ne s’agit pas d’éviter les défaillances, mais d’y répondre en évitant les temps d’arrêt ou la perte de données. La haute disponibilité et la reprise d’activité sont deux aspects importants de la résilience.<br>