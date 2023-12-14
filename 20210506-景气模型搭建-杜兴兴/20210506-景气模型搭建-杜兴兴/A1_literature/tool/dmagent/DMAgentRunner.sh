#!/bin/sh
PRG="$0"
PRGDIR=`dirname "$PRG"`
DIST_OS=`uname`

if [ -f "/etc/profile" ]
then
	. /etc/profile
fi

JAVA_EXE_FULL_PATH=""
if [ "x$JAVA_HOME" != "x" ]
then
	if [ -f "$JAVA_HOME/jre/bin/java" ] 
	then
		JAVA_EXE_FULL_PATH="$JAVA_HOME/jre/bin/java"
	fi
fi

if [ "x$JAVA_EXE_FULL_PATH" = "x" ]
then
	if [ "x$JRE_HOME" != "x" ]
	then
		JAVA_EXE_PART_PATH="bin/java"
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
DM_AGENT_LIB="${DM_AGENT_HOME}/lib"
CLIENT_CLASS=com.dameng.agent.DMAgentRunner

DM_EXT_DIRS="${DM_AGENT_LIB}"
if [ "$DIST_OS" = "AIX" ]
then
	JAVA_EXE_DIRS=`"${JAVA_EXE_FULL_PATH}" -cp "${DM_AGENT_LIB}/dmagent.jar" com.dameng.agent.share.PrintJavaExtDir`
	if [ "x$JAVA_EXE_DIRS" != "x" ]
	then
		DM_EXT_DIRS="${DM_EXT_DIRS}:${JAVA_EXE_DIRS}"
	fi
fi

if [ "x$1" = "x-noconsole" ]
then
	NO_CONSOLE_FLAG="-noconsole"
fi

"${JAVA_EXE_FULL_PATH}" -Xms40m -Xmx256m -Dorg.hyperic.sigar.path="${DM_AGENT_LIB}/sigar" -Djava.ext.dirs="${DM_EXT_DIRS}" -Ddameng.log.file="${DM_AGENT_HOME}/log4j.xml" -Ddm_agent.home="${DM_AGENT_HOME}" -Ddmagent.pid.file="${DM_AGENT_HOME}/wrapper/bin/dmagent.pid" -Dconfig.path="${DM_AGENT_HOME}/config.properties" ${CLIENT_CLASS} "$NO_CONSOLE_FLAG"



