Summary:	Network traffic tracking tool
Summary(pl):	Narz�dzie do �ledzenia ruchu sieciowego
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
BuildRequires:	libpng-devel
BuildRequires:	gd-devel
BuildRequires:	libpcap-devel
BuildRequires:	autoconf
PreReq:		rc-scripts
Requires:	webserver
Requires(post,preun):	/sbin/chkconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define         _htmldir        /home/services/httpd/html/bandwidthd

%description
BandwidthD tracks usage of TCP/IP network subnets and builds html
files with graphs to display utilization. Charts are built by
individual IPs, and by default display utilization over 2 day, 8 day,
40 day, and 400 day periods. Furthermore, each ip address's
utilization can be logged out at intervals of 3.3 minutes, 10 minutes,
1 hour or 12 hours in cdf format, or to a backend database server.
HTTP, TCP, UDP, ICMP, VPN, and P2P traffic are color coded.

%description -l pl
BandwidthD �ledzi u�ycie sieci TCP/IP i buduje pliki html
wy�wietlaj�ce ruch sieciowy. Wykresy pokazuj� IP u�ytkownik�w i
domy�lnie wy�wietlaj� zu�ycie na przestrzeni 2, 8, 40 i 400 dni.
Ponadto udzia� ka�dego adresu IP w ruchu sieciowym mo�e by� zapisywany
w przedzia�ach 3.3 minut, 10 minut, 1 godziny lub 12 godzin w formacie
cdf, albo zapisywany do bazy danych. Ruch HTTP, TCP, UDP, ICMP, VPN, i
P2P jest kodowany w r�nych kolorach.

%prep
%setup -q
%patch0 -p0
%patch1 -p0
%patch2 -p1

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

cat  << EOF > $RPM_BUILD_ROOT/etc/cron.d/bandwidthd
0 0 * * *      root    /bin/kill -HUP \`cat /var/run/bandwidthd.pid\`
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add bandwidthd
if [ -f /var/lock/subsys/bandwidthd ]; then
        /etc/rc.d/init.d/bandwidthd restart 1>&2
else
        echo "Run \"/etc/rc.d/init.d/bandwidthd start\" to start bandwidthd."
fi

%preun
if [ "$1" = "0" ]; then
        if [ -f /var/lock/subsys/bandwidthd ]; then
                /etc/rc.d/init.d/bandwidthd stop 1>&2
        fi
        /sbin/chkconfig --del bandwidthd
fi

%files
%defattr(644,root,root,755)
%doc CHANGELOG README TODO
%attr(755,root,root) %{_sbindir}/bandwidthd
%dir %{_htmldir}
%{_htmldir}/*
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/%{name}.conf
%attr(755,root,root) /etc/rc.d/init.d/bandwidthd
%config(noreplace) %verify(not size mtime md5) %attr(640,root,root) /etc/cron.d/bandwidthd
/etc/sysconfig/bandwidthd