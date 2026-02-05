$TargetDir = "F:\kbj2"
$OldDir = "F:\kbj_repo"
$CurrentPath = [Environment]::GetEnvironmentVariable("Path", "User")

# Remove Old
if ($CurrentPath -like "*$OldDir*") {
    $CurrentPath = $CurrentPath.Replace("$OldDir;", "").Replace(";$OldDir", "")
}

# Add New
if ($CurrentPath -notlike "*$TargetDir*") {
    $NewPath = "$CurrentPath;$TargetDir"
    [Environment]::SetEnvironmentVariable("Path", $NewPath, "User")
    Write-Host "✅ Switched PATH to $TargetDir (Headquarters)."
}
