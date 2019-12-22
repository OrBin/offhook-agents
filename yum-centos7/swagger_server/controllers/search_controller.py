import yum
from flask import request, jsonify, abort
from yum.Errors import PackageSackError
from ..models.download_spec import DownloadSpec  # noqa: E501
from .base_controller import BaseController


class SearchController(BaseController):

    def search(self):  # noqa: E501
        """Search for packages

         # noqa: E501

        :param body:
        :type body: dict | bytes

        :rtype: List[SearchResult]
        """

        dl_spec = DownloadSpec.from_dict(request.json)

        if not dl_spec.architecture:
            abort(400, 'Architecture must be specified')

        # YumBase object must be created on each call, since its package sack cannot be used from multiple threads
        yum_base = yum.YumBase()

        try:
            results = yum_base.pkgSack.returnNewestByName(patterns=dl_spec.packages)
            results = filter(lambda result: result.arch == dl_spec.architecture, results)

            results = [{'name': result.name, 'nevraString': result.nevra} for result in results]
        except PackageSackError:
            results = []

        return jsonify(results)

    def add_url_rules(self):
        self._add_url_rule('/', self.search, methods=['POST'])
