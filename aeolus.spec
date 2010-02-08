Name:          aeolus
Summary:       Synthesised pipe organ emulator
Version:       0.8.2
Release:       %mkrel 5
License:       GPLv2+ and CC-BY-SA
Group:	       Sound
Source0:       http://www.kokkinizita.net/linuxaudio/downloads/%{name}-%{version}.tar.bz2
Source1:       http://www.kokkinizita.net/linuxaudio/downloads/stops-0.3.0.tar.bz2
Source2:       %{name}.desktop
# http://commons.wikimedia.org/wiki/File:Logo_aeolus.png / resized to 48x48
# CC-BY-SA License
Source3:       %{name}48x48.png
Patch0:        aeolus-0.6.6-2-fix-install.patch
Patch1:        aeolus-0.8.2-fix-linkage.patch
URL: 	       http://www.kokkinizita.net/linuxaudio/aeolus/index.html
BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Obsoletes:     %mklibname %{name}
BuildRequires: clthreads-devel
BuildRequires: clalsadrv-devel
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
%patch0 -p0
%patch1 -p1 -b .linkage
sed -i -e 's#-O3#%{optflags}#' Makefile

%build
%make PREFIX=%{_prefix}

%install
rm -fr %{buildroot}
%makeinstall_std PREFIX=%{_prefix}

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
