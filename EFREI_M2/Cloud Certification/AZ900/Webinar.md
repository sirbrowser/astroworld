# Webinar Azure AZ-900

## Index

- [Concepts clés du cloud](#concepts-clés-du-cloud)
- [Les principaux services Azure](#les-principaux-services-azure)
- [Sécurité, confidentialité, conformité et integrité](#sécurité-confidentialité-conformité-et-integrité)



CSP = Cloud Service Provider (Microsoft (azure), Google(gcp) et Amazon(aws))  

#### Concepts clés du cloud

- haute disponibilité
- évolutivité
- portée mondiale
- agilité
- récupération d'urgence
- tolérance au panne
- élasticité
- latence client
- prévision des coûts (via la calculatrice azure)
- sécurité


Economie d'échelle : les fournisseurs de cloud peuvent réduire les coûts et gagner en efficacité en opérant à grande échelle.  

Plusieurs racks de serveurs = cluster  

CapEx = dépenses en capital - cloud privé = capex  
coût initial élevé, la valeur de l'investissement diminuant au fil du temps.  

OpEx = dépenses de fonctionnement - Cloud public = opex    
achat de services ou produits selon les besoins, aucun cout initial, paiement à l'utilisation.  

scaling horizontal = dupliquer des vms  

IaaS --> creer des vm dans azure mais on gere ce qu'on fait dessus  
PaaS --> on gere pas l'OS mais les données des applications  
SaaS --> Excel, Skype, Teams = on peut rien faire dessus cela sert juste aux utilisateurs finaux  


#### Les principaux services Azure

SLA :  
- machine virtuelle simple = 99,9%
- groupes à haute disponibilité = 99,95% (ex: deux vm sur un mm datacenter)
- zones de disponibilité = 99,99% (ex: plusieurs vm réparties sur les différents datacenter d'une meme région)
  
Groupes de disponibilité :  
- Domaines de mise à jour (Update Domains) : les maj de maintenance, de niveaux de performance ou de sécurité planifiés sont séquencées via des domaines de maj.
- Domaines d'erreur (Fault Domain) : 

Groupe de ressource = contient des ressources azure, il est dans une région et peut contenir des ressources de différentes régions, une ressource ne peut pas etre dans plusieurs groupes de ressources.  
Fait obligatoirement parti d'un abonnement.  

Node == VM qui heberge des POD (conteneur docker)  
Kubernetes == Cluster de nodes qui hébergent des pods  

Azure Network Services :  
- le réseau virtuel Azure
- Azure Load Balancer (couche 3 et 4 OSI)
- passerelle VPN (3 composants : dans un Vnet il faut un gateway subnet / Virtual Network Gateway (vpn coté azure / ip publique) / Local Network Gateway (vpn coté client on prem / ip publique)) --> liés par une clé de chiffrement
- Azure Application Gateway --> fournit la gestion du trafic vers les applis web (couche 4 OSI)
- réseau de distribution de contenu


Services de base données Azure :  
- Azure cosmos DB --> service de bdd mondialement distribué
- bdd Azure SQL --> bdd relationnelle en tant que service (DaaS = 
- migration de bdd Azure --> service entièrement managbé, conçu pour permettre des migrations transparentes de plusieurs sources de bdd (migrer des bdd on prem dans azure bit par bit).

Serverless :  
- Azure functions : code exécutant votre service et non la plateforme ou l'infra sous jacente. Crée une infra en fonction d'un événement.
- Azure Logic Apps : automatiser et orchestrer les tâches, les process métier, et les workflows lorsque vous devez integrer des app, des données, des systèmes et des services.
- Azure Event Grid

DevOps :  
- Azure devops : fournit des outils de collab de dev, notamment des pipelines, des referentiels git, des tableaux kanban et des tests de charge étezndus automatisés.
- azure devtest labs :

Azure App Service :  
Créez rapidement et facilement des app web et mobiles pour nptq plateforme

#### Sécurité, confidentialité, conformité et integrité












