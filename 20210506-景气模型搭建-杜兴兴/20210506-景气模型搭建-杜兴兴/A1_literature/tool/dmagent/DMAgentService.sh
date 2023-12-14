#!/bin/sh
PRG="$0"
PRGDIR=`dirname "$PRG"`

if [ -f "/etc/profile" ]
then
	. /etc/profile
fi

JAVA_EXE_FULL_PATH=""
if [ "x$JAVA_HOME" != "x" ]
then
	if [ -d "$JAVA_HOME/jre" -a -f "$JAVA_HOME/jre/bin/java" ] 
	then
		JAVA_EXE_FULL_PATH="$JAVA_HOME/jre/bin/java"
	fi
fi

if [ "x$JAVA_EXE_FULL_PATH" = "x" ]
then
	if [ "x$JRE_HOME" != "x" ]
	then
		JAVA_EXE_PART_PATH="bin/java"
		#os name
		DIST_OS=`uname`
		if [ "$DIST_OS" = "SunOS" -o "$DIST_OS" = "Solaris" ]
		then
			BITS_NUM=`isainfo -b`
			if [ "x$BITS_NUM" = "x64" ]
			then
				JAVA_EXE_PART_PATH="bin/sparcv9/java"
			fi
		fi
		JAVA_EXE_FULL_PATH="$JRE_HOME/$JAVA_EXE_PART_PATH"
	fi
fi

if [ "x$JAVA_EXE_FULL_PATH" = "x" ]
then
	java -version > /dev/null 2>&1
	RETURN_CODE=`echo $?`
	if [ "$RETURN_CODE" != 0 ]
	then
		echo "please set JRE_HOME or JAVA_HOME environment variable, or add \"java\" to PATH environment variable."
		exit 1
	else
		JAVA_EXE_FULL_PATH="java"
	fi
else
	if [ ! -f "$JAVA_EXE_FULL_PATH" ]
	then
		echo "$JAVA_EXE_FULL_PATH file is not exist!"
		exit 1
	fi

	if [ ! -x "$JAVA_EXE_FULL_PATH" ]
	then
		chmod +x "$JAVA_EXE_FULL_PATH"
	fi
fi

cd "$PRGDIR"
DM_AGENT_HOME=`pwd`
DM_AGENT_COMMAND=$1

if [ ! -x "$DM_AGENT_HOME/wrapper/bin/sh.script" ]
then
	chmod +x "$DM_AGENT_HOME/wrapper/bin/sh.script"
fi

if [ ! -x "$DM_AGENT_HOME/DMAgentRunner.sh" ]
then
	chmod +x "$DM_AGENT_HOME/DMAgentRunner.sh"
fi

if [ "$DM_AGENT_COMMAND" = "start" -o "$DM_AGENT_COMMAND" = "stop" -o "$DM_AGENT_COMMAND" = "install" -o "$DM_AGENT_COMMAND" = "remove" -o "$DM_AGENT_COMMAND" = "restart" -o "$DM_AGENT_COMMAND" = "status" ]
then
	"$DM_AGENT_HOME/wrapper/bin/sh.script" $DM_AGENT_COMMAND
else
	echo "Usage: $0 [ start | stop | restart | status | install | remove ]"
fi
