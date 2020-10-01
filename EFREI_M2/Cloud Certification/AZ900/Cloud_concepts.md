# Concept du cloud

- [Concept du cloud](#concept-du-cloud)
  * [Ques que le cloud computing](#ques-que-le-cloud-computing)
    + [Puissance de calcul](#puissance-de-calcul)
      - [Les conteneurs](#les-conteneurs)
      - [Informatique Serverless](#informatique-serverless)
    + [Stockage](#stockage)
  * [Avantages du cloud computing](#avantages-du-cloud-computing)
    + [Rentabilité](#rentabilit-)
    + [Scalabilité](#scalabilit-)
    + [Elasticité](#elasticit-)
    + [Toujours à jour](#toujours---jour)
    + [Fiabilité](#fiabilit-)
    + [Mondialisé](#mondialis-)
    + [Sécurisé](#s-curis-)
  * [Conditions et exigences de conformité](#conditions-et-exigences-de-conformit-)
  * [Économie d'echelle](#-conomie-d-echelle)
  * [Dépenses en capital et dépenses de fonctionnement](#d-penses-en-capital-et-d-penses-de-fonctionnement)
    + [Coûts informatiques à titre de dépenses en capital](#co-ts-informatiques---titre-de-d-penses-en-capital)
    + [Coûts de cloud computing à titre de dépenses de fonctionnement](#co-ts-de-cloud-computing---titre-de-d-penses-de-fonctionnement)
  * [Modèles de déploiement cloud](#mod-les-de-d-ploiement-cloud)
    + [Cloud public](#cloud-public)
      - [Avantages](#avantages)
      - [Inconvénients](#inconv-nients)
    + [Cloud privé](#cloud-priv-)
      - [Avantages](#avantages-1)
      - [Inconvénients](#inconv-nients-1)
    + [Cloud hybride](#cloud-hybride)
      - [Avantages](#avantages-2)
      - [Inconvénients](#inconv-nients-2)
  * [Types de services cloud](#types-de-services-cloud)
    + [IaaS](#iaas)
    + [PaaS](#paas)
    + [SaaS](#saas)

## Ques que le cloud computing

Le cloud computing consiste à louer des ressources, comme de l’espace de stockage ou des cycles CPU, sur les ordinateurs d’une autre société. Vous ne payez que ce que vous utilisez.<br>
Le fournisseur de cloud est responsable du matériel physique nécessaire à l’exécution de votre travail, et de maintenir ce matériel à jour.<br>
Les services proposés :
- Puissance de calcul, comme des serveurs Linux ou des applications web utilisés pour les tâches de calcul et de traitement
- Stockage, comme des fichiers et des bases de données
- Réseau, comme des connexions sécurisées entre le fournisseur cloud et votre entreprise
- Analytique, comme la visualisation de la télémétrie et des données de performances

### Puissance de calcul

Le fournisseur cloud exécute votre machine virtuelle sur un serveur physique dans un de ses centres de données, souvent en partageant ce serveur avec d’autres machines virtuelles (isolées et sécurisées). Avec le cloud, vous pouvez avoir une machine virtuelle prête à l’emploi en quelques minutes à un coût moindre que celui d’un ordinateur physique.<br>
Les **machines virtuelles** ne sont pas le seul choix possible, car il existe deux autres options répandues : **les conteneurs** et **l’informatique serverless**.<br>

#### Les conteneurs

Les conteneurs fournissent un environnement d’exécution cohérent et isolé aux applications.<br>
Le conteneur démarre en quelques secondes car il n’y a pas de système d’exploitation à démarrer et à initialiser. Vous avez seulement besoin de l’application à lancer.<br>
La portabilité du conteneur facilite considérablement le déploiement d’applications dans plusieurs environnements, localement ou dans le cloud.<br>

#### Informatique Serverless

L’idée fondamentale est que votre application est divisée en fonctions distinctes qui s’exécutent quand elles sont déclenchées par une action.<br>
Le modèle serverless diffère des machines virtuelles et des conteneurs en cela que vous payez seulement pour le temps de traitement utilisé par chaque fonction au fil de son exécution.<br>
Les machines virtuelles et les conteneurs sont facturés pour la durée de leur exécution, même si les applications qui s’y trouvent sont inactives.<br>
Cette architecture ne fonctionne pas pour chaque application.<br>

**Insérer image**

### Stockage

L’avantage d’utiliser un stockage de données cloud est que vous pouvez le mettre à l’échelle en fonction de vos besoins. Si vous trouvez que vous avez besoin de davantage d’espace pour stocker vos clips vidéo, vous pouvez payer un peu plus et augmenter votre espace disponible. Dans certains cas, le stockage peut même être étendu et réduit automatiquement : vous payez ainsi exactement ce dont vous avez besoin à un moment donné dans le temps.<br>

## Avantages du cloud computing

### Rentabilité

Le cloud computing fournit un modèle tarifaire de type paiement à l’utilisation ou paiement basé sur la consommation.<br>
Cela permet une meilleure prédiction des coûts. Les prix des différents services et ressources sont fournis afin de prédire le montant des dépenses dans une période de facturation donnée en fonction de l'utilisation prévue.<br>

### Scalabilité

Vous pouvez augmenter ou diminuer les ressources et les services utilisés en fonction de la demande ou de la charge de travail à tout moment. Le cloud computing prend en charge la mise à l’échelle verticale et la mise à l’échelle horizontale selon les besoins. <br>

### Elasticité

Quand votre charge de travail évolue au gré des hausses et des baisses de demande, un système de cloud computing peut ajouter ou supprimer automatiquement des ressources pour compenser ces variations.<br>
Par exemple, imaginons que votre site web apparaît dans un article de journal et que cela entraîne un pic de trafic du jour au lendemain. Dans la mesure où le cloud est élastique, il alloue automatiquement des ressources informatiques supplémentaires pour gérer l’augmentation du trafic.<br>

### Toujours à jour

En utilisant le cloud, vous n’avez plus à charge la gestion des correctifs logiciels, l’installation du matériel, les mises à niveau et d’autres tâches de gestion informatique.<br>

### Fiabilité

Les fournisseurs de cloud computing offrent des services de sauvegarde, de reprise d’activité après sinistre et de réplication des données pour que vos données soient sécurisées en permanence.<br>

### Mondialisé

Les fournisseurs de cloud ont des centres de données entièrement redondants situés dans différentes régions du monde entier. Ainsi, vous êtes proches de vos clients, qui bénéficient du meilleur temps de réponse possible où qu’ils se trouvent dans le monde.<br>

### Sécurisé

Les fournisseurs de cloud offrent un large éventail de stratégies, de technologies, de contrôles et de compétences techniques pouvant fournir une meilleure sécurité (physique et numérique) que peu d’organisations peuvent atteindre.<br>

## Conditions et exigences de conformité

Quand vous sélectionnez un fournisseur de cloud pour héberger vos solutions, vous devez comprendre comment ce fournisseur peut vous aider à respecter les réglementations et les normes. Voici une liste de certaines offres de conformité disponible : 

- **CJIS (Criminal Justice Information Services)** : Tout État ou toute agence locale des États-Unis qui souhaite accéder à la base de données CJIS du FBI doit respecter la stratégie de sécurité du CJIS.
- **Certification CSA (Cloud Security Alliance) STAR** : Implique une évaluation rigoureuse par un tiers indépendant des dispositifs de sécurité d’un fournisseur de cloud.
- **Règlement général sur la protection des données (RGPD).** : Nouvelles règles sur la collecte et l'analyse des données utilisateurs.
- **Clauses types de l’UE** : Garanties contractuelles sur le transfert de données personnelles en dehors de l’UE.
- **HIPAA (Health Insurance Portability and Accountability Act)** : Loi fédérale américaine qui régit les informations médicales protégées des patients.
- **ISO (International Organization for Standardization) et IEC (International Electrotechnical Commission) 27018** : couvre le traitement des informations personnelles par les fournisseurs de services cloud.
- **MTCS (Multi-Tier Cloud Security) Singapore** : Certification pour la possibilité de proposer différentes solutions cloud (Iaas, Paas, Saas, ...)
- **SOC (Service Organization Controls) 1, 2 et 3** : Contrôles de la sécurité, de la disponibilité, de l’intégrité du traitement et de la confidentialité des données pour chaque service.
- **NIST (National Institute of Standards and Technology) CSF (Cybersecurity Framework)** : Standards, recommandations et bonnes pratiques sur la gestion des risques liés à la cybersécurité.
- **UK Government G-Cloud.** : Certification de cloud computing pour les services utilisés par les entités administratives au Royaume-Uni.

## Économie d'echelle

Les économies d’échelle permettent d’effectuer des opérations plus efficacement ou à un coût unitaire moindre quand elles sont exécutées à une plus grande échelle.<br>
Du point de vue des utilisateurs finaux, ces économies peuvent prendre différentes formes, par exemple la possibilité d’acquérir du matériel à un coût inférieur. Les fournisseurs de cloud peuvent également négocier avec les administrations locales et les services publics pour obtenir des baisses de taxes ainsi que pour faire baisser les prix sur l’approvisionnement électrique, le refroidissement et la connectivité réseau à haut débit entre les sites.<br>

## Dépenses en capital et dépenses de fonctionnement

Dans le passé, les entreprises devaient acquérir des installations et une infrastructure physiques pour démarrer leur activité. Le démarrage ou le développement d’une activité engendrait un coût initial important en matériel et infrastructure. Le cloud computing fournit des services aux clients sans qu’ils aient à consacrer beaucoup d’argent ou de temps à la mise en place des équipements.<br>

### Coûts informatiques à titre de dépenses en capital

Investissements initiaux en infrastructure physique, amortissables fiscalement sur une certaine durée.<br>
- Coûts des serveurs
- Coûts liés au stockage
- Coûts liés au réseau
- Coûts liés à la sauvegarde et à l’archivage
- Coûts liés à la continuité et à la reprise d’activité
- Coûts d’infrastructure du centre de données
- Équipe technique


### Coûts de cloud computing à titre de dépenses de fonctionnement

Les dépenses de fonctionnement représentent les achats quotidiens de services ou produits dans le cadre des activités courantes. Vous payez un service ou un produit quand vous l’utilisez.<br>
- Location de logiciels et de fonctionnalités personnalisées
- Frais variables selon l’utilisation ou la demande, et non basés sur du matériel ou une capacité fixe : RAM allouée, IOPS, ...
- Facturation au niveau de l’utilisateur ou de l’organisation
- Avantages des dépenses en capital
- Avantages des dépenses de fonctionnement

## Modèles de déploiement cloud

### Cloud public

Il s’agit du modèle de déploiement le plus courant. Dans ce cas, vous ne disposez d’aucun matériel local à gérer ou à maintenir à jour : tout s’exécute sur le matériel de votre fournisseur de cloud

#### Avantages

- Haute scalabilité/agilité : vous n’avez pas besoin d’acheter un nouveau serveur à des fins de scalabilité
- Tarif de type paiement à l’utilisation : vous payez uniquement ce que vous utilisez (aucune dépense en capital)
- Vous n’êtes pas responsable de la maintenance ni des mises à jour du matériel
- Connaissances techniques minimales pour la configuration et l’utilisation

#### Inconvénients

- Il peut y avoir des exigences de sécurité spécifiques qu’un cloud public ne permet pas de respecter
- Il peut y avoir des politiques publiques, des normes sectorielles ou des exigences légales que les clouds publics ne peuvent pas respecter
- Vous ne possédez pas le matériel ou les services et ne pouvez donc pas les gérer comme vous le souhaiteriez
- Les exigences métier particulières, telles que le fait de devoir gérer une application héritée, peuvent être difficiles à respecter

### Cloud privé

Dans un cloud privé, vous créez un environnement cloud dans votre propre centre de données. Vous offrez ainsi à vos utilisateurs une simulation de cloud public, mais vous restez entièrement responsable de l’achat et de la maintenance du matériel et des services logiciels que vous fournissez.

#### Avantages

- Vous pouvez garantir que la configuration peut prendre en charge n’importe quel scénario ou application existante
- Vous avez le contrôle (et la responsabilité) de la sécurité
- Les clouds privés peuvent répondre à des critères de sécurité, de conformité ou de réglementation stricts

#### Inconvénients

- Vous avez des dépenses d’investissement initiales, et vous devez acheter le matériel pour le démarrage et la maintenance.
- Le fait de posséder l’équipement limite l’agilité : pour effectuer une mise à l’échelle, vous devez acheter, installer et configurer un nouveau matériel.
- Les clouds privés nécessitent des qualifications et une expertise en informatique qui sont difficiles à acquérir.

### Cloud hybride

Un cloud hybride combine des clouds publics et privés, ce qui vous permet d’exécuter vos applications à l’emplacement le plus approprié.

#### Avantages

- Vous pouvez laisser tous les systèmes en cours d’exécution et accessibles qui utilisent du matériel ou un système d’exploitation obsolètes.
- Vous bénéficiez d’une grande flexibilité quant au choix des éléments que vous exécutez localement et de ceux que vous exécutez dans le cloud.
- Vous pouvez tirer parti des économies d’échelle offertes par les fournisseurs de cloud public pour acquérir des services et des ressources à moindre coût, que vous pouvez compléter avec votre propre équipement si cela s’avère plus économique pour vous.
- Vous pouvez utiliser votre propre équipement pour faire face aux scénarios de sécurité, de conformité ou hérités dans lesquels vous devez contrôler complètement l’environnement

#### Inconvénients

- Cette approche peut être plus coûteuse que la sélection d’un modèle de déploiement, car elle implique quelques dépenses en capital initiales.
- Elle peut se révéler plus difficile à configurer et à gérer.

## Types de services cloud

### IaaS

Elle vise à vous donner le plus grand contrôle sur le matériel fourni qui exécute votre application (serveurs et machines virtuelles de l’infrastructure informatique, stockage et systèmes d’exploitation). Avec IaaS, au lieu d’acheter du matériel, vous le louez. Il s’agit d’une infrastructure de calcul instantané, provisionnée et gérée via Internet.<br>
Cette solution peut être utilisé pour des scénarios de migration des charges de travail, pour le test et le développement, pour le stockage,lasauvegarde et la récupération de données.<br>

Aucun coût initial, les utilisateurs paient pour ce qu'ils utilisent.<br>
L'utilisateur est responsable de l'achat, installation, configuration et gestion des OS, middlewares et applications.<br>
Le fournisseur cloud s'assure de la disponibilité des VMs, du stockage et du réseau.<br>

### PaaS

PaaS fournit un environnement de génération, de test et de déploiement d’applications logicielles. L’objectif du PaaS est de vous aider à créer rapidement une application sans avoir à gérer l’infrastructure sous-jacente.<br>
PaaS est un environnement de développement et de déploiement complet dans le cloud, dont les ressources permettent aux organisations de fournir tout type d’application<br>
Par exemple, au moment du déploiement d’une application web avec PaaS, vous n’avez pas besoin d’installer un système d’exploitation, un serveur web ou même des mises à jour système.<br>

Aucun coût initial, les utilisateurs paient pour ce qu'ils utilisent.<br>
L'utilisateur est responsable de du développement de ses applications.<br>
Le fournisseur cloud s'assure de tout sauf de l'application que l'utilisateur veut exécuter.<br>

### SaaS

SaaS est un logiciel qui est hébergé et géré de manière centralisée pour le client final. Il est généralement basé sur une architecture où une seule version de l’application est utilisée pour tous les clients.<br>
Microsoft 365 est un exemple de logiciel SaaS.

Aucun coût initial, les utilisateurs paient pour ce qu'ils utilisent.<br>
Ils utilisent simplement les logiciels mais ne sont pas responsable de la gestion et maintenance.<br>
Le fournisseur cloud s'assure de tout.<br>
