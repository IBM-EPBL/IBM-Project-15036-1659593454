from flask import Flask, render_template, request, redirect,url_for,flash
from datetime import date
import ibm_boto3
from ibm_botocore.client import Config, ClientError
import ibm_db


#ibm cloud object storage

# {
#   "apikey": "sLufdH2rBzVPhLTrHzduCiMwz8pKe-kHz-36BnFNX2zc",
#   "endpoints": "https://control.cloud-object-storage.cloud.ibm.com/v2/endpoints",
#   "iam_apikey_description": "Auto-generated for key crn:v1:bluemix:public:cloud-object-storage:global:a/5b8b2e5240a748028af0acae403b9b4f:74aaacd1-290e-4616-aa49-396e53f3291c:resource-key:c87928e1-a4f2-47f7-acc9-6ff29acd8653",
#   "iam_apikey_name": "Service credentials-1",
#   "iam_role_crn": "crn:v1:bluemix:public:iam::::serviceRole:Writer",
#   "iam_serviceid_crn": "crn:v1:bluemix:public:iam-identity::a/5b8b2e5240a748028af0acae403b9b4f::serviceid:ServiceId-f3adefa0-2e1c-4c29-9a3f-5655edff4cce",
#   "resource_instance_id": "crn:v1:bluemix:public:cloud-object-storage:global:a/5b8b2e5240a748028af0acae403b9b4f:74aaacd1-290e-4616-aa49-396e53f3291c::"
# }


#ibm db2

