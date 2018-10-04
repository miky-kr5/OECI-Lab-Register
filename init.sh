#! /bin/bash
### BEGIN INIT INFO
# Provides: weblabsd
# Required-Start: $network $mysql
# Required-Stop: $network $mysql
# Default-Start: 2 3 4 5
# Default-Stop: 0 1 6
# Short-Description: Laboratory inscription daemon.
### END INIT INFO

start() {
    PID=`pidof weblabsd`
    if [ $? -eq 0 ]
    then
	echo "weblabsd already started."
	return
    else
	echo "Starting weblabsd."
	cd /home/miky/Documentos/repos/Weblabs.py
	weblabsd &
	echo "Done."
    fi
}

stop() {
    PID=`pidof weblabsd`
    if [ $? -eq 0 ]
    then
	echo "Stopping weblabsd."
        kill -9 -- -`pidof weblabsd`
        echo "Done."
    else
	echo "weblabsd already stopped."
    fi
}

case "$1" in
    start)
        start
        ;;
    stop)
        stop
        ;;
    status)
	PID=`pidof weblabsd`
	if [ $? -eq 0 ]
	then
	    echo "weblabsd is running."
	else
	    echo "weblabsd is down."
	fi
        ;;
    restart)
        stop
        start
        ;;
    *)
        echo "Usage:  {start|stop|restart|status}"
        exit 1
        ;;
esac
exit $?
