# AWS-Learning
Trying out different services of AWS by loosely following the tutorial from https://www.reddit.com/r/sysadmin/comments/8inzn5/so_you_want_to_learn_aws_aka_how_do_i_learn_to_be/?utm_source=amp&utm_medium=&utm_content=post_body  

## live website
http://ec2test-env.eba-iwvbnmgv.ap-east-1.elasticbeanstalk.com/  
a website that displays random movie information (JSON data from Amazon DynamoDB official tutorial);  
allows users to submit movie information

## Used AWS Services
EC2  
Autoscaling group  
ELB  
DynamoDB  
IAM role for EC2 instance to use DynamoDB  
Elastic Beanstalk to deploy the application directly  
Lambda and API Gateway for REST API

## python package
Flask for simple web development  
waitress for web server on EC2 instance  
gunicorn for web server on Elastic Beanstalk  

## Linux
tmux for continuously running the web server on EC2 instance  
iptables for port forwarding  

## docker
used `docker` and `docker-compose` to dockerize the application

## 3-tier architecture
presentation tier: HTML  
application tier: python with `flask` and `boto3`  
data tier: DynamoDB from AWS