# {
#   "connection": {
#     "cli": {
#       "arguments": [
#         [
#           "-u",
#           "nbn39747",
#           "-p",
#           "u9wDq7XVWmkLtukT",
#           "--ssl",
#           "--sslCAFile",
#           "1cbbb1b6-3a1a-4d49-9262-3102a8f7a7c8",
#           "--authenticationDatabase",
#           "admin",
#           "--host",
#           "b70af05b-76e4-4bca-a1f5-23dbb4c6a74e.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud:32716"
#         ]
#       ],
#       "bin": "db2",
#       "certificate": {
#         "certificate_base64": "LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tCk1JSURFakNDQWZxZ0F3SUJBZ0lKQVA1S0R3ZTNCTkxiTUEwR0NTcUdTSWIzRFFFQkN3VUFNQjR4SERBYUJnTlYKQkFNTUUwbENUU0JEYkc5MVpDQkVZWFJoWW1GelpYTXdIaGNOTWpBd01qSTVNRFF5TVRBeVdoY05NekF3TWpJMgpNRFF5TVRBeVdqQWVNUnd3R2dZRFZRUUREQk5KUWswZ1EyeHZkV1FnUkdGMFlXSmhjMlZ6TUlJQklqQU5CZ2txCmhraUc5dzBCQVFFRkFBT0NBUThBTUlJQkNnS0NBUUVBdXUvbitpWW9xdkdGNU8xSGpEalpsK25iYjE4UkR4ZGwKTzRUL3FoUGMxMTREY1FUK0plRXdhdG13aGljTGxaQnF2QWFMb1hrbmhqSVFOMG01L0x5YzdBY291VXNmSGR0QwpDVGcrSUsxbjBrdDMrTHM3d1dTakxqVE96N3M3MlZUSU5yYmx3cnRIRUlvM1JWTkV6SkNHYW5LSXdZMWZVSUtrCldNMlR0SDl5cnFsSGN0Z2pIUlFmRkVTRmlYaHJiODhSQmd0amIva0xtVGpCaTFBeEVadWNobWZ2QVRmNENOY3EKY21QcHNqdDBPTnI0YnhJMVRyUWxEemNiN1hMSFBrWW91SUprdnVzMUZvaTEySmRNM1MrK3labFZPMUZmZkU3bwpKMjhUdGJoZ3JGOGtIU0NMSkJvTTFSZ3FPZG9OVm5QOC9EOWZhamNNN0lWd2V4a0lSOTNKR1FJREFRQUJvMU13ClVUQWRCZ05WSFE0RUZnUVVlQ3JZanFJQzc1VUpxVmZEMDh1ZWdqeDZiUmN3SHdZRFZSMGpCQmd3Rm9BVWVDclkKanFJQzc1VUpxVmZEMDh1ZWdqeDZiUmN3RHdZRFZSMFRBUUgvQkFVd0F3RUIvekFOQmdrcWhraUc5dzBCQVFzRgpBQU9DQVFFQUkyRTBUOUt3MlN3RjJ2MXBqaHV4M0lkWWV2SGFVSkRMb0tPd0hSRnFSOHgxZ2dRcGVEcFBnMk5SCkx3R08yek85SWZUMmhLaWd1d2orWnJ5SGxxcHlxQ0pLOHJEU28xZUVPekIyWmE2S1YrQTVscEttMWdjV3VHYzMKK1UrVTFzTDdlUjd3ZFFuVjU0TVU4aERvNi9sVHRMRVB2Mnc3VlNPSlFDK013ejgrTFJMdjVHSW5BNlJySWNhKwozM0wxNnB4ZEttd1pLYThWcnBnMXJ3QzRnY3dlYUhYMUNEWE42K0JIbzhvWG5YWkh6UG91cldYS1BoaGdXZ2J5CkNDcUdIK0NWNnQ1eFg3b05NS3VNSUNqRVZndnNLWnRqeTQ5VW5iNVZZbHQ0b1J3dTFlbGdzRDNjekltbjlLREQKNHB1REFvYTZyMktZZE4xVkxuN3F3VG1TbDlTU05RPT0KLS0tLS1FTkQgQ0VSVElGSUNBVEUtLS0tLQo=",
#         "name": "1cbbb1b6-3a1a-4d49-9262-3102a8f7a7c8"
#       },
#       "composed": [
#         "db2 -u nbn39747 -p u9wDq7XVWmkLtukT --ssl --sslCAFile 1cbbb1b6-3a1a-4d49-9262-3102a8f7a7c8 --authenticationDatabase admin --host b70af05b-76e4-4bca-a1f5-23dbb4c6a74e.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud:32716"
#       ],
#       "environment": {},
#       "type": "cli"
#     },
#     "db2": {
#       "authentication": {
#         "method": "direct",
#         "password": "u9wDq7XVWmkLtukT",
#         "username": "nbn39747"
#       },
#       "certificate": {
#         "certificate_base64": "LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tCk1JSURFakNDQWZxZ0F3SUJBZ0lKQVA1S0R3ZTNCTkxiTUEwR0NTcUdTSWIzRFFFQkN3VUFNQjR4SERBYUJnTlYKQkFNTUUwbENUU0JEYkc5MVpDQkVZWFJoWW1GelpYTXdIaGNOTWpBd01qSTVNRFF5TVRBeVdoY05NekF3TWpJMgpNRFF5TVRBeVdqQWVNUnd3R2dZRFZRUUREQk5KUWswZ1EyeHZkV1FnUkdGMFlXSmhjMlZ6TUlJQklqQU5CZ2txCmhraUc5dzBCQVFFRkFBT0NBUThBTUlJQkNnS0NBUUVBdXUvbitpWW9xdkdGNU8xSGpEalpsK25iYjE4UkR4ZGwKTzRUL3FoUGMxMTREY1FUK0plRXdhdG13aGljTGxaQnF2QWFMb1hrbmhqSVFOMG01L0x5YzdBY291VXNmSGR0QwpDVGcrSUsxbjBrdDMrTHM3d1dTakxqVE96N3M3MlZUSU5yYmx3cnRIRUlvM1JWTkV6SkNHYW5LSXdZMWZVSUtrCldNMlR0SDl5cnFsSGN0Z2pIUlFmRkVTRmlYaHJiODhSQmd0amIva0xtVGpCaTFBeEVadWNobWZ2QVRmNENOY3EKY21QcHNqdDBPTnI0YnhJMVRyUWxEemNiN1hMSFBrWW91SUprdnVzMUZvaTEySmRNM1MrK3labFZPMUZmZkU3bwpKMjhUdGJoZ3JGOGtIU0NMSkJvTTFSZ3FPZG9OVm5QOC9EOWZhamNNN0lWd2V4a0lSOTNKR1FJREFRQUJvMU13ClVUQWRCZ05WSFE0RUZnUVVlQ3JZanFJQzc1VUpxVmZEMDh1ZWdqeDZiUmN3SHdZRFZSMGpCQmd3Rm9BVWVDclkKanFJQzc1VUpxVmZEMDh1ZWdqeDZiUmN3RHdZRFZSMFRBUUgvQkFVd0F3RUIvekFOQmdrcWhraUc5dzBCQVFzRgpBQU9DQVFFQUkyRTBUOUt3MlN3RjJ2MXBqaHV4M0lkWWV2SGFVSkRMb0tPd0hSRnFSOHgxZ2dRcGVEcFBnMk5SCkx3R08yek85SWZUMmhLaWd1d2orWnJ5SGxxcHlxQ0pLOHJEU28xZUVPekIyWmE2S1YrQTVscEttMWdjV3VHYzMKK1UrVTFzTDdlUjd3ZFFuVjU0TVU4aERvNi9sVHRMRVB2Mnc3VlNPSlFDK013ejgrTFJMdjVHSW5BNlJySWNhKwozM0wxNnB4ZEttd1pLYThWcnBnMXJ3QzRnY3dlYUhYMUNEWE42K0JIbzhvWG5YWkh6UG91cldYS1BoaGdXZ2J5CkNDcUdIK0NWNnQ1eFg3b05NS3VNSUNqRVZndnNLWnRqeTQ5VW5iNVZZbHQ0b1J3dTFlbGdzRDNjekltbjlLREQKNHB1REFvYTZyMktZZE4xVkxuN3F3VG1TbDlTU05RPT0KLS0tLS1FTkQgQ0VSVElGSUNBVEUtLS0tLQo=",
#         "name": "1cbbb1b6-3a1a-4d49-9262-3102a8f7a7c8"
#       },
#       "composed": [
#         "db2://nbn39747:u9wDq7XVWmkLtukT@b70af05b-76e4-4bca-a1f5-23dbb4c6a74e.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud:32716/bludb?authSource=admin&replicaSet=replset"
#       ],
#       "database": "bludb",
#       "host_ros": [
#         "b70af05b-76e4-4bca-a1f5-23dbb4c6a74e.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud:30505"
#       ],
#       "hosts": [
#         {
#           "hostname": "b70af05b-76e4-4bca-a1f5-23dbb4c6a74e.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud",
#           "port": 32716
#         }
#       ],
#       "jdbc_url": [
#         "jdbc:db2://b70af05b-76e4-4bca-a1f5-23dbb4c6a74e.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud:32716/bludb:user=<userid>;password=<your_password>;sslConnection=true;"
#       ],
#       "path": "/bludb",
#       "query_options": {
#         "authSource": "admin",
#         "replicaSet": "replset"
#       },
#       "replica_set": "replset",
#       "scheme": "db2",
#       "type": "uri"
#     }
#   },
#   "instance_administration_api": {
#     "deployment_id": "crn:v1:bluemix:public:dashdb-for-transactions:us-south:a/5b8b2e5240a748028af0acae403b9b4f:9ce4b160-9cdc-46a8-a39c-e481c3c60be9::",
#     "instance_id": "crn:v1:bluemix:public:dashdb-for-transactions:us-south:a/5b8b2e5240a748028af0acae403b9b4f:9ce4b160-9cdc-46a8-a39c-e481c3c60be9::",
#     "root": "https://api.db2.cloud.ibm.com/v5/ibm"
#   }
# }


