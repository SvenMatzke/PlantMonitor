"""
For the purpose of logging and that we might not be able to connect we will log the last 10-30 dataspots

"""
import os
import json
import time
import btree

# btree muss alls binär haben mit config daten ist das kein problem

_data_file_path = "plant_monitor_data"


def get_last_dataset():
    raise

def get_datasets():
    """
    Returns the dataset from the logging file
    :rtype: dict
    """
    if not os.path.exists(_data_file_path):
        return []


    if os.path.exists(_log_file_path):
        return json.load(_log_file_path)
    return []


def _cleanup_data(btree_db):
    raise

def save_dataset(data_set):
    """

    :param data_set:
    :return:
    """
    old_data = get_logged_data()
    old_data.append(data_set)
    json.dumps(old_data)