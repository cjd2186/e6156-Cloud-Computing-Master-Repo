# e6156-Cloud-Computing-Master-Repo
This is a repository that comprises of all micro-services and cloud technologies used for Columbia e6156 Cloud Computing Project. Code from existing repositories used for this project were collected and organized into this master repository.

Project Overview:
Our cloud-based application NFL FanZone is built and designed for NFL fans' casual interaction and NFL-related information lookup. It offers three features that will enhance fans’ NFL experience:

1. NFL searching: fans can find information (eg. player stats, player basic information.) in HTML format or JSON format regarding their favorite players. The microservice also has operations to add/modify/delete players. 

2. Team management: management personnel with different clearance levels can modify team/player information to keep fans updated. 
Users can access general information about coaches, as well as the team that they coach. Users can use the management person’s information with their id.

3. Fan post-game reviews forum: fans can share their insights and comments on the games they watched with other fans in our interactive forum. 

Folders in Repo:

* Microservice 1 on EC2: 'EC2_NFLsearching-master'
    * (search NFL player database)
    * https://github.com/ICAcap/NFLsearching.git
* Microservice 2 on GCP App Engine: 'Team-Management-main'
    * (search NFL coaching/adminstration database)
    * https://github.com/darieloespinal/Team-Management 
* Microservice 3 with Docker on EC2: 'EC2_Docker_microservice_post-master'
    * (interact with NFL fan forum)
    * https://github.com/harry881218/microservice_post/tree/master
* S3 Frontend: 'S3_NFLApplicationReact-main'
    * (web interface for project)
    * node_modules folder was omitted due to large size, for the full 'node_modules' folder visit following repo:
    * https://github.com/linhtbui/NFLApplicationReact
* Aggregator Service on EC2: 'Composite_NFL_CompositiveSvc-master'
    * (uses public api to retrieve player news updates)
    * https://github.com/Beza4598/NFLCompositeSvc
* Pub/Sub with AWS Lambda function: 'PubSub_Pub-Sub-main'
    * (sends notification on discord server when player added to database)
    * https://github.com/cjd2186/Pub-Sub
* Infrastructure as a service: 'IaaS_terraform-main'
    * (automates deployment of microservices)
    * https://github.com/harry881218/IaaS_terraform 
