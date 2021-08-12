#https://www.reddit.com/r/PowerShell/comments/ft1gab/moving_cursor_to_specific_position_on_screen/
#https://flamingkeys.com/moving-the-mouse-cursor-with-windows-powershell/
Add-Type -AssemblyName System.Windows.Forms
$WShell = New-Object -com "Wscript.Shell"
$screen = [System.Windows.Forms.SystemInformation]::VirtualScreen

while ($true){
    #300,700
    $add_width = Get-Random -Minimum 400 -Maximum 800
    $add_height = Get-Random -Minimum 1100 -Maximum 2200
    $default_width = $screen.width / 10 + $add_width
    $default_height = $screen.height / 10 + $add_height
    [Windows.Forms.Cursor]::Position = "$default_width, $default_height"
    $WShell.sendkeys("{SCROLLLOCK 2}")
    Start-Sleep -Seconds 10
}