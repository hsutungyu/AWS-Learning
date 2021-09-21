from flask import Flask, render_template, request
import boto3
import uuid
from boto3.dynamodb.conditions import Key
from decimal import Decimal
from datetime import datetime
from waitress import serve
import requests
import json

# Elastic Beanstalk looks for application callable
application = Flask(__name__)

@application.route("/")
def hello(title=None, year=None, director=None, release_date=None, rating=None, genres=None, image_url=None, plot=None, rank=None, running_time_secs=None, actors=None, apiYear=None, apiInfo=None):
    # DynamoDB part
    dynamodb = boto3.resource('dynamodb', region_name='ap-east-1')
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

    # REST api part
    # randomly get the year and the title of five movies
    response = requests.get("https://df2k401ugi.execute-api.ap-east-1.amazonaws.com/beta/fivemovies")
    apiInfo = json.loads(response.json()['body'])
    return render_template('hello.html', title=title, year=year, director=director, release_date=release_date, rating=rating, genres=genres, image_url=image_url, plot=plot, rank=rank, running_time_secs=running_time_secs, actors=actors, apiYear=apiYear, apiInfo=apiInfo)

@application.route("/add", methods=['POST'])
def add():
    # assume that the user would input both year and title
    # in reality, can do form validation using javascript before posting to /add
    year = Decimal(request.form['yearInput'])
    title = request.form['titleInput']
    info = {}
    if request.form['directorsInput']:
        info['directors'] = request.form['directorsInput'].split()
    if request.form['releaseDateInput']:
        info['release_date'] = request.form['releaseDateInput']
    if request.form['genresInput']:
        info['genres'] = request.form['genresInput'].split()
    if request.form['plotInput']:
        info['plot'] = request.form['plotInput']
    if request.form['rankInput']:
        info['rank'] = request.form['rankInput']
    if request.form['actorsInput']:
        info['actors'] = request.form['actorsInput'].split()
    dynamodb = boto3.resource('dynamodb', region_name='ap-east-1')
    table = dynamodb.Table('Movies')
    randomuuid = str(uuid.uuid4())
    putItem = table.put_item(
        Item={
            'year': year,
            'title': title,
            'info': info,
            'randomid': randomuuid,
            'test': 1
        }
    )
    statusCode = putItem['ResponseMetadata']['HTTPStatusCode']
    return render_template('add.html', statusCode=statusCode)

if __name__ == "__main__":
    # https://stackoverflow.com/questions/21193988/keep-server-running-on-ec2-instance-after-ssh-is-terminated
    # https://stackoverflow.com/questions/12464926/linux-in-ec2amazon-cannot-use-port-80-for-tomcat
    # https://sean22492249.medium.com/flask-with-gunicorn-9a37bca29227
    # https://camillovisini.com/article/barebone-flask-website-on-aws-elastic-beanstalk/#deployment-to-aws-elastic-beanstalk
    application.run()