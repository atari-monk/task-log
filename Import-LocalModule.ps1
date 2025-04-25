$code_path = "C:\atari-monk\code"
$repo_name = "task_log"
$egg_info_path = "$code_path\$repo_name\$repo_name.egg-info"

pip uninstall $repo_name -y

if (Test-Path $egg_info_path) {
    Remove-Item -Path $egg_info_path -Recurse -Force
    Write-Host "Removed: $egg_info_path"
}
else {
    Write-Host "Directory does not exist: $egg_info_path"
}

pip install -e .