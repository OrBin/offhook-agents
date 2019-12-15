# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server import util


class SearchResult(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    def __init__(self, name=None, nevra_string=None):  # noqa: E501
        """SearchResult - a model defined in Swagger

        :param name: The name of this SearchResult.  # noqa: E501
        :type name: str
        :param nevra_string: The nevra_string of this SearchResult.  # noqa: E501
        :type nevra_string: str
        """
        self.swagger_types = {
            'name': str,
            'nevra_string': str
        }

        self.attribute_map = {
            'name': 'name',
            'nevra_string': 'nevraString'
        }

        self._name = name
        self._nevra_string = nevra_string

    @classmethod
    def from_dict(cls, dikt):
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The SearchResult of this SearchResult.  # noqa: E501
        :rtype: SearchResult
        """
        return util.deserialize_model(dikt, cls)

    @property
    def name(self):
        """Gets the name of this SearchResult.


        :return: The name of this SearchResult.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this SearchResult.


        :param name: The name of this SearchResult.
        :type name: str
        """
        if name is None:
            raise ValueError("Invalid value for `name`, must not be `None`")  # noqa: E501

        self._name = name

    @property
    def nevra_string(self):
        """Gets the nevra_string of this SearchResult.

        NEVRA (Name, Epoch, Version, Revision, Architecture) of the package  # noqa: E501

        :return: The nevra_string of this SearchResult.
        :rtype: str
        """
        return self._nevra_string

    @nevra_string.setter
    def nevra_string(self, nevra_string):
        """Sets the nevra_string of this SearchResult.

        NEVRA (Name, Epoch, Version, Revision, Architecture) of the package  # noqa: E501

        :param nevra_string: The nevra_string of this SearchResult.
        :type nevra_string: str
        """
        if nevra_string is None:
            raise ValueError("Invalid value for `nevra_string`, must not be `None`")  # noqa: E501

        self._nevra_string = nevra_string
