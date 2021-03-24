from dockerfile_generator_interface import dockerfileGeneratorInterface
from enums import Enum
import regex
from PyInquirer import style_from_dict, Token, prompt
from PyInquirer import Validator, ValidationError

class PhoneNumberValidator(Validator):
    def validate(self, document):
        ok = regex.match('^[0-9]{4,7}', document.text)
        if not ok:
            raise ValidationError(
                message='Please enter a valid phone number',
                cursor_position=len(document.text))  # Move cursor to end

class GenerateDockerfileForJava(dockerfileGeneratorInterface):

    def __init__(self):
        self.server = ""
        self.project_name = ""
        self.open_jdk_version = ""
        self.SPECE = ""

        self.questions()
        self.APP_HOME = "ENV APP_HOME={}".format(self.project_name)
        self.ENV_PROJECT_NAME = "ENV PROJECT_NAME={}".format(self.project_name)
        self.JAVA_VERSION = "ENV JAVA_VERSON {}".format(self.open_jdk_version)
        self.BUILD_ARTIFACT = "/{}/build/libs/{}-0.0.1-SNAPSHOT.jar".format(self.project_name, self.project_name)
        self.BUILD_FILE = "ENV BUILD_FILE {}".format(self.BUILD_ARTIFACT)
        self.CMD = 'CMD ["java","-jar","{}"]'.format(self.BUILD_ARTIFACT)
        self.EXPOSE_PORT = 'EXPOSE {}'.format(self.port)

        self.apache_dockerfile = [
            "FROM gradle:6.7.0-jdk11 AS builder",
            self.APP_HOME,
            "WORKDIR $APP_HOME",
            "COPY . .",
            "RUN gradle build",
            self.SPECE,
            "FROM centos:7",
            "ENV DEBIAN_FRONTEND=noninteractive",
            self.JAVA_VERSION,
            self.BUILD_FILE,
            "RUN yum -y update && \\",
            "    yum install -y \\",
            "    java-$JAVA_VERSON-openjdk \\",
            "    java-$JAVA_VERSON-openjdk-devel \\",
            "    && yum clean all \\",
            "    && rm -rf /var/cache/yum",
            self.SPECE,
            "COPY --from=builder $BUILD_FILE $BUILD_FILE",
            self.EXPOSE_PORT,
            self.CMD
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
                'type': 'input',
                'name': 'project_name',
                'message': 'What\'s your project name?',
                #'validate': PhoneNumberValidator
            },
            {
                'type': 'list',
                'name': 'java_version',
                'message': 'What is java version for Dockerfile?',
                'choices': ['8', '11'],
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
        self.project_name = answers["project_name"]
        self.open_jdk_version = answers["java_version"]
        self.port = answers["port"]