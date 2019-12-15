from flask import Flask
import yum
from .controllers.downloads_controller import DownloadsController
from .controllers.search_controller import SearchController


app = Flask(__name__)

controller_pairs = [
    ('/search', SearchController),
    ('/download', DownloadsController),
]

yum_base = yum.YumBase()
yum_base.setCacheDir()

for route, klass in controller_pairs:
    controller = klass(app, route, yum_base)
    controller.add_url_rules()


def main():
    app.run(host='0.0.0.0', port=8080)


if __name__ == '__main__':
    main()
