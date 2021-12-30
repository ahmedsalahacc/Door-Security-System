from flask import Flask
from src.extensions import db, cors
from src.controller import main
from src.seeder.seeder import seed
from uuid import uuid4
import os


def create_app():
    '''
    create flask app
    '''
    # get the base directory
    basedir = os.getcwd()
    repo_path = os.path.abspath(os.path.dirname(__name__))
    template_dir = os.path.join(
        repo_path,  'views'  # location of front end pages
    )
    static_dir = os.path.join(
        repo_path,  'static'  # location of front end pages
    )

    # init flask app
    app = Flask(__name__, template_folder=template_dir,
                static_folder=static_dir)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{basedir}/database.db'
    app.config['SECRET_KEY'] = str(uuid4())
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
    app.config['UPLOAD_FOLDER'] = 'static'
    db.init_app(app)

    # create database If it doesnt exist, seed database if env variable SEED is set
    if not os.path.isfile(os.path.join(basedir, 'database.db')):
        with app.app_context():
            db.create_all()
            if os.environ.get('SEED'):
                seed()

    cors.init_app(app)
    app.register_blueprint(main)

    return app


# create flask app
app = create_app()
