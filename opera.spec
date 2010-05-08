%define name opera
%define version 10.10
%define release %mkrel 1
%define buildnb 4742

%define tarball_base %{name}-%{version}.gcc4-shared-qt3
%define dirname %{name}-%{version}-%{buildnb}.gcc4-shared-qt3.%{_arch}

%ifarch x86_64
# Exclude 32-bit requires on x86_64; plugins will pull them.
%define _exclude_files_from_autoreq ^%{_libdir}/%{name}/operapluginwrapper-ia32-linux$
%endif

Summary:	Opera Web Browser for Linux
Name: 		%{name}
Version: 	%{version}
Release: 	%{release}
Source0:	%{tarball_base}.i386.tar.bz2
Source1: 	%{tarball_base}.x86_64.tar.bz2
Source2: 	opera6.adr
License: 	Commercial
Url:		http://www.opera.com/
Group: 		Networking/WWW
BuildRoot: 	%{_tmppath}/%{name}-buildroot
ExclusiveArch:	%ix86 x86_64
BuildRequires:	desktop-file-utils

%description
Opera for Linux is an alternative, lightweight, X11-based Web browser 
for Linux. 

%prep
%ifarch x86_64
%setup -q -n %dirname -T -b 1
%else
%setup -q -n %dirname -T -a 0
%endif

# extract upstream .desktop file
gawk '{ if (section) print } /^}/ { section=0 } /desktop_content\(\)/ { section=1 }' install.sh > shortcut-script
bash shortcut-script xdg | sed 's,opera.png,opera,' > opera.desktop

%install
rm -rf $RPM_BUILD_ROOT

./install.sh --prefix=$RPM_BUILD_ROOT%_prefix --exec_prefix=$RPM_BUILD_ROOT%_libdir/%name \
              --wrapperdir=$RPM_BUILD_ROOT%_bindir/ --sharedir=$RPM_BUILD_ROOT%_datadir/%name \
              --plugindir=$RPM_BUILD_ROOT%_libdir/opera/plugins --docdir=$PWD/rpmdocs \
              --mandir=%{buildroot}%{_mandir}

install -m755 -d %{buildroot}%{_sysconfdir}
install -m644 etc/* %{buildroot}%{_sysconfdir}

# install mandrakized bookmarks file
install -m644 %{SOURCE2} $RPM_BUILD_ROOT%_datadir/%name/opera6.adr

# remove buildroot path copied in the wrapper by the install script
perl -pi -e "s|$RPM_BUILD_ROOT||g" $RPM_BUILD_ROOT%_bindir/opera
# remove builddir
perl -pi -e "s|$PWD|%{_bindir}|" %{buildroot}%{_bindir}/opera

%if %{mdkversion} < 200700
# Mandrake menu entry
(cd $RPM_BUILD_ROOT
mkdir -p ./usr/lib/menu
cat > ./usr/lib/menu/%{name} << EOF
?package(%{name}):  \
command="/usr/bin/opera" \
icon="%{name}.png" \
needs="kde" \
needs="x11" \
title="Opera" \
longtitle="Opera Web Browser" \
section="Networking/WWW" \
xdg="true"
EOF
)
%endif

desktop-file-install --dir %{buildroot}%{_datadir}/applications \
	--add-category=X-MandrivaLinux-CrossDesktop \
	--add-category=X-MandrivaLinux-Internet-WebBrowsers \
	--remove-category=Application \
	%{name}.desktop

# install icons (install.sh misses these when run with --prefix)
install -d -m755 %{buildroot}%{_iconsdir}
cp -a usr/share/icons/hicolor %{buildroot}%{_iconsdir}

# legacy icon locations
install -d -m755 %{buildroot}%{_miconsdir} %{buildroot}%{_liconsdir}
cp -a %{buildroot}%{_iconsdir}/hicolor/16x16/apps/opera.png %{buildroot}%{_miconsdir}
cp -a %{buildroot}%{_iconsdir}/hicolor/32x32/apps/opera.png %{buildroot}%{_iconsdir}
cp -a %{buildroot}%{_iconsdir}/hicolor/48x48/apps/opera.png %{buildroot}%{_liconsdir}

%if %{mdkversion} < 200900
%post
%{update_icon_cache hicolor}
%{update_desktop_database}
%{update_menus}

%postun
%{clean_icon_cache hicolor}
%{clean_desktop_database}
%{clean_menus}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc rpmdocs/*
%config(noreplace) %{_sysconfdir}/operaprefs_default.ini
%config(noreplace) %{_sysconfdir}/operaprefs_fixed.ini
%_bindir/opera
%_libdir/opera
%_datadir/%name

%if %{mdkversion} < 200700
%_menudir/%name
%endif

%_iconsdir/opera.png
%_iconsdir/mini/opera.png
%_iconsdir/large/opera.png
%_iconsdir/hicolor/*/apps/%{name}.*
%_datadir/applications/%{name}.desktop
#

%_mandir/man1/opera*
# langs
%lang(be) %{_datadir}/%name/locale/be
%lang(bg) %{_datadir}/%name/locale/bg
%lang(cs) %{_datadir}/%name/locale/cs
%lang(da) %{_datadir}/%name/locale/da
%lang(de) %{_datadir}/%name/locale/de
%lang(el) %{_datadir}/%name/locale/el
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
%lang(ro) %{_datadir}/%name/locale/ru
%lang(ru) %{_datadir}/%name/locale/ru
%lang(sk) %{_datadir}/%name/locale/sv
%lang(sr) %{_datadir}/%name/locale/sv
%lang(sv) %{_datadir}/%name/locale/sv
%lang(te) %{_datadir}/%name/locale/te
%lang(ta) %{_datadir}/%name/locale/ta
%lang(tr) %{_datadir}/%name/locale/tr
%lang(uk) %{_datadir}/%name/locale/uk
%lang(zh_CN) %{_datadir}/%name/locale/zh-cn
%lang(zh_HK) %{_datadir}/%name/locale/zh-hk
%lang(zh_TW) %{_datadir}/%name/locale/zh-tw
