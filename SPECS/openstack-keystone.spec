
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

Patch1:         keystone-move-tools-tracer.patch

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

find . \( -name .gitignore -o -name .placeholder \) -delete
find keystone -name \*.py -exec sed -i '/\/usr\/bin\/env python/d' {} \;


%build
%{__python} setup.py build
find examples -type f -exec chmod 0664 \{\} \;

%install
%{__python} setup.py install -O1 --skip-build --root %{buildroot}

install -p -D -m 644 etc/keystone.conf %{buildroot}%{_sysconfdir}/keystone/keystone.conf

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

%files
%doc README.md
%doc doc/build/html
%doc examples
%{python_sitelib}/*
%{_bindir}/keystone*
%dir %{_sysconfdir}/keystone
%config(noreplace) %{_sysconfdir}/keystone/keystone.conf

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

* Thu Sep  1 2011 Matt Domsch <Matt_Domsch@dell.com> - 1.0-0.1.20110901git396f0bfd%{?dist}
- initial packaging
