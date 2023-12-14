@echo off

set DM_HOME=%~dp0..
set JAVA_HOME=%DM_HOME%/jdk
set TOOL_HOME=%DM_HOME%/tool

set DM_CLIENT_PLUGINS=%TOOL_HOME%/dropins/com.dameng/plugins
set DM_CLIENT_PLUGINS_THIRD=%DM_CLIENT_PLUGINS%/com.dameng.third
set DM_CLIENT_PLUGINS_JDBC=%DM_CLIENT_PLUGINS%/com.dameng.jdbc.drivers

set DTS_CMD_CLASSPATH=%DM_CLIENT_PLUGINS%/com.dameng.dts_8.0.0.jar
set DTS_CMD_CLASSPATH=%DTS_CMD_CLASSPATH%;%DM_CLIENT_PLUGINS%/com.dameng.common.log_8.0.0.jar
set DTS_CMD_CLASSPATH=%DTS_CMD_CLASSPATH%;%DM_CLIENT_PLUGINS%/com.dameng.common.i18n_8.0.0.jar
set DTS_CMD_CLASSPATH=%DTS_CMD_CLASSPATH%;%DM_CLIENT_PLUGINS%/com.dameng.common.persistence_8.0.0.jar
set DTS_CMD_CLASSPATH=%DTS_CMD_CLASSPATH%;%DM_CLIENT_PLUGINS%/com.dameng.common.util_8.0.0.jar
set DTS_CMD_CLASSPATH=%DTS_CMD_CLASSPATH%;%DM_CLIENT_PLUGINS%/com.dameng.tool_8.0.0.jar
set DTS_CMD_CLASSPATH=%DTS_CMD_CLASSPATH%;%DM_CLIENT_PLUGINS%/com.dameng.common.sql_8.0.0.jar
set DTS_CMD_CLASSPATH=%DTS_CMD_CLASSPATH%;%DM_CLIENT_PLUGINS%/com.dameng.common.excel_8.0.0.jar
set DTS_CMD_CLASSPATH=%DTS_CMD_CLASSPATH%;%DM_CLIENT_PLUGINS_THIRD%/dom4j-1.6.1.jar
set DTS_CMD_CLASSPATH=%DTS_CMD_CLASSPATH%;%DM_CLIENT_PLUGINS_THIRD%/bsh.jar
set DTS_CMD_CLASSPATH=%DTS_CMD_CLASSPATH%;%DM_CLIENT_PLUGINS_THIRD%/jxl.jar
set DTS_CMD_CLASSPATH=%DTS_CMD_CLASSPATH%;%DM_CLIENT_PLUGINS_THIRD%/poi-3.8-20120326.jar
set DTS_CMD_CLASSPATH=%DTS_CMD_CLASSPATH%;%DM_CLIENT_PLUGINS_THIRD%/poi-ooxml-3.8-20120326.jar
set DTS_CMD_CLASSPATH=%DTS_CMD_CLASSPATH%;%DM_CLIENT_PLUGINS_THIRD%/poi-ooxml-schemas-3.8-20120326.jar
set DTS_CMD_CLASSPATH=%DTS_CMD_CLASSPATH%;%DM_CLIENT_PLUGINS_THIRD%/poi-scratchpad-3.8-20120326.jar
set DTS_CMD_CLASSPATH=%DTS_CMD_CLASSPATH%;%DM_CLIENT_PLUGINS_THIRD%/xmlbeans-2.3.0.jar
set DTS_CMD_CLASSPATH=%DTS_CMD_CLASSPATH%;%DM_CLIENT_PLUGINS_THIRD%/jaxen-1.1-beta-6.jar
set DTS_CMD_CLASSPATH=%DTS_CMD_CLASSPATH%;%DM_CLIENT_PLUGINS_JDBC%/DmJdbcDriver.jar
set DTS_CMD_CLASSPATH=%DTS_CMD_CLASSPATH%;%TOOL_HOME%/plugins/org.apache.log4j_1.2.15.v201005080500.jar

set startime=%time%
"%JAVA_HOME%/bin/java" -Xverify:none -Xms1024m -Xmx1024m -DwriteExcelByXml=false -DreadExcelByXml=-1 -cp "%DTS_CMD_CLASSPATH%" -Djava.library.path="%DM_HOME%/bin" -Ddameng.log.file="%TOOL_HOME%/log4j.xml" com.dameng.dts.cmd.Command %*
set endtime=%time%
echo Total time: (%endtime% - %startime%) seconds
pause
