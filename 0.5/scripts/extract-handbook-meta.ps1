# Extrae cabecera, TOC, Relacionado e Historial de handbook/*.md a _meta/.
$ErrorActionPreference = "Stop"
$handbook = Join-Path $PSScriptRoot "..\handbook" | Resolve-Path
$metaDir = Join-Path $handbook "_meta"
New-Item -ItemType Directory -Force -Path $metaDir | Out-Null

function Convert-YamlScalar([string]$value) {
    if ($null -eq $value) { return '""' }
    $t = $value.Trim()
    if ($t -eq "") { return '""' }
    if ($t -match '[:#\[\]\{\}&*!|>%@`]|^\s|\s$|^(true|false|null|yes|no)$' -or $t -match '"') {
        $esc = $t.Replace('\', '\\').Replace('"', '\"')
        return '"' + $esc + '"'
    }
    return $t
}

function Parse-Cabecera([string]$block) {
    $map = [ordered]@{}
    foreach ($line in $block -split "`n") {
        $m = [regex]::Match($line.Trim(), '^\|\s*\*{0,2}([^|*]+)\*{0,2}\s*\|\s*(.*?)\s*\|$')
        if (-not $m.Success) { continue }
        $key = $m.Groups[1].Value.Trim()
        $val = $m.Groups[2].Value.Trim()
        if ($key -match '^(Campo|-)') { continue }
        $map[$key] = $val
    }
    return $map
}

function Parse-Related([string]$block) {
    $rows = @()
    foreach ($line in $block -split "`n") {
        $trim = $line.Trim()
        if (-not $trim.StartsWith("|") -or $trim -match '^\|\s*-+') { continue }
        $cells = @($trim.Trim('|').Split('|') | ForEach-Object { $_.Trim() })
        if ($cells.Count -lt 2) { continue }
        if ($cells[0] -match 'Destino|por qu') { continue }
        $destino = $cells[0]
        $porque = $cells[1]
        if ($cells.Count -ge 3 -and $cells[0] -match '^(🧭|🛠️|📖|📝|⛔|📦|🖼️)?$') {
            $destino = $cells[1]
            $porque = $cells[2]
        }
        if ($destino -eq "Destino") { continue }
        $rows += [pscustomobject]@{ destino = $destino; por_que = $porque }
    }
    return $rows
}

function Parse-Historial([string]$block) {
    $rows = @()
    foreach ($line in $block -split "`n") {
        $m = [regex]::Match($line.Trim(), '^\|\s*([0-9]+(?:\.[0-9]+){1,2})\s*\|\s*([^\|]+)\|\s*(.+?)\s*\|$')
        if ($m.Success) {
            $rows += [pscustomobject]@{
                version = $m.Groups[1].Value
                fecha   = $m.Groups[2].Value.Trim()
                cambio  = $m.Groups[3].Value.Trim()
            }
        }
    }
    return $rows
}

function Get-Cab($map, [string[]]$names) {
    foreach ($n in $names) {
        foreach ($k in $map.Keys) {
            if ($k.Trim('*') -eq $n) { return [string]$map[$k] }
        }
    }
    return ""
}

$files = Get-ChildItem $handbook -Filter "*.md" | Where-Object { $_.Name -ne "CHANGELOG.md" } | Sort-Object Name
$indexItems = @()

foreach ($file in $files) {
    $text = [System.IO.File]::ReadAllText($file.FullName)
    $nl = if ($text.Contains("`r`n")) { "`r`n" } else { "`n" }
    $lines = $text -split "`r?`n"
    $title = $lines[0]
    $i = 1
    while ($i -lt $lines.Length -and $lines[$i].Trim() -eq "") { $i++ }
    $cabLines = @()
    if ($i -lt $lines.Length -and $lines[$i].StartsWith("|")) {
        while ($i -lt $lines.Length -and ($lines[$i].StartsWith("|") -or $lines[$i].Trim() -eq "")) {
            if ($lines[$i].Trim()) { $cabLines += $lines[$i] }
            $i++
        }
    }
    while ($i -lt $lines.Length -and ($lines[$i].Trim() -eq "" -or $lines[$i].Trim() -eq "---")) { $i++ }
    $toc = ""
    if ($i -lt $lines.Length -and $lines[$i].StartsWith("**En esta página:**")) {
        $toc = $lines[$i]
        $i++
        while ($i -lt $lines.Length -and $lines[$i].Trim() -eq "") { $i++ }
    }
    $rest = ($lines[$i..($lines.Length - 1)] -join "`n")
    $relM = [regex]::Match($rest, '(?m)^## Relacionado\s*$')
    $histM = [regex]::Match($rest, '(?m)^## (?:\d+\.\s+)?Historial\s*$')
    $cut = @()
    if ($relM.Success) { $cut += $relM.Index }
    if ($histM.Success) { $cut += $histM.Index }
    $body = if ($cut.Count) { $rest.Substring(0, ($cut | Measure-Object -Minimum).Minimum).TrimEnd() } else { $rest.TrimEnd() }
    $relacionado = @()
    $historial = @()
    if ($relM.Success -and $histM.Success) {
        if ($relM.Index -lt $histM.Index) {
            $relacionado = Parse-Related $rest.Substring($relM.Index + $relM.Length, $histM.Index - ($relM.Index + $relM.Length))
            $historial = Parse-Historial $rest.Substring($histM.Index + $histM.Length)
        } else {
            $historial = Parse-Historial $rest.Substring($histM.Index + $histM.Length, $relM.Index - ($histM.Index + $histM.Length))
            $relacionado = Parse-Related $rest.Substring($relM.Index + $relM.Length)
        }
    } elseif ($relM.Success) {
        $relacionado = Parse-Related $rest.Substring($relM.Index + $relM.Length)
    } elseif ($histM.Success) {
        $historial = Parse-Historial $rest.Substring($histM.Index + $histM.Length)
    }

    $cab = Parse-Cabecera ($cabLines -join "`n")
    $version = Get-Cab $cab @("Versión", "Version")
    $estado = Get-Cab $cab @("Estado")
    $fecha = Get-Cab $cab @("Fecha", "Última actualización")
    $parte = Get-Cab $cab @("Parte")
    $norma = Get-Cab $cab @("Norma superior", "Norma")
    $deriva = Get-Cab $cab @("Deriva hacia")

    $yaml = New-Object System.Text.StringBuilder
    [void]$yaml.AppendLine("archivo: $($file.Name)")
    [void]$yaml.AppendLine("titulo: $(Convert-YamlScalar ($title -replace '^#\s+', ''))")
    [void]$yaml.AppendLine("version: $(Convert-YamlScalar $version)")
    [void]$yaml.AppendLine("estado: $(Convert-YamlScalar $estado)")
    [void]$yaml.AppendLine("fecha: $(Convert-YamlScalar $fecha)")
    [void]$yaml.AppendLine("parte: $(Convert-YamlScalar $parte)")
    [void]$yaml.AppendLine("norma_superior: $(Convert-YamlScalar $norma)")
    [void]$yaml.AppendLine("deriva_hacia: $(Convert-YamlScalar $deriva)")
    [void]$yaml.AppendLine("toc: $(Convert-YamlScalar $toc)")
    [void]$yaml.AppendLine("relacionado:")
    if ($relacionado.Count -eq 0) {
        [void]$yaml.AppendLine("  []")
    } else {
        foreach ($r in $relacionado) {
            [void]$yaml.AppendLine("  - destino: $(Convert-YamlScalar $r.destino)")
            [void]$yaml.AppendLine("    por_que: $(Convert-YamlScalar $r.por_que)")
        }
    }
    [void]$yaml.AppendLine("historial:")
    if ($historial.Count -eq 0) {
        [void]$yaml.AppendLine("  []")
    } else {
        foreach ($h in $historial) {
            [void]$yaml.AppendLine("  - version: $(Convert-YamlScalar $h.version)")
            [void]$yaml.AppendLine("    fecha: $(Convert-YamlScalar $h.fecha)")
            [void]$yaml.AppendLine("    cambio: $(Convert-YamlScalar $h.cambio)")
        }
    }
    [void]$yaml.AppendLine("cabecera:")
    foreach ($k in $cab.Keys) {
        [void]$yaml.AppendLine("  $(Convert-YamlScalar $k): $(Convert-YamlScalar $cab[$k])")
    }

    $side = Join-Path $metaDir ($file.BaseName + ".yaml")
    $utf8 = New-Object System.Text.UTF8Encoding $false
    [System.IO.File]::WriteAllText($side, $yaml.ToString(), $utf8)

    $pointer = "$title`n`n> Andamiaje (cabecera, TOC, Relacionado, Historial): [``_meta/$($file.BaseName).yaml``](_meta/$($file.BaseName).yaml).`n`n$body`n"
    [System.IO.File]::WriteAllText($file.FullName, $pointer.Replace("`n", $nl), $utf8)
    Write-Host "OK $($file.Name)"

    $indexItems += [pscustomobject]@{
        id = $file.BaseName
        archivo = $file.Name
        meta = "_meta/$($file.BaseName).yaml"
        version = $version
        estado = $estado
        titulo = ($title -replace '^#\s+', '')
    }
}

$ix = New-Object System.Text.StringBuilder
[void]$ix.AppendLine("linea: `"0.4.0`"")
[void]$ix.AppendLine("nota: Andamiaje de capítulos en handbook/_meta. El cuerpo es norma.")
[void]$ix.AppendLine("capitulos:")
foreach ($it in $indexItems) {
    [void]$ix.AppendLine("  - id: $(Convert-YamlScalar $it.id)")
    [void]$ix.AppendLine("    archivo: $(Convert-YamlScalar $it.archivo)")
    [void]$ix.AppendLine("    meta: $(Convert-YamlScalar $it.meta)")
    [void]$ix.AppendLine("    version: $(Convert-YamlScalar $it.version)")
    [void]$ix.AppendLine("    estado: $(Convert-YamlScalar $it.estado)")
    [void]$ix.AppendLine("    titulo: $(Convert-YamlScalar $it.titulo)")
}
$utf8 = New-Object System.Text.UTF8Encoding $false
[System.IO.File]::WriteAllText((Join-Path $handbook "index.yaml"), $ix.ToString(), $utf8)
Write-Host "OK handbook/index.yaml"
