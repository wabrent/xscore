$lines = Get-Content 'C:\Users\waabrent\Documents\trae_projects\twitter\templates\index.html'
$newLines = @()
for ($i = 0; $i -lt $lines.Count; $i++) {
    $lineNumber = $i + 1
    if ($lineNumber -ge 639 -and $lineNumber -le 656) {
        continue
    }
    $newLines += $lines[$i]
}
Set-Content -Path 'C:\Users\waabrent\Documents\trae_projects\twitter\templates\index.html' -Value $newLines
Write-Host 'Removed leftover lines 639-656'