# dsn_hostname = "b70af05b-76e4-4bca-a1f5-23dbb4c6a74e.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud"
# dsn_uid = "nbn39747"
# dsn_pwd = "u9wDq7XVWmkLtukT"

# dsn_driver = "{IBM DB2 ODBC DRIVER}"
# dsn_database = "bludb"
# dsn_port = "32716"
# dsn_protocol = "TCP/IP"

# dsn = (
#     "DRIVER={0};"
#     "DATABASE={1};"
#     "HOSTNAME={2};"
#     "PORT={3};"
#     "PROTOCOL={4};"
#     "UID={5};"
#     "PWD={6};").format(dsn_driver, dsn_database, dsn_hostname, dsn_port, dsn_protocol, dsn_uid, dsn_pwd)


COS_ENDPOINT = "https://control.cloud-object-storage.cloud.ibm.com/v2/endpoints"
COS_API_KEY_ID = "sLufdH2rBzVPhLTrHzduCiMwz8pKe-kHz-36BnFNX2zc"
COS_INSTANCE_CRN = "crn:v1:bluemix:public:iam-identity::a/5b8b2e5240a748028af0acae403b9b4f::serviceid:ServiceId-f3adefa0-2e1c-4c29-9a3f-5655edff4cce"

cos = ibm_boto3.resource("s3",
                         ibm_api_key_id=COS_API_KEY_ID,
                         ibm_service_instance_id=COS_INSTANCE_CRN,
                         config=Config(signature_version="oauth"),
                         endpoint_url=COS_ENDPOINT
                         )


