from fabric.api import sudo, hide

from result import ok

def install(target):
	if type(target) is str:
		__install(target)
	else:
		[__install(package) for package in target]


def __install(package):
	if __isNotInstalled(package):
		with hide('stdout'):
			sudo('yum install -y %s' % package)
		ok('echo %s' % __version(package))
	else:
		ok('echo %s is already installed' % package)


def __isNotInstalled(package):
	return 'not installed' in __version(package)


def __version(package):
	with hide('everything'):
		return sudo('rpm -q %s; true' % package)


def addEpel():
	__addRepository('epel', 'http://dl.fedoraproject.org/pub/epel/6/x86_64/epel-release-6-8.noarch.rpm')


def addRemi():
	__addRepository('remi', 'http://rpms.famillecollet.com/enterprise/remi-release-6.rpm')


def addRpmForge():
	__addRepository('rpmforge', 'http://pkgs.repoforge.org/rpmforge-release/rpmforge-release-0.5.3-1.el6.rf.x86_64.rpm')


def __addRepository(name, url):
	package = __repository(name)

	if __doesNotHasRepository(package):
		sudo('rpm -iv %s' % url)
		ok('echo install complete : %s' % __repository(name))
	else:
		ok('echo %s is already installed' % package)


def __doesNotHasRepository(package):
	return '' == package


def __repository(name):
	with hide('everything'):
		return sudo('rpm -qa | grep %s-release; true' % name)
