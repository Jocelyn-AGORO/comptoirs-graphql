from jinja2 import Environment, FileSystemLoader
from django.apps import apps

# Load the Jinja template from a file
env = Environment(loader=FileSystemLoader("templates"))
template = env.get_template("pagination.jinja")

# Render the Jinja template with the desired variables
models = [model for model in apps.get_models() if repr(model).startswith("<class 'django.") is False]
generated_text = template.render(models=models)

# print(generated_text)

with open('test_pagination.py', "a") as f:
    f.write(generated_text)
