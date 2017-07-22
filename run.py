# import os
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database

from theroot import create_app, users_bundle, categories_bundle
# port = int(os.environ.get('PORT', 8080))
from theroot.services import db
app = create_app()
engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
if not database_exists(engine.url):
    print('Creating the database')
    create_database(engine.url)
    db.create_all()
else:
    print('The database exists: ' + str(database_exists(engine.url)))
app.register_blueprint(users_bundle)
app.register_blueprint(categories_bundle)

app.run(debug=True, host='0.0.0.0', port=5001)
