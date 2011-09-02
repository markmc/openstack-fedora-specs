
%global milestone d4
%global git_revno 1078
%global snapdate 20110823
%global snaptag ~%{milestone}~%{snapdate}.%{git_revno}

Name:           openstack-keystone
Version:        1.0
Release:        0.2.%{milestone}.%{git_revno}%{?dist}
Summary:        OpenStack Identity Service

License:        ASL 2.0
URL:            http://keystone.openstack.org/
Source0:        http://keystone.openstack.org/tarballs/keystone-%{version}%{snaptag}.tar.gz
Source1:        openstack-keystone.logrotate

Patch1:         keystone-move-tools-tracer.patch
Patch2:         keystone-logging-watched-file-handler.patch

BuildArch:      noarch
BuildRequires:  python2-devel
BuildRequires:  python-sphinx >= 1.0

Requires:       python-eventlet
Requires:       python-httplib2
Requires:       python-ldap
Requires:       python-lxml
Requires:       python-memcached
Requires:       python-paste
Requires:       python-paste-deploy
Requires:       python-paste-script
Requires:       python-routes
Requires:       python-sqlalchemy
Requires:       python-sqlite2
Requires:       python-webob

Requires(pre):  shadow-utils

%description
Keystone is a proposed independent authentication service for
OpenStack (http://www.openstack.org).

This initial proof of concept aims to address the current use cases in
Swift and Nova which are:

* REST-based, token auth for Swift
* many-to-many relationship between identity and tenant for Nova.


%prep
%setup -q -n keystone-%{version}

%patch1 -p1
%patch2 -p1

sed -i 's|\(log_file = \)\(keystone.log\)|\1%{_localstatedir}/log/keystone/\2|' etc/keystone.conf
sed -i 's|\(sql_connection = sqlite:///\)keystone.db|\1%{_sharedstatedir}/keystone/keystone.sqlite|' etc/keystone.conf

find . \( -name .gitignore -o -name .placeholder \) -delete
find keystone -name \*.py -exec sed -i '/\/usr\/bin\/env python/d' {} \;


%build
%{__python} setup.py build
find examples -type f -exec chmod 0664 \{\} \;

%install
%{__python} setup.py install -O1 --skip-build --root %{buildroot}

install -p -D -m 644 etc/keystone.conf %{buildroot}%{_sysconfdir}/keystone/keystone.conf
install -p -D -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/logrotate.d/openstack-keystone
install -d -m 755 %{buildroot}%{_sharedstatedir}/keystone
install -d -m 755 %{buildroot}%{_localstatedir}/log/keystone

rm -rf %{buildroot}%{python_sitelib}/tools
rm -rf %{buildroot}%{python_sitelib}/examples
rm -rf %{buildroot}%{python_sitelib}/doc

# docs generation requires everything to be installed first
export PYTHONPATH="$( pwd ):$PYTHONPATH"
pushd doc
make
popd
# Fix hidden-file-or-dir warnings
rm -fr doc/build/html/.doctrees doc/build/html/.buildinfo

%pre
getent group keystone >/dev/null || groupadd -r keystone
getent passwd keystone >/dev/null || \
useradd -r -g keystone -d %{_sharedstatedir}/keystone -s /sbin/nologin \
-c "OpenStack Keystone Daemons" keystone
exit 0

%files
%doc README.md
%doc doc/build/html
%doc examples
%{python_sitelib}/*
%{_bindir}/keystone*
%dir %{_sysconfdir}/keystone
%config(noreplace) %{_sysconfdir}/keystone/keystone.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/openstack-keystone
%dir %attr(-, keystone, keystone) %{_sharedstatedir}/keystone
%dir %attr(-, keystone, keystone) %{_localstatedir}/log/keystone

%changelog
* Fri Sep  2 2011 Mark McLoughlin <markmc@redhat.com> - 1.0-0.2.d4.1078
- Use upstream snapshot tarball
- No need to define python_sitelib anymore
- BR python2-devel
- Remove BRs only needed for unit tests
- No need to clean buildroot in install anymore
- Use slightly more canonical site for URL tag
- Prettify the requires tags
- Cherry-pick tools.tracer patch from upstream
- Add config file
- Add keystone user and group
- Ensure log file is in /var/log/keystone
- Ensure the sqlite db is in /var/lib/keystone
- Add logrotate support

* Thu Sep  1 2011 Matt Domsch <Matt_Domsch@dell.com> - 1.0-0.1.20110901git396f0bfd%{?dist}
- initial packaging
