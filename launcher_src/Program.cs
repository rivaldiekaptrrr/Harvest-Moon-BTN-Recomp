using System;
using System.Diagnostics;
using System.Drawing;
using System.IO;
using System.Text;
using System.Windows.Forms;

namespace HarvestMoonLauncher
{
    static class Program
    {
        [STAThread]
        static void Main(string[] args)
        {
            Application.EnableVisualStyles();
            Application.SetCompatibleTextRenderingDefault(false);
            Application.Run(new MainForm());
        }
    }

    public class MainForm : Form
    {
        // Controls
        private ComboBox cmbResolution;
        private ComboBox cmbDisplayMode;
        private ComboBox cmbAspectRatio;
        private ComboBox cmbInternalRes;
        private ComboBox cmbTextureFilter;
        private CheckBox chkPgxp;
        private CheckBox chkAntialiasing;

        private ComboBox cmbFpsTarget;
        private ComboBox cmbVsync;
        private CheckBox chkShowFps;
        private CheckBox chkLowLatency;
        private CheckBox chkMultiThread;
        private ComboBox cmbFastForward;

        private ComboBox cmbPadDevice;
        private ComboBox cmbPadMode;
        private TrackBar tbDeadzone;
        private Label lblDeadzoneVal;

        private CheckBox chkAlwaysShowLauncher;

        private string baseDir;
        private string gameTomlPath;
        private string settingsTomlPath;
        private string exePath;

        public MainForm()
        {
            baseDir = AppDomain.CurrentDomain.BaseDirectory;
            gameTomlPath = Path.Combine(baseDir, "game.toml");
            settingsTomlPath = Path.Combine(baseDir, "settings.toml");
            exePath = Path.Combine(baseDir, "HarvestMoonBTN_Recompiled.exe");

            InitializeComponent();
            LoadConfig();
        }

