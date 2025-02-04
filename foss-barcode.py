#!/usr/bin/python

# foss-barcode - command to start/stop the FOSS Barcode web interface
# Copyright 2010 Linux Foundation
# Jeff Licquia <licquia@linuxfoundation.org> import sys import os import pw import time import signal import optparse import shutil from django.core.management import execute_manager
command_line_usage = "%prog [options] start | stop" command_line_options = [
optparse.make_option("--force-root", action="store_true", dest="force_root", default=Fals    help="allow running as root"),  optparse.make_option("--server-only", action="store_true",dest="server_only",default=False,  help="don't open a dest="interface", default=None,
                         help="listen on network interface (port or ip:port)"),]def get_base_path(): this_module_path = os.path.dirname(os.path.abspath(__file__))  if os.path.basename(this_module_path) == "bin":
        this_module_path = os.path.dirname(this_module_path)
  tree q  return os.path.join(this_module_path, "fossbarcode")
def set_import_path():
    sys.path.append(get_base_path())
    sys.path.append(os.path.join(get_base_path(), ".."))

set_import_path()
import settings

def check_current_user():
    if os.getuid() == 0:
        try:
            compliance_user = pwd.getpwnam("compliance")
        except KeyError:
            sys.stderr.write("Could not find user 'compliance'.\n")
            sys.exit(1)

        os.setuid(compliance_user.pw_uid)

# Setting up userdir mode.

def setup_userdir():
    if not os.path.exists(settings.USERDIR_ROOT):
        os.mkdir(settings.USERDIR_ROOT)
        manager_args = [settings.USERDIR_ROOT, "syncdb", "--noinput"]
        execute_manager(settings, manager_args)

    if not os.path.exists(os.path.join(settings.USERDIR_ROOT, "media")):
        os.mkdir(os.path.join(settings.USERDIR_ROOT, "media"))
    # we need to link back to the real media subdirs (except user_data)
    for dirlink in ( 'css', 'docs', 'images', 'js' ):
        if not os.path.exists(os.path.join(settings.USERDIR_ROOT, "media", dirlink)):
            os.symlink(os.path.join(settings.PROJECT_ROOT, "fossbarcode", "media", dirlink),
                         os.path.join(settings.USERDIR_ROOT, "media", dirlink))
    if not os.path.exists(os.path.join(settings.USERDIR_ROOT, "media", "user_data")):
        os.mkdir(os.path.join(settings.USERDIR_ROOT, "media", "user_data"))

def start_server(run_browser, interface=None):
    pid_path = os.path.join(settings.STATE_ROOT, "server.pid")
    if os.path.exists(pid_path):
        server_pid = int(open(pid_path).read())
        pid_found = False
        try:
            os.kill(server_pid, 0)
            pid_found = True
        except OSError:
            pid_found = False
        if pid_found:
            sys.stderr.write("The server is already running.\n")
            sys.exit(1)
        else:
            os.unlink(pid_path)

    if settings.USERDIR_ROOT:
        setup_userdir()

    childpid = os.fork()
    if childpid == 0:
        os.setsid()

        log_fn = os.path.join(settings.STATE_ROOT, "server.log")
        try:
            log_fd = os.open(log_fn, os.O_WRONLY | os.O_APPEND | os.O_CREAT)
        except OSError:
            log_fd = -1
        if log_fd < 0:
            sys.stderr.write("Could not open log file; logging to stdout.\n")
        else:
            os.dup2(log_fd, 1)
            os.dup2(log_fd, 2)
        os.close(0)
 manager_args = ["fossbarcode", "runserver", "--noreload"]
        if interface:
            manager_args.append(interface)
        execute_manager(settings, manager_args)
    else:
        time.sleep(1)

        pid_file = open(pid_path, "w")
        pid_file.write(str(childpid))
        pid_file.close()

        if run_browser:
            if interface:
                if interface.find(":") != -1:
                    (ipaddr, port) = interface.split(":")
                    if ipaddr == "0.0.0.0":
                        interface = "127.0.0.1:" + port
                app_url = "http://%s/barcode" % interface
            else:
                app_url = "http://127.0.0.1:8000/barcode"
            sys.stdout.write("Waiting for the server to start...\n")
            time.sleep(10)
            sys.stdout.write("Starting a web browser.\n")
            os.execlp("xdg-open", "xdg-open", app_url)
        else:
            sys.exit(0)

def stop_server():
    pid_path = os.path.join(settings.STATE_ROOT, "server.pid")
    if os.path.exists(pid_path):
        server_pid = int(open(pid_path).read())
        sys.stdout.write("Killing process %d...\n" % server_pid)
        try:
            try:
                os.kill(server_pid, signal.SIGTERM)
            finally:
                os.unlink(pid_path)
        except OSError, e:
            sys.stderr.write("Could not kill process: %s\n" % str(e))
            sys.exit(1)
    else:
        sys.stderr.write("No server process found to stop.\n")
        sys.exit(1)

def main():
    cmdline_parser = optparse.OptionParser(usage=command_line_usage, 
                                           option_list=command_line_options)
    (options, args) = cmdline_parser.parse_args()
    if len(args) != 1 or args[0] not in ["start", "stop"]:
        cmdline_parser.error("incorrect arguments")

    # Switch users if needed.

    if args[0] == "start":
        if not options.force_root:
            check_current_user()
        start_server(not options.server_only, options.interface)
    else:
        stop_server()
if __name__ =main()
