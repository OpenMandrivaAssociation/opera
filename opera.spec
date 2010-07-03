%define name opera
%define version 10.60
%define release %mkrel 1
%define buildnb 6386

%define tarball_base %{name}-%{version}-%{buildnb}
%define dirname %{name}-%{version}-%{buildnb}.%{_arch}.linux

%ifarch x86_64
# Exclude 32-bit requires on x86_64; plugins will pull them.
%define _exclude_files_from_autoreq ^%{_libdir}/%{name}/operapluginwrapper-ia32-linux$
%endif

Summary:	Opera Web Browser for Linux
Name: 		%{name}
Version: 	%{version}
Release: 	%{release}
Source0:	http://get.opera.com/pub/opera/linux/1060/%{tarball_base}.i386.linux.tar.bz2
Source1: 	http://get.opera.com/pub/opera/linux/1060/%{tarball_base}.x86_64.linux.tar.bz2
Source2: 	bookmarks.adr
License: 	Commercial
Url:		http://www.opera.com/
Group: 		Networking/WWW
BuildRoot: 	%{_tmppath}/%{name}-buildroot
ExclusiveArch:	%ix86 x86_64
BuildRequires:	desktop-file-utils
Requires:	liboperatoolkit = %version

%description
Opera for Linux is an alternative, lightweight, X11-based Web browser 
for Linux. 

%package -n liboperagtk
Summary:	Opera Dialog Tookit GTK
Group:		Networking/WWW
Requires:	%name = %version
Provides:	liboperatoolkit = %version

%description -n liboperagtk
This package provides GTK file selector for Opera.

%package -n liboperakde4
Summary:	Opera Dialog Tookit KDE4
Group:		Networking/WWW
Requires:	%name = %version
Provides:	liboperatoolkit = %version

%description -n liboperakde4
This package provides KDE4 file selector for Opera.

%prep
%ifarch x86_64
%setup -q -n %dirname -T -b 1
%else
%setup -q -n %dirname -T -b 0
%endif

# use buildroot
sed -i -e 's#/usr/local#%{buildroot}/usr#' install

%install
rm -rf $RPM_BUILD_ROOT

./install --text --quiet --system --force

rm -f %buildroot%{_datadir}/applications/mimeinfo.cache
rm -f %buildroot%{_bindir}/uninstall-opera
rm -fr %buildroot%{_datadir}/doc/opera
rm -fr %buildroot%{_datadir}/mime

sed -i -e 's#%{buildroot}##' %buildroot%{_bindir}/*

# install mandrakized bookmarks file
install -m644 %{SOURCE2} %{buildroot}%_datadir/%name/defaults/bookmarks.adr

desktop-file-install --dir %{buildroot}%{_datadir}/applications \
	--add-category=X-MandrivaLinux-CrossDesktop \
	%{buildroot}%{_datadir}/applications/%{name}-browser.desktop

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc share/doc/opera/*
%_bindir/*
%_libdir/opera
%exclude %_libdir/opera/liboperagtk.so
%exclude %_libdir/opera/liboperakde4.so
%dir %{_datadir}/opera
%{_datadir}/opera/encoding.bin
%{_datadir}/opera/*.dtd
%{_datadir}/opera/lngcode.txt
%{_datadir}/opera/package-id.ini
%{_datadir}/opera/defaults
%{_datadir}/opera/extra
%{_datadir}/opera/package
%{_datadir}/opera/skin
%{_datadir}/opera/styles
%{_datadir}/opera/ui
%{_datadir}/opera/unite
%{_datadir}/opera/locale/en
%_iconsdir/*/*/*/*
%_datadir/applications/*.desktop
%_mandir/man?/opera*
# langs
%lang(be) %{_datadir}/%name/locale/be
%lang(bg) %{_datadir}/%name/locale/bg
%lang(cs) %{_datadir}/%name/locale/cs
%lang(da) %{_datadir}/%name/locale/da
%lang(de) %{_datadir}/%name/locale/de
%lang(el) %{_datadir}/%name/locale/el
%lang(en_GB) %{_datadir}/%name/locale/en-GB
%lang(es) %{_datadir}/%name/locale/es-ES
%lang(es) %{_datadir}/%name/locale/es-LA
%lang(et) %{_datadir}/%name/locale/et
%lang(fi) %{_datadir}/%name/locale/fi
%lang(fr) %{_datadir}/%name/locale/fr
%lang(fr_CA) %{_datadir}/%name/locale/fr-CA
%lang(fy) %{_datadir}/%name/locale/fy
%lang(hi) %{_datadir}/%name/locale/hi
%lang(hu) %{_datadir}/%name/locale/hu
%lang(hr) %{_datadir}/%name/locale/hr
%lang(id) %{_datadir}/%name/locale/id
%lang(it) %{_datadir}/%name/locale/it
%lang(ja) %{_datadir}/%name/locale/ja
%lang(ka) %{_datadir}/%name/locale/ka
%lang(ko) %{_datadir}/%name/locale/ko
%lang(lt) %{_datadir}/%name/locale/lt
%lang(mk) %{_datadir}/%name/locale/mk
%lang(nn) %{_datadir}/%name/locale/nn
%lang(nb) %{_datadir}/%name/locale/nb
%lang(nl) %{_datadir}/%name/locale/nl
%lang(pl) %{_datadir}/%name/locale/pl
%lang(pt) %{_datadir}/%name/locale/pt
%lang(pt_BR) %{_datadir}/%name/locale/pt-BR
%lang(ro) %{_datadir}/%name/locale/ro
%lang(ru) %{_datadir}/%name/locale/ru
%lang(sk) %{_datadir}/%name/locale/sk
%lang(sr) %{_datadir}/%name/locale/sr
%lang(sv) %{_datadir}/%name/locale/sv
%lang(te) %{_datadir}/%name/locale/te
%lang(ta) %{_datadir}/%name/locale/ta
%lang(tr) %{_datadir}/%name/locale/tr
%lang(uk) %{_datadir}/%name/locale/uk
%lang(vi) %{_datadir}/%name/locale/vi
%lang(zh_CN) %{_datadir}/%name/locale/zh-cn
%lang(zh_HK) %{_datadir}/%name/locale/zh-hk
%lang(zh_TW) %{_datadir}/%name/locale/zh-tw

%files -n liboperagtk
%defattr(-,root,root)
%{_libdir}/opera/liboperagtk.so

%files -n liboperakde4
%defattr(-,root,root)
%{_libdir}/opera/liboperakde4.so