        private void InitializeComponent()
        {
            this.Text = "Harvest Moon: Back to Nature - Launcher & Configuration";
            this.Size = new Size(680, 680);
            this.StartPosition = FormStartPosition.CenterScreen;
            this.FormBorderStyle = FormBorderStyle.FixedDialog;
            this.MaximizeBox = false;
            this.BackColor = Color.FromArgb(24, 25, 29);
            this.ForeColor = Color.FromArgb(230, 230, 230);
            this.Font = new Font("Segoe UI", 9.5f, FontStyle.Regular);

            // Header Banner
            Panel pnlHeader = new Panel
            {
                Dock = DockStyle.Top,
                Height = 85,
                BackColor = Color.FromArgb(34, 112, 62)
            };

            Label lblTitle = new Label
            {
                Text = "HARVEST MOON: BACK TO NATURE",
                Font = new Font("Segoe UI", 14f, FontStyle.Bold),
                ForeColor = Color.White,
                Location = new Point(20, 16),
                AutoSize = true
            };

            Label lblSubtitle = new Label
            {
                Text = "Native PC Port (Enhanced Recompilation) • Game Launcher & Settings",
                Font = new Font("Segoe UI", 9.5f, FontStyle.Regular),
                ForeColor = Color.FromArgb(210, 240, 220),
                Location = new Point(22, 48),
                AutoSize = true
            };

            pnlHeader.Controls.Add(lblTitle);
            pnlHeader.Controls.Add(lblSubtitle);
            this.Controls.Add(pnlHeader);

            // Tab Control
            TabControl tabs = new TabControl
            {
                Location = new Point(15, 100),
                Size = new Size(635, 470),
                Font = new Font("Segoe UI", 9.5f, FontStyle.Regular)
            };

            TabPage tabDisplay = new TabPage("  🖥️ Layar & Grafis  ") { BackColor = Color.FromArgb(30, 31, 36) };
            TabPage tabPerf = new TabPage("  ⚡ Performa & FPS  ") { BackColor = Color.FromArgb(30, 31, 36) };
            TabPage tabControls = new TabPage("  🎮 Kontroler & Input  ") { BackColor = Color.FromArgb(30, 31, 36) };
            TabPage tabHelp = new TabPage("  ℹ️ Hotkeys & Save  ") { BackColor = Color.FromArgb(30, 31, 36) };

            tabs.TabPages.Add(tabDisplay);
            tabs.TabPages.Add(tabPerf);
            tabs.TabPages.Add(tabControls);
            tabs.TabPages.Add(tabHelp);
            this.Controls.Add(tabs);

            // ==================== TAB 1: DISPLAY & GRAPHICS ====================
            int y = 20;
            tabDisplay.Controls.Add(CreateHeaderLabel("Pengaturan Tampilan Layar", 20, y)); y += 30;

            tabDisplay.Controls.Add(CreateFieldLabel("Mode Layar (Display Mode):", 25, y));
            cmbDisplayMode = CreateComboBox(230, y - 3, 280);
            cmbDisplayMode.Items.AddRange(new object[] {
                "Windowed (Mode Jendela)",
                "Borderless Fullscreen (Layar Penuh Tanpa Batas)",
                "Exclusive Fullscreen (Layar Penuh Eksklusif)"
            });
            cmbDisplayMode.SelectedIndex = 0;
            tabDisplay.Controls.Add(cmbDisplayMode);
            y += 40;

            tabDisplay.Controls.Add(CreateFieldLabel("Resolusi Layar (Window Size):", 25, y));
            cmbResolution = CreateComboBox(230, y - 3, 280);
            cmbResolution.Items.AddRange(new object[] {
                "1280 x 960 (4:3 Standard Quad VGA - Rekomendasi)",
                "1920 x 1080 (16:9 Full HD)",
                "1280 x 720 (16:9 HD)",
                "1600 x 900 (16:9 HD+)",
                "1024 x 768 (4:3 XGA)",
                "800 x 600 (4:3 SVGA)",
                "2560 x 1440 (16:9 2K QHD)",
                "3840 x 2160 (16:9 4K UHD)"
            });
            cmbResolution.SelectedIndex = 0;
            tabDisplay.Controls.Add(cmbResolution);
            y += 40;

            tabDisplay.Controls.Add(CreateFieldLabel("Aspek Rasio (Aspect Ratio):", 25, y));
            cmbAspectRatio = CreateComboBox(230, y - 3, 280);
            cmbAspectRatio.Items.AddRange(new object[] {
                "4:3 (Original Otentik PlayStation 1)",
                "16:9 (Widescreen Modern)",
                "21:9 (Ultrawide Monitor)"
            });
            cmbAspectRatio.SelectedIndex = 0;
            tabDisplay.Controls.Add(cmbAspectRatio);
            y += 50;

            tabDisplay.Controls.Add(CreateHeaderLabel("Kualitas Gambar & Render", 20, y)); y += 30;

            tabDisplay.Controls.Add(CreateFieldLabel("Resolusi Internal (Scale):", 25, y));
            cmbInternalRes = CreateComboBox(230, y - 3, 280);
            cmbInternalRes.Items.AddRange(new object[] {
                "1x Native PS1 240p (Klasik Asli)",
                "2x Enhanced 480p",
                "4x High Definition 960p",
                "8x Ultra HD 1920p (Sangat Tajam)"
            });
            cmbInternalRes.SelectedIndex = 0;
            tabDisplay.Controls.Add(cmbInternalRes);
            y += 40;

            tabDisplay.Controls.Add(CreateFieldLabel("Texture Filtering:", 25, y));
            cmbTextureFilter = CreateComboBox(230, y - 3, 280);
            cmbTextureFilter.Items.AddRange(new object[] {
                "Nearest (Retro Pixel Art Asli - Rekomendasi)",
                "Bilinear (Tekstur Lebih Halus)"
            });
            cmbTextureFilter.SelectedIndex = 0;
            tabDisplay.Controls.Add(cmbTextureFilter);
            y += 40;

            chkPgxp = CreateCheckBox("PGXP 3D Geometry Precision (Hilangkan goyangan poligon khas PS1)", 25, y);
            chkPgxp.Checked = true;
            tabDisplay.Controls.Add(chkPgxp);
            y += 30;

            chkAntialiasing = CreateCheckBox("Aktifkan Fast Approximate Anti-Aliasing (FXAA)", 25, y);
            chkAntialiasing.Checked = false;
            tabDisplay.Controls.Add(chkAntialiasing);

            // ==================== TAB 2: PERFORMANCE & FPS ====================
            y = 20;
            tabPerf.Controls.Add(CreateHeaderLabel("Kecepatan Frame & Refresh Rate", 20, y)); y += 30;

            tabPerf.Controls.Add(CreateFieldLabel("Target Frame Rate (FPS):", 25, y));
            cmbFpsTarget = CreateComboBox(230, y - 3, 280);
            cmbFpsTarget.Items.AddRange(new object[] {
                "60 FPS (Standar Halus 60 Hz - Rekomendasi)",
                "120 FPS (High Refresh Rate Gaming Monitor)",
                "144 FPS (Monitor 144 Hz)",
                "240 FPS (Esports Display)",
                "30 FPS (Kecepatan Asli PS1 NTSC)"
            });
            cmbFpsTarget.SelectedIndex = 0;
            tabPerf.Controls.Add(cmbFpsTarget);
            y += 40;

            tabPerf.Controls.Add(CreateFieldLabel("Vertical Sync (V-Sync):", 25, y));
            cmbVsync = CreateComboBox(230, y - 3, 280);
            cmbVsync.Items.AddRange(new object[] {
                "V-Sync On (Tear-Free, Sinkron dengan Monitor)",
                "V-Sync Off (Latency Terendah)",
                "Adaptive V-Sync"
            });
            cmbVsync.SelectedIndex = 0;
            tabPerf.Controls.Add(cmbVsync);
            y += 40;

            tabPerf.Controls.Add(CreateFieldLabel("Kecepatan Turbo (Fast Forward):", 25, y));
            cmbFastForward = CreateComboBox(230, y - 3, 280);
            cmbFastForward.Items.AddRange(new object[] {
                "2.0x (2x Kecepatan Normal)",
                "3.0x (3x Kecepatan Normal)",
                "4.0x (4x Kecepatan Normal)",
                "1.5x (Sedikit Lebih Cepat)"
            });
            cmbFastForward.SelectedIndex = 1;
            tabPerf.Controls.Add(cmbFastForward);
            y += 50;

            tabPerf.Controls.Add(CreateHeaderLabel("Optimasi Hardware & Latensi", 20, y)); y += 30;

            chkLowLatency = CreateCheckBox("Low Latency Input (Respon Kontroler Lebih Cepat 1 Frame)", 25, y);
            chkLowLatency.Checked = true;
            tabPerf.Controls.Add(chkLowLatency);
            y += 35;

            chkMultiThread = CreateCheckBox("Multi-threaded Render Pipeline (Performa Lebih Ringan di CPU Multi-Core)", 25, y);
            chkMultiThread.Checked = true;
            tabPerf.Controls.Add(chkMultiThread);
            y += 35;

            chkShowFps = CreateCheckBox("Tampilkan FPS Meter / Overlay di Layar (HotKey: F)", 25, y);
            chkShowFps.Checked = false;
            tabPerf.Controls.Add(chkShowFps);

            // ==================== TAB 3: CONTROLS & GAMEPAD ====================
            y = 20;
            tabControls.Controls.Add(CreateHeaderLabel("Konfigurasi Kontroler / Gamepad", 20, y)); y += 30;

            tabControls.Controls.Add(CreateFieldLabel("Perangkat Input P1:", 25, y));
            cmbPadDevice = CreateComboBox(230, y - 3, 280);
            cmbPadDevice.Items.AddRange(new object[] {
                "Auto (Otomatis Deteksi Xbox / Bluetooth Gamepad)",
                "Keyboard (Keyboard PC Saja)"
            });
            cmbPadDevice.SelectedIndex = 0;
            tabControls.Controls.Add(cmbPadDevice);
            y += 40;

            tabControls.Controls.Add(CreateFieldLabel("Mode Stik (Pad Mode):", 25, y));
            cmbPadMode = CreateComboBox(230, y - 3, 280);
            cmbPadMode.Items.AddRange(new object[] {
                "Analog DualShock (Stik Kiri & D-Pad Aktif)",
                "Digital Pad (D-Pad Saja)"
            });
            cmbPadMode.SelectedIndex = 0;
            tabControls.Controls.Add(cmbPadMode);
            y += 40;

            tabControls.Controls.Add(CreateFieldLabel("Deadzone Analog Stick:", 25, y));
            tbDeadzone = new TrackBar
            {
                Location = new Point(230, y - 5),
                Size = new Size(220, 45),
                Minimum = 2,
                Maximum = 30,
                Value = 10,
                TickFrequency = 2,
                BackColor = Color.FromArgb(30, 31, 36)
            };
            lblDeadzoneVal = new Label
            {
                Location = new Point(460, y),
                Size = new Size(80, 25),
                Text = "10%",
                ForeColor = Color.FromArgb(100, 220, 140)
            };
            tbDeadzone.ValueChanged += (s, e) => {
                lblDeadzoneVal.Text = tbDeadzone.Value + "%";
            };
            tabControls.Controls.Add(tbDeadzone);
            tabControls.Controls.Add(lblDeadzoneVal);
            y += 50;

            tabControls.Controls.Add(CreateHeaderLabel("Pemetaan Tombol Bawaan (Xbox & Bluetooth X3):", 20, y)); y += 25;
            string keyInfo = "• A: Konfirmasi / Bicara / Ambil Barang\n" +
                             "• B: Cancel / Lari Cepat (Tahan)\n" +
                             "• X: Menggunakan Alat Tani (Cangkul, Sabit, dsb)\n" +
                             "• Y: Memasukkan Barang ke Ransel (Backpack)\n" +
                             "• LB / RB: Ganti Alat Tani / Ganti Barang\n" +
                             "• Start: Buka Menu Utama (Inventori, Ternak, Jam)\n" +
                             "• Select: Peta Desa Mineral Town / Cuaca\n" +
                             "• Left Stick / D-Pad: Bergerak 8 Arah";
            Label lblKeyHelp = new Label
            {
                Location = new Point(30, y),
                Size = new Size(570, 150),
                Text = keyInfo,
                ForeColor = Color.FromArgb(190, 195, 205),
                Font = new Font("Segoe UI", 9.0f)
            };
            tabControls.Controls.Add(lblKeyHelp);

            // ==================== TAB 4: HOTKEYS & SAVE ====================
            y = 20;
            tabHelp.Controls.Add(CreateHeaderLabel("Pintasan Keyboard (In-Game Hotkeys)", 20, y)); y += 30;
            string hotkeyInfo = "• Alt + Enter  atau  Ctrl + F : Toggle Layar Penuh (Fullscreen)\n" +
                                "• F : Toggle Tampilan FPS Meter (OSD & Title Bar)\n" +
                                "• Tab (Tahan) : Fast Forward / Percepat Game (Turbo Mode)\n" +
                                "• Minus (-) / Plus (+) : Kecilkan / Besarkan Volume Audio\n" +
                                "• F1 - F12 : Toggle Pengaturan Grafis Langsung (PGXP, Widescreen)\n" +
                                "• Esc : Keluar dari Game";
            Label lblHotkeys = new Label
            {
                Location = new Point(30, y),
                Size = new Size(570, 110),
                Text = hotkeyInfo,
                ForeColor = Color.FromArgb(200, 205, 215),
                Font = new Font("Segoe UI", 9.2f)
            };
            tabHelp.Controls.Add(lblHotkeys);
            y += 120;

            tabHelp.Controls.Add(CreateHeaderLabel("Penyimpanan Permainan (Memory Card)", 20, y)); y += 30;
            Label lblSaveDesc = new Label
            {
                Location = new Point(30, y),
                Size = new Size(570, 45),
                Text = "File save game disimpan dalam format kartu memori standar PS1 (card1.mcd & card2.mcd) di folder game.",
                ForeColor = Color.FromArgb(180, 185, 195)
            };
            tabHelp.Controls.Add(lblSaveDesc);
            y += 45;

            Button btnOpenSave = new Button
            {
                Text = "📁 Buka Folder Save Game (card1.mcd)",
                Location = new Point(30, y),
                Size = new Size(280, 36),
                BackColor = Color.FromArgb(50, 55, 65),
                ForeColor = Color.White,
                FlatStyle = FlatStyle.Flat
            };
            btnOpenSave.FlatAppearance.BorderColor = Color.FromArgb(80, 85, 95);
            btnOpenSave.Click += (s, e) => {
                Process.Start("explorer.exe", baseDir);
            };
            tabHelp.Controls.Add(btnOpenSave);

            // ==================== BOTTOM FOOTER ====================
            Panel pnlFooter = new Panel
            {
                Dock = DockStyle.Bottom,
                Height = 85,
                BackColor = Color.FromArgb(18, 19, 22)
            };

            chkAlwaysShowLauncher = new CheckBox
            {
                Text = "Tampilkan Launcher ini sebelum memulai game",
                Location = new Point(20, 12),
                AutoSize = true,
                Checked = true,
                ForeColor = Color.FromArgb(180, 185, 195),
                Font = new Font("Segoe UI", 9.0f)
            };
            pnlFooter.Controls.Add(chkAlwaysShowLauncher);

            Button btnPlay = new Button
            {
                Text = "▶  MAINKAN GAME",
                Location = new Point(440, 20),
                Size = new Size(210, 48),
                BackColor = Color.FromArgb(46, 175, 90),
                ForeColor = Color.White,
                Font = new Font("Segoe UI", 11.5f, FontStyle.Bold),
                FlatStyle = FlatStyle.Flat,
                Cursor = Cursors.Hand
            };
            btnPlay.FlatAppearance.BorderSize = 0;
            btnPlay.Click += (s, e) => {
                SaveConfig();
                LaunchGame();
            };
            pnlFooter.Controls.Add(btnPlay);

            Button btnSave = new Button
            {
                Text = "💾 Simpan",
                Location = new Point(310, 26),
                Size = new Size(115, 38),
                BackColor = Color.FromArgb(45, 50, 60),
                ForeColor = Color.White,
                FlatStyle = FlatStyle.Flat,
                Cursor = Cursors.Hand
            };
            btnSave.FlatAppearance.BorderColor = Color.FromArgb(70, 75, 85);
            btnSave.Click += (s, e) => {
                SaveConfig();
                MessageBox.Show("Pengaturan berhasil disimpan!", "Tersimpan", MessageBoxButtons.OK, MessageBoxIcon.Information);
            };
            pnlFooter.Controls.Add(btnSave);

            Button btnExit = new Button
            {
                Text = "Keluar",
                Location = new Point(20, 38),
                Size = new Size(90, 32),
                BackColor = Color.FromArgb(35, 38, 45),
                ForeColor = Color.FromArgb(180, 180, 180),
                FlatStyle = FlatStyle.Flat
            };
            btnExit.FlatAppearance.BorderColor = Color.FromArgb(55, 58, 65);
            btnExit.Click += (s, e) => this.Close();
            pnlFooter.Controls.Add(btnExit);

            this.Controls.Add(pnlFooter);
        }

