```bash
.
├── README.md                   <-- This instructions file
├── master.yaml                 <-- SAM template
├── deploy.sh                   <-- Deployment bash file    
├── setup.sh                    <-- Setting up bash file
|
├── ScheduledEcs
|  ├── raw                      <-- Source code for lambda functions
|  └── requirements.txt         <-- Python dependencies
|
├── infrastructure              <-- YAML file for cloudformation
|  ├── database.yaml            <-- Database & ElasticSearch infrastructure
|  ├── ecs-cluster.yaml         <-- ECS cluster & Network infrastructure
|  └── task.yaml                <-- ECS TaskDefinition infrastructure     
|
└── services                    <-- Spider services
   └── hkdoctors                <-- HKdoctors site\'s spider program with dockerfile
   
```
## Setup process

### Getting Ready

```bash
cd Spider/
chmod +x setup.sh
./setup.sh
```

### Deployment

```bash
chmod +x deploy.sh
./deploy.sh
```


