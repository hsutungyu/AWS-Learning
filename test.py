import boto3
import json
import uuid
from boto3.dynamodb.conditions import Key
from decimal import Decimal
import requests



def create_movie_table():
	table = dynamodb.create_table(
	TableName = 'Movies',
	KeySchema = [
			{'AttributeName': 'year',
		            'KeyType': 'HASH' # Partition Key
		            },
		        {'AttributeName': 'title',
		            'KeyType': 'RANGE' # Sort Key
		            }
		        ],
	AttributeDefinitions = [
		    {'AttributeName': 'year',
		        'AttributeType': 'N'
		        },
		    {'AttributeName': 'title',
		        'AttributeType': 'S'
		        },
		    ],
	ProvisionedThroughput = {
			'ReadCapacityUnits': 10,
		    'WriteCapacityUnits': 10
		    }
		)

	return table
	

def load_movie_table(moviedata):
	table = dynamodb.Table('Movies')
	for x in moviedata:
		table.put_item(Item=x)
	return

def movie_table_uuid(moviedata):
	table = dynamodb.Table('Movies')
	for x in moviedata:
		result = table.update_item(
			Key={
				'year': x['year'],
				'title': x['title']
			},
			UpdateExpression="SET randomid = :uuid",
			ExpressionAttributeValues={
				':uuid': str(uuid.uuid4())
			}
		)

def movie_table_for_query(moviedata):
	table = dynamodb.Table('Movies')
	for x in moviedata:
		result = table.update_item(
			Key={
				'year': x['year'],
				'title': x['title']
			},
			UpdateExpression="SET test = :test",
			ExpressionAttributeValues={
				':test': Decimal(1)
			}
		)

if __name__ == '__main__':
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Movies')
    randomuuid = str(uuid.uuid4())
    #index = table.Index('')
    # movie_table = create_movie_table()
    #with open('moviedata.json') as f:
	#    moviedata = json.load(f, parse_float=Decimal)
    #movie_table_uuid(moviedata)
    #movie_table_for_query(moviedata)
    # randomItem = table.query(
    #     IndexName="test-randomid-index",
    #     KeyConditionExpression=Key('test').eq(Decimal(1)) & Key('randomid').gt(randomuuid),
    #     Limit=5
    # )
    # print(randomItem['Items'][5])
    response = requests.get("https://df2k401ugi.execute-api.ap-east-1.amazonaws.com/beta/fivemovies")
    jsonString = json.loads(response.json()['body'])
    #print(type(yearList))
    # print("Table status:", movie_table.table_status)

