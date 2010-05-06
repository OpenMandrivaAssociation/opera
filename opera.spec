%define name opera
%define version 10.10
%define fullname %{name}-%{version}.gcc4-shared-qt3.x86_64
%define release %mkrel 1
%define buildnb 4742

Summary:	Opera for linux Web browser
Name: 		%{name}
Version: 	%{version}
Release: 	%{release}
Source0: 	%{fullname}.tar.bz2
Source1: 	opera-icons.tar.bz2
Source2: 	opera6.adr.bz2
Source3: be.lng
Source4: bg.lng
Source5: cs.lng
Source6: da.lng
Source7: de.lng
Source8: el.lng
Source9: en-GB.lng
Source10: en.lng
Source11: es-ES.lng
Source12: es-LA.lng
Source13: et.lng
Source14: fi.lng
Source15: fr-CA.lng
Source16: fr.lng
Source17: fy.lng
Source18: hi.lng
Source19: hr.lng
Source20: hu.lng
Source21: id.lng
Source22: it.lng
Source23: ja.lng
Source24: ka.lng
Source25: ko.lng
Source26: lt.lng
Source27: mk.lng
Source28: nb.lng
Source29: nl.lng
Source30: nn.lng
Source31: pl.lng
Source32: pt-BR.lng
Source33: pt.lng
Source34: ru.lng
Source35: sv.lng
Source36: ta.lng
Source37: te.lng
Source38: tr.lng
Source39: uk.lng
Source40: zh-cn.lng
Source41: zh-tw.lng
Source42: ro.lng
Source43: sk.lng
Source44: sr.lng
License: 	Commercial
Url:		http://www.opera.com
Group: 		Networking/WWW
BuildRoot: 	%{_tmppath}/%{name}-buildroot
Requires:	liblesstif2

%description
Opera for Linux is an alternative, lightweight, X11-based Web browser 
for Linux. 

- Static Version -

%prep

%setup -n  %{name}-%{version}-%{buildnb}.gcc4-shared-qt3.x86_64

%install
rm -rf $RPM_BUILD_ROOT

grep -v '.license'  install.sh | tee install2.sh > /dev/null

chmod 755 install2.sh

./install2.sh --prefix=$RPM_BUILD_ROOT --exec_prefix=$RPM_BUILD_ROOT%_prefix/X11R6/bin --wrapperdir=$RPM_BUILD_ROOT%_bindir/ --sharedir=$RPM_BUILD_ROOT%_datadir/%name --plugindir=$RPM_BUILD_ROOT%_libdir/opera/plugins --docdir=$RPM_BUILD_ROOT%_docdir/%name-%version

# install mandrakized bookmarks file
bzcat %{SOURCE2} > $RPM_BUILD_ROOT%_datadir/%name/opera6.adr

# install languages
cp %SOURCE4 %SOURCE5 %SOURCE6 %SOURCE7 %SOURCE8 %SOURCE9 \
%SOURCE10 %SOURCE11 %SOURCE12 %SOURCE13 %SOURCE14 %SOURCE15 %SOURCE16 \
%SOURCE17 %SOURCE18 %SOURCE19 %SOURCE20 %SOURCE21 %SOURCE22 %SOURCE23 \
%SOURCE24 %SOURCE25 %SOURCE26 %SOURCE27 %SOURCE28 %SOURCE29 %SOURCE30 \
%SOURCE31 %SOURCE32 %SOURCE33 %SOURCE34 %SOURCE35 %SOURCE36 %SOURCE37 \
%SOURCE38 %SOURCE39 %SOURCE40 %SOURCE41 %SOURCE42 %SOURCE43 %SOURCE44 \
$RPM_BUILD_ROOT%_datadir/%name/locale

# remove buildroot path copied in the wrapper by the install script
perl -pi -e "s|$RPM_BUILD_ROOT||g" $RPM_BUILD_ROOT%_bindir/opera
perl -pi -e "s|\/usr\/lib ||g" $RPM_BUILD_ROOT%_bindir/opera

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

mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Name=Opera
Comment=Opera for linux Web browser
Exec=opera
Icon=%{name}
Terminal=false
Type=Application
Categories=X-MandrivaLinux-Internet-WebBrowsers;Network;WebBrowser;X-MandrivaLinux-CrossDesktop;
EOF


# mdk icons
install -d $RPM_BUILD_ROOT%{_iconsdir}
bzip2 -dc %{SOURCE1} | tar xvf - -C $RPM_BUILD_ROOT%{_iconsdir}
install -m 644 %{SOURCE2}  $RPM_BUILD_ROOT%{_datadir}/%{name}

# remove misplaced license file
rm -rf $RPM_BUILD_ROOT%_docdir/LICENSE

# fix doc link
rm -rf $RPM_BUILD_ROOT/%_docdir/%name-%version/help
#ln -sf %_docdir/%name-%version/help $RPM_BUILD_ROOT/%_docdir/%name-%version/help

# remove openmotif-3 wrapper
#rm $RPM_BUILD_ROOT/%_libdir/opera/plugins/operamotifwrapper-3

# remove wrong opera.jar reference
perl -pi -e "s|$RPM_BUILD_ROOT\/usr\/share\/opera\/java\/\/opera.jar|file:\/\/\/usr\/share\/opera\/java\/opera.jar|g" $RPM_BUILD_ROOT%_datadir/opera/java/opera.policy

# mode man file
mkdir -p $RPM_BUILD_ROOT%_mandir/man1
mv $RPM_BUILD_ROOT/share/man/man1/* $RPM_BUILD_ROOT%_mandir/man1/

%post 
%{update_menus}
/sbin/ldconfig

%postun 
%{clean_menus}
/sbin/ldconfig

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
#%doc LICENSE
%_bindir/*
%_prefix/X11R6/bin/*
#
#%_prefix/X11R6/lib/*
%_libdir/opera
#%_libdir/opera*
#
%_datadir/%name

%_menudir/%name
%_iconsdir/opera*
%_iconsdir/mini/*
%_iconsdir/large/*
%_datadir/applications/*
#
%_docdir/%name-%version
%_mandir/man1/*
# langs
#%_datadir/%name/locale/be.lng
%_datadir/%name/locale/bg.lng
%_datadir/%name/locale/cs.lng
%_datadir/%name/locale/da.lng
%_datadir/%name/locale/de.lng
%_datadir/%name/locale/el.lng
%_datadir/%name/locale/en-GB.lng
%_datadir/%name/locale/en.lng
%_datadir/%name/locale/es-ES.lng
%_datadir/%name/locale/es-LA.lng
%_datadir/%name/locale/et.lng
%_datadir/%name/locale/fi.lng
%_datadir/%name/locale/fr-CA.lng
%_datadir/%name/locale/fr.lng
%_datadir/%name/locale/fy.lng
%_datadir/%name/locale/hi.lng
%_datadir/%name/locale/hr.lng
%_datadir/%name/locale/hu.lng
%_datadir/%name/locale/id.lng
%_datadir/%name/locale/it.lng
%_datadir/%name/locale/ja.lng
%_datadir/%name/locale/ka.lng
%_datadir/%name/locale/ko.lng
%_datadir/%name/locale/lt.lng
%_datadir/%name/locale/mk.lng
%_datadir/%name/locale/nb.lng
%_datadir/%name/locale/nl.lng
%_datadir/%name/locale/nn.lng
%_datadir/%name/locale/pl.lng
%_datadir/%name/locale/pt-BR.lng
%_datadir/%name/locale/pt.lng
%_datadir/%name/locale/ru.lng
%_datadir/%name/locale/sv.lng
%_datadir/%name/locale/ta.lng
%_datadir/%name/locale/te.lng
%_datadir/%name/locale/tr.lng
%_datadir/%name/locale/uk.lng
%_datadir/%name/locale/zh-cn.lng
%_datadir/%name/locale/zh-tw.lng
%_datadir/%name/locale/ro.lng
%_datadir/%name/locale/sk.lng
%_datadir/%name/locale/sr.lng

