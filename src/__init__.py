import os
import click
from flask import Flask
from flask_cors import CORS
from src.extensions import db
from src.settings import config
from src.blueprints.user import user_bp
from src.blueprints.auth import auth_bp


def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')
    app = Flask('juejin')
    CORS(app, supports_credentials=True)  # 开放跨域限制
    app.config.from_object(config[config_name])
    register_extensions(app)  # 注册拓展（拓展初始化）
    register_commands(app)  # 注册自定义 shell 命令
    register_blueprints(app)  # 注册蓝本
    return app


# 注册拓展（拓展初始化）
def register_extensions(app):
    db.init_app(app)


# 注册蓝本
def register_blueprints(app):
    app.register_blueprint(user_bp, url_prefix='/user')
    app.register_blueprint(auth_bp, url_prefix='/auth')


def register_commands(app):
    #  删除表和数据库后进行重建
    @app.cli.command()
    @click.option('--drop', is_flag=True, help='Create after drop.')
    def initdb(drop):
        #  初始化数据库
        if drop:
            click.confirm('This operation will delete the database, do you want to continue?', abort=True)
            db.drop_all()
            click.echo('Drop tables.')
        db.create_all()
        click.echo('Initialized database.')

    @app.cli.command()
    @click.option('--user', default=10, help='Quantity of users, default is 10.')
    @click.option('--category', default=10, help='Quantity of categories, default is 10.')
    @click.option('--post', default=5, help='Quantity of posts, default is 50.')
    def forge(user, category, post):
        # 生成虚拟数据
        from src.fakes import fake_categories, fake_posts, fake_user

        db.drop_all()
        db.create_all()

        click.echo('Generating %d users...' % user)
        fake_user(user)

        click.echo('Generating %d categories for every user...' % category)
        fake_categories(category)

        click.echo('Generating %d posts for every user...' % post)
        fake_posts(post)

        click.echo('Done.')
