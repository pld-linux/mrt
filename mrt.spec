%include        /usr/lib/rpm/macros.perl
Summary:	Multi-threaded Routing Toolkit
Summary(pl):	Wielow±tkowe narzêdzia do routingu dynamicznego
Name:		mrt
Version:	2.2.2a
Release:	2
License:	distributable
Group:		Networking/Admin
Source0:	http://prdownloads.sourceforge.net/mrt/%{name}-%{version}.tar.gz
Source1:	%{name}.init
Patch0:		%{name}-perl.patch
Patch1:		%{name}-fix.patch
URL:		http://www.mrtd.net/
BuildRequires:	gdbm-devel
BuildRequires:	rpm-perlprov
Prereq:		/sbin/chkconfig
Prereq:		rc-scripts
Provides:	routingdaemon
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
Obsoletes:	bird
Obsoletes:	gated
Obsoletes:	zebra
Obsoletes:	zebra-guile

%description
MRT is a multi-threaded routing toolkit. It supports RIP, RIPng, BGP
and BGP4+ protocols, for both IPv4 and IPv6.

%description -l pl
MRT jest wielow±tkowym narzêdziem do routingu obs³uguj±cym protoko³y:
RIP, RIPng, BGP oraz BGP4+.

%prep
%setup -q -n %{name}-2.2a-Aug-14-2000
%patch0 -p1
%patch1 -p1

%build
./make-sym-links
(cd src; chmod u+rw configure; autoconf)

cd `ls -d src.*`
ac_n="-n"; export ac_n
%configure \
	--enable-ipv6 \
	--enable-thread \
	--with-gdbm \
	--disable-mrouting # broken
	
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_mandir}/man{1,8}} \
	$RPM_BUILD_ROOT%{_sysconfdir}/rc.d/init.d

cd `ls -d src.*`

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT%{_sbindir} \
	MANDIR=$RPM_BUILD_ROOT%{_mandir}

install ../src/programs/mrtd/mrtd.conf $RPM_BUILD_ROOT%{_sysconfdir}
install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/init.d/mrtd
install -d docs/scripts; cd docs

cp -f ../../src/programs/bgpsim/*.conf .
cp -f ../../src/programs/mrtd/mrtd.pim.conf .
cp -f ../../src/programs/{bgpsim,route_{atob,btoa}}/*.pl scripts/
cp -f ../../src/programs/{sbgp,route_{atob,btoa}}/*.1 $RPM_BUILD_ROOT%{_mandir}/man1/

gzip -9nf ../../src.*/docs/{*.conf,scripts/*.pl}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add mrtd >&2
if [ -f /var/lock/subsys/mrtd ]; then
	/etc/rc.d/init.d/mrtd restart >&2
else
	echo "Run '/etc/rc.d/init.d/mrtd start' to start routing deamon." >&2
fi

%preun
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/mrtd ]; then
		/etc/rc.d/init.d/mrtd stop >&2
	fi
	/sbin/chkconfig --del mrtd >&2
fi

%files
%defattr(644,root,root,755)
%doc src.*/docs/*

%attr(600,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/*.conf
%attr(754,root,root) %{_sysconfdir}/rc.d/init.d/mrtd
%attr(755,root,root) %{_sbindir}/*
%{_mandir}/man[18]/*
