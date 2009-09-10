Name:          aeolus
Summary:       Synthesised pipe organ emulator
Version:       0.8.2
Release:       %mkrel 2
License:       GPLv2+
Group:	       Sound
Source0:       http://www.kokkinizita.net/linuxaudio/downloads/%{name}-%{version}.tar.bz2
Source1:       http://www.kokkinizita.net/linuxaudio/downloads/stops-0.3.0.tar.bz2
Patch0:        aeolus-0.6.6-2-fix-install.patch
URL: 	       http://www.kokkinizita.net/linuxaudio/aeolus/index.html
BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Obsoletes:     %mklibname %name
BuildRequires: clthreads-devel
BuildRequires: clalsadrv-devel
BuildRequires: clxclient-devel
BuildRequires: libjack-devel

%description
Aeolus is a synthesised (i.e. not sampled) pipe organ emulator that 
should be good enough to make an organist enjoy playing it. It is a 
software synthesiser optimised for this job, with possibly hundreds 
of controls for each stop, that enable the user to "voice" 
his instrument.

Main features of the default instrument: three manuals and one pedal, 
five different temperaments, variable tuning, MIDI control of course, 
stereo, surround or Ambisonics output, flexible audio controls 
including a large church reverb.

Aeolus is not very CPU-hungry, and should run without problems on a 
e.g. a 1GHz, 256Mb machine. 

%files
%defattr(-,root,root)
%config %{_sysconfdir}/%name.conf
%_bindir/aeolus
%_datadir/stops
%_libdir/aeolus_txt.so
%_libdir/aeolus_x11.so
#--------------------------------------------------------------------

%prep
%setup -q -n %name-%version -a1
%patch0 -p0
sed -i -e 's#-O3#%{optflags}#' Makefile

%build
%make

%install
rm -fr %buildroot
%makeinstall_std PREFIX=%{_prefix}

mkdir -p %buildroot%_datadir/stops
cp -fr stops-0.3.0/* %buildroot%_datadir/stops/

mkdir -p %buildroot%_sysconfdir/
cat > %buildroot%_sysconfdir/%name.conf <<EOF
-S %_datadir/stops
EOF

%clean
rm -fr %buildroot
