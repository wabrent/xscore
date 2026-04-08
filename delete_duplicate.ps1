$content = Get-Content -Raw 'C:\Users\waabrent\Documents\trae_projects\twitter\templates\index.html'
$pattern = '<!-- MAIN ANALYZE SECTION -->[\s\S]*?</section>'
$matches = [regex]::Matches($content, $pattern)
if ($matches.Count -gt 1) {
    # Remove second occurrence
    $secondMatch = $matches[1]
    $newContent = $content.Remove($secondMatch.Index, $secondMatch.Length)
    Set-Content -Path 'C:\Users\waabrent\Documents\trae_projects\twitter\templates\index.html' -Value $newContent
    Write-Host 'Removed duplicate demo section'
} else {
    Write-Host 'Only one demo section found'
}