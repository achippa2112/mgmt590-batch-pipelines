# Overview of the batch-pipelines
## About this Repository
The goal of this assignment is to build batch pipelines which reads multiple csv files containing questions and contexts and then saves answers to those questions in the database. These pipelines are mainly important/useful when processing huge number of files which would normally take very high processing time. 

### Pipeline 1 : 
A batch pipeline - pipeline1 has been built to check for new csv files on GCS bucket and to produce answers for each question. This batch-pipeline enriches the csv file with new column containing the answers. The final enriched file is then push into the output repository on pachyderm GCS.
### Pipeline 2: 
Another batch pipeline - pipeline2 will read the final enriched csv files from the output repository of the pipeline1 and saves those answers in the database. 

Below is a high-level diagram to show how the pipelines fit in the overall framework:</br>

<img width="889" alt="3" src="https://user-images.githubusercontent.com/84465734/121768365-e02cd980-cb2b-11eb-9a6e-7776ff856d55.PNG">

## Deploying these pipelines
### Pre-requisites
- Must have an account on docker hub
- Must have gcs bucket created on google storage
- Must have access to pachyderm

### Below are the steps to deploy your pipeline code to docker hub:
- Build and deploy the images to DockerHub
- Create pachyderm workspace
   <img width="309" alt="1" src="https://user-images.githubusercontent.com/84465734/121768778-fb98e400-cb2d-11eb-91c4-46e1946636f2.PNG">
 Refer : https://docs.pachyderm.com/latest/hub/hub_getting_started/
####  Login to Pachyderm Cluster 
## TODO 
####  Install pachctl on your machine
The "pachctl" or pach control is a command line tool that you can use to interact with a Pachyderm cluster in your terminal. For a Debian based Linux 64-bit or Windows 10    or later running on WSL run the following code:
   ```
   curl -o /tmp/pachctl.deb -L https://github.com/pachyderm/pachyderm/releases/download/v1.13.2/pachctl_1.13.2_amd64.deb && sudo dpkg -i /tmp/pachctl.deb
   ```
For macOS use the below command:
   ```
   brew tap pachyderm/tap && brew install pachyderm/tap/pachctl@1.13
   ```
For all other Linux systems use below command:
   ```
   curl -o /tmp/pachctl.tar.gz -L https://github.com/pachyderm/pachyderm/releases/download/v1.13.2/pachctl_1.13.2_linux_amd64.tar.gz && tar -xvf /tmp/pachctl.tar.gz -C /tmp && sudo cp /tmp/pachctl_1.13.2_linux_amd64/pachctl /usr/local/bin
   ```
Refer : https://docs.pachyderm.com/latest/getting_started/local_installation/#install-pachctl
####  Connect to your Pachyderm workspace
Click "Connect" on your Pachyderm workspace and follow the below listed steps to connect to your workspace via the machine:
   
   <img width="306" alt="2" src="https://user-images.githubusercontent.com/84465734/121769024-50892a00-cb2f-11eb-8546-97b039618abb.PNG">
    
####  Verify the installation
   ```
    pachctl version
   ```
####  Copy below files to your local system (where pachtcl is installed)
  - create_secret.sh 
  - create_secret_db.sh
  - secret_template.json
  - secret_template_db.jso
  - credentials.json <your service account for google cloud storage>
  - server-ca.pem <your server certificate for Postgres database>
  - client-cert.pem <your client certificate for Postgres database>
  - client-key.pem <your client key for Postgres database>
Export the required environment variables to your OS environment . 
For Example : If you are using LINUX , you can you below commands:
```
export GOOGLE_APPLICATION_CREDENTIALS=<YOUR-CLOUD-SERVICE_ACCOUNT_KEY>
export PG_HOST=<POSTGRES-DATABASE-HOST>
export PG_PASSWORD=<POSTGRES-DATABASE-PASSWOD>
export PG_DBNAME=<POSTGRES-DATABASE-DBNAME>
export PG_USER=<POSTGRES-DATABASE-USER>
export PG_SSLROOTCERT=<POSTGRES-DATABASE-HOST>
export PG_SSLCLIENT_CERT=<POSTGRES-DATABASE-HOST>
export PG_SSL_CLIENT_KEY=<POSTGRES-DATABASE-HOST>
```
####  Now execute the scripts to create secrets for pachctl
   ```
      ./create_secret.sh
      ./create_secret_db.sh
   ```
####  Verify whether secrets are created or not 
  ```
    pachctl list secret
```
#### Create the pipelines
On you local system , create two json files 
 - pipeline1.json <github Link >
 - pipeline2.json <github link>
