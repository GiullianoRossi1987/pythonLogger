# coding = utf-8
# using namespace std
from json import dumps, loads
from conf.configurer import ConfFile
from typing import AnyStr


class LoadJsonLog(object):
    """

    """
    #        Envvars
    source_file = AnyStr
    logs = list()
    got_data = False
    configuration_obj = ConfFile()
    std_formatter = ("  " * 4)  # 4 spaces format, ident guide basic

    #        Exceptions
    class InvalidFileExtension(Exception):
        args = "That's not a valid file extension, expecting .json file, try the text mode log"

    class UnloadMainLogs(Exception):
        args = "The system can't do that action without the main logs of the system!"

    class InvalidFailureNumber(Exception):
        args = "That's not a valid fails number"

    #        Methods

    @classmethod
    def check_file_ext(cls, file_path: AnyStr, auto_raise: bool = False) -> bool:
        """

        :param file_path:
        :param auto_raise:
        :return:
        """
        sp = str(file_path).split(".")
        if sp[-1] != "json":
            if auto_raise is True: raise cls.InvalidFileExtension()
            else: return False
        else: return True

    def __init__(self, log_file: AnyStr):
        """

        :param log_file:
        """
        if self.check_file_ext(log_file, True) is True:
            self.source_file = log_file
            with open(self.source_file, "r") as logs:
                self.logs = loads(logs.read())
            self.got_data = True

    @classmethod
    def update_log_file(cls):
        """

        :return:
        """
        if cls.got_data is False: raise cls.UnloadMainLogs()
        with open(cls.source_file, "w") as logs_source:
            dumped_data = dumps(cls.logs)
            logs_source.write(dumped_data)

    @classmethod
    def clear_all_logs(cls):
        """

        :return:
        """
        cls.logs = []
        cls.update_log_file()

    def add_log(self, action: AnyStr, failures: int, failure_code: str, auto_commit = False):
        """

        :param action:
        :param failures:
        :param failure_code:
        :param auto_commit:
        :return:
        """
        log_new = {}
        datetime = self.configuration_obj.get_date_time_from_conf()
        log_new['Time'] = datetime
        log_new['Action'] = action
        if failures < 0: raise self.InvalidFailureNumber()
        log_new['Failures'] = failures
        log_new['FailureCode'] = failure_code
        self.logs.append(log_new)
        del log_new
        if auto_commit is True: self.update_log_file()

    def query_logs_action(self, action: str) -> list:
        """

        :param action:
        :return:
        """
        results = []
        for log in self.logs:
            if action in log['Action']: results.append(results)
        return results

    def query_logs_failure(self, failed = False) -> list:
        """

        :param failed:
        :return:
        """
        results = []
        if failed is True:
            for log in self.logs:
                if log['Failures'] > 0: results.append(log)
        else:
            for log in self.logs:
                if log['Failures'] == 0: results.append(log)
        return results

    def query_logs_failure_code(self, code: str) -> list:
        """

        :param code:
        :return:
        """
        results = []
        for log in self.logs:
            if log['FailureCode'] == code: results.append(log)
        return results

    def query_logs_date(self, date: str) -> list:
        """

        :param date:
        :return:
        """
        results = []
        for log in self.logs:
            separed = str(log['Time']).split(self.configuration_obj.std_formatter)
            if separed[0] == date: results.append(log)
        return results

    def query_logs_time(self, time: str) -> list:
        """

        :param time:
        :return:
        """
        results = []
        for log in self.logs:
            sep = str(log['Time']).split(self.configuration_obj.std_formatter)
            if sep[1] == time: results.append(log)
        return results



