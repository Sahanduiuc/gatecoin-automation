from apistar import Include, Route
from apistar.frameworks.wsgi import WSGIApp as App
from apistar.handlers import docs_urls, static_urls

import api.index
import api.balance

routes = [
    Route('/', 'GET', api.index.index_get),
    Route('/balance', 'GET', api.balance.balance_get),
    Include('/docs', docs_urls),
    Include('/static', static_urls)
]

app = App(routes=routes)


if __name__ == '__main__':
    app.main()
