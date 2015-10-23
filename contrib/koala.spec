Name:             koala
Version:          2015.1.1
Release:          1
Summary:          OpenStack Billing (koala)

Group:            Applications/System
License:          ASL 2.0
URL:              https://github.com/DeliangFan/koala

Source0:          koala-2015.1.1.tar.gz
Source1:          koala.conf.sample
Source2:          koala-api.init

BuildArch:        noarch
BuildRequires:    python-setuptools
BuildRequires:    python-netaddr
BuildRequires:    python-pbr
BuildRequires:    python-six
BuildRequires:    python-sqlalchemy
BuildRequires:    intltool
BuildRequires:    python-d2to1
BuildRequires:    python2-devel

%if ! (0%{?rhel} && 0%{?rhel} <= 6)
BuildRequires:    systemd-units
%endif

%description
OpenStack koala provides services to billing and generate
consumption records.

%package -n       python-koala
Summary:          OpenStack koala python libraries
Group:            Applications/System

Requires:         python-anyjson
Requires:         python-babel
Requires:         python-eventlet
Requires:         python-iso8601
Requires:         python-pbr
Requires:         python-netaddr

Requires:         python-sqlalchemy
Requires:         python-migrate

Requires:         python-oslo-config >= 1:1.2.0

%description -n   python-koala
OpenStack koala provides services to billing and generate
consumption records.

This package contains the koala python library.


%package api
Summary:          OpenStack koala API service
Group:            Applications/System

Requires:         python-koala = %{version}-%{release}

Requires:         python-wsme
Requires:         python-pecan

%description api
OpenStack koala provides services to billing and generate
consumption records.

This package contains the koala API service.

%prep
%setup -q -n koala-%{version}

# Remove the requirements file so that pbr hooks don't add it
# to distutils requires_dist config
rm -rf {test-,}requirements.txt tools/{pip,test}-requires
find . \( -name .gitignore -o -name .placeholder \) -delete
find koala -name \*.py -exec sed -i '/\/usr\/bin\/env python/{d;q}' {} +

%build
%{__python} setup.py build

%install
getent group koala >/dev/null || groupadd -r koala --gid 191
if ! getent passwd koala >/dev/null; then
  useradd -u 191 -r -g koala -G koala,nobody -d %{_sharedstatedir}/koala -s /sbin/nologin -c "OpenStack Koala Daemons" koala
fi

%{__python} setup.py install -O1 --skip-build --root %{buildroot}

# Setup directories
mkdir -p %{buildroot}/var/log/koala/
mkdir -p %{buildroot}/var/run/koala/
mkdir -p %{buildroot}/var/lib/koala/
mkdir -p %{buildroot}/etc/koala/

# Setup log file
touch %{buildroot}/var/log/koala/koala.log

# Install config files
install -p -D -m 640 etc/koala/koala.conf.sample %{buildroot}%{_sysconfdir}/koala/koala.conf

# Install initscripts for services
install -p -D -m 755 %{SOURCE2} %{buildroot}%{_initrddir}/%{name}-api

# Install logrotate

# Remove unneeded in production stuff
rm -f %{buildroot}%{_bindir}/koala-debug
rm -fr %{buildroot}%{python_sitelib}/tests/
rm -fr %{buildroot}%{python_sitelib}/run_tests.*

%post api
# Initial installation
/sbin/chkconfig --add koala-api > /dev/null 2>&1

%preun api
/sbin/service koala-api stop > /dev/null 2>&1
/sbin/chkconfig --del koala-api > /dev/null 2>&1

%files -n python-koala
%dir %{_sysconfdir}/koala
%{_bindir}/koala-manage
%{python_sitelib}/koala*
%dir %attr(0755,koala,root) %{_localstatedir}/log/koala
%dir %attr(0755,koala,root) %{_localstatedir}/run/koala
%dir %attr(0755,koala,root) %{_sharedstatedir}/koala
%dir %attr(0755,koala,root) %{_sysconfdir}/koala
%config(noreplace) %attr(-, root, koala) %{_sysconfdir}/koala/koala.conf
%config(noreplace) %attr(0664, koala, koala) %{_localstatedir}/log/koala/koala.log 

%files api
%{_bindir}/koala-api
%{_initrddir}/%{name}-api

%changelog
* Thu Oct 22 2015 Deliang Fan <vanderliang@gmail.com> 2015.1.1-1
- Start koala.
