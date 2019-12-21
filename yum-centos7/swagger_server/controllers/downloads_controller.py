import os
import sched
import threading
import time
import uuid
import yum
from flask import request, jsonify, abort, send_file
from ..models.download_request import DownloadRequest
from .base_controller import BaseController
from .zip_helper import compress_files


class ProcessedRequest:
    def __init__(self, submitted_request):
        self.__request = submitted_request
        self.__output_file_path = None

    @property
    def request(self):
        return self.__request

    @property
    def output_file_path(self):
        return self.__output_file_path

    @output_file_path.setter
    def set_output_file_path(self, output_file_path):
        self.__output_file_path = output_file_path


class DownloadsController(BaseController):

    OUTPUT_FILE_TEMPLATE = '/opt/offhook/outputs/{request_id}.{compressed_file_type}'
    REQUEST_KEEPING_TIMEOUT_SEC = 60 * 60 * 2  # 2 hours

    def __init__(self, *args):
        super(DownloadsController, self).__init__(*args)
        self.__processed_requests = {}
        self.__scheduler = sched.scheduler(time.time, time.sleep)

    @staticmethod
    def _get_package_list(yum_base):
        dlpkgs = map(lambda x: x.po, filter(lambda txmbr:
                                            txmbr.ts_state in ("i", "u"),
                                            yum_base.tsInfo.getMembers()))
        return dlpkgs

    def _download_packages(self, patterns):
        yb = yum.YumBase()
        results = yb.pkgSack.returnNewestByName(patterns=patterns)

        yb.install(results[0])
        yb.resolveDeps()
        all_packages = self._get_package_list(yb)
        yb.downloadPkgs(all_packages)

        package_local_paths = [pkg.localpath for pkg in all_packages]
        return package_local_paths

    def _delete_request(self, request_id):
        processed_request = self.__processed_requests.pop(request_id, None)
        os.remove(processed_request.output_file_path)

    def _handle_request(self, request_id):
        req = self.__processed_requests[request_id].request
        req.status = 'Downloading'
        package_local_paths = self._download_packages(req.spec.packages)
        req.status = 'Compressing'

        self.__processed_requests[request_id].output_file_path = self.OUTPUT_FILE_TEMPLATE.format(
            request_id=request_id,
            compressed_file_type=req.compressed_file_type
        )

        compress_files(req.compressed_file_type,
                       package_local_paths,
                       self.__processed_requests[request_id].output_file_path,
                       password=None)

        req.status = 'Ready'
        req.is_consumable = True

        self.__scheduler.enter(self.REQUEST_KEEPING_TIMEOUT_SEC, 1, self._delete_request, (request_id,))
        self.__scheduler.run()


    def submit_download_request(self):  # noqa: E501
        """Submit a download request

         # noqa: E501

        :param body:
        :type body: dict | bytes

        :rtype: DownloadRequest
        """

        dl_req = DownloadRequest.from_dict(request.json)

        dl_req.is_consumable = False
        dl_req.status = 'Submitted'

        processed_req = ProcessedRequest(dl_req)
        req_id = uuid.uuid4().hex

        dl_req.id = req_id
        self.__processed_requests[req_id] = processed_req

        request_handling_thread = threading.Thread(target=self._handle_request, args=(req_id,))
        request_handling_thread.start()

        return jsonify(dl_req.to_dict())

    def get_download_request(self, request_id):  # noqa: E501
        """Get a download request

         # noqa: E501

        :param request_id: ID of request to return
        :type request_id: int

        :rtype: DownloadRequest
        """

        if request_id not in self.__processed_requests:
            abort(404)

        dl_req = self.__processed_requests[request_id].request
        return jsonify(dl_req.to_dict())

    def get_download_files(self, request_id):  # noqa: E501
        """Get files from a download request

         # noqa: E501

        :param request_id: ID of request to get the files for
        :type request_id: int

        :rtype: file
        """

        if request_id not in self.__processed_requests:
            abort(404)

        processed_req = self.__processed_requests[request_id]
        dl_req = processed_req.request

        if not dl_req.is_consumable:
            abort(400, 'Request is not yet consumable')

        attachment_filename = '{requested_pkgs}.{file_type}'.format(requested_pkgs='_'.join(dl_req.spec.packages),
                                                                    file_type=dl_req.compressed_file_type)

        return send_file(processed_req.output_file_path, as_attachment=True, attachment_filename=attachment_filename)

    def add_url_rules(self):
        self._add_url_rule('/', self.submit_download_request, methods=['POST'])
        self._add_url_rule('/<request_id>', self.get_download_request, methods=['GET'])
        self._add_url_rule('/<request_id>/files', self.get_download_files, methods=['GET'])
