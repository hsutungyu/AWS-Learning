from flask import Flask, render_template
import boto3
import uuid
from boto3.dynamodb.conditions import Key
from decimal import Decimal

app = Flask(__name__)

@app.route("/")
def hello(title=None, year=None, director=None, release_date=None, rating=None, genres=None, image_url=None, plot=None, rank=None, running_time_secs=None, actors=None):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Movies')
    randomuuid = str(uuid.uuid4())
    randomItem = table.query(
        IndexName="test-randomid-index",
        KeyConditionExpression=Key('test').eq(Decimal(1)) & Key('randomid').gt(randomuuid),
        Limit=1
    )
    if 'title' in randomItem['Items'][0]:
        title = randomItem['Items'][0]['title']
    if 'year' in randomItem['Items'][0]:
        year = randomItem['Items'][0]['year']
    if 'directors' in randomItem['Items'][0]['info']:
        director = randomItem['Items'][0]['info']['directors']
    if 'release_date' in randomItem['Items'][0]['info']:
        release_date = randomItem['Items'][0]['info']['release_date'][:10]
    if 'rating' in randomItem['Items'][0]['info']:
        rating = randomItem['Items'][0]['info']['rating']
    if 'genres' in randomItem['Items'][0]['info']:
        genres = randomItem['Items'][0]['info']['genres']
    if 'image_url' in randomItem['Items'][0]['info']:
        image_url = randomItem['Items'][0]['info']['image_url']
    if 'plot' in randomItem['Items'][0]['info']:
        plot = randomItem['Items'][0]['info']['plot']
    if 'rank' in randomItem['Items'][0]['info']:
        rank = randomItem['Items'][0]['info']['rank']
    if 'running_time_secs' in randomItem['Items'][0]['info']:
        running_time_secs = randomItem['Items'][0]['info']['running_time_secs']
    if 'actors' in randomItem['Items'][0]['info']:
        actors = randomItem['Items'][0]['info']['actors']
    return render_template('hello.html', title=title, year=year, director=director, release_date=release_date, rating=rating, genres=genres, image_url=image_url, plot=plot, rank=rank, running_time_secs=running_time_secs, actors=actors)