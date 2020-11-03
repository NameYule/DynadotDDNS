#!/usr/bin/env bash
RUN_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )";

CMD="\"$RUN_DIR/dynadot.py\" >> \"$RUN_DIR/run.log\""

echo "*/30 * * * *   root    $CMD" > /etc/cron.d/dynadot;
/etc/init.d/cron reload;
