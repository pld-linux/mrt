Summary:	Multi-threaded Routing Toolkit
Summary(pl.UTF-8):	Wielowątkowe narzędzia do routingu dynamicznego
Name:		mrt
Version:	2.2.2a
Release:	6
License:	distributable
Group:		Networking/Admin
Source0:	http://dl.sourceforge.net/mrt/%{name}-%{version}.tar.gz
# Source0-md5:	68d6e681b0c01599d02ab60a640463a0
Source1:	%{name}.init
Patch0:		%{name}-perl.patch
Patch1:		%{name}-fix.patch
Patch2:		%{name}-va_arg.patch
Patch3:		%{name}-nolibs.patch
URL:		http://www.mrtd.net/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gdbm-devel
BuildRequires:	rpm-perlprov
BuildRequires:	rpmbuild(macros) >= 1.268
Requires(post,preun):	/sbin/chkconfig
Requires:	rc-scripts
Provides:	routingdaemon
Obsoletes:	bird
Obsoletes:	gated
Obsoletes:	zebra
Obsoletes:	zebra-guile
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
MRT is a multi-threaded routing toolkit. It supports RIP, RIPng, BGP
and BGP4+ protocols, for both IPv4 and IPv6.

%description -l pl.UTF-8
MRT jest wielowątkowym narzędziem do routingu obsługującym protokoły:
RIP, RIPng, BGP oraz BGP4+.

%prep
%setup -q -n %{name}-2.2a-Aug-14-2000
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
./make-sym-links
cd src
chmod u+rw configure
%{__autoconf}
cd ..

cd `ls -d src.*`
cp %{_datadir}/automake/config.*   .
cp %{_datadir}/automake/install-sh .
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
	$RPM_BUILD_ROOT/etc/rc.d/init.d

cd `ls -d src.*`

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT%{_sbindir} \
	MANDIR=$RPM_BUILD_ROOT%{_mandir}

install ../src/programs/mrtd/mrtd.conf $RPM_BUILD_ROOT%{_sysconfdir}
install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/mrtd
install -d docs/scripts; cd docs

cp -f ../../src/programs/bgpsim/*.conf .
cp -f ../../src/programs/mrtd/mrtd.pim.conf .
cp -f ../../src/programs/{bgpsim,route_{atob,btoa}}/*.pl scripts
cp -f ../../src/programs/{sbgp,route_{atob,btoa}}/*.1 $RPM_BUILD_ROOT%{_mandir}/man1

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add mrtd >&2
%service mrtd restart "routing daemon"

%preun
if [ "$1" = "0" ]; then
	%service mrtd stop
	/sbin/chkconfig --del mrtd >&2
fi

%files
%defattr(644,root,root,755)
%doc src.*/docs/*

%attr(600,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/*.conf
%attr(754,root,root) /etc/rc.d/init.d/mrtd
%attr(755,root,root) %{_sbindir}/*
%{_mandir}/man[18]/*
