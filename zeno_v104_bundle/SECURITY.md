# Security Notes

- This app is **local-first** and makes no external API calls by default.
- The sidecar exposes a WebSocket on localhost; do not bind it to 0.0.0.0 unless you understand the risks.
- If you enable Tauri Shell sidecar spawning, the capability scope restricts which binary can be executed.
- Do not embed secret keys in the frontend; this project does not require any.
- When distributing, use OS code-signing and secure update channels.