Then run the below commands to create the pachctl pipelines
```
  pachctl create pipeline -f pipeline1.json
  pachctl create pipeline -f pipeline2.json
```
#### You may use below command to check the status of pipelines created and jobs triggered
```
 -- Create the pipeline 
pachctl create pipeline -f pipeline1.json
pachctl create pipeline -f pipeline2.json
-- Delete Pipeline
pachctl delete pipeline push-answers
pachctl delete pipeline pull_files
-- Update pipelibe 
pachctl update pipeline -f pipeline1.json
pachctl update pipeline -f pipeline2.json
-- to list pipelines 
pachctl list pipeline
-- to list jobs 
pachctl list job 
-- stop pipeline 
pachctl list pipeline
-- to watch 
watch pachctl list job 
-- to view logs 
pachctl logs -j <job_id>
-- List repo 
pachctl list repo
```

# Batch Processing 
## About this repository
The goal of this repo is to connect DockerHub through Github actions in order to create our pipelines in Dockerhub. We will be creating 2 separate pipelines. These pipelines will further interact with our terminal (Cloud Shell used here) with the use of Pachyderm.
Each of these pipelines will have a python file, Dockerfile and json file. Through Github actions, these pipelines will build images and finally push these images to Docker Hub. Once both these pipelines are deployed with the use of Pachyderm on Cloud Shell from GCS, with the use of PostgreSQL(2nd pipeline), they will eventually start running on Google Cloud Run.
## Batch Pipelines
The REST API for which these batch pipelines are constructed is an API made to provide the user the ability to ask questions based on provided contexts, by uploading them as .csv files, and the API generates the answer. The goal of these batch pipelines is to act as data pipelines between the REST API and the Cloud SQL database, where the answers generated by the pipeline is stored. The pipelines automate the data storage process by acting as a non-real time data updation link between the model and the databas
Below is a high-level diagram to show how the pipelines fit in the overall framework:
<img width="889" alt="3" src="" title="https://user-images.githubusercontent.com/84465734/121768365-e02cd980-cb2b-11eb-9a6e-7776ff856d55.png%22>" target="_blank" rel="noreferrer noopener">https://user-images.githubusercontent.com/84465734/121768365-e02cd980-cb2b-11eb-9a6e-7776ff856d55.PNG">
### Pipeline 1 Operation
Through the pipeline one, we would be able to upload csv files directly and get the answers in Docker Hub. The answers.csv file will be generated with the outputs in Docker HUb
### Pipeline 2 Operation 
The 2nd Pipeline would connect to our Cloud SQL through Postgre SQL. The answers file generated will be the input here.
## Deployment using Pachyderm Hub
Here we have used Cloud Shell terminal to deploy our pipelines using Pachyderm. Following are the steps to be following for deployment:
#### 1) Getting Started with Pachyderm Hub
<img width="526" alt="gettingstartedwithpachctl" src="" title="https://user-images.githubusercontent.com/53135460/121783899-5b6bab00-cb7f-11eb-8be2-833bc164c041.png%22>" target="_blank" rel="noreferrer noopener">https://user-images.githubusercontent.com/53135460/121783899-5b6bab00-cb7f-11eb-8be2-833bc164c041.PNG">
**Create a 4 hr workspace if you're using the free version of pachctl**
Note that the workspace will disappaear after 4 hours and a new workspace would need to be created and loaded on the terminal
**Install pachyderm**
- Run the corresponding steps for your operating system on your terminal
For macOS, run:
```
brew tap pachyderm/tap && brew install pachyderm/tap/pachctl@1.13
```
For a Debian-based Linux 64-bit or Windows 10 or later running on WSL/Cloud Shell:
```
curl -o /tmp/pachctl.deb -L https://github.com/pachyderm/pachyderm/releases/download/v1.13.2/pachctl_1.13.2_amd64.deb && sudo dpkg -i /tmp/pachctl.deb
```
For all other Linux flavors:
```
curl -o /tmp/pachctl.tar.gz -L https://github.com/pachyderm/pachyderm/releases/download/v1.13.2/pac
```
**Verify that installation was successful by running pachctl version --client-only**
```
pachctl version --client-only
```
**Connect Pachyderm Workspace with Cloud Shell**
To configure a Pachyderm context and log in to your workspace (i.e. have your pachctl point to your new workspace), click the Connect link on your workspace name in the Hub UI.
<img width="843" alt="connect pachctl" src="" title="https://user-images.githubusercontent.com/53135460/121787884-cffe1400-cb96-11eb-9fd2-8031c8130041.png%22>" target="_blank" rel="noreferrer noopener">https://user-images.githubusercontent.com/53135460/121787884-cffe1400-cb96-11eb-9fd2-8031c8130041.PNG">
Follow the steps provided below:
<img width="368" alt="connect pachctl 2" src="" title="https://user-images.githubusercontent.com/53135460/121787891-ddb39980-cb96-11eb-967c-b48a88529adb.png%22>" target="_blank" rel="noreferrer noopener">https://user-images.githubusercontent.com/53135460/121787891-ddb39980-cb96-11eb-967c-b48a88529adb.PNG">
#### 2) Create your secret on Google Cloud
Go to IAM & Admin --> Service Accounts --> Creat Service Account --> Input Roles
**Roles:**
Storage Admin
Storage Object Creator
Storage Object Viewer
Click on 'Create' Service Account.
Go to Keys, and generate your secret. A jsn file will be downloaded for you, save that file 
#### 3) Upload secret created
Upload the json file on Cloud Shell
Following the following steps
```
chmod +x create_secret.sh
```
Add your json secret name generated here 
```
export GOOGLE_APPLICATION_CREDENTIALS="json.file"
```
Create your secret
```
./create_secret.sh
```
#### 4)Create your service on Docker Hub and built it
Go to Docker Hub and create a new service(check sir's video to understand) 
Run the following command on your terminal
```
docker build -t anishadocker/mgmt590-gcs
```
If your docker account is not logged in then type the following code and input your username and password
``` 
docker login
```
#### 5) Create pipeline through pachctl
Run the following code on your terminal
```
pachctl create pipeline -f spec.json
```
Check the status of your pipeline using the command
```
watch pachctl list pipeline
```
Once your status updates, run the command to verify your status
```
pachctl list job
```
#### 6) Input your encoded secret into GCS_CREDS in the restapi repo
To encode your secret input the following code:
```
base64 - w 0 anishadocker-d747ead3f6b1.json
```
Input your secret name in "anishadocker-d747ead3f6b1.json"
Copy this secret and put the text in your secrets in this repo as GCS_CREDS. Change the '=' to '@'
#### 7) Make changes to Github and run on Postman
Check your github actions and deploy your code on google cloud. Once that's done input your link on postman as:
```
https://anishadocker-2-jex3nf4qrq-uc.a.run.app/upload
```
Input any csv file in Body--> form-data. Put the Key as 'file' and send the command. You should see the following output on postman
<img width="628" alt="postman" src="" title="https://user-images.githubusercontent.com/53135460/121788163-20767100-cb99-11eb-9060-b84983c9dcf7.png%22>" target="_blank" rel="noreferrer noopener">https://user-images.githubusercontent.com/53135460/121788163-20767100-cb99-11eb-9060-b84983c9dcf7.PNG">
<img width="398" alt="dash pachctl" src="" title="https://user-images.githubusercontent.com/53135460/121788580-4a7d6280-cb9c-11eb-86ee-56f51b927b0a.png%22>" target="_blank" rel="noreferrer noopener">https://user-images.githubusercontent.com/53135460/121788580-4a7d6280-cb9c-11eb-86ee-56f51b927b0a.PNG">
#### 8) Create another Docker repo
Create a new docker repo as mgmt590-sql in Dockerhub. The same name should be updated on the yaml file. 
The code will automatically connect your output from pipeline 1 as the input for pipeline 2. The input will run in Cloud SQL through postgreSQL and return the output
### Your 2nd pipeline is created as well
## Expected Output from pachctl commands
**pachctl list job**
<img width="627" alt="pachctl list repo" src="" title="https://user-images.githubusercontent.com/53135460/121788683-2ec68c00-cb9d-11eb-8d9a-ea6ce7e0a1a7.png%22>" target="_blank" rel="noreferrer noopener">https://user-images.githubusercontent.com/53135460/121788683-2ec68c00-cb9d-11eb-8d9a-ea6ce7e0a1a7.PNG">
**pachctl list repo**
<img width="748" alt="pachctl list job" src="" title="https://user-images.githubusercontent.com/53135460/121788686-38e88a80-cb9d-11eb-972c-efc13484f25f.png%22>" target="_blank" rel="noreferrer noopener">https://user-images.githubusercontent.com/53135460/121788686-38e88a80-cb9d-11eb-972c-efc13484f25f.PNG">
**pachctl list file**
<img width="758" alt="pachctl list file" src="" title="https://user-images.githubusercontent.com/53135460/121788688-41d95c00-cb9d-11eb-9f7b-667f3d909592.png%22>" target="_blank" rel="noreferrer noopener">https://user-images.githubusercontent.com/53135460/121788688-41d95c00-cb9d-11eb-9f7b-667f3d909592.PNG">
Once all these commands are working, your pipelines are set and working!




