import boto3
import json
import mysql.connector
from datetime import datetime, timezone, timedelta

def lambda_handler(event, context):
    client = boto3.client('iot-data', region_name='ap-northeast-2') 
    topic = 'dispenser/sub'

    db_host = ''
    db_user = ''
    db_password = ''
    db_name = ''

    connection = mysql.connector.connect(host=db_host, user=db_user, password=db_password, database=db_name)

    try:
        cursor = connection.cursor()
        sql = "SELECT medicine_name, medicine_dose FROM medicine_schedule WHERE medicine_when = %s"
        cursor.execute(sql, ("저녁",))
        schedule = cursor.fetchall()

        if schedule:
            medicine_name = [row[0] for row in schedule]  
            medicine_dose = [row[1] for row in schedule]  

            message = {
                "when": "3",
                "name1": medicine_name[0], 
                "dose1": medicine_dose[0]    
            }
            if len(medicine_name) > 1:
                message["name2"] = medicine_name[1]  
                message["dose2"] = medicine_dose[1]  

            client.publish(topic=topic, qos=1, payload=json.dumps(message))
        else:
            print("저녁에 복용할 약이 없습니다.")

    except Exception as e:
        print("Error:", e)
    finally:
        cursor.close()
        connection.close()