conn = ibm_db.connect('DATABASE=bludb;'
                     'HOSTNAME=8e359033-a1c9-4643-82ef-8ac06f5107eb.bs2io90l08kqb1od8lcg.databases.appdomain.cloud;'  # 127.0.0.1 or localhost works if it's local
                     'PORT=30120;'
                     'PROTOCOL=TCPIP;'
                     'UID=zsy87446;'
                     'PWD=CoV6JEBhlIYZGUfq;', '', '')
# conn = ibm_db.connect('bludb','nbn39747','u9wDq7XVWmkLtukT')
# conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=b70af05b-76e4-4bca-a1f5-23dbb4c6a74e.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;PORT=32716;PROTOCOL=TCP/IP;UID=nbn39747;PWD=u9wDq7XVWmkLtukT;", "", "")
def get_bucket_contents(bucket_name):
    print("Retrieving bucket contents from: {0}".format(bucket_name))
    try:
        files = cos.Bucket(bucket_name).objects.all()
        files_names = []
        for file in files:
            files_names.append(file.key)
            print("Item: {0} ({1} bytes).".format(file.key, file.size))
        return files_names
    except ClientError as be:
        print("CLIENT ERROR: {0}\n".format(be))
    except Exception as e:
        print("Unable to retrieve bucket contents: {0}".format(e))
app = Flask(__name__)
@app.route('/')
def index():
    return redirect(url_for('sign_in'))
@app.route('/sign_in')
def sign_in():

    return render_template('sign_in.html')


@app.route('/sign_up')
def sign_up():
    return render_template('sign_up.html')

@app.route('/verifyid',methods=['GET', 'POST'])
def verifyid():
    all_users=[]
    if request.method=='POST':
        emailid = request.form['email']
        pwd = request.form['password']
        sql = "SELECT * FROM users"
        stmt = ibm_db.exec_immediate(conn, sql)
        users = ibm_db.fetch_both(stmt)
        while users != False:
            # print ("The Name is : ",  dictionary)
            all_users.append(users)
            users = ibm_db.fetch_both(stmt)
        for user in all_users:
            if emailid == user['EMAIL']:
                if pwd == user['PWD']:
                    files = get_bucket_contents('funedu')
                    return render_template('home.html', files=files)
        return render_template('login_failed.html')


@app.route('/create_id', methods=['GET', 'POST'])
def create_id():
    temp=0



    if request.method == 'POST':
        name = request.form['username']
        emailid = request.form['email']
        pwd = request.form['password']
        sql = "SELECT * FROM users WHERE email =?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt, 1, emailid)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)

        if account:
            return render_template('user_already_exists.html')
        else:
            insert_sql = "INSERT INTO users VALUES (?,?,?,?)"
            prep_stmt = ibm_db.prepare(conn, insert_sql)
            ibm_db.bind_param(prep_stmt, 1, name)
            ibm_db.bind_param(prep_stmt, 2, emailid)
            ibm_db.bind_param(prep_stmt, 3, pwd)
            ibm_db.bind_param(prep_stmt, 4, date.today())
            ibm_db.execute(prep_stmt)
            return render_template('id_created.html')






if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
