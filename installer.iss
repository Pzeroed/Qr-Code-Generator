; --------------------------
; QR Code Generator Installer
; Version 1.1.1
; --------------------------

[Setup]
AppName=QR Code Generator
AppVersion=1.1.1
; Install EXE in AppData\Local (fully writable by the user)
DefaultDirName={localappdata}\QR Code Generator
DefaultGroupName=QR Code Generator
OutputBaseFilename=QRCodeGeneratorInstaller_v1.1.1
Compression=lzma
SolidCompression=yes
SetupIconFile=icon.ico
UninstallDisplayIcon={app}\QR Code Generator.exe

[Files]
; Copy EXE from dist folder
Source: "dist\main.exe"; DestDir: "{app}"; Flags: ignoreversion

[Tasks]
; Optional desktop shortcut
Name: "desktopicon"; Description: "Create a desktop shortcut"; GroupDescription: "Additional icons"; Flags: unchecked

[Icons]
; Start menu shortcut
Name: "{group}\QR Code Generator"; Filename: "{app}\main.exe"
; Desktop shortcut (if selected)
Name: "{commondesktop}\QR Code Generator"; Filename: "{app}\main.exe"; Tasks: desktopicon
