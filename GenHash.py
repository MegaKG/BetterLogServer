#!/usr/bin/env python3
import hashlib
Input = input("> ")
print(hashlib.sha256(Input.encode()).hexdigest())