        private Label CreateHeaderLabel(string text, int x, int y)
        {
            return new Label
            {
                Text = text,
                Location = new Point(x, y),
                AutoSize = true,
                Font = new Font("Segoe UI", 10.5f, FontStyle.Bold),
                ForeColor = Color.FromArgb(100, 215, 140)
            };
        }

        private Label CreateFieldLabel(string text, int x, int y)
        {
            return new Label
            {
                Text = text,
                Location = new Point(x, y),
                AutoSize = true,
                ForeColor = Color.FromArgb(220, 220, 225)
            };
        }

        private ComboBox CreateComboBox(int x, int y, int width)
        {
            return new ComboBox
            {
                Location = new Point(x, y),
                Width = width,
                DropDownStyle = ComboBoxStyle.DropDownList,
                BackColor = Color.FromArgb(45, 48, 56),
                ForeColor = Color.White,
                FlatStyle = FlatStyle.Flat
            };
        }

        private CheckBox CreateCheckBox(string text, int x, int y)
        {
            return new CheckBox
            {
                Text = text,
                Location = new Point(x, y),
                AutoSize = true,
                ForeColor = Color.FromArgb(220, 220, 225),
                FlatStyle = FlatStyle.Standard
            };
        }

        private void LoadConfig()
        {
            try
            {
                if (File.Exists(settingsTomlPath))
                {
                    string content = File.ReadAllText(settingsTomlPath);

                    if (content.Contains("fullscreen = 1")) cmbDisplayMode.SelectedIndex = 1;
                    else if (content.Contains("fullscreen = 2")) cmbDisplayMode.SelectedIndex = 2;
                    else cmbDisplayMode.SelectedIndex = 0;

                    if (content.Contains("window_width = 1920")) cmbResolution.SelectedIndex = 1;
                    else if (content.Contains("window_width = 1280")) cmbResolution.SelectedIndex = 0;
                    else if (content.Contains("window_width = 2560")) cmbResolution.SelectedIndex = 6;
                    else if (content.Contains("window_width = 3840")) cmbResolution.SelectedIndex = 7;

                    if (content.Contains("aspect_num = 16")) cmbAspectRatio.SelectedIndex = 1;
                    else if (content.Contains("aspect_num = 21")) cmbAspectRatio.SelectedIndex = 2;
                    else cmbAspectRatio.SelectedIndex = 0;

                    if (content.Contains("vsync = 0")) cmbVsync.SelectedIndex = 1;
                    else if (content.Contains("vsync = -1")) cmbVsync.SelectedIndex = 2;
                    else cmbVsync.SelectedIndex = 0;

                    if (content.Contains("low_latency_input = false")) chkLowLatency.Checked = false;
                    else chkLowLatency.Checked = true;

                    if (content.Contains("fps_meter = true")) chkShowFps.Checked = true;
                    else chkShowFps.Checked = false;
                }

                if (File.Exists(gameTomlPath))
                {
                    string content = File.ReadAllText(gameTomlPath);
                    if (content.Contains("p1_device = \"keyboard\"")) cmbPadDevice.SelectedIndex = 1;
                    else cmbPadDevice.SelectedIndex = 0;

                    if (content.Contains("p1_mode = \"digital\"")) cmbPadMode.SelectedIndex = 1;
                    else cmbPadMode.SelectedIndex = 0;

                    if (content.Contains("deadzone ="))
                    {
                        // parse deadzone value e.g. 3277 = 10%
                        int idx = content.IndexOf("deadzone =");
                        string sub = content.Substring(idx);
                        string[] lines = sub.Split('\n');
                        if (lines.Length > 0)
                        {
                            string[] parts = lines[0].Split('=');
                            if (parts.Length > 1)
                            {
                                int dz;
                                if (int.TryParse(parts[1].Trim(), out dz))
                                {
                                    int pct = (dz * 100) / 32767;
                                    if (pct >= 2 && pct <= 30) tbDeadzone.Value = pct;
                                }
                            }
                        }
                    }
                }
            }
            catch { }
        }

