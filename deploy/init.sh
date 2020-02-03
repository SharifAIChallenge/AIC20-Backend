#!/bin/bash
set -e

su - postgres bash -c "
    createuser -E -w $user << '$pass';
    createdb $name -O $user;
    "
