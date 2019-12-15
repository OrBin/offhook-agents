from flask import Flask
from .controllers.downloads_controller import DownloadsController
from .controllers.search_controller import SearchController


def main():
    app = Flask(__name__)

    controller_pairs = [
        ('/search', SearchController),
        ('/download', DownloadsController),
    ]

    for route, klass in controller_pairs:
        controller = klass(app, route)
        controller.add_url_rules()

    app.run(port=8080)


if __name__ == '__main__':
    main()
