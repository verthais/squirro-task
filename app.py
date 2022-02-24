from flask import Flask
from api import api_bp, DATABASE_NAME
from database import migrate
import logging
import os
from summary import initialize

def create_app(name: str) -> Flask:
    logger = logging.getLogger('main:create_app')
    cwd = os.getcwd()
    db_file = f'{cwd}/{DATABASE_NAME}'

    if not os.path.exists(db_file):
        logger.info('creating new db: %s', DATABASE_NAME)
        migrate(DATABASE_NAME)

    initialize()

    app = Flask(name)
    app.register_blueprint(api_bp)

    return app


def main():
    app = create_app('squirro-app')
    app.run(port=50000)


if __name__ == '__main__':
    main()