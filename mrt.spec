%define	date	990502

Summary:	Multi-threaded Routing Toolkit
Summary(pl):	Wielow±tkowe narzêdzia do routingu dynamicznego
Name:		mrt
Version:	1.6.0a
Release:	1.%{date}
Copyright:	Distributable
Group:		Networking/Admin
Group(pl):	Sieci/Administracja
URL:		ftp://ftp.merit.edu/net-research/mrt
Source0:	%{name}-%{version}-%{date}-src.tar.gz
Source1:	%{name}.init
Patch0:		%{name}-perl.patch
Patch1:		%{name}-linux.patch
Prereq:		/sbin/chkconfig
Buildroot:	/tmp/%{name}-%{version}-root

%description
MRT is a multi-threaded routing toolkit. It supports RIP, RIPng, BGP
and BGP4+ protocols, for both IPv4 and IPv6.

%description -l pl
MRT jest wielow±tkowym narzêdziem do routingu obs³uguj±cym
protoko³y: RIP, RIPng, BGP oraz BGP4+.

%prep
%setup -q 
%patch0 -p1
#%patch1 -p1

%build
./make-sym-links
cd `ls -d src.*`
CFLAGS="$RPM_OPT_FLAGS" LDFLAGS=-s \
    ./configure %{_target} \
	--prefix=/usr 

make

%install
rm -rf $RPM_BUILD_ROOT
cd `ls -d src.*`

install -d $RPM_BUILD_ROOT/usr/{sbin,man/{man8,man1}}
install -d $RPM_BUILD_ROOT/etc/rc.d/init.d

make DESTDIR=$RPM_BUILD_ROOT/usr/sbin MANDIR=$RPM_BUILD_ROOT/usr/man install

install ../src/programs/mrtd/mrtd.conf $RPM_BUILD_ROOT/etc

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/mrtd

install -d docs/scripts; cd docs

cp  ../../src/programs/bgpsim/*.conf .
cp  ../../src/programs/bgpsim/*.pl scripts/

cp  ../../src/programs/route_atob/*.pl scripts/
cp  ../../src/programs/route_atob/*.1 $RPM_BUILD_ROOT/usr/man/man1/

cp  ../../src/programs/route_btoa/*.pl scripts/
cp  ../../src/programs/route_btoa/*.1 $RPM_BUILD_ROOT/usr/man/man1/

cp  ../../src/programs/sbgp/*.1 $RPM_BUILD_ROOT/usr/man/man1/

gzip -9nf $RPM_BUILD_ROOT/usr/man/{man1/*,man8/*} \
	../../src.*/docs/{*.conf,scripts/*.pl}

%clean
#rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add mrtd

%preun
if [ $1 = 0 ]; then
    /sbin/chkconfig --del mrtd
fi
    
%files
%defattr(644,root,root,755)
%doc src.*/docs/*

%attr(600,root,root) %config(noreplace) %verify(not size mtime md5) /etc/*.conf
%attr(700,root,root) %config %verify(not size mtime md5) /etc/rc.d/*

%attr(755,root,root) /usr/sbin/*
/usr/man/man[18]/*

%changelog
* Wed Jan 27 1999 Wojtek ¦lusarczyk <wojtek@shadow.eu.org>
  [1.5.0a-3d]
- final build for Tornado,
- compressed man pages && documentaction,
- fixed group, && added Group(pl),
- other changes.

* Sat Sep 05 1998 Wojtek ¦lusarczyk <wojtek@shadow.eu.org>
  [1.4.9-1d]
- updated to 1.4.9a.

* Thu Sep 03 1998 Wojtek ¦lusarczyk <wojtek@shadow.eu.org>
  [1.4.8-1-RH]
- added Buildroot,
- fixed files permissions,
- build from non root's account.

* Sat Aug 22 1998 Marek Obuchowicz <elephant@shadow.eu.org>
  [1.4.8-1d]
- first try at RPM,
- build against GNU Libc-2.1.
