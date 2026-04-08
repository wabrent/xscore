$content = Get-Content -Raw 'C:\Users\waabrent\Documents\trae_projects\twitter\templates\index.html'
$cleanTicker = @'
<!-- TICKER -->
<div class="ticker">
  <div class="ticker-inner">
    <span>Virality Score <em>★</em></span>
    <span>Account Analysis <em>★</em></span>
    <span>Competitor Intel <em>★</em></span>
    <span>Best Post Times <em>★</em></span>
    <span>Engagement Forecast <em>★</em></span>
    <span>Audience Insights <em>★</em></span>
    <span>Fake Follower Score <em>★</em></span>
    <span>Virality Score <em>★</em></span>
    <span>Account Analysis <em>★</em></span>
    <span>Competitor Intel <em>★</em></span>
    <span>Best Post Times <em>★</em></span>
    <span>Engagement Forecast <em>★</em></span>
    <span>Audience Insights <em>★</em></span>
    <span>Fake Follower Score <em>★</em></span>
  </div>
</div>
'@
$pattern = '<!-- TICKER -->[\s\S]*?</div>\s*</div>'
$content = [regex]::Replace($content, $pattern, $cleanTicker)
Set-Content -Path 'C:\Users\waabrent\Documents\trae_projects\twitter\templates\index.html' -Value $content
Write-Host 'Cleaned ticker'