Name:          aeolus
Summary:       Synthesised pipe organ emulator
Version:       0.8.4
Release:       %mkrel 1
License:       GPLv2+ and CC-BY-SA
Group:	       Sound
Source0:       http://www.kokkinizita.net/linuxaudio/downloads/%{name}-%{version}.tar.bz2
Source1:       http://www.kokkinizita.net/linuxaudio/downloads/stops-0.3.0.tar.bz2
Source2:       %{name}.desktop
# http://commons.wikimedia.org/wiki/File:Logo_aeolus.png / resized to 48x48
# CC-BY-SA License
Source3:       %{name}48x48.png
URL: 	       http://www.kokkinizita.net/linuxaudio/aeolus/index.html
BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Obsoletes:     %mklibname %{name}
BuildRequires: clthreads-devel
BuildRequires: clalsadrv-devel >= 2.0.0
BuildRequires: clxclient-devel
BuildRequires: libjack-devel
BuildRequires: readline-devel

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
%config %{_sysconfdir}/%{name}.conf
%{_bindir}/%{name}
%{_datadir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/pixmaps/%{name}.png
%{_libdir}/aeolus_txt.so
%{_libdir}/aeolus_x11.so

#--------------------------------------------------------------------

%prep
%setup -q -n %{name}-%{version} -a1

# fix wrong perms
chmod +r stops-0.3.0/*
cd source
sed -i -e 's/PREFIX =/#PREFIX =/g' Makefile
sed -i -e 's/-lXft//g' Makefile
sed -i -e 's/-lrt//g' Makefile
sed -i -e 's/\/sbin\/ldconfig/#\/sbin\/ldconfig/g' Makefile
sed -i -e 's#-O3#%{optflags}#' Makefile

%build
cd source
PREFIX=%{_prefix} %make

%install
rm -fr %{buildroot}
cd source
PREFIX=%{_prefix} %makeinstall_std 
cd ..

mkdir -p %{buildroot}%{_datadir}/%{name}/stops
cp -fr stops-0.3.0/* %{buildroot}%{_datadir}/%{name}/stops/

mkdir -p %{buildroot}%{_sysconfdir}/
cat > %{buildroot}%{_sysconfdir}/%{name}.conf <<EOF
-u -J -S %{_datadir}/%{name}/stops
EOF

# desktop file and icon
install -d -m755 %{buildroot}%{_datadir}/{applications,pixmaps}
install -D -m644 %{SOURCE2} %{buildroot}%{_datadir}/applications
install -m644 %{SOURCE3} %{buildroot}%{_datadir}/pixmaps/%{name}.png

%clean
rm -fr %{buildroot}
