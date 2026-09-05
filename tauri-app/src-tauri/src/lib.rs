use base64::Engine;

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        .plugin(tauri_plugin_dialog::init())
        .invoke_handler(tauri::generate_handler![export_image, desktop_dir])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}

/// 把拼接图写入指定路径（路径由前端 JS 对话框选定）
#[tauri::command]
fn export_image(data: String, path: String) -> Result<String, String> {
    let bytes = base64::engine::general_purpose::STANDARD
        .decode(data)
        .map_err(|e| e.to_string())?;
    std::fs::write(&path, bytes).map_err(|e| e.to_string())?;
    Ok(path)
}

/// 返回桌面目录绝对路径，用于保存对话框的默认位置
#[tauri::command]
fn desktop_dir() -> Option<String> {
    dirs::desktop_dir().map(|p| p.to_string_lossy().to_string())
}
