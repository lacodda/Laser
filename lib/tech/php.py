import configparser
import os
import shutil
import sys
import tarfile
import urllib.request

from config import *
from lib.helper import *
from lib.tech import Tech


class Php (Tech):
	techDescription = 'PHP Description'

	def __init__ (self, **kwargs):
		super (Php, self).__init__ (**kwargs)

		self.nginxConf['server']['location'] = {
			'/'               :
				{
					'try_files': '$uri $uri/ /index.php?$args'
				},
			'~ [^/]\.php(/|$)':
				{
					'fastcgi_index'       : 'index.php',
					'include'             : 'fcgi.conf',
					'fastcgi_pass'        : 'unix:' + self.socket,
					'fastcgi_param'       : 'SCRIPT_FILENAME $document_root$fastcgi_script_name',
					'fastcgi_read_timeout': '300',
				}
		}

		self.nginxConf['server']['index'] = 'index.html index.htm index.php'

		self.techConf = {
			'user'                     : 'vagrant',
			'group'                    : 'www-data',
			'listen'                   : self.socket,
			'listen.owner'             : 'www-data',
			'listen.group'             : 'www-data',
			'listen.mode'              : '0660',
			'pm'                       : 'dynamic',
			'pm.max_children'          : '5',
			'pm.start_servers'         : '1',
			'pm.min_spare_servers'     : '1',
			'pm.max_spare_servers'     : '5',
			# 'log_level'                : 'warning',
			# 'daemonize'                : 'yes',
			'request_terminate_timeout': '90s',
			'request_slowlog_timeout'  : '5s',
			'slowlog'                  : CreatePath (Config.serverRoot, self.serverName, Config.serverDirs['log'], 'php_slow.log'),
			'catch_workers_output'     : 'yes',
			'php_admin_value'          : {
				'open_basedir'              : 'none',
				'error_reporting'           : 'E_ALL & ~E_NOTICE & ~E_WARNING',
				'display_errors'            : 'On',
				'display_startup_errors'    : 'On',
				'log_errors'                : 'On',
				'error_log'                 : CreatePath (Config.serverRoot, self.serverName, Config.serverDirs['log'], 'php_error.log'),
				'short_open_tag'            : 'On',
				'max_execution_time'        : '0',
				'session.gc_maxlifetime'    : '100000',
				'mbstring.func_overload'    : '2',
				'mbstring.internal_encoding': 'UTF-8',
				'default_charset'           : 'UTF-8',
				'date.timezone'             : 'Europe/Samara',
				'max_input_vars'            : '10000',
				'post_max_size'             : '200M',
				'upload_max_filesize'       : '200M',
				'sendmail_path'             : '/usr/sbin/ssmtp -t',
				'session.use_cookies'       : '1',
				'session.use_only_cookies'  : '1',
				'opcache.revalidate_freq'   : '0',
			},
		}

	# [global]
	# pid = /var/run/php5-fpm.pid
	# error_log = /var/log/php5-fpm/error.log
	# log_level = warning
	# daemonize = yes
	# request_terminate_timeout = 90s
	# request_slowlog_timeout = 5s
	# slowlog = /var/log/php5-fpm/slow.$pool.log
	# chdir = /
	# catch_workers_output = yes
	# php_flag[display_errors] = off
	# php_admin_value[error_log] = /var/log/php5-fpm/error.$pool.log
	# php_admin_flag[log_errors] = on
	# include = /home/vagrant/.phpbrew/php/php-7.0.4/etc/php-fpm.d/*.conf


	# СТАНДАРТНЫЙ ВАРИАНТ

	# 	; Start a new pool named 'www'.
	# ; the variable $pool can we used in any directive and will be replaced by the
	# ; pool name ('www' here)
	# [www]
	#
	# ; Per pool prefix
	# ; It only applies on the following directives:
	# ; - 'access.log'
	# ; - 'slowlog'
	# ; - 'listen' (unixsocket)
	# ; - 'chroot'
	# ; - 'chdir'
	# ; - 'php_values'
	# ; - 'php_admin_values'
	# ; When not set, the global prefix (or /usr) applies instead.
	# ; Note: This directive can also be relative to the global prefix.
	# ; Default Value: none
	# ;prefix = /path/to/pools/$pool
	#
	# ; Unix user/group of processes
	# ; Note: The user is mandatory. If the group is not set, the default user's group
	# ;       will be used.
	# user = www-data
	# group = www-data
	#
	# ; The address on which to accept FastCGI requests.
	# ; Valid syntaxes are:
	# ;   'ip.add.re.ss:port'    - to listen on a TCP socket to a specific IPv4 address on
	# ;                            a specific port;
	# ;   '[ip:6:addr:ess]:port' - to listen on a TCP socket to a specific IPv6 address on
	# ;                            a specific port;
	# ;   'port'                 - to listen on a TCP socket to all IPv4 addresses on a
	# ;                            specific port;
	# ;   '[::]:port'            - to listen on a TCP socket to all addresses
	# ;                            (IPv6 and IPv4-mapped) on a specific port;
	# ;   '/path/to/unix/socket' - to listen on a unix socket.
	# ; Note: This value is mandatory.
	# listen = /var/run/php5-fpm.sock
	#
	# ; Set listen(2) backlog.
	# ; Default Value: 65535 (-1 on FreeBSD and OpenBSD)
	# ;listen.backlog = 65535
	#
	# ; Set permissions for unix socket, if one is used. In Linux, read/write
	# ; permissions must be set in order to allow connections from a web server. Many
	# ; BSD-derived systems allow connections regardless of permissions.
	# ; Default Values: user and group are set as the running user
	# ;                 mode is set to 0660
	# listen.owner = www-data
	# listen.group = www-data
	# listen.mode = 0666
	# ; When POSIX Access Control Lists are supported you can set them using
	# ; these options, value is a comma separated list of user/group names.
	# ; When set, listen.owner and listen.group are ignored
	# ;listen.acl_users =
	# ;listen.acl_groups =
	#
	# ; List of addresses (IPv4/IPv6) of FastCGI clients which are allowed to connect.
	# ; Equivalent to the FCGI_WEB_SERVER_ADDRS environment variable in the original
	# ; PHP FCGI (5.2.2+). Makes sense only with a tcp listening socket. Each address
	# ; must be separated by a comma. If this value is left blank, connections will be
	# ; accepted from any ip address.
	# ; Default Value: any
	# ;listen.allowed_clients = 127.0.0.1
	#
	# ; Specify the nice(2) priority to apply to the pool processes (only if set)
	# ; The value can vary from -19 (highest priority) to 20 (lower priority)
	# ; Note: - It will only work if the FPM master process is launched as root
	# ;       - The pool processes will inherit the master process priority
	# ;         unless it specified otherwise
	# ; Default Value: no set
	# ; process.priority = -19
	#
	# ; Choose how the process manager will control the number of child processes.
	# ; Possible Values:
	# ;   static  - a fixed number (pm.max_children) of child processes;
	# ;   dynamic - the number of child processes are set dynamically based on the
	# ;             following directives. With this process management, there will be
	# ;             always at least 1 children.
	# ;             pm.max_children      - the maximum number of children that can
	# ;                                    be alive at the same time.
	# ;             pm.start_servers     - the number of children created on startup.
	# ;             pm.min_spare_servers - the minimum number of children in 'idle'
	# ;                                    state (waiting to process). If the number
	# ;                                    of 'idle' processes is less than this
	# ;                                    number then some children will be created.
	# ;             pm.max_spare_servers - the maximum number of children in 'idle'
	# ;                                    state (waiting to process). If the number
	# ;                                    of 'idle' processes is greater than this
	# ;                                    number then some children will be killed.
	# ;  ondemand - no children are created at startup. Children will be forked when
	# ;             new requests will connect. The following parameter are used:
	# ;             pm.max_children           - the maximum number of children that
	# ;                                         can be alive at the same time.
	# ;             pm.process_idle_timeout   - The number of seconds after which
	# ;                                         an idle process will be killed.
	# ; Note: This value is mandatory.
	# pm = dynamic
	#
	# ; The number of child processes to be created when pm is set to 'static' and the
	# ; maximum number of child processes when pm is set to 'dynamic' or 'ondemand'.
	# ; This value sets the limit on the number of simultaneous requests that will be
	# ; served. Equivalent to the ApacheMaxClients directive with mpm_prefork.
	# 	; Equivalent to the PHP_FCGI_CHILDREN environment variable in the original PHP
	# ; CGI. The below defaults are based on a server without much resources. Don't
	# ; forget to tweak pm.* to fit your needs.
	# ; Note: Used when pm is set to 'static', 'dynamic' or 'ondemand'
	# ; Note: This value is mandatory.
	# pm.max_children = 5
	#
	# ; The number of child processes created on startup.
	# ; Note: Used only when pm is set to 'dynamic'
	# ; Default Value: min_spare_servers + (max_spare_servers - min_spare_servers) / 2
	# pm.start_servers = 2
	#
	# ; The desired minimum number of idle server processes.
	# ; Note: Used only when pm is set to 'dynamic'
	# ; Note: Mandatory when pm is set to 'dynamic'
	# pm.min_spare_servers = 1
	#
	# ; The desired maximum number of idle server processes.
	# ; Note: Used only when pm is set to 'dynamic'
	# ; Note: Mandatory when pm is set to 'dynamic'
	# pm.max_spare_servers = 3
	#
	# ; The number of seconds after which an idle process will be killed.
	# ; Note: Used only when pm is set to 'ondemand'
	# ; Default Value: 10s
	# ;pm.process_idle_timeout = 10s;
	#
	# ; The number of requests each child process should execute before respawning.
	# ; This can be useful to work around memory leaks in 3rd party libraries. For
	# ; endless request processing specify '0'. Equivalent to PHP_FCGI_MAX_REQUESTS.
	# ; Default Value: 0
	# ;pm.max_requests = 500
	#
	# ; The URI to view the FPM status page. If this value is not set, no URI will be
	# ; recognized as a status page. It shows the following informations:
	# ;   pool                 - the name of the pool;
	# ;   process manager      - static, dynamic or ondemand;
	# ;   start time           - the date and time FPM has started;
	# ;   start since          - number of seconds since FPM has started;
	# ;   accepted conn        - the number of request accepted by the pool;
	# ;   listen queue         - the number of request in the queue of pending
	# ;                          connections (see backlog in listen(2));
	# ;   max listen queue     - the maximum number of requests in the queue
	# ;                          of pending connections since FPM has started;
	# ;   listen queue len     - the size of the socket queue of pending connections;
	# ;   idle processes       - the number of idle processes;
	# ;   active processes     - the number of active processes;
	# ;   total processes      - the number of idle + active processes;
	# ;   max active processes - the maximum number of active processes since FPM
	# ;                          has started;
	# ;   max children reached - number of times, the process limit has been reached,
	# ;                          when pm tries to start more children (works only for
	# ;                          pm 'dynamic' and 'ondemand');
	# ; Value are updated in real time.
	# ; Example output:
	# ;   pool:                 www
	# ;   process manager:      static
	# ;   start time:           01/Jul/2011:17:53:49 +0200
	# ;   start since:          62636
	# ;   accepted conn:        190460
	# ;   listen queue:         0
	# ;   max listen queue:     1
	# ;   listen queue len:     42
	# ;   idle processes:       4
	# ;   active processes:     11
	# ;   total processes:      15
	# ;   max active processes: 12
	# ;   max children reached: 0
	# ;
	# ; By default the status page output is formatted as text/plain. Passing either
	# ; 'html', 'xml' or 'json' in the query string will return the corresponding
	# ; output syntax. Example:
	# ;   http://www.foo.bar/status
	# ;   http://www.foo.bar/status?json
	# ;   http://www.foo.bar/status?html
	# ;   http://www.foo.bar/status?xml
	# ;
	# ; By default the status page only outputs short status. Passing 'full' in the
	# ; query string will also return status for each pool process.
	# ; Example:
	# ;   http://www.foo.bar/status?full
	# ;   http://www.foo.bar/status?json&full
	# ;   http://www.foo.bar/status?html&full
	# ;   http://www.foo.bar/status?xml&full
	# ; The Full status returns for each process:
	# 	;   pid                  - the PID of the process;
	# ;   state                - the state of the process (Idle, Running, ...);
	# ;   start time           - the date and time the process has started;
	# ;   start since          - the number of seconds since the process has started;
	# ;   requests             - the number of requests the process has served;
	# ;   request duration     - the duration in µs of the requests;
	# ;   request method       - the request method (GET, POST, ...);
	# ;   request URI          - the request URI with the query string;
	# ;   content length       - the content length of the request (only with POST);
	# ;   user                 - the user (PHP_AUTH_USER) (or '-' if not set);
	# ;   script               - the main script called (or '-' if not set);
	# ;   last request cpu     - the %cpu the last request consumed
	# ;                          it's always 0 if the process is not in Idle state
	# ;                          because CPU calculation is done when the request
	# ;                          processing has terminated;
	# ;   last request memory  - the max amount of memory the last request consumed
	# ;                          it's always 0 if the process is not in Idle state
	# ;                          because memory calculation is done when the request
	# ;                          processing has terminated;
	# ; If the process is in Idle state, then informations are related to the
	# ; last request the process has served. Otherwise informations are related to
	# ; the current request being served.
	# ; Example output:
	# ;   ************************
	# ;   pid:                  31330
	# ;   state:                Running
	# ;   start time:           01/Jul/2011:17:53:49 +0200
	# ;   start since:          63087
	# ;   requests:             12808
	# ;   request duration:     1250261
	# ;   request method:       GET
	# ;   request URI:          /test_mem.php?N=10000
	# ;   content length:       0
	# ;   user:                 -
	# ;   script:               /home/fat/web/docs/php/test_mem.php
	# ;   last request cpu:     0.00
	# ;   last request memory:  0
	# ;
	# ; Note: There is a real-time FPM status monitoring sample web page available
	# ;       It's available in: /usr/share/php5/fpm/status.html
	# ;
	# ; Note: The value must start with a leading slash (/). The value can be
	# ;       anything, but it may not be a good idea to use the .php extension or it
	# ;       may conflict with a real PHP file.
	# ; Default Value: not set
	# ;pm.status_path = /status
	#
	# ; The ping URI to call the monitoring page of FPM. If this value is not set, no
	# ; URI will be recognized as a ping page. This could be used to test from outside
	# ; that FPM is alive and responding, or to
	# ; - create a graph of FPM availability (rrd or such);
	# ; - remove a server from a group if it is not responding (load balancing);
	# ; - trigger alerts for the operating team (24/7).
	# ; Note: The value must start with a leading slash (/). The value can be
	# ;       anything, but it may not be a good idea to use the .php extension or it
	# ;       may conflict with a real PHP file.
	# ; Default Value: not set
	# ;ping.path = /ping
	#
	# ; This directive may be used to customize the response of a ping request. The
	# ; response is formatted as text/plain with a 200 response code.
	# ; Default Value: pong
	# ;ping.response = pong
	#
	# ; The access log file
	# ; Default: not set
	# ;access.log = log/$pool.access.log
	#
	# ; The access log format.
	# ; The following syntax is allowed
	# ;  %%: the '%' character
	# ;  %C: %CPU used by the request
	# ;      it can accept the following format:
	# ;      - %{user}C for user CPU only
	# ;      - %{system}C for system CPU only
	# ;      - %{total}C  for user + system CPU (default)
	# 	;  %d: time taken to serve the request
	# ;      it can accept the following format:
	# ;      - %{seconds}d (default)
	# ;      - %{miliseconds}d
	# ;      - %{mili}d
	# ;      - %{microseconds}d
	# ;      - %{micro}d
	# ;  %e: an environment variable (same as $_ENV or $_SERVER)
	# ;      it must be associated with embraces to specify the name of the env
	# ;      variable. Some exemples:
	# ;      - server specifics like: %{REQUEST_METHOD}e or %{SERVER_PROTOCOL}e
	# ;      - HTTP headers like: %{HTTP_HOST}e or %{HTTP_USER_AGENT}e
	# ;  %f: script filename
	# ;  %l: content-length of the request (for POST request only)
	# ;  %m: request method
	# ;  %M: peak of memory allocated by PHP
	# ;      it can accept the following format:
	# ;      - %{bytes}M (default)
	# ;      - %{kilobytes}M
	# ;      - %{kilo}M
	# ;      - %{megabytes}M
	# ;      - %{mega}M
	# ;  %n: pool name
	# ;  %o: output header
	# ;      it must be associated with embraces to specify the name of the header:
	# 	;      - %{Content-Type}o
	# ;      - %{X-Powered-By}o
	# ;      - %{Transfert-Encoding}o
	# ;      - ....
	# ;  %p: PID of the child that serviced the request
	# ;  %P: PID of the parent of the child that serviced the request
	# ;  %q: the query string
	# ;  %Q: the '?' character if query string exists
	# ;  %r: the request URI (without the query string, see %q and %Q)
	# ;  %R: remote IP address
	# ;  %s: status (response code)
	# ;  %t: server time the request was received
	# ;      it can accept a strftime(3) format:
	# ;      %d/%b/%Y:%H:%M:%S %z (default)
	# ;  %T: time the log has been written (the request has finished)
	# ;      it can accept a strftime(3) format:
	# ;      %d/%b/%Y:%H:%M:%S %z (default)
	# ;  %u: remote user
	# ;
	# ; Default: "%R - %u %t \"%m %r\" %s"
	# ;access.format = "%R - %u %t \"%m %r%Q%q\" %s %f %{mili}d %{kilo}M %C%%"
	#
	# ; The log file for slow requests
	# 	; Default Value: not set
	# ; Note: slowlog is mandatory if request_slowlog_timeout is set
	# ;slowlog = log/$pool.log.slow
	#
	# ; The timeout for serving a single request after which a PHP backtrace will be
	# ; dumped to the 'slowlog' file. A value of '0s' means 'off'.
	# ; Available units: s(econds)(default), m(inutes), h(ours), or d(ays)
	# ; Default Value: 0
	# ;request_slowlog_timeout = 0
	#
	# ; The timeout for serving a single request after which the worker process will
	# ; be killed. This option should be used when the 'max_execution_time' ini option
	# ; does not stop script execution for some reason. A value of '0' means 'off'.
	# ; Available units: s(econds)(default), m(inutes), h(ours), or d(ays)
	# ; Default Value: 0
	# ;request_terminate_timeout = 0
	#
	# ; Set open file descriptor rlimit.
	# ; Default Value: system defined value
	# ;rlimit_files = 1024
	#
	# ; Set max core size rlimit.
	# ; Possible Values: 'unlimited' or an integer greater or equal to 0
	# ; Default Value: system defined value
	# ;rlimit_core = 0
	#
	# ; Chroot to this directory at the start. This value must be defined as an
	# ; absolute path. When this value is not set, chroot is not used.
	# ; Note: you can prefix with '$prefix' to chroot to the pool prefix or one
	# ; of its subdirectories. If the pool prefix is not set, the global prefix
	# ; will be used instead.
	# ; Note: chrooting is a great security feature and should be used whenever
	# ;       possible. However, all PHP paths will be relative to the chroot
	# ;       (error_log, sessions.save_path, ...).
	# ; Default Value: not set
	# ;chroot =
	#
	# ; Chdir to this directory at the start.
	# ; Note: relative path can be used.
	# ; Default Value: current directory or / when chroot
	# chdir = /
	#
	# ; Redirect worker stdout and stderr into main error log. If not set, stdout and
	# ; stderr will be redirected to /dev/null according to FastCGI specs.
	# ; Note: on highloaded environement, this can cause some delay in the page
	# ; process time (several ms).
	# ; Default Value: no
	# ;catch_workers_output = yes
	#
	# ; Clear environment in FPM workers
	# ; Prevents arbitrary environment variables from reaching FPM worker processes
	# ; by clearing the environment in workers before env vars specified in this
	# ; pool configuration are added.
	# ; Setting to "no" will make all environment variables available to PHP code
	# ; via getenv(), $_ENV and $_SERVER.
	# ; Default Value: yes
	# ;clear_env = no
	#
	# ; Limits the extensions of the main script FPM will allow to parse. This can
	# ; prevent configuration mistakes on the web server side. You should only limit
	# ; FPM to .php extensions to prevent malicious users to use other extensions to
	# ; exectute php code.
	# ; Note: set an empty value to allow all extensions.
	# ; Default Value: .php
	# ;security.limit_extensions = .php .php3 .php4 .php5
	#
	# ; Pass environment variables like LD_LIBRARY_PATH. All $VARIABLEs are taken from
	# ; the current environment.
	# ; Default Value: clean env
	# ;env[HOSTNAME] = $HOSTNAME
	# ;env[PATH] = /usr/local/bin:/usr/bin:/bin
	# ;env[TMP] = /tmp
	# ;env[TMPDIR] = /tmp
	# ;env[TEMP] = /tmp
	#
	# ; Additional php.ini defines, specific to this pool of workers. These settings
	# ; overwrite the values previously defined in the php.ini. The directives are the
	# ; same as the PHP SAPI:
	# ;   php_value/php_flag             - you can set classic ini defines which can
	# ;                                    be overwritten from PHP call 'ini_set'.
	# ;   php_admin_value/php_admin_flag - these directives won't be overwritten by
	# ;                                     PHP call 'ini_set'
	# ; For php_*flag, valid values are on, off, 1, 0, true, false, yes or no.
	#
	# ; Defining 'extension' will load the corresponding shared extension from
	# ; extension_dir. Defining 'disable_functions' or 'disable_classes' will not
	# ; overwrite previously defined php.ini values, but will append the new value
	# ; instead.
	#
	# ; Note: path INI options can be relative and will be expanded with the prefix
	# ; (pool, global or /usr)
	#
	# ; Default Value: nothing is defined by default except the values in php.ini and
	# ;                specified at startup with the -d argument
	# ;php_admin_value[sendmail_path] = /usr/sbin/sendmail -t -i -f www@my.domain.com
	# ;php_flag[display_errors] = off
	# ;php_admin_value[error_log] = /var/log/fpm-php.www.log
	# ;php_admin_flag[log_errors] = on
	# ;php_admin_value[memory_limit] = 32M
	# include = /home/vagrant/.phpbrew/php/php-5.6.23/etc/php-fpm.d/*.conf




	# СТАНДАРТНЫЙ ВАРИАНТ 5.5.33



	# ;;;;;;;;;;;;;;;;;;;;;
	# ; FPM Configuration ;
	# ;;;;;;;;;;;;;;;;;;;;;
	#
	# ; All relative paths in this configuration file are relative to PHP's install
	# ; prefix (/home/vagrant/.phpbrew/php/php-5.5.33). This prefix can be dynamically changed by using the
	# ; '-p' argument from the command line.
	#
	# ; Include one or more files. If glob(3) exists, it is used to include a bunch of
	# ; files from a glob(3) pattern. This directive can be used everywhere in the
	# ; file.
	# ; Relative path can also be used. They will be prefixed by:
	# ;  - the global prefix if it's been set (-p argument)
	# ;  - /home/vagrant/.phpbrew/php/php-5.5.33 otherwise
	# ;include=etc/fpm.d/*.conf
	#
	# ;;;;;;;;;;;;;;;;;;
	# ; Global Options ;
	# ;;;;;;;;;;;;;;;;;;
	#
	# [global]
	# ; Pid file
	# ; Note: the default prefix is /home/vagrant/.phpbrew/php/php-5.5.33/var
	# ; Default Value: none
	# ;pid = run/php-fpm.pid
	#
	# ; Error log file
	# ; If it's set to "syslog", log is sent to syslogd instead of being written
	# ; in a local file.
	# ; Note: the default prefix is /home/vagrant/.phpbrew/php/php-5.5.33/var
	# ; Default Value: log/php-fpm.log
	# ;error_log = log/php-fpm.log
	#
	# ; syslog_facility is used to specify what type of program is logging the
	# ; message. This lets syslogd specify that messages from different facilities
	# ; will be handled differently.
	# ; See syslog(3) for possible values (ex daemon equiv LOG_DAEMON)
	# ; Default Value: daemon
	# ;syslog.facility = daemon
	#
	# ; syslog_ident is prepended to every message. If you have multiple FPM
	# ; instances running on the same server, you can change the default value
	# ; which must suit common needs.
	# ; Default Value: php-fpm
	# ;syslog.ident = php-fpm
	#
	# ; Log level
	# ; Possible Values: alert, error, warning, notice, debug
	# ; Default Value: notice
	# ;log_level = notice
	#
	# ; If this number of child processes exit with SIGSEGV or SIGBUS within the time
	# ; interval set by emergency_restart_interval then FPM will restart. A value
	# ; of '0' means 'Off'.
	# ; Default Value: 0
	# ;emergency_restart_threshold = 0
	#
	# ; Interval of time used by emergency_restart_interval to determine when
	# ; a graceful restart will be initiated.  This can be useful to work around
	# ; accidental corruptions in an accelerator's shared memory.
	# ; Available Units: s(econds), m(inutes), h(ours), or d(ays)
	# ; Default Unit: seconds
	# ; Default Value: 0
	# ;emergency_restart_interval = 0
	#
	# ; Time limit for child processes to wait for a reaction on signals from master.
	# ; Available units: s(econds), m(inutes), h(ours), or d(ays)
	# ; Default Unit: seconds
	# ; Default Value: 0
	# ;process_control_timeout = 0
	#
	# ; The maximum number of processes FPM will fork. This has been design to control
	# ; the global number of processes when using dynamic PM within a lot of pools.
	# ; Use it with caution.
	# 	; Note: A value of 0 indicates no limit
	# ; Default Value: 0
	# ; process.max = 128
	#
	# ; Specify the nice(2) priority to apply to the master process (only if set)
	# ; The value can vary from -19 (highest priority) to 20 (lower priority)
	# ; Note: - It will only work if the FPM master process is launched as root
	# ;       - The pool process will inherit the master process priority
	# ;         unless it specified otherwise
	# ; Default Value: no set
	# ; process.priority = -19
	#
	# ; Send FPM to background. Set to 'no' to keep FPM in foreground for debugging.
	# 	; Default Value: yes
	# ;daemonize = yes
	#
	# ; Set open file descriptor rlimit for the master process.
	# ; Default Value: system defined value
	# ;rlimit_files = 1024
	#
	# ; Set max core size rlimit for the master process.
	# ; Possible Values: 'unlimited' or an integer greater or equal to 0
	# ; Default Value: system defined value
	# ;rlimit_core = 0
	#
	# ; Specify the event mechanism FPM will use. The following is available:
	# ; - select     (any POSIX os)
	# ; - poll       (any POSIX os)
	# ; - epoll      (linux >= 2.5.44)
	# ; - kqueue     (FreeBSD >= 4.1, OpenBSD >= 2.9, NetBSD >= 2.0)
	# ; - /dev/poll  (Solaris >= 7)
	# ; - port       (Solaris >= 10)
	# ; Default Value: not set (auto detection)
	# ;events.mechanism = epoll
	#
	# ; When FPM is build with systemd integration, specify the interval,
	# ; in second, between health report notification to systemd.
	# ; Set to 0 to disable.
	# ; Available Units: s(econds), m(inutes), h(ours)
	# ; Default Unit: seconds
	# ; Default value: 10
	# ;systemd_interval = 10
	#
	# ;;;;;;;;;;;;;;;;;;;;
	# ; Pool Definitions ;
	# ;;;;;;;;;;;;;;;;;;;;
	#
	# ; Multiple pools of child processes may be started with different listening
	# ; ports and different management options.  The name of the pool will be
	# ; used in logs and stats. There is no limitation on the number of pools which
	# ; FPM can handle. Your system will tell you anyway :)
	#
	# ; Start a new pool named 'www'.
	# ; the variable $pool can we used in any directive and will be replaced by the \
	# ; pool name ('www' here)
	# [www] \
	#
	# ; Per pool prefix \
	# ; It only applies on the following directives:
	# ; - 'access.log' \
	# ; - 'slowlog' \
	# ; - 'listen' (unixsocket) \
	# ; - 'chroot' \
	# ; - 'chdir' \
	# ; - 'php_values' \
	# ; - 'php_admin_values' \
	# ; When not set, the global prefix (or /home/vagrant/.phpbrew/php/php-5.5.33) applies instead.
	# ; Note: This directive can also be relative to the global prefix.
	# ; Default Value: none \
	# ;prefix = /path/to/pools/$pool \
	#
	# ; Unix user/group of processes \
	# ; Note: The user is mandatory. If the group is not set, the default user's group \
	# ;       will be used.
	# user = nobody
	# group = nobody \
	#
	# ; The address on which to accept FastCGI requests.
	# ; Valid syntaxes are:
	# ;   'ip.add.re.ss:port'    - to listen on a TCP socket to a specific IPv4 address on \
	# ;                            a specific port;
	# ;   '[ip:6:addr:ess]:port' - to listen on a TCP socket to a specific IPv6 address on \
	# ;                            a specific port;
	# ;   'port'                 - to listen on a TCP socket to all IPv4 addresses on a \
	# ;                            specific port;
	# ;   '[::]:port'            - to listen on a TCP socket to all addresses \
	# ;                            (IPv6 and IPv4-mapped) on a specific port;
	# ;   '/path/to/unix/socket' - to listen on a unix socket.
	# ; Note: This value is mandatory.
	# listen = 127.0.0.1:9000 \
	#
	# ; Set listen(2) backlog.
	# ; Default Value: 65535 (-1 on FreeBSD and OpenBSD)
	# ;listen.backlog = 65535 \
	#
	# ; Set permissions for unix socket, if one is used. In Linux, read/write
	# ; permissions must be set in order to allow connections from a web server. Many
	# ; BSD-derived systems allow connections regardless of permissions.
	# ; Default Values: user and group are set as the running user \
	# ;                 mode is set to 0660 \
	# ;listen.owner = nobody \
	# ;listen.group = nobody \
	# ;listen.mode = 0660 \
	#
	# ; List of addresses (IPv4/IPv6) of FastCGI clients which are allowed to connect.
	# ; Equivalent to the FCGI_WEB_SERVER_ADDRS environment variable in the original \
	# ; PHP FCGI (5.2.2+). Makes sense only with a tcp listening socket. Each address
	# ; must be separated by a comma. If this value is left blank, connections will be
	# ; accepted from any ip address.
	# ; Default Value: any
	# ;listen.allowed_clients = 127.0.0.1 \
	#
	# ; Specify the nice(2) priority to apply to the pool processes (only if set)
	# ; The value can vary from -19 (highest priority) to 20 (lower priority)
	# ; Note: - It will only work if the FPM master process is launched as root \
	# ;       - The pool processes will inherit the master process priority \
	# ;         unless it specified otherwise \
	# ; Default Value: no set \
	# ; process.priority = -19 \
	#
	# ; Choose how the process manager will control the number of child processes.
	# ; Possible Values:
	# ;   static  - a fixed number (pm.max_children) of child processes;
	# ;   dynamic - the number of child processes are set dynamically based on the \
	# ;             following directives. With this process management, there will be \
	# ;             always at least 1 children.
	# ;             pm.max_children      - the maximum number of children that can \
	# ;                                    be alive at the same time.
	# ;             pm.start_servers     - the number of children created on startup.
	# ;             pm.min_spare_servers - the minimum number of children in 'idle' \
	# ;                                    state (waiting to process). If the number \
	# ;                                    of 'idle' processes is less than this \
	# ;                                    number then some children will be created.
	# ;             pm.max_spare_servers - the maximum number of children in 'idle' \
	# ;                                    state (waiting to process). If the number \
	# ;                                    of 'idle' processes is greater than this \
	# ;                                    number then some children will be killed.
	# ;  ondemand - no children are created at startup. Children will be forked when \
	# ;             new requests will connect. The following parameter are used:
	# ;             pm.max_children           - the maximum number of children that \
	# ;                                         can be alive at the same time.
	# ;             pm.process_idle_timeout   - The number of seconds after which \
	# ;                                         an idle process will be killed.
	# ; Note: This value is mandatory. \
	# pm = dynamic \
	#
	# ; The number of child processes to be created when pm is set to 'static' and the \
	# ; maximum number of child processes when pm is set to 'dynamic' or 'ondemand'.
	# ; This value sets the limit on the number of simultaneous requests that will be \
	# ; served. Equivalent to the ApacheMaxClients directive with mpm_prefork.
	# ; Equivalent to the PHP_FCGI_CHILDREN environment variable in the original PHP
	# ; CGI. The below defaults are based on a server without much resources. Don't
	# ; forget to tweak pm.* to fit your needs.
	# ; Note: Used when pm is set to 'static', 'dynamic' or 'ondemand' \
	# ; Note: This value is mandatory. \
	# 	pm.max_children = 5 \
	#
	# ; The number of child processes created on startup.
	# ; Note: Used only when pm is set to 'dynamic' \
	# ; Default Value: min_spare_servers + (max_spare_servers - min_spare_servers) / 2
	# pm.start_servers = 2 \
	#
	# ; The desired minimum number of idle server processes.
	# ; Note: Used only when pm is set to 'dynamic' \
	# ; Note: Mandatory when pm is set to 'dynamic'
	# pm.min_spare_servers = 1 \
	#
	# ; The desired maximum number of idle server processes.
	# ; Note: Used only when pm is set to 'dynamic' \
	# ; Note: Mandatory when pm is set to 'dynamic'
	# pm.max_spare_servers = 3 \
	#
	# ; The number of seconds after which an idle process will be killed.
	# ; Note: Used only when pm is set to 'ondemand' \
	# ; Default Value: 10s \
	# ;pm.process_idle_timeout = 10s;
	#
	# ; The number of requests each child process should execute before respawning.
	# ; This can be useful to work around memory leaks in 3rd party libraries. For \
	# ; endless request processing specify '0'. Equivalent to PHP_FCGI_MAX_REQUESTS.
	# ; Default Value: 0 \
	# ;pm.max_requests = 500 \
	#
	# ; The URI to view the FPM status page. If this value is not set, no URI will be \
	# ; recognized as a status page. It shows the following informations:
	# ;   pool                 - the name of the pool;
	# ;   process manager      - static, dynamic or ondemand;
	# ;   start time           - the date and time FPM has started;
	# ;   start since          - number of seconds since FPM has started;
	# ;   accepted conn        - the number of request accepted by the pool;
	# ;   listen queue         - the number of request in the queue of pending \
	# ;                          connections (see backlog in listen(2));
	# ;   max listen queue     - the maximum number of requests in the queue \
	# ;                          of pending connections since FPM has started;
	# ;   listen queue len     - the size of the socket queue of pending connections;
	# ;   idle processes       - the number of idle processes;
	# ;   active processes     - the number of active processes;
	# ;   total processes      - the number of idle + active processes;
	# ;   max active processes - the maximum number of active processes since FPM \
	# ;                          has started;
	# ;   max children reached - number of times, the process limit has been reached, \
	# ;                          when pm tries to start more children (works only for
	# 	;                          pm 'dynamic' and 'ondemand');
	# ; Value are updated in real time.
	# ; Example output:
	# ;   pool:                 www \
	# ;   process manager:      static \
	# ;   start time:           01/Jul/2011:17:53:49 +0200 \
	# ;   start since:          62636 \
	# ;   accepted conn:        190460 \
	# ;   listen queue:         0 \
	# ;   max listen queue:     1 \
	# ;   listen queue len:     42 \
	# ;   idle processes:       4 \
	# ;   active processes:     11 \
	# ;   total processes:      15 \
	# ;   max active processes: 12 \
	# ;   max children reached: 0 \
	# ;
	# ; By default the status page output is formatted as text/plain. Passing either \
	# ; 'html', 'xml' or 'json' in the query string will return the corresponding
	# ; output syntax. Example:
	# ;   http://www.foo.bar/status
	# ;   http://www.foo.bar/status?json
	# ;   http://www.foo.bar/status?html
	# ;   http://www.foo.bar/status?xml
	# ;
	# ; By default the status page only outputs short status. Passing 'full' in the
	# ; query string will also return status for each pool process.
	# ; Example:
	# ;   http://www.foo.bar/status?full
	# ;   http://www.foo.bar/status?json&full
	# ;   http://www.foo.bar/status?html&full
	# ;   http://www.foo.bar/status?xml&full
	# ; The Full status returns for each process:
	# 	;   pid                  - the PID of the process;
	# ;   state                - the state of the process (Idle, Running, ...);
	# ;   start time           - the date and time the process has started;
	# ;   start since          - the number of seconds since the process has started;
	# ;   requests             - the number of requests the process has served;
	# ;   request duration     - the duration in µs of the requests;
	# ;   request method       - the request method (GET, POST, ...);
	# ;   request URI          - the request URI with the query string;
	# ;   content length       - the content length of the request (only with POST);
	# ;   user                 - the user (PHP_AUTH_USER) (or '-' if not set);
	# ;   script               - the main script called (or '-' if not set);
	# ;   last request cpu     - the %cpu the last request consumed
	# ;                          it's always 0 if the process is not in Idle state
	# ;                          because CPU calculation is done when the request
	# ;                          processing has terminated;
	# ;   last request memory  - the max amount of memory the last request consumed
	# ;                          it's always 0 if the process is not in Idle state
	# ;                          because memory calculation is done when the request
	# ;                          processing has terminated;
	# ; If the process is in Idle state, then informations are related to the
	# ; last request the process has served. Otherwise informations are related to
	# ; the current request being served.
	# ; Example output:
	# ;   ************************
	# ;   pid:                  31330
	# ;   state:                Running
	# ;   start time:           01/Jul/2011:17:53:49 +0200
	# ;   start since:          63087
	# ;   requests:             12808
	# ;   request duration:     1250261
	# ;   request method:       GET
	# ;   request URI:          /test_mem.php?N=10000
	# ;   content length:       0
	# ;   user:                 -
	# ;   script:               /home/fat/web/docs/php/test_mem.php
	# ;   last request cpu:     0.00
	# ;   last request memory:  0
	# ;
	# ; Note: There is a real-time FPM status monitoring sample web page available
	# ;       It's available in: /home/vagrant/.phpbrew/php/php-5.5.33/share/php/fpm/status.html
	# ;
	# ; Note: The value must start with a leading slash (/). The value can be
	# ;       anything, but it may not be a good idea to use the .php extension or it
	# ;       may conflict with a real PHP file.
	# ; Default Value: not set
	# ;pm.status_path = /status
	#
	# ; The ping URI to call the monitoring page of FPM. If this value is not set, no
	# ; URI will be recognized as a ping page. This could be used to test from outside
	# ; that FPM is alive and responding, or to
	# ; - create a graph of FPM availability (rrd or such);
	# ; - remove a server from a group if it is not responding (load balancing);
	# ; - trigger alerts for the operating team (24/7).
	# ; Note: The value must start with a leading slash (/). The value can be
	# ;       anything, but it may not be a good idea to use the .php extension or it
	# ;       may conflict with a real PHP file.
	# ; Default Value: not set
	# ;ping.path = /ping
	#
	# ; This directive may be used to customize the response of a ping request. The
	# ; response is formatted as text/plain with a 200 response code.
	# ; Default Value: pong
	# ;ping.response = pong
	#
	# ; The access log file
	# ; Default: not set
	# ;access.log = log/$pool.access.log
	#
	# ; The access log format.
	# ; The following syntax is allowed
	# ;  %%: the '%' character
	# ;  %C: %CPU used by the request
	# ;      it can accept the following format:
	# ;      - %{user}C for user CPU only
	# ;      - %{system}C for system CPU only
	# ;      - %{total}C  for user + system CPU (default)
	# 	;  %d: time taken to serve the request
	# ;      it can accept the following format:
	# ;      - %{seconds}d (default)
	# ;      - %{miliseconds}d
	# ;      - %{mili}d
	# ;      - %{microseconds}d
	# ;      - %{micro}d
	# ;  %e: an environment variable (same as $_ENV or $_SERVER)
	# ;      it must be associated with embraces to specify the name of the env
	# ;      variable. Some exemples:
	# ;      - server specifics like: %{REQUEST_METHOD}e or %{SERVER_PROTOCOL}e
	# ;      - HTTP headers like: %{HTTP_HOST}e or %{HTTP_USER_AGENT}e
	# ;  %f: script filename
	# ;  %l: content-length of the request (for POST request only)
	# ;  %m: request method
	# ;  %M: peak of memory allocated by PHP
	# ;      it can accept the following format:
	# ;      - %{bytes}M (default)
	# ;      - %{kilobytes}M
	# ;      - %{kilo}M
	# ;      - %{megabytes}M
	# ;      - %{mega}M
	# ;  %n: pool name
	# ;  %o: output header
	# ;      it must be associated with embraces to specify the name of the header:
	# 	;      - %{Content-Type}o
	# ;      - %{X-Powered-By}o
	# ;      - %{Transfert-Encoding}o
	# ;      - ....
	# ;  %p: PID of the child that serviced the request
	# ;  %P: PID of the parent of the child that serviced the request
	# ;  %q: the query string
	# ;  %Q: the '?' character if query string exists
	# ;  %r: the request URI (without the query string, see %q and %Q)
	# ;  %R: remote IP address
	# ;  %s: status (response code)
	# ;  %t: server time the request was received
	# ;      it can accept a strftime(3) format:
	# ;      %d/%b/%Y:%H:%M:%S %z (default)
	# ;  %T: time the log has been written (the request has finished)
	# ;      it can accept a strftime(3) format:
	# ;      %d/%b/%Y:%H:%M:%S %z (default)
	# ;  %u: remote user
	# ;
	# ; Default: "%R - %u %t \"%m %r\" %s"
	# ;access.format = "%R - %u %t \"%m %r%Q%q\" %s %f %{mili}d %{kilo}M %C%%"
	#
	# ; The log file for slow requests
	# 	; Default Value: not set
	# ; Note: slowlog is mandatory if request_slowlog_timeout is set
	# ;slowlog = log/$pool.log.slow
	#
	# ; The timeout for serving a single request after which a PHP backtrace will be
	# ; dumped to the 'slowlog' file. A value of '0s' means 'off'.
	# ; Available units: s(econds)(default), m(inutes), h(ours), or d(ays)
	# ; Default Value: 0
	# ;request_slowlog_timeout = 0
	#
	# ; The timeout for serving a single request after which the worker process will
	# ; be killed. This option should be used when the 'max_execution_time' ini option
	# ; does not stop script execution for some reason. A value of '0' means 'off'.
	# ; Available units: s(econds)(default), m(inutes), h(ours), or d(ays)
	# ; Default Value: 0
	# ;request_terminate_timeout = 0
	#
	# ; Set open file descriptor rlimit.
	# ; Default Value: system defined value
	# ;rlimit_files = 1024
	#
	# ; Set max core size rlimit.
	# ; Possible Values: 'unlimited' or an integer greater or equal to 0
	# ; Default Value: system defined value
	# ;rlimit_core = 0
	#
	# ; Chroot to this directory at the start. This value must be defined as an
	# ; absolute path. When this value is not set, chroot is not used.
	# ; Note: you can prefix with '$prefix' to chroot to the pool prefix or one
	# ; of its subdirectories. If the pool prefix is not set, the global prefix
	# ; will be used instead.
	# ; Note: chrooting is a great security feature and should be used whenever
	# ;       possible. However, all PHP paths will be relative to the chroot
	# ;       (error_log, sessions.save_path, ...).
	# ; Default Value: not set
	# ;chroot =
	#
	# ; Chdir to this directory at the start.
	# ; Note: relative path can be used.
	# ; Default Value: current directory or / when chroot
	# ;chdir = /var/www
	#
	# ; Redirect worker stdout and stderr into main error log. If not set, stdout and
	# ; stderr will be redirected to /dev/null according to FastCGI specs.
	# ; Note: on highloaded environement, this can cause some delay in the page
	# ; process time (several ms).
	# ; Default Value: no
	# ;catch_workers_output = yes
	#
	# ; Clear environment in FPM workers
	# ; Prevents arbitrary environment variables from reaching FPM worker processes
	# ; by clearing the environment in workers before env vars specified in this
	# ; pool configuration are added.
	# ; Setting to "no" will make all environment variables available to PHP code
	# ; via getenv(), $_ENV and $_SERVER.
	# ; Default Value: yes
	# ;clear_env = no
	#
	# ; Limits the extensions of the main script FPM will allow to parse. This can
	# ; prevent configuration mistakes on the web server side. You should only limit
	# ; FPM to .php extensions to prevent malicious users to use other extensions to
	# ; exectute php code.
	# ; Note: set an empty value to allow all extensions.
	# ; Default Value: .php
	# ;security.limit_extensions = .php .php3 .php4 .php5
	#
	# ; Pass environment variables like LD_LIBRARY_PATH. All $VARIABLEs are taken from
	# ; the current environment.
	# ; Default Value: clean env
	# ;env[HOSTNAME] = $HOSTNAME
	# ;env[PATH] = /usr/local/bin:/usr/bin:/bin
	# ;env[TMP] = /tmp
	# ;env[TMPDIR] = /tmp
	# ;env[TEMP] = /tmp
	#
	# ; Additional php.ini defines, specific to this pool of workers. These settings
	# ; overwrite the values previously defined in the php.ini. The directives are the
	# ; same as the PHP SAPI:
	# ;   php_value/php_flag             - you can set classic ini defines which can
	# ;                                    be overwritten from PHP call 'ini_set'.
	# ;   php_admin_value/php_admin_flag - these directives won't be overwritten by
	# ;                                     PHP call 'ini_set'
	# ; For php_*flag, valid values are on, off, 1, 0, true, false, yes or no.
	#
	# ; Defining 'extension' will load the corresponding shared extension from
	# ; extension_dir. Defining 'disable_functions' or 'disable_classes' will not
	# ; overwrite previously defined php.ini values, but will append the new value
	# ; instead.
	#
	# ; Note: path INI options can be relative and will be expanded with the prefix
	# ; (pool, global or /home/vagrant/.phpbrew/php/php-5.5.33)
	#
	# ; Default Value: nothing is defined by default except the values in php.ini and
	# ;                specified at startup with the -d argument
	# ;php_admin_value[sendmail_path] = /usr/sbin/sendmail -t -i -f www@my.domain.com
	# ;php_flag[display_errors] = off
	# ;php_admin_value[error_log] = /var/log/fpm-php.www.log
	# ;php_admin_flag[log_errors] = on
	# ;php_admin_value[memory_limit] = 32M


	def configCreate (self):
		if not os.path.exists (Config.phpBrew['confDir']):
			os.makedirs (Config.phpBrew['confDir'])
		permissions = Permissions ('nobody')
		permissions.checkAndAddGroup ()
		config = configparser.RawConfigParser ()
		sectionName = self.kwargs['serverName'].replace ('.', '-') + '-laser-0'
		config.add_section (sectionName)
		for confKey, confValue in self.kwargs['techConf'].items ():
			if isinstance (confValue, dict):
				for key, value in confValue.items ():
					config.set (sectionName, '{}[{}]'.format (confKey, key), value)
			else:
				config.set (sectionName, confKey, confValue)

		confFile = CreatePath (Config.phpBrew['confDir'], self.kwargs['serverName'].replace ('.', '-') + '.conf')

		with open (confFile, 'w') as configfile:
			config.write (configfile)

	def configRemove (self):
		if not os.path.exists (Config.phpBrew['confDir']):
			os.makedirs (Config.phpBrew['confDir'])
		# TODO: костыль нужно по-возможности заменить
		for file in os.listdir (Config.phpBrew['confDir']):
			os.remove (CreatePath (Config.phpBrew['confDir'], file))

	def start (self):
		# TODO: КОСТЫЛЬ НУЖНО ИСПРАВИТЬ
		os.system ("sudo pkill -f fpm")
		# TODO: заменить более правильным решением
		os.system (Config.phpBrew['fpm'])

	def stop (self):
		# TODO: заменить более правильным решением
		os.system ("sudo pkill -f fpm")

	def checkComposer (self):
		try:
			path = shutil.which ("composer")
			if path:
				return True
			else:
				return self.installComposer ()
		except:
			print ('Ошибка выполнения проверки установки Composer!')
			return False

	def installComposer (self):
		try:
			tempDir = '/tmp'
			destinationDir = '/usr/local/bin'
			url = 'https://getcomposer.org/composer.phar'
			destinationFile = CreatePath (destinationDir, 'composer.phar')
			tempFile = CreatePath (tempDir, 'composer.phar')
			os.chdir (destinationDir)
			urllib.request.urlretrieve (url, tempFile)
			os.system ('sudo mv {} {}'.format (tempFile, destinationFile))
			os.system ('sudo chmod -R 0755 {}'.format (destinationFile))
			os.system ('sudo ln -s composer.phar composer')
			print ('Новая версия Composer успешно установлена!')
			return True
		except:
			print ('Ошибка установки Composer!')
			return False