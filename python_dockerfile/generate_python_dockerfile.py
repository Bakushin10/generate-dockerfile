from dockerfile_generator_interface import dockerfileGeneratorInterface
from enums import Enum
import regex
from PyInquirer import style_from_dict, Token, prompt
from PyInquirer import Validator, ValidationError

class GenerateDockerfileForPython(dockerfileGeneratorInterface):

    def __init__(self):
        self.SPECE = ""
        self.is_alpine_image = True
        self.questions()
        self.alpine_image = "FROM docker pull {}".format(self.base_image)

        self.centos_dockerfile =[
            "FROM centos:7",
            self.SPECE,
            "USER root",
            "ENV APP_HOME=/src",
            "ENV PYTHON_VERSION=36",
            "WORKDIR $APP_HOME",
            self.SPECE,
            "RUN yum -y install \\",
            "    epel-release \\",
            "    postgresql \\",
            "    postgresql-devel \\",
            "    gcc \\",
            "    python-devel \\",
            "    python$PYTHON_VERSION \\",
            "    && yum clean all \\",
            "    && rm /tmp/* \\",
            "    && rm -rf /var/cache/yum \\",
            "    && python3.6 -m ensurepip\\",
            "    && python3.6 -m ensurepip\\",
            self.SPECE,
            "COPY ./requirements.txt requirements.txt",
            "RUN pip3 install -r requirements.txt",
            "COPY . $APP_HOME",
            'CMD ["python3","run.py"]'
        ]

        self.alpine_dockerfile = [
            self.alpine_image,
            "ENV APP_HOME=/src",
            "COPY ./requirements.txt requirements.txt",
            "RUN pip3 install -r requirements.txt",
            "COPY . $APP_HOME",
            'CMD ["python3","run.py"]'
        ]

    def questions(self):
        style = Enum.style
        questions = [
            {
                'type': 'list',
                'name': 'base_image',
                'message': 'What is java version for Dockerfile?',
                'choices': ['centos:7', "python:3.8-alpine", 'python:3.7-alpine', "python:3.6-alpine"],
                'filter': lambda val: val.lower()
            }
        ]

        answers = prompt(questions, style=style)
        self.base_image = answers["base_image"]
        if self.base_image == 'centos:7':
            self.is_alpine_image = False
    
    def generate(self):
        f = open("Dockerfile", "a")
        dockerfile = self.alpine_dockerfile if self.is_alpine_image else self.centos_dockerfile
        for i in range(len(dockerfile)):
            f.write(dockerfile[i] + "\n")
        f.close()