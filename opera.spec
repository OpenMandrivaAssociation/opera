%define name opera
%define version 10.62
%define rel	2
%define snap	0
%define buildnb 6438

%define tarball_base %{name}-%{version}-%{buildnb}
%define dirname %{tarball_base}.%{_arch}.linux

%define arch_exclude_files_from_autoreq ^$
%ifarch x86_64
# Exclude 32-bit requires on x86_64; plugins will pull them.
%define arch_exclude_files_from_autoreq ^%{_libdir}/%{name}/operapluginwrapper-ia32-linux$
%endif

# Exclude requires on GTK/KDE toolkits, they are optional and used
# automatically when present.
%define common_exclude_files_from_autoreq ^%{_libdir}/%{name}/libopera.\\+\\.so$

%define _exclude_files_from_autoreq %{arch_exclude_files_from_autoreq}\\|%{common_exclude_files_from_autoreq}

Summary:	Opera Web Browser for Linux
Name: 		%{name}
Version: 	%{version}
%if %snap
Release: 	%mkrel 0.%buildnb.%rel
%else
Release:	%mkrel %rel
%endif
%define shortver %(echo %version | tr -d .)
Source0:	http://get.opera.com/pub/opera/linux/%{shortver}/%{tarball_base}.i386.linux.tar.bz2
Source1: 	http://get.opera.com/pub/opera/linux/%{shortver}/%{tarball_base}.x86_64.linux.tar.bz2
Source2: 	bookmarks.adr
Patch0:		opera-destdir.patch
# StartupNotify does not work correctly when opera is already running;
# the already-existing window is activated and a new tab is opened
# and the completion signal is not sent.
Patch1:		opera-disable-startupnotify.patch
License: 	Freeware
Url:		http://www.opera.com/
Group: 		Networking/WWW
BuildRoot: 	%{_tmppath}/%{name}-buildroot
ExclusiveArch:	%ix86 x86_64
BuildRequires:	desktop-file-utils

%description
Opera for Linux is an alternative feature-rich Web browser. 

%prep
%ifarch x86_64
%setup -q -n %dirname -T -b 1
%else
%setup -q -n %dirname -T -b 0
%endif
%patch0 -p1
%patch1 -p1

%install
rm -rf $RPM_BUILD_ROOT

DESTDIR=%{buildroot} ./install --unattended --system --force

%if "%_lib" != "lib"
mv %{buildroot}%{_prefix}/lib %{buildroot}%{_libdir}
%endif
sed -i 's,/usr/lib,%{_libdir},' %{buildroot}%{_bindir}/opera

rm -rf rpmdocs
mv %{buildroot}%{_docdir}/opera rpmdocs

rm %{buildroot}%{_bindir}/uninstall-opera

# install mandrakized bookmarks file
install -m644 %{SOURCE2} %{buildroot}%_datadir/%name/defaults/bookmarks.adr

desktop-file-install --dir %{buildroot}%{_datadir}/applications \
	--add-category=X-MandrivaLinux-CrossDesktop \
	%{buildroot}%{_datadir}/applications/%{name}-browser.desktop

%if %{mdkversion} < 200900
%post
%{update_icon_cache hicolor}
%{update_desktop_database}
%{update_mime_database}
%{update_menus}

%postun
%{clean_icon_cache hicolor}
%{clean_desktop_database}
%{clean_mime_database}
%{clean_menus}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc rpmdocs/*
%_bindir/opera
%_bindir/opera-widget-manager
%_libdir/opera

%_iconsdir/hicolor/*/apps/%{name}-*.*
%_iconsdir/hicolor/*/mimetypes/%{name}-*.*
%_datadir/applications/%{name}-browser.desktop
%_datadir/applications/%{name}-widget-installer.desktop
%_datadir/applications/%{name}-widget-manager.desktop
%_datadir/mime/packages/%{name}-*.xml
%_mandir/man1/opera*

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

# langs
%dir %{_datadir}/%{name}/locale
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

