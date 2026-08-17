#define AppName "PDF SafeTools"
#define AppVersion "0.1.0"
#define AppPublisher "Yahya"
#define AppExeName "PDFSafeTools.exe"

[Setup]
AppId={{D7C3A5C8-9DF4-4FE8-9A50-6B9E6A6B8F30}
AppName={#AppName}
AppVersion={#AppVersion}
AppPublisher={#AppPublisher}
DefaultDirName={autopf}\PDF SafeTools
DefaultGroupName={#AppName}
OutputDir=dist\installer
OutputBaseFilename=PDFSafeTools-Setup
Compression=lzma
SolidCompression=yes
WizardStyle=modern
ArchitecturesInstallIn64BitMode=x64
PrivilegesRequired=lowest

[Files]
Source: "..\dist\PDFSafeTools\*"; DestDir: "{app}"; Flags: recursesubdirs ignoreversion

[Icons]
Name: "{group}\{#AppName}"; Filename: "{app}\{#AppExeName}"
Name: "{autodesktop}\{#AppName}"; Filename: "{app}\{#AppExeName}"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "Create a desktop shortcut"; GroupDescription: "Additional icons:"

[Run]
Filename: "{app}\{#AppExeName}"; Description: "Launch {#AppName}"; Flags: nowait postinstall skipifsilent
