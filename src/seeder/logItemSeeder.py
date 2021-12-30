from src.model import LogItem


def logItemSeeder():
    LogItem.insert(None, False)
    LogItem.insert(None, False)
    LogItem.insert(2, True)
    LogItem.insert(2, True)
    LogItem.insert(5, True)
    LogItem.insert(7, True)
    LogItem.insert(1, True)
