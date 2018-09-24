from lore import create_app
from lore import db

app = create_app()
app.app_context().push()

db.drop_all()
print("Dropped tables")
db.create_all()
print("Created tables")