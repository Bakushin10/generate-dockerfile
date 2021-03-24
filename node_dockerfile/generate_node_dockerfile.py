from dockerfile_generator_interface import dockerfileGeneratorInterface
from enums import Enum
import regex
from PyInquirer import style_from_dict, Token, prompt
from PyInquirer import Validator, ValidationError

class GenerateDockerfileForNode(dockerfileGeneratorInterface):

    def __init__(self):
        self.server = ""
        self.project_name = ""
        self.open_jdk_version = ""
        self.SPECE = ""

        self.questions()
        self.BASE_IMAGE = 'FROM node:{}'.format(self.node_version)
        self.EXPOSE_PORT = 'EXPOSE {}'.format(self.port)

        self.apache_dockerfile = [
            self.BASE_IMAGE ,
            "WORKDIR /src",
            "COPY . /src",
            "RUN npm install",
            self.EXPOSE_PORT,
            'CMD ["node","index.js"]'
        ]

    def generate(self):
        f = open("Dockerfile", "a")
        dockerfile = self.apache_dockerfile
        for i in range(len(dockerfile)):
            f.write(dockerfile[i] + "\n")
        f.close()
    
    def questions(self):
        style = Enum.style
        questions = [
            {
                'type': 'list',
                'name': 'node_version',
                'message': 'select node version for Dockerfile?',
                'choices': ['15.12.0-alpine3.10','14.16.0-alpine3.10', '12.21.0-alpine3.10', '10.24.0-alpine3.10'],
                'filter': lambda val: val.lower()
            },
            {
                'type': 'input',
                'name': 'port',
                'message': 'What\'s the default port ?',
                'default': "8080"
                #'validate': PhoneNumberValidator
            }
        ]

        answers = prompt(questions, style=style)
        self.port = answers["port"]
        self.node_version = answers["node_version"]