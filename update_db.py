from website import create_app, db

app = create_app()
db.init_app(app)

with app.app_context():
    db.create_all()
