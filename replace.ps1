$content = Get-Content -Raw 'C:\Users\waabrent\Documents\trae_projects\twitter\templates\index.html'
$hero = [regex]::Match($content, '<!-- HERO -->[\s\S]*?</section>').Value
$demo = [regex]::Match($content, '<!-- MAIN ANALYZE SECTION -->[\s\S]*?</section>').Value
$newContent = $content.Replace($hero, $demo)
Set-Content -Path 'C:\Users\waabrent\Documents\trae_projects\twitter\templates\index.html' -Value $newContent
Write-Host 'Replaced hero with demo'