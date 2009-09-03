%define	name	ede
%define	version	1.2
%define	release	%mkrel 4

Name: 		%{name}
Version: 	%{version}
Release: 	%{release}
Source0: 	http://ovh.dl.sourceforge.net/sourceforge/ede/%{name}-%{version}.tar.gz
Patch0:		ede-1.0.4-exclude-unused-progs.patch
Patch2:		ede-mandriva-menufixes.patch
Summary:	The core programs for the Equinox Desktop Environment
URL: 		http://ede.sourceforge.net/
License: 	GPLv2+
Group: 		Graphical desktop/Other

BuildRoot: 	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires:	efltk-devel autoconf libx11-devel libxext-devel xft2-devel libpng-devel libjpeg-devel

%description
Equinox Desktop Environment (EDE) is desktop environment - the piece of
software that enables you to launch applications in a convenient way,
show what windows you have opened, manages icons and background of your
desktop, etc. This core package provides panel with tasklist, clock,
load status; icon manager that take care of your icons on background,
control panel for easy access to your settings, sound volume control, 
color configuration, panel configuration, menu editor, icons configuration, 
tips, time/date and timezone configuration, fast file search tool and of 
course window manager that manages your windows with config utility.

%prep
%setup -q -n %{name}
%patch0 -p1
%patch2 -p1

%build
# delete a bunch of obsolete launchers
rm -f datas/programs-links/{Casino.desktop,dialup.desktop,ecdplayer.desktop,Mastermind.desktop,Netscape.desktop,Notepad.desktop,Qubix.desktop,sccalc.desktop,UNIX.desktop,UNIX-regular,desktop,Vnterm.desktop,WordPerfect.desktop,x11amp.desktop,xwpe.desktop}
rm -f datas/desktop-links/Internet.desktop

autoconf
%configure
%make

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT{%{_bindir},%{_datadir}}
%makeinstall LOCALEDIR=$RPM_BUILD_ROOT%{_datadir}/locale

# Mandriva specific stuff - add to wmsessions
mkdir -p %{buildroot}%{_sysconfdir}/X11/wmsession.d/
cat << EOF > %{buildroot}%{_sysconfdir}/X11/wmsession.d/08EDE
NAME=EDE
ICON=ede-wmsession.xpm
EXEC=%{_bindir}/startede
DESC=Equinox Lightweight desktop environment
SCRIPT:
exec %{_bindir}/startede
EOF

#(peroyvind): several locale files, find those automatically..
for i in e*; do %find_lang $i; done
echo "%%defattr (644, root, root, 755)" > %{name}.lang
cat *.lang|grep %%lang >> %{name}.lang

# AdamW 2007/06 - update DM config files per http://wiki.mandriva.com/en/Development/Howto/Wmsession

%post
%make_session

%postun
%make_session

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(-,root,root)
%doc AUTHORS COPYING ChangeLog NEWS README
%config(noreplace) %{_sysconfdir}/X11/wmsession.d/08EDE
%{_bindir}/*
%{_datadir}/ede

