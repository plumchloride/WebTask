from flask import Flask

app = Flask(__name__, template_folder='template')
app.config.from_object("contents.config")

import contents.views