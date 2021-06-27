#!/usr/bin/env bash
RUN_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )";

CMD="\"$RUN_DIR/dynadot.py\" >> \"$RUN_DIR/run.log\""

echo "0 0 /2 * * ? root    $CMD" > /etc/cron.d/dynadot;
/etc/init.d/cron reload;
