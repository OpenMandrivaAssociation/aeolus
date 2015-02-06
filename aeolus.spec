Summary:	Synthesized pipe organ emulator
Name:		aeolus
Version:	0.9.0
Release:	4
License:	GPLv2+ and CC-BY-SA
Group:		Sound
Url:		http://okkinizita.net/linuxaudio/aeolus/index.html
Source0:	http://kokkinizita.linuxaudio.org/linuxaudio/downloads/%{name}-%{version}.tar.bz2
Source1:	http://kokkinizita.linuxaudio.org/linuxaudio/downloads/stops-0.3.0.tar.bz2
# http://commons.wikimedia.org/wiki/File:Logo_aeolus.png / resized to 48x48
# CC-BY-SA License
Source2:	%{name}48x48.png
Patch0:		aeolus-0.9.0-makefile.patch
BuildRequires:	clthreads-devel >= 2.4.0
BuildRequires:	clxclient-devel >= 3.9.0
BuildRequires:	readline-devel
BuildRequires:	zita-alsa-pcmi-devel >= 0.2.0
BuildRequires:	pkgconfig(jack)

%description
Aeolus is a synthesized (i.e. not sampled) pipe organ emulator that
should be good enough to make an organist enjoy playing it. It is a
software synthesizer optimized for this job, with possibly hundreds
of controls for each stop, that enable the user to "voice" his instrument.

Main features of the default instrument: three manuals and one pedal,
five different temperaments, variable tuning, MIDI control of course,
stereo, surround or Ambisonics output, flexible audio controls
including a large church reverb.

Aeolus is not very CPU-hungry, and should run without problems on a
e.g. a 1GHz, 256MB machine.

%files
%config %{_sysconfdir}/%{name}.conf
%{_bindir}/%{name}
%{_datadir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/pixmaps/%{name}.png
%{_libdir}/aeolus*.so

#----------------------------------------------------------------------------

%prep
%setup -q -a1
%patch0 -p1

# fix wrong perms
chmod +r stops-0.3.0/*
pushd source
sed -i -e 's/-lXft//g' Makefile
sed -i -e 's/-lrt//g' Makefile
sed -i -e 's#-O3#%{optflags}#' Makefile
popd

%build
cd source
PREFIX=%{_prefix} %make

%install
pushd source
PREFIX=%{_prefix} %makeinstall_std
popd

mkdir -p %{buildroot}%{_datadir}/%{name}/stops
cp -fr stops-0.3.0/* %{buildroot}%{_datadir}/%{name}/stops/

mkdir -p %{buildroot}%{_sysconfdir}/
cat > %{buildroot}%{_sysconfdir}/%{name}.conf <<EOF
-u -J -S %{_datadir}/%{name}/stops
EOF

# desktop file and icon
install -d -m755 %{buildroot}%{_datadir}/pixmaps
install -m644 %{SOURCE2} %{buildroot}%{_datadir}/pixmaps/%{name}.png

mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/%{name}.desktop << EOL
[Desktop Entry]
Type=Application
Exec=aeolus
GenericName=Aeolus
GenericName[en_GB]=Aeolus
Icon=aeolus
Name=Aeolus
Comment=Virtual pipe organ based on additive synthesis
Name[en_GB]=Aeolus
Comment[en_GB]=Virtual pipe organ based on additive synthesis
Name[cs]=Aeolus
Comment[cs]=VirtuÃ¡lnÃ­ varhany zaloÅ¾enÃ© na aditivnÃ­ syntÃ©ze
Name[de]=Aeolus
Comment[de]=Virtuelle Pfeifenorgel, auf additiver Synthese beasierend
Name[es]=Aeolus
Comment[es]=Ã“rgano virtual basado en la sÃ­ntesis aditiva
Name[fr]=Aeolus
Comment[fr]=Orgue virtuel basÃ© sur la synthÃ¨se additive
Name[it]= Aeolus
Comment[it]= Virtual pipe organ basato sulla sintesi additiva
Name[ja]=Aeolus
Comment[ja]=ãƒãƒ¼ãƒãƒ£ãƒ«ãƒ‘ã‚¤ãƒ—ã‚ªãƒ«ã‚¬ãƒ³
Name[nb]=Aeolus
Comment[nb]=Virtuelt orgel basert pÃ¥ additivsyntese
Name[nl]=Aeolus
Comment[nl]=Virtueel pijporgel gebaseerd op toegevoegde syntheses
Name[pl]=Aeolus
Comment[pl]=Wirtualne organy piszczaÅ‚kowe
Name[pt_BR]=Aeolus
Comment[pt_BR]=Virtual pipe organ based on additive synthesis
Name[sk]=Aeolus
Comment[sk]=VirtuÃ¡lny pÃ­Å¡talovÃ½ organ zaloÅ¾enÃ½ na aditÃ­vnej syntÃ©ze
Name[zh_CN]=Aeolus
Comment[zh_CN]=åŸºäºŽåŠ æ³•åˆæˆçš„è™šæ‹Ÿç®¡é“å…ƒä»¶
Name[zh_TW]=Aeolus
Comment[zh_TW]=ä»¥ç–Šåˆå¤šç¨®åˆæˆå™¨ç‚ºåŸºç¤Žçš„è™›æ“¬ç®¡é¢¨ç´
StartupNotify=true
Terminal=false
Categories=Audio;AudioVideo;Midi;
X-KDE-SubstituteUID=false
EOL

