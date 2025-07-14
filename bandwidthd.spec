Summary:	Network traffic tracking tool
Summary(pl.UTF-8):	Narzędzie do śledzenia ruchu sieciowego
Name:		bandwidthd
Version:	2.0.1
Release:	0.1
License:	GPL
Group:		Networking/Admin
Source0:	http://dl.sourceforge.net/bandwidthd/%{name}-%{version}.tgz
# Source0-md5:	aa79aad7bd489fd2cae1f7dc086ca8b6
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Source3:	%{name}.conf
Patch0:		%{name}-makefile.patch
Patch1:		%{name}-pgsql.patch
Patch2:		%{name}-path.patch
URL:		http://bandwidthd.sourceforge.net/
BuildRequires:	autoconf
BuildRequires:	gd-devel
BuildRequires:	libpcap-devel
BuildRequires:	libpng-devel
BuildRequires:	rpmbuild(macros) >= 1.268
Requires(post,preun):	/sbin/chkconfig
Requires:	rc-scripts
Requires:	webserver
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_htmldir	/home/services/httpd/html/bandwidthd

%description
BandwidthD tracks usage of TCP/IP network subnets and builds html
files with graphs to display utilization. Charts are built by
individual IPs, and by default display utilization over 2 day, 8 day,
40 day, and 400 day periods. Furthermore, each ip address's
utilization can be logged out at intervals of 3.3 minutes, 10 minutes,
1 hour or 12 hours in cdf format, or to a backend database server.
HTTP, TCP, UDP, ICMP, VPN, and P2P traffic are color coded.

%description -l pl.UTF-8
BandwidthD śledzi użycie sieci TCP/IP i buduje pliki HTML
wyświetlające ruch sieciowy. Wykresy pokazują IP użytkowników i
domyślnie wyświetlają zużycie na przestrzeni 2, 8, 40 i 400 dni.
Ponadto udział każdego adresu IP w ruchu sieciowym może być zapisywany
w przedziałach 3.3 minut, 10 minut, 1 godziny lub 12 godzin w formacie
cdf, albo zapisywany do bazy danych. Ruch HTTP, TCP, UDP, ICMP, VPN, i
P2P jest kodowany w różnych kolorach.

%prep
%setup -q
%patch -P0 -p0
%patch -P1 -p0
%patch -P2 -p1

%build
%{__autoconf}
%{__autoheader}
%configure

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{_sbindir},%{_htmldir},/etc/{sysconfig,rc.d/init.d,cron.d}}

install bandwidthd $RPM_BUILD_ROOT%{_sbindir}
install htdocs/* $RPM_BUILD_ROOT%{_htmldir}
install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/bandwidthd
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/bandwidthd
install %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}

cat  << 'EOF' > $RPM_BUILD_ROOT/etc/cron.d/bandwidthd
0 0 * * *      root    /bin/kill -HUP `cat /var/run/bandwidthd.pid`
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add bandwidthd
%service bandwidthd restart

%preun
if [ "$1" = "0" ]; then
	%service bandwidthd stop
	/sbin/chkconfig --del bandwidthd
fi

%files
%defattr(644,root,root,755)
%doc CHANGELOG README TODO
%attr(755,root,root) %{_sbindir}/bandwidthd
%dir %{_htmldir}
%{_htmldir}/*
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}.conf
%attr(754,root,root) /etc/rc.d/init.d/bandwidthd
%config(noreplace) %verify(not md5 mtime size) %attr(640,root,root) /etc/cron.d/bandwidthd
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/bandwidthd
