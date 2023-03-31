import platform


def check_system_is_linux() -> bool:
    sys_name = platform.system()
    if sys_name == 'Linux':
        return True

    return False


def check_system_is_windows() -> bool:
    sys_name = platform.system()
    if sys_name == 'Windows':
        return True

    return False
