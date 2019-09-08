# coding = utf-8
# using namespace std
import json
from typing import AnyStr
from datetime import date, datetime


class LogOnJson:
    """
    """
    source_file = AnyStr
    document = list()
    got_data = False
    empty_logs = bool

    class UnloadData(Exception):
        args = "The system can't do that action without a loaded log file!"

    class EmptyLogsError(Exception):
        args = "The system can't do that action without logs on the log file!"

    class LogNotFound(Exception):
        args = "That log can't be found on the system!"

    @classmethod
    def check_valid_file_type(cls, fl_name: AnyStr, auto_raise=True) -> bool:
        """

        :param fl_name:
        :param auto_raise:
        :return:
        """
        sep = str(fl_name).split(".")
        if sep[-1] != ".json":
            if auto_raise is True: raise cls.UnloadData()
            else: return False
        else: return True

    def __init__(self, source: AnyStr):
        if self.check_valid_file_type(source, True):
            self.source_file = source
            with open(self.source_file, "r+") as doc: self.document = json.loads(doc.read())
            self.got_data = True
            self.empty_logs = len(self.document) <= 0

    @classmethod
    def update_log_file(cls):
        """

        :return:
        """
        converted_logs = json.dumps(cls.document)
        with open(cls.source_file, "w") as logs: logs.write(converted_logs)
        del converted_logs




