$files = @(
    @{name="problem.html"; id="problem"},
    @{name="objectives.html"; id="objectives"},
    @{name="architecture.html"; id="architecture"},
    @{name="simulation.html"; id="simulation"},
    @{name="results.html"; id="results"},
    @{name="tech.html"; id="tech"},
    @{name="ai-guide.html"; id="ai-guide"}
)

$content = [System.IO.File]::ReadAllText("index.html")

foreach ($f in $files) {
    $newContent = $content.Replace("show('home');", "show('" + $f.id + "');")
    [System.IO.File]::WriteAllText($f.name, $newContent)
}
Write-Host "Files generated."
