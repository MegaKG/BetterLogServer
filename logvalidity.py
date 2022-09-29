#!/usr/bin/env python3
import re

LogExpr = rb"^<([0-9]|[0-9][0-9])>([a-z]|[A-Z]){3}( |  )([0-9]|[0-9][0-9]) [0-9][0-9]:[0-9][0-9]:[0-9][0-9] "

def check(Log):
    if re.match(LogExpr,Log,flags=re.M):
        return True
    return False