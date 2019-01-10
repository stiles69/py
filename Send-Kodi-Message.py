#!/bin/env/python
#updated on 3/15/2016 by Harry to pass parameters for title and message
#meassage parameter should be the filename of the file just processed by Comskip
#also utilizing xbmcjson due to easier interface.
#
#
import sys
import time
from xbmcjson import XBMC, PLAYER_VIDEO
# constants start
semi_colon = ';'
colon = ':'
comma = ','
slash = "\x5C"
back_slash = "\x2F"
question_mark = "\x3F"
char1 = "\x5E"
char2 = "\x7B"
char3 = "\x7D"
char4 = "\x7E"
# char5 = "\x7F"
char6 = "\x5D"
char7 = "\x5B"
underscore = "_"
dot = "."
dash = "-"
space = " "
quoate = "\x22"
debug_it = False
# Settings
# The IP address for the XBMC instance you want to talk to
ip = 'localhost'
#ip = '192.168.11.59'
# The port number XBMC's web interface is listening on
port = '8080'
#port = '80'
# The username on XBMC's web interface (just comment or delete this line if you don't use authentication
#username = 'xbmc'
# Same as the username. No password for my system.
password = ''
#
json_name =  back_slash + "jsonrpc"
full_http = "http:" + back_slash + back_slash + ip + colon + port + json_name
xbmc = XBMC(full_http)
#
# Here you specify the method and parameters you want to pass to the XBMC JSON API
# For a LOT of info on the kinds of things you can do with the interface go here:
# http://wiki.xbmc.org/index.php?title=JSON-RPC_API/v6
# Here's an example of just sending an on-screen notification. This should help you understand the syntax
# method = 'GUI.ShowNotification'
# parameters = {"title":"Hello There!", "message":"This is a notification!", "displaytime":3000}
# This is what I am actually doing with this script, running the Artwork Downloader.
# Note: I am using the "silent" mode to avoid having a pop-up dialog box that would need to be closed.
# Also note: this stuff is very syntax-specific. Boolean and Int values must not be quoted. Strings must be doublequoted.
method = 'GUI.ShowNotification'
method2 = 'VideoLibrary.Clean'
method3 = 'VideoLibrary.Scan'
notify_method = method
libclean_method = method2
libscan_method = method3
# parameters = {'title': "Comskip completed for:",'message': "A recorded program"}
# above is original format. Trying in final version to pass a filename as a parameter
# below line is a test line with variable input
recorded_program = ""
# No Program Name Provided"
# constants start
slash = "\\"
underscore = "_"
dot = "."
iplist_file = 'IPList.txt'
# constants end
arguments = len(sys.argv)
#print ("Parameters received = ",arguments)
#argument [0] is the name of the Python program being executed.
#argument [1] is the parameter being passed to the Python program as the message
#argument [2] is the parameter being passed to the Python program as the title
title_text = "Comskip Completed."
if arguments >= 2 :
         title_text = sys.argv[1]
         if arguments >= 3:
                 recorded_program = sys.argv[2]
                 if arguments >= 4:
                          ip = sys.argv[3]
                          if arguments >= 3:
                                   port = sys.argv[4]
         json_name =  back_slash + "jsonrpc"
         full_http = "http:" + back_slash + back_slash + ip + colon + port + json_name
         xbmc = XBMC(full_http)
if arguments == 1 :
        recorded_program = sys.argv[0]
str1 = recorded_program
str2 = str1.rpartition(slash)[2]
str3 = str2.partition(dot)[0]
if debug_it:
         print "str1=",str1, "str2=",str2, "str3=",str3
str4 = str3.partition(underscore)
if debug_it:
         print "str4= ",str4
recorded_program = str4[0]
if debug_it:
         print "str4 =", str4, "recorded program = ",recorded_program
parameters = {'title': title_text,'message': recorded_program}

# This is a single, reusable method that makes a call to XBMC and gives you back the response

def sendJson(url_in,method,parameters):
        #
        results = 0
        temp_str = url_in
        xbmc = XBMC(temp_str)
        if method == notify_method:
                #xbmc.method(parameters)
                results = xbmc.GUI.ShowNotification(parameters)
                #title="Library Clean", message = "Initiated")
        else:
                if method == libscan_method:
                        if "win" in sys.platform:
                                if ip in url_in:
                                        results = xbmc.VideoLibrary.Scan(parameters)
                                else:
                                        results = xbmc.VideoLibrary.Scan()
                        else:
                                results = xbmc.VideoLibrary.Scan()
                else:
                        if method == libclean_method:
                                results = xbmc.VideoLibrary.Clean()
        if debug_it:
                print results
        return results['result']
#

# Here's an example of using the above method and variable values to make XBMC show a Notify
results =sendJson(full_http,method,parameters)
time.sleep(2)
# I just print the results out
print "results= ", results, " from ", full_http

