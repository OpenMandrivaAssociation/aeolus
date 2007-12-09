%define	libname	%mklibname %name

Name:          aeolus
Summary:       Synthesised pipe organ emulator
Version:       0.6.6
Release:       %mkrel 1
License:       GPL
Group:	       System/Libraries 
Source0:       %{name}-%{version}-2.tar.bz2
Patch0:        aeolus-0.6.6-2-fix-install.patch
URL: 	       http://users.skynet.be/solaris/linuxaudio/getit.html
BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-buildroot

BuildRequires: clthreads-devel
BuildRequires: clalsadrv-devel
BuildRequires: clxclient-devel
BuildRequires: jack-devel

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
%_bindir/aeolus

#--------------------------------------------------------------------

%package -n	%libname
Group: 		System/Libraries
Summary: 	Libraries for %name
Provides: 	lib%name = %version-%release
Requires:       %name  = %version-%release

%description  -n %libname
%name Libraries

%post -n %libname -p /sbin/ldconfig
%postun -n %libname -p /sbin/ldconfig

%files -n %libname
%defattr(-,root,root)
%_libdir/aeolus_txt.so
%_libdir/aeolus_x11.so
#--------------------------------------------------------------------

%prep
%setup -q -n %name-%version
%patch0 -p0

%build

%make

%install
make DESTDIR=%buildroot  install

%clean

