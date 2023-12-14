@echo off
setlocal
set "PRGDIR=%~dp0"
cd /d "%PRGDIR%"

set "JAVA_EXE_FULL_PATH="
set "DMAGENT_JAVA_PATH_CONF="
if not "%JAVA_HOME%" == "" (
	if exist "%JAVA_HOME%\jre\bin\java.exe" (
		set "JAVA_EXE_FULL_PATH=%JAVA_HOME%\jre\bin\java.exe"
		set "DMAGENT_JAVA_PATH_CONF=%%JAVA_HOME%%\jre\bin\java.exe"
	)
)

if "%JAVA_EXE_FULL_PATH%" == "" (
	if not "%JRE_HOME%" == "" (
		set "JAVA_EXE_FULL_PATH=%JRE_HOME%\bin\java.exe"
		set "DMAGENT_JAVA_PATH_CONF=%%JRE_HOME%%\bin\java.exe"
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
		echo %JAVA_EXE_FULL_PATH% file is not exist!
		goto :eof
	)
)

set "DM_AGENT_HOME=%cd%"
set "DM_AGENT_COMMAND=%1"

echo set.DMAGENT_JAVA_PATH=%DMAGENT_JAVA_PATH_CONF% > "%DM_AGENT_HOME%\wrapper\conf\dmagent-java.conf"

if "%DM_AGENT_COMMAND%" == "start" (
	goto execAgentCommang
) else if "%DM_AGENT_COMMAND%" == "stop" (
	goto execAgentCommang
) else if "%DM_AGENT_COMMAND%" == "restart" (
	goto execAgentCommang
) else if "%DM_AGENT_COMMAND%" == "install" (
	goto execAgentCommang
) else if "%DM_AGENT_COMMAND%" == "remove" (
	goto execAgentCommang
) else if "%DM_AGENT_COMMAND%" == "status" (
	goto execAgentCommang
) else (
	 echo Usage: %0 [ start : stop : restart : install : remove : status ]
	 goto :eof
)



:execAgentCommang
	"%DM_AGENT_HOME%\wrapper\bin\AppCommand.bat" %DM_AGENT_COMMAND%
	goto :eof