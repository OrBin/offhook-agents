import six

from swagger_server.models.download_request import DownloadRequest  # noqa: E501
from swagger_server.models.download_spec import DownloadSpec  # noqa: E501
from swagger_server import util
from .base_controller import BaseController

class DownloadsController(BaseController):

    def get_download_files(requestId):  # noqa: E501
        """Get files from a download request

         # noqa: E501

        :param requestId: ID of request to get the files for
        :type requestId: int

        :rtype: file
        """

        #searchword = request.args.get('fileType', '')

        return 'do some magic!'


    def get_download_request(requestId):  # noqa: E501
        """Get a download request

         # noqa: E501

        :param requestId: ID of request to return
        :type requestId: int

        :rtype: DownloadRequest
        """
        return 'do some magic!'


    def submit_download_request():  # noqa: E501
        """Submit a download request

         # noqa: E501

        :param body:
        :type body: dict | bytes

        :rtype: DownloadRequest
        """
        return 'do some magic!'

    def add_url_rules(self):
        self._add_url_rule('/', DownloadsController.submit_download_request, methods=['POST'])
        self._add_url_rule('/<requestId>', DownloadsController.get_download_request, methods=['GET'])
        self._add_url_rule('/<requestId>/files', DownloadsController.get_download_files, methods=['GET'])
