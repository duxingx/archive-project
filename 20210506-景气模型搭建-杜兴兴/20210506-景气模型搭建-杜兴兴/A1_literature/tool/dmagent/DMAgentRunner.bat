@echo off
setlocal
set "PRGDIR=%~dp0"
cd /d "%PRGDIR%"

set "JAVA_EXE_FULL_PATH="
if not "%JAVA_HOME%" == "" (
	if exist "%JAVA_HOME%\jre\bin\java.exe" (
		set "JAVA_EXE_FULL_PATH=%JAVA_HOME%\jre\bin\java.exe"
	)
)

if "%JAVA_EXE_FULL_PATH%" == "" (
	if not "%JRE_HOME%" == "" (
		set "JAVA_EXE_FULL_PATH=%JRE_HOME%\bin\java.exe"
	)
)

if "%JAVA_EXE_FULL_PATH%" == "" (
	java -version > nul 2>&1
	if "%ERRORLEVEL%" == "0" (
		set "JAVA_EXE_FULL_PATH=java"
	) else (
		echo please set JRE_HOME or JAVA_HOME environment variable, or add "java" to PATH environment variable.
		goto :eof
	)
) else (
	if not exist "%JAVA_EXE_FULL_PATH%" (
		echo "%JAVA_EXE_FULL_PATH% file is not exist!"
		goto :eof
	)
)

set "DM_AGENT_HOME=%cd%"
set "DM_AGENT_LIB=%DM_AGENT_HOME%\lib"
set CLIENT_CLASS=com.dameng.agent.DMAgentRunner

start "DMAGENT" "%JAVA_EXE_FULL_PATH%" -Xms40m -Xmx256m -Dorg.hyperic.sigar.path="%DM_AGENT_LIB%\sigar" -Djava.ext.dirs="%DM_AGENT_LIB%"  -Ddameng.log.file="%DM_AGENT_HOME%\log4j.xml" -Ddm_agent.home="%DM_AGENT_HOME%" -Dconfig.path="%DM_AGENT_HOME%\config.properties" %CLIENT_CLASS%

goto :eof



