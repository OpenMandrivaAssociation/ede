Name: 		ede
Version: 	2.0
Release: 	1
Source0: 	http://downloads.sourceforge.net/project/ede/%{name}/%{version}/%{name}-%{version}.tar.gz
Patch0:		ede-1.0.4-exclude-unused-progs.patch
Patch1:		ede-2.0-mdv-linking.patch
Patch2:		ede-mandriva-menufixes.patch
Patch3:		ede-2.0-rosa-flags.patch
Patch4:		ede-2.0-rosa-format-security.patch
Patch5:		ede-2.0-rosa-no-update-mime-database.patch
Summary:	The core programs for the Equinox Desktop Environment
URL: 		http://equinox-project.org/
License: 	GPLv2+
Group: 		Graphical desktop/Other

BuildRequires:	jam
BuildRequires:	pkgconfig(edelib)
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(xext)
BuildRequires:	fltk-devel
BuildRequires:	pkgconfig(libstartup-notification-1.0)
BuildRequires:	pkgconfig(xpm)
BuildRequires:	pkgconfig(xkbfile)
BuildRequires:	pkgconfig(libcurl)
BuildRequires:	pkgconfig(ice)
BuildRequires:	pkgconfig(cairo)
BuildRequires:	pkgconfig(pixman-1)
BuildRequires:	jpeg-devel
BuildRequires:	png-devel

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
%setup -q
#patch0 -p1
%patch1 -p1
#patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1

%build
%define _disable_ld_no_undefined 1

%configure
jam -d+5

%install
jam install DESTDIR=%{buildroot}

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

mv %{buildroot}%{_docdir}/%{name}-%{version}* %{buildroot}%{_docdir}/%{name}



%files
%doc AUTHORS AUTHORS.pekwm ChangeLog README
%config(noreplace) %{_sysconfdir}/X11/wmsession.d/08EDE
%{_bindir}/*
%{_datadir}/applications/*.desktop
%{_iconsdir}/edeneu
%{_iconsdir}/kbflags
%{_datadir}/dbus-1/services/*.service
%{_datadir}/desktop-directories/ede-*.directory
%{_datadir}/ede
%{_datadir}/mime/packages/*.xml
%{_datadir}/pekwm
%{_datadir}/wallpapers/*
%{_datadir}/xsessions/ede.desktop
%config(noreplace) %{_sysconfdir}/pekwm/*
%config(noreplace) %{_sysconfdir}/xdg/ede/*
%config(noreplace) %{_sysconfdir}/xdg/menus/*
