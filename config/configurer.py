# coding = utf-8
# using namespace std
import json
from typing import AnyStr
from datetime import date, datetime


class ConfigFile(object):
    """

    """
    source = "./config/configurations.json"
    document_config = dict()
    got_config = False
    date_models = ("Y%M%D", "M%D%Y", "D%M%Y")
    time_models = ("H%M", "H%M%S", "M%H", "M%H%S")

    class UnloadedConfigurations(Exception):
        args = "The system can't do that action without the main document!"

    class InvalidDateTimeModel(Exception):
        args = "That is not a valid datetime model!"

    class InvalidDocument(Exception):
        args = "That is not a valid document!"

    @classmethod
    def check_document_conf(cls, doc, from_file = False, auto_raise = False) -> bool:
        """

        :param doc:
        :param from_file:
        :param auto_raise:
        :return:
        """
        if from_file is True:
            with open(doc, "r") as config:
                tmp = json.loads(config.read())
                for i in tmp.keys():
                    if i not in ("DateConf", "TimeConf", "LastConf"):
                        if auto_raise is True: raise cls.InvalidDocument()
                        else: return False
                    else: pass
                return True
        else:
            for i in doc.keys():
                if i not in ("DateConf", "TimeConf", "LastConf"):
                    if auto_raise is True:
                        raise cls.InvalidDocument()
                    else:
                        return False
                else:
                    pass
            return True

    def __init__(self, config_file = "./config/configurations.json"):
        """

        :param config_file:
        """
        if self.check_document_conf(config_file, True, True):


