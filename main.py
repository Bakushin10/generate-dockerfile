import fire
from enums import Enum
from PyInquirer import style_from_dict, Token, prompt
from PyInquirer import Validator, ValidationError
from angular_dockerfile.generate_angular_dockerfile import GenerateDockerfileForAngular
from java_dockerfile.generate_java_dockerfile import GenerateDockerfileForJava
from node_dockerfile.generate_node_dockerfile import GenerateDockerfileForNode
from python_dockerfile.generate_python_dockerfile import GenerateDockerfileForPython


def create():
    style = Enum.style
    questions = [
        {
            'type': 'list',
            'name': 'language',
            'message': 'What language or framework are you creating Dockerfile for ?',
            'choices': ['Angular', 'python', 'Java', 'node'],
            'filter': lambda val: val.lower()
        }
    ]

    answers = prompt(questions, style=style)
    selected_language = answers["language"]

    if selected_language == "angular":
        angular = GenerateDockerfileForAngular()
        angular.generate()
    elif selected_language == "java":
        java = GenerateDockerfileForJava()
        java.generate()
    elif selected_language == "node":
        node = GenerateDockerfileForNode()
        node.generate()
    elif selected_language == "python":
        python = GenerateDockerfileForPython()
        python.generate()
    return


if __name__ == "__main__":
    fire.Fire({
        "create": create
    })