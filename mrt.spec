%include        /usr/lib/rpm/macros.perl
Summary:	Multi-threaded Routing Toolkit
Summary(pl):	Wielow±tkowe narzêdzia do routingu dynamicznego
Name:		mrt
Version:	2.2.2a
Release:	2
Copyright:	Distributable
Group:		Networking/Admin
Group(de):	Netzwerkwesen/Administration
Group(pl):	Sieciowe/Administacyjne
URL:		http://www.mrtd.net/
Source0:	ftp://ftp.merit.edu/net-research/mrt/%{name}-%{version}-Aug11.tar.gz
Source1:	%{name}.init
Patch0:		%{name}-perl.patch
Prereq:		/sbin/chkconfig
BuildRequires:	gdbm-devel
Prereq:		rc-scripts
Provides:	routingdaemon
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
Obsoletes:	bird
Obsoletes:      gated
Obsoletes:	zebra
Obsoletes:	zebra-guile

%description
MRT is a multi-threaded routing toolkit. It supports RIP, RIPng, BGP
and BGP4+ protocols, for both IPv4 and IPv6.

%description -l pl
MRT jest wielow±tkowym narzêdziem do routingu obs³uguj±cym protoko³y:
RIP, RIPng, BGP oraz BGP4+.

%prep
%setup -q -n %{name}
%patch0 -p1

%build
./make-sym-links
(cd src; chmod u+rw configure; autoconf)

cd `ls -d src.*`
%configure \
	--enable-ipv6 \
	--enable-thread \
	--with-gdbm \
	--disable-mrouting # broken
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOTP{%{_sbindir},%{_mandir}/man{1,8}} \
	$RPM_BUILD_ROOT%{_sysconfdir}/rc.d/init.d

cd `ls -d src.*`

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT%{_sbindir}

install ../src/programs/mrtd/mrtd.conf $RPM_BUILD_ROOT%{_sysconfdir}
install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/init.d/mrtd
install -d docs/scripts; cd docs

cp  ../../src/programs/bgpsim/*.conf .
cp  ../../src/programs/mrtd/mrtd.pim.conf .
cp  ../../src/programs/{bgpsim,route_{atob,btoa}}/*.pl scripts/
cp  ../../src/programs/{sbgp,route_{atob,btoa}}/*.1 $RPM_BUILD_ROOT%{_mandir}/man1/

gzip -9nf ../../src.*/docs/{*.conf,scripts/*.pl}

%post
NAME=mrtd; DESC="routing daemon"; %chkconfig_add

%preun
NAME=mrtd; %chkconfig_del

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc src.*/docs/*

%attr(600,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/*.conf
%attr(754,root,root) %{_sysconfdir}/rc.d/init.d/mrtd
%attr(755,root,root) %{_sbindir}/*
%{_mandir}/man[18]/*
