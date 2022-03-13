# FAMCY
![famcy_logo](famcylogo.png)

Famcy is an All-round Management Console for You (FAMCY). It is designed for Nexuni Co. Management Console app development. The goal of this framework is to provide a lightweighted, python-based frontend development platform for web applications. It is built on top of the Flask framework and contains various useful plugins for backend management and user dashboard actions. As we work on a lot of robotics and automation related applications, FAMCY natively supports [ROS2](https://docs.ros.org/en/foxy/index.html) integration. 

## Prerequisites
For now, we only support ubuntu development with python3.7. If you have other environment settings, please use our [docker](https://github.com/nexuni/FamcyDocker)!

1. Make sure your home directory start with ```/home/{USER}/....```
2. Make sure ```python3.7``` exist in your CLI environment. 

## Installation
The installation requires the install of additional package [FamcyTools](https://github.com/nexuni/FamcyTools). 
1. Install FamcyTools
```
pip3 install FamcyTools
```
2. Initialize famcy environment
```
famcy init {PROJECT_NAME} (e.g. famcy init template)
```
Wait until it finishes initialization and ignore warnings for now. It will generate the environment in ```~/.local/share/famcy/{PROJECT_NAME}``` with initial template `console`, `logs`, and `venv`. 
3. You can start developing your famcy software or import your existing code to the console folder. 

## Usage
After you finish all the development, you would need to run the following command to deploy your code. 
```
famcy deploy {PROJECT_NAME}
```
### Development
When you are running this in a debugging mode. We have provided a basic run and test method that link the web to your local port. Please run the following command to achieve this. 
```
famcy run {PROJECT_NAME}
```
### Deploy
When it comes to deploying to the production instance, you should follow the steps:
1. Make sure you have run ```famcy deploy {PROJECT_NAME}``` and you should get an output similar to the following:
```
== Copy the following part and setup system service == (Need to change path if necessary)

[Unit]
Description=uWSGI instance to serve famcy
After=network.target

[Service]
User=user
Group=www-data
WorkingDirectory=/home/user/.local/share/famcy/template/venv/lib/python3.7/site-packages/Famcy
Environment="PATH=/home/user/.local/share/famcy/template/venv/bin"
ExecStart=/home/user/.local/share/famcy/template/venv/bin/uwsgi --ini famcy.ini --lazy

[Install]
WantedBy=multi-user.target


== Copy the following part to nginx configurations == (Need to change alias path if necessary)

location / {
	include uwsgi_params;
	uwsgi_pass unix:/tmp/template.sock;
}

location /static  {
    alias /home/user/.local/share/famcy/template/venv/lib/python3.7/site-packages/Famcy/static;
}

Deployed to wsgi
```
2. Create a system file and copy the consequent info into the system configuration. Please double check the system path is correct. 
3. Create a nginx configuration file with the info above. 
4. Modify ```/etc/nginx/nginx.conf``` file and set the user to the username of your instance.
5. Restart the system service you have created.  

## Features
We provided default services with some default pages in Famcy. 

* [Famcy Quick Start](https://github.com/nexuni/Famcy/blob/main/docs/fstart.md)
* [FamcyPage](https://github.com/nexuni/Famcy/blob/main/docs/fpage.md)
* [FamcyItems](https://github.com/nexuni/Famcy/blob/main/docs/fitems.md)
* [FamcyStyles](https://github.com/nexuni/Famcy/blob/main/docs/fstyles.md)
* [FamcyElements](https://github.com/nexuni/Famcy/blob/main/docs/felements.md)
