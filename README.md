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

### Below are the steps to deploy your pipeline using pachyderm:
- Build and deploy the images to DockerHub using github actions.
- Create pachyderm workspace

   <img width="309" alt="1" src="https://user-images.githubusercontent.com/84465734/121768778-fb98e400-cb2d-11eb-91c4-46e1946636f2.PNG">
 Refer : https://docs.pachyderm.com/latest/hub/hub_getting_started/
 
- login to pachyderm for your local
- run the below exports on your local system/wsl/cloudshell
  ```
  export PG_SSLROOTCERT=`cat <path>/server-ca.pem`
  export PG_SSLCERT=`cat <path>/client-cert.pem`
  export PG_SSLKEY=`cat <path>/client-key.pem`
  export PG_HOST=<host>
  export PG_PASSWORD=<db_password>
  export GOOGLE_APPLICATION_CREDENTIALS=<path>/<gcs_storage_json_key>.json
  ```
   
 - Execute the create_secrets.sh bash script to create pachctl secrets from above env variables. Make sure secret.json and secret_db.json files are created.
   
 - create pipelines using below command
   ```
   pachctl create pipeline -f spec.json --> creates pipeline getfiles
   ```
   ```
   pachctl create pipeline -f spec_db.json --> creates pipeline push-answers
   ```
   
 - Check the status of the pipelines created using below command
   ```
   pachctl list pipeline
   NAME         VERSION INPUT            CREATED        STATE / LAST JOB  DESCRIPTION
   push-answers 1       getfiles:/       19 seconds ago running / success A pipeline that pushes answers to the database
   getfiles     1       tick:@every 300s 46 minutes ago running / success A pipeline that gets a file out of GCS
   ```
   
 - Check the status of the each job instance of the pipeline using below command
   ```
   pachctl list job
   ID                               PIPELINE     STARTED            DURATION  RESTART PROGRESS    DL UL STATE
   65273b1f98364057b6d67f0eb96b4b2a push-answers About a minute ago 3 seconds 0       1 + 0 / 1   0B 0B success
   fa5728275c6f49898f785876f3cfbf91 getfiles     About a minute ago 5 seconds 0       1 + 28 / 29 0B 0B success
   939b06df098148119e82b81d9bec779f push-answers 6 minutes ago      3 seconds 0       1 + 0 / 1   0B 0B success
   c71268b355434d20ab30ceba9ea786f6 getfiles     6 minutes ago      5 seconds 0       1 + 27 / 28 0B 0B success
   4df5d27e26ee426dabe8bca7b1dca261 push-answers 11 minutes ago     3 seconds 0       1 + 0 / 1   0B 0B success
   3fa681f5083147f7844c60762ac5d9a7 getfiles     11 minutes ago     5 seconds 0       1 + 26 / 27 0B 0B success
   ```
 - In case of failure of a pipeline job use the below command to get the debug log
   ```
   pachctl logs -j <jobid from above command>
   
   abhishek@DESKTOP-KIJ0DOR:/mnt/c/data/Course_Work/Summer/Module1/prodscale/assignment3_repo/mgmt590-batch-pipelines$ pachctl logs -j 07b89298528b4d2a8f4aee71f0278a02
   Traceback (most recent call last):
   File "/app/pipeline2.py", line 92, in <module>
    insertInDB(os.path.join(dirpath, file))
   File "/app/pipeline2.py", line 85, in insertInDB
    runSqlQuery(query, params)
   File "/app/pipeline2.py", line 58, in runSqlQuery
    conn = psycopg2.connect(dbconnect)
   File "/usr/local/lib/python3.9/site-packages/psycopg2/__init__.py", line 127, in connect
    conn = _connect(dsn, connection_factory=connection_factory, **kwasync)
   psycopg2.OperationalError: could not read root certificate file ".ssl/server-ca.pem": no certificate or crl found
   /pfs/getfiles/Example_Data_-_Sheet11623541034.csv
   ```
 - Check the repositories created using below command
   ```
   pachctl list repo
   ```
 
  
