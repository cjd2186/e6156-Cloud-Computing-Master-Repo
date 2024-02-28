# e6156-Cloud-Computing-Master-Repo
This is a repository that comprises of all micro-services and cloud technologies used for Columbia e6156 Cloud Computing Project.

Project Overview:
Our cloud-based application NFL FanZone is built and designed for NFL fans' casual interaction and NFL-related information lookup. It offers three features that will enhance fans’ NFL experience:

1. NFL searching: fans can find information (eg. player stats, player basic information.) in HTML format or JSON format regarding their favorite players. The microservice also has operations to add/modify/delete players. 

2. Team management: management personnel with different clearance levels can modify team/player information to keep fans updated. 
Users can access general information about coaches, as well as the team that they coach. Users can use the management person’s information with their id.

3. Fan post-game reviews forum: fans can share their insights and comments on the games they watched with other fans in our interactive forum. 

Folders in Repo:

* Microservice 1 on EC2: 'EC2_NFLsearching-master' (search NFL player database)
* Microservice 2 on GCP App Engine: 'Team-Management-main' (search NFL coaching/adminstration database)
-Microservice 3 with Docker on EC2: 'EC2_Docker_microservice_post-master' (interact with NFL fan forum)
-S3 Frontend: 'S3_NFLApplicationReact-main' (web interface for project)
-Aggregator Service on EC2: 'Composite_NFL_CompositiveSvc-master' (uses public api to retrieve player news updates)
-Pub/Sub with AWS Lambda function: 'PubSub_Pub-Sub-main' (sends notification on discord server when player added to database)
-Infrastructure as a service: 'IaaS_terraform-main' (automates deployment of microservices)
