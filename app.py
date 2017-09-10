from apistar import Include, Route
from apistar.interfaces import Templates
from apistar.frameworks.wsgi import WSGIApp as App
from apistar.handlers import docs_urls, static_urls, serve_static

import api.index
import api.balance

def home(templates: Templates):
    home = templates.get_template('index.html')
    return home.render()

routes = [
    Route('/', 'GET', home),
    Route('/static/{path}', 'GET', serve_static),
    Route('/api', 'GET', api.index.index_get),
    Route('/api/balance', 'GET', api.balance.balance_get),
    Include('/api/docs', docs_urls),
    Include('/api/static', static_urls, "static_docs")
]

settings = {
    'TEMPLATES': {
        'ROOT_DIR': 'templates',     # Include the 'templates/' directory.
        'PACKAGE_DIRS': ['apistar']  # Include the built-in apistar templates.
    },
    'STATICS': {
        'ROOT_DIR': 'statics',       # Include the 'statics/' directory.
        'PACKAGE_DIRS': ['apistar']  # Include the built-in apistar static files.
    }
}

app = App(routes=routes, settings=settings)

if __name__ == '__main__':
    app.main()
