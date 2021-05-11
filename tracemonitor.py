import click
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from initapp import create_app, db
from models import Admin, User, Record

app = create_app()




@app.shell_context_processor
def make_shell_context():
    return dict(db=db, Admin=Admin, User=User, Record=Record)



@app.cli.command()
@click.option('--drop', is_flag=True, help='Create after drop.')
def initdb(drop):
    """Initialize the database."""
    if drop:
        click.confirm('This operation will delete the database, do you want to continue?', abort=True)
        db.drop_all()
        click.echo('Drop tables.')
    db.create_all()
    click.echo('Initialized database.')

@app.cli.command()
def init():
    """Initialize Albumy."""
    click.echo('Initializing the database...')
    db.create_all()

    click.echo('Done.')

@app.cli.command()
#@click.option('--admin', default=1, help='Quantity of admin, default is 1.')
@click.option('--user', default=5, help='Quantity of users, default is 10.')
@click.option('--record', default=50, help='Quantity of comments, default is 100.')
def forge(user, record):
    """Generate fake data."""

    from fakes import fake_admin, fake_user, fake_record

    db.drop_all()
    db.create_all()

    click.echo('Generating the administrator...')
    fake_admin()
    click.echo('Generating %d users...' % user)
    fake_user(user)
    click.echo('Generating %d comments...' % record)
    fake_record(record)
    click.echo('Done.')


import views
