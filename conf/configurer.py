# coding = utf-8
# using namespace std
import json
from typing import AnyStr
import time


class ConfFile(object):
    """

    """
    source = AnyStr
    configurations = dict()
    got_data = False

    # constants formats
    all_formats_date = ("%Y-$M-%D", "$Y-%D-%M", "%M-%D-%Y", "%D-%Y-%M", "%D-%M-%Y")
    all_formats_time = ("%H:%M:%S", "$M:%H:%S", "%S:%M:%H")

    # general constants
    std_formatter = " | "

    class UnloadConfig(Exception):
        args = "The system can't do that action without the main configuration document!"

    class InvalidDateFormat(Exception):
        args = "That's not a valid date format!"

    class InvalidTimeFormat(Exception):
        args = "That's not a valid time format!"

    class InvalidFileType(Exception):
        args = "That's not a valid file for the configurations!"

    class InvalidCampValue(Exception):
        args = "That's not a valid camp param value!"

    @classmethod
    def check_file_ext(cls, file_name: AnyStr, auto_throw = False) -> bool:
        """

        :param file_name:
        :param auto_throw:
        :return:
        """
        sp = str(file_name).split(".")
        if sp[-1] != ".json":
            if auto_throw is True: raise cls.InvalidFileType()
            else: return False
        else: return True

    def __init__(self, conf_file = "./conf/config.json"):
        """

        :param conf_file:
        """
        if self.check_file_ext(conf_file, True):
            self.source = conf_file
            with open(self.source, "r") as configurations:
                self.configurations = json.loads(configurations)
            self.got_data = True

    @classmethod
    def check_format_exists_date(cls, format_to: str, auto_throw = True) -> bool:
        """

        :param format_to:
        :param auto_throw:
        :return:
        """
        if format_to not in cls.all_formats_date:
            if auto_throw is True: raise cls.InvalidDateFormat()
            else: return False
        else: return True

    @classmethod
    def check_format_exists_time(cls, format_to: str, auto_throw = True) -> bool:
        """

        :param format_to:
        :param auto_throw:
        :return:
        """
        if format_to not in cls.all_formats_time:
            if auto_throw is True: raise cls.InvalidTimeFormat()
            else: return False
        else: return False

    def get_time_formatted(self, date_format_str: str, time_format_str: str) -> str:
        """

        :param date_format_str:
        :param time_format_str:
        :return:
        """
        if self.check_format_exists_date(date_format_str, False) is False: raise self.InvalidDateFormat()
        elif self.got_data is False: raise self.UnloadConfig()
        elif self.check_format_exists_time(time_format_str, False) is False: raise self.InvalidTimeFormat()
        else:
            dt =  time.strftime(date_format_str)
            tm = time.strftime(time_format_str)
            return dt +self.std_formatter+ tm

    def get_date_time_from_conf(self) -> str:
        """

        :return:
        """
        return self.get_time_formatted(self.configurations['DateFormat'], self.configurations['TimeForm'])

    def update_config(self, new_value: str, camp: int):
        """

        :param new_value:
        :param camp:
        :return:
        """
        if camp == 0:
            # date format
            if self.check_format_exists_date(new_value, False) is False: raise self.InvalidDateFormat()
            else:
                self.configurations['DateFormat'] = new_value
                # updates the file config
        elif camp == 1:
            # time format
            if self.check_format_exists_time(new_value, False) is False: raise self.InvalidTimeFormat()
            else:
                self.configurations['TimeForm'] = new_value
                # updates the file config
        else: raise self.InvalidCampValue()

    @classmethod
    def update_file_config(cls):
        """

        :return:
        """
        with open(cls.source, "w") as config:
            dumped_data = json.dumps(cls.configurations)
            config.write(dumped_data)
            del dumped_data

    @classmethod
    def get_formats(cls) -> str:
        """

        :return:
        """
        return f"Date format: {cls.configurations['DateFomat']} \n Time Format: {cls.configurations['TimeForm']}"

















