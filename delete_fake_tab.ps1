$content = Get-Content -Raw 'C:\Users\waabrent\Documents\trae_projects\twitter\templates\index.html'
$pattern = '<!-- Fake Score Tab -->[\s\S]*?</div>\s*</div>\s*</div>'
# Need to match the exact structure: ticker div contains ticker-inner div, then fake tab div, then closing ticker div.
# Let's match from <!-- Fake Score Tab --> to the next </div> that closes the ticker? Actually we want to remove the entire fake tab div and its contents.
# Use non-greedy match up to the closing </div> that matches the fake tab div.
$pattern2 = '(\s*<!-- Fake Score Tab -->\s*<div id="tab-fake" class="tab-content" style="display:none;">[\s\S]*?</div>\s*)'
$newContent = [regex]::Replace($content, $pattern2, '')
Set-Content -Path 'C:\Users\waabrent\Documents\trae_projects\twitter\templates\index.html' -Value $newContent
Write-Host 'Removed fake score tab from ticker'