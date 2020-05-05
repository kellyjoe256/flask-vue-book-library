import os
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand
from app import create_app, db
from app.models import User
from seeder import Seeder

app = create_app(os.environ.get('FLASK_CONFIG') or 'default')

manager = Manager(app)
migrate = Migrate(app, db, compare_type=True)


def make_shell_context():
    return dict(
        db=db,
        app=app,
        User=User,
    )


manager.add_command("db", MigrateCommand)
manager.add_command("seed", Seeder())
manager.add_command("shell", Shell(make_context=make_shell_context))


if __name__ == "__main__":
    manager.run()