        private void SaveConfig()
        {
            try
            {
                // Fullscreen
                int fs = cmbDisplayMode.SelectedIndex; // 0, 1, 2
                int winW = 1280;
                switch (cmbResolution.SelectedIndex)
                {
                    case 0: winW = 1280; break;
                    case 1: winW = 1920; break;
                    case 2: winW = 1280; break;
                    case 3: winW = 1600; break;
                    case 4: winW = 1024; break;
                    case 5: winW = 800; break;
                    case 6: winW = 2560; break;
                    case 7: winW = 3840; break;
                }

                int aspNum = 4, aspDen = 3;
                if (cmbAspectRatio.SelectedIndex == 1) { aspNum = 16; aspDen = 9; }
                else if (cmbAspectRatio.SelectedIndex == 2) { aspNum = 21; aspDen = 9; }

                int vs = 1;
                if (cmbVsync.SelectedIndex == 1) vs = 0;
                else if (cmbVsync.SelectedIndex == 2) vs = -1;

                string pDevice = cmbPadDevice.SelectedIndex == 1 ? "keyboard" : "auto";
                string pMode = cmbPadMode.SelectedIndex == 1 ? "digital" : "analog";
                int deadzoneRaw = (tbDeadzone.Value * 32767) / 100;
                string langCode = "id";

                // Save settings.toml
                StringBuilder sbSettings = new StringBuilder();
                sbSettings.AppendLine("# Harvest Moon: Back to Nature - Player Settings");
                sbSettings.AppendLine("[localization]");
                sbSettings.AppendLine("language = \"" + langCode + "\"");
                sbSettings.AppendLine();
                sbSettings.AppendLine("[video]");
                sbSettings.AppendLine("fullscreen = " + fs);
                sbSettings.AppendLine("window_width = " + winW);
                sbSettings.AppendLine("renderer = 1");
                sbSettings.AppendLine("vsync = " + vs);
                sbSettings.AppendLine("aspect_num = " + aspNum);
                sbSettings.AppendLine("aspect_den = " + aspDen);
                sbSettings.AppendLine("low_latency_input = " + (chkLowLatency.Checked ? "true" : "false"));
                sbSettings.AppendLine("render_thread = " + (chkMultiThread.Checked ? "true" : "false"));
                sbSettings.AppendLine("present_thread = " + (chkMultiThread.Checked ? "true" : "false"));
                sbSettings.AppendLine("fps_meter = " + (chkShowFps.Checked ? "true" : "false"));
                sbSettings.AppendLine();
                sbSettings.AppendLine("[controller]");
                sbSettings.AppendLine("p1_device = \"" + pDevice + "\"");
                sbSettings.AppendLine("p1_mode = \"" + pMode + "\"");
                sbSettings.AppendLine("deadzone = " + deadzoneRaw);
                File.WriteAllText(settingsTomlPath, sbSettings.ToString());

                // Detect disc file dynamically from game folder
                string discPath = "game/Harvest Moon - Back to Nature (USA).cue";
                string gameDir = Path.Combine(baseDir, "game");
                if (Directory.Exists(gameDir))
                {
                    string[] candidates = Directory.GetFiles(gameDir, "*.*");
                    string foundDisc = null;
                    foreach (string ext in new[] { ".iso", ".cue", ".bin", ".chd" })
                    {
                        foreach (string f in candidates)
                        {
                            if (f.EndsWith(ext, StringComparison.OrdinalIgnoreCase))
                            {
                                foundDisc = "game/" + Path.GetFileName(f);
                                break;
                            }
                        }
                        if (foundDisc != null) break;
                    }
                    if (foundDisc != null) discPath = foundDisc;
                }

                // Save/Update game.toml
                StringBuilder sbGame = new StringBuilder();
                sbGame.AppendLine("[game]");
                sbGame.AppendLine("name = \"HarvestMoonBTN\"");
                sbGame.AppendLine("id = \"SLUS-01115\"");
                sbGame.AppendLine("exe = \"input/SLUS_011.15\"");
                sbGame.AppendLine("disc = \"" + discPath.Replace("\\", "/") + "\"");
                sbGame.AppendLine("load_address = \"0x80010000\"");
                sbGame.AppendLine("entry_pc = \"0x80011278\"");
                sbGame.AppendLine("text_size = \"0x4F000\"");
                sbGame.AppendLine("stack_base = \"0x801FFFF0\"");
                sbGame.AppendLine();
                sbGame.AppendLine("[recompiler]");
                sbGame.AppendLine("seeds = \"seeds/functions.txt\"");
                sbGame.AppendLine("bios_config = \"psxrecomp/bios/OpenBIOS.toml\"");
                sbGame.AppendLine("strict = true");
                sbGame.AppendLine("out_dir = \"generated\"");
                sbGame.AppendLine();
                sbGame.AppendLine("[runtime]");
                sbGame.AppendLine("window_title = \"Harvest Moon: Back to Nature (PC Port)\"");
                sbGame.AppendLine("language = \"" + langCode + "\"");
                sbGame.AppendLine("bios_hle = false");
                sbGame.AppendLine("overlay_cache = true");
                sbGame.AppendLine();
                sbGame.AppendLine("[controller]");
                sbGame.AppendLine("p1_device = \"" + pDevice + "\"");
                sbGame.AppendLine("p1_mode = \"" + pMode + "\"");
                sbGame.AppendLine("deadzone = " + deadzoneRaw);
                sbGame.AppendLine();
                sbGame.AppendLine("[video]");
                sbGame.AppendLine("renderer = \"opengl\"");
                sbGame.AppendLine("geometry_correction = " + (chkPgxp.Checked ? "true" : "false"));
                if (chkAntialiasing.Checked) sbGame.AppendLine("antialiasing = \"fxaa\"");

                File.WriteAllText(gameTomlPath, sbGame.ToString());
            }
            catch (Exception ex)
            {
                MessageBox.Show("Gagal menyimpan konfigurasi: " + ex.Message, "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        private void LaunchGame()
        {
            if (!File.Exists(exePath))
            {
                MessageBox.Show("File game executable tidak ditemukan:\n" + exePath, "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                return;
            }

            try
            {
                ProcessStartInfo psi = new ProcessStartInfo();
                psi.FileName = exePath;
                psi.WorkingDirectory = baseDir;

                // Localization
                psi.EnvironmentVariables["PSX_LANG"] = "id";
                psi.EnvironmentVariables["PSX_ENCODING"] = "harvest_moon";

                // FPS environment variable
                int fps = 60;
                if (cmbFpsTarget.SelectedIndex == 1) fps = 120;
                else if (cmbFpsTarget.SelectedIndex == 2) fps = 144;
                else if (cmbFpsTarget.SelectedIndex == 3) fps = 240;
                else if (cmbFpsTarget.SelectedIndex == 4) fps = 30;

                psi.EnvironmentVariables["PSX_HOST_REFRESH_HZ"] = fps.ToString();

                // FPS Meter Telemetry
                psi.EnvironmentVariables["PSX_FPS_TELEMETRY"] = chkShowFps.Checked ? "1" : "0";

                // Fast forward speed
                double ffSpeed = 3.0;
                if (cmbFastForward.SelectedIndex == 0) ffSpeed = 2.0;
                else if (cmbFastForward.SelectedIndex == 1) ffSpeed = 3.0;
                else if (cmbFastForward.SelectedIndex == 2) ffSpeed = 4.0;
                else if (cmbFastForward.SelectedIndex == 3) ffSpeed = 1.5;
                psi.EnvironmentVariables["PSX_FAST_FORWARD_SPEED"] = ffSpeed.ToString();

                psi.UseShellExecute = false;
                Process.Start(psi);

                // Close launcher after starting game
                this.Close();
            }
            catch (Exception ex)
            {
                MessageBox.Show("Gagal menjalankan game: " + ex.Message, "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }
    }
}
