

def create_app(object_name='pygameweb.config.Config',
               engine=None,
               session_factory=None):
    """returns a flask app.

    http://flask.pocoo.org/docs/patterns/appfactories/

    :param object_name: the object to load the config from.
    :param engine: an sqlalchemy engine.
    :param session_factory: an sqlalchemy session_factory.
    """

    from flask import Flask
    from flask_bootstrap import Bootstrap
    from flask_mail import Mail

    from pygameweb import db
    app = Flask(__name__)
    app.config.from_object(object_name)
    Bootstrap(app)

    db.init(app, engine, session_factory)
    Mail(app)


    # https://flask-debugtoolbar.readthedocs.io/en/latest/
    if app.config['DEBUG'] and not app.config['TESTING']:
        app.config['DEBUG_TB_PROFILER_ENABLED'] = True
        app.config['DEBUG_TB_TEMPLATE_EDITOR_ENABLED'] = True
        app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

        from flask_debugtoolbar import DebugToolbarExtension
        toolbar = DebugToolbarExtension(app)

    return app


def add_views_front(app):
    """ Adds all the front end views to the app.

    Kept separate from create_app so we can test individual views.
    """
    from pygameweb.wiki.views import add_wiki_blueprint
    from pygameweb.project.views import add_project_blueprint
    from pygameweb.static.views import add_static_blueprint
    from pygameweb.thumb.views import add_thumb_blueprint
    from pygameweb.news.views import add_news_blueprint
    from pygameweb.user.views import add_user_blueprint
    from pygameweb.nav.views import add_nav
    from pygameweb.page.views import add_page
    from pygameweb.dashboard.views import add_dashboard



    from pygameweb.admin.views import add_admin
    add_wiki_blueprint(app)
    add_project_blueprint(app)
    add_thumb_blueprint(app)
    add_static_blueprint(app)
    add_news_blueprint(app)
    add_user_blueprint(app)
    add_dashboard(app)
    add_page(app)

    # nav should be last, since it uses other routes.
    add_nav(app)
    add_admin(app)
