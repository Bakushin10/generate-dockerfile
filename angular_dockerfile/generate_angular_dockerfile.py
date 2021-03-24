from dockerfile_generator_interface import dockerfileGeneratorInterface
from pprint import pprint
from enums import Enum
from PyInquirer import style_from_dict, Token, prompt
from PyInquirer import Validator, ValidationError

class GenerateDockerfileForAngular(dockerfileGeneratorInterface):

    def __init__(self):
        self.server = ""
        self.project_name = ""
        self.SPECE = ""

        self.questions()
        self.APP_HOME = "ENV APP_HOME=/{}".format(self.project_name)
        self.ENV_PROJECT_NAME = "ENV PROJECT_NAME={}".format(self.project_name)

        self.apache_dockerfile = [
            "FROM node:12.14.1-slim AS builder",
            self.APP_HOME,
            "WORKDIR $APP_HOME",
            self.SPECE,
            "COPY ./package.json package.json",
            "RUN npm install",
            "COPY . .",
            "RUN npm run build",
            self.SPECE,
            "FROM ubuntu:18.04",
            self.ENV_PROJECT_NAME,
            "ENV DEBIAN_FRONTEND=noninteractive",
            "RUN apt-get update && apt-get install -y \\",
            "    apache2 \\",
            "    apache2-utils \\",
            self.SPECE,
            "COPY --from=builder /dcp/dist/$PROJECT_NAME /var/www/html/$PROJECT_NAME",
            "COPY --from=builder /dcp/config/apache/000-default.conf /etc/apache2/sites-available/000-default.conf",
            "RUN a2enmod headers",
            "EXPOSE 80",
            'CMD ["apache2ctl", "-D", "FOREGROUND"]'
        ]

        self.nginx_dockerfile = [
            "FROM node:12.14.1-slim AS builder",
            self.APP_HOME,
            "WORKDIR $APP_HOME",
            "COPY ./package.json package.json",
            "RUN npm install",
            "COPY . .",
            "RUN npm run build",
            self.SPECE,
            "FROM nginx:1.19.0-alpine",
            self.ENV_PROJECT_NAME,
            "COPY --from=builder /dcp/dist/$PROJECT_NAME /dcp/$PROJECT_NAME",
            "COPY --from=builder /dcp/config/nginx/nginx.conf /etc/nginx/nginx.conf",
            "EXPOSE 80",
            'CMD ["nginx", "-g", "daemon off;"]'
        ]

    def generate(self):
        f = open("Dockerfile", "a")
        dockerfile = self.apache_dockerfile if self.server == "apache" else self.nginx_dockerfile
        for i in range(len(dockerfile)):
            f.write(dockerfile[i] + "\n")
        f.close()
    
    def questions(self):
        style = Enum.style
        questions = [
            {
                'type': 'list',
                'name': 'server',
                'message': 'What is your prefer web server?',
                'choices': ['Apache', 'Nginx'],
                'filter': lambda val: val.lower()
            },
            {
                'type': 'input',
                'name': 'project_name',
                'message': 'What\'s your project name?',
                #'validate': PhoneNumberValidator
            }
        ]

        answers = prompt(questions, style=style)
        self.server = answers["server"]
        self.project_name = answers["project_name"]