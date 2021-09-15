from flask import Flask, render_template
import boto3
import uuid
from boto3.dynamodb.conditions import Key
from decimal import Decimal

app = Flask(__name__)

@app.route("/")
def hello(movie=None):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Movies')
    randomuuid = str(uuid.uuid4())
    randomItem = table.query(
        IndexName="test-randomid-index",
        KeyConditionExpression=Key('test').eq(Decimal(1)) & Key('randomid').gt(randomuuid),
        Limit=1
    )
    movie = randomItem['Items'][0]['title']
    return render_template('hello.html', movie=movie)