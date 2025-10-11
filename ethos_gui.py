# ethos_gui.py
"""
ETHOS FINDER v2 - GUI Application
Modern graphical interface for OSINT searches
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import json
from typing import Optional

# Import core functionality
from tools import email_search, handle_search, phone_search
try:
    from secure_config import load_config, save_config, secure_config
    SECURE_MODE = True
except ImportError:
    from config import load_config, save_config
    secure_config = None
    SECURE_MODE = False


class EthosFinderGUI:
    """Main GUI application for ETHOS FINDER."""

    def __init__(self, root):
        self.root = root
        self.root.title("ETHOS FINDER v2")
        self.root.geometry("900x700")
        self.root.minsize(800, 600)

        # Load configuration
        try:
            load_config()
        except Exception as e:
            messagebox.showwarning("Config Warning", f"Error loading config: {e}\nUsing defaults.")

        # Setup theme
        self.setup_theme()

        # Create UI
        self.create_menu()
        self.create_header()
        self.create_search_panel()
        self.create_results_panel()
        self.create_status_bar()

    def setup_theme(self):
        """Configure application theme and colors."""
        style = ttk.Style()
        style.theme_use('clam')

        # Color scheme
        self.colors = {
            'bg': '#1e1e1e',
            'fg': '#e0e0e0',
            'accent': '#007acc',
            'success': '#4ec9b0',
            'warning': '#ce9178',
            'error': '#f48771',
            'panel': '#252526',
            'button': '#0e639c'
        }

        # Configure styles
        style.configure('TFrame', background=self.colors['bg'])
        style.configure('TLabel', background=self.colors['bg'], foreground=self.colors['fg'])
        style.configure('TButton', background=self.colors['button'], foreground=self.colors['fg'])
        style.configure('Header.TLabel', font=('Arial', 16, 'bold'), foreground=self.colors['accent'])
        style.configure('TNotebook', background=self.colors['bg'])
        style.configure('TNotebook.Tab', padding=[20, 10])

        self.root.configure(bg=self.colors['bg'])

    def create_menu(self):
        """Create application menu bar."""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Clear Results", command=self.clear_results)
        file_menu.add_command(label="Export Results", command=self.export_results)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)

        # Settings menu
        settings_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Settings", menu=settings_menu)
        settings_menu.add_command(label="Configure API Keys", command=self.open_settings)
        settings_menu.add_command(label="View Configuration", command=self.view_config)
        settings_menu.add_separator()
        settings_menu.add_command(label="Reset Configuration", command=self.reset_config)

        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)
        help_menu.add_command(label="Documentation", command=self.show_docs)

    def create_header(self):
        """Create application header."""
        header_frame = ttk.Frame(self.root)
        header_frame.pack(fill=tk.X, padx=10, pady=10)

        title = ttk.Label(header_frame, text="🔍 ETHOS FINDER v2", style='Header.TLabel')
        title.pack(side=tk.LEFT)

        subtitle = ttk.Label(header_frame, text="Open Source Intelligence Tool", font=('Arial', 9))
        subtitle.pack(side=tk.LEFT, padx=10)

    def create_search_panel(self):
        """Create search input panel with tabs."""
        search_frame = ttk.Frame(self.root)
        search_frame.pack(fill=tk.BOTH, expand=False, padx=10, pady=5)

        # Create notebook for different search types
        self.notebook = ttk.Notebook(search_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Email search tab
        self.email_tab = self.create_email_tab()
        self.notebook.add(self.email_tab, text="📧 Email Search")

        # Phone search tab
        self.phone_tab = self.create_phone_tab()
        self.notebook.add(self.phone_tab, text="📱 Phone Search")

        # Username search tab
        self.handle_tab = self.create_handle_tab()
        self.notebook.add(self.handle_tab, text="👤 Username Search")

        # Future tabs
        name_tab = ttk.Frame(self.notebook)
        ttk.Label(name_tab, text="🚧 Coming Soon: Name/Surname Search",
                 font=('Arial', 12)).pack(pady=50)
        self.notebook.add(name_tab, text="👥 Name Search")

    def create_email_tab(self):
        """Create email search tab."""
        frame = ttk.Frame(self.notebook)

        # Input section
        input_frame = ttk.Frame(frame)
        input_frame.pack(fill=tk.X, padx=20, pady=20)

        ttk.Label(input_frame, text="Email Address:", font=('Arial', 10, 'bold')).pack(anchor=tk.W)

        entry_frame = ttk.Frame(input_frame)
        entry_frame.pack(fill=tk.X, pady=5)

        self.email_entry = ttk.Entry(entry_frame, font=('Arial', 11))
        self.email_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        self.email_entry.bind('<Return>', lambda e: self.search_email())

        search_btn = tk.Button(entry_frame, text="🔍 Search", command=self.search_email,
                               bg=self.colors['button'], fg=self.colors['fg'],
                               font=('Arial', 10, 'bold'), padx=20, pady=5, cursor='hand2')
        search_btn.pack(side=tk.RIGHT)

        # Options
        options_frame = ttk.Frame(input_frame)
        options_frame.pack(fill=tk.X, pady=5)

        self.email_use_api = tk.BooleanVar(value=False)
        ttk.Checkbutton(options_frame, text="Use RapidAPI for enhanced results",
                       variable=self.email_use_api).pack(anchor=tk.W)

        return frame

    def create_phone_tab(self):
        """Create phone search tab."""
        frame = ttk.Frame(self.notebook)

        # Input section
        input_frame = ttk.Frame(frame)
        input_frame.pack(fill=tk.X, padx=20, pady=20)

        ttk.Label(input_frame, text="Phone Number:", font=('Arial', 10, 'bold')).pack(anchor=tk.W)
        ttk.Label(input_frame, text="Format: +[country code][number] (e.g., +1234567890)",
                 font=('Arial', 8), foreground=self.colors['warning']).pack(anchor=tk.W)

        entry_frame = ttk.Frame(input_frame)
        entry_frame.pack(fill=tk.X, pady=5)

        self.phone_entry = ttk.Entry(entry_frame, font=('Arial', 11))
        self.phone_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        self.phone_entry.bind('<Return>', lambda e: self.search_phone())

        search_btn = tk.Button(entry_frame, text="🔍 Search", command=self.search_phone,
                               bg=self.colors['button'], fg=self.colors['fg'],
                               font=('Arial', 10, 'bold'), padx=20, pady=5, cursor='hand2')
        search_btn.pack(side=tk.RIGHT)

        # Options
        options_frame = ttk.Frame(input_frame)
        options_frame.pack(fill=tk.X, pady=5)

        self.phone_use_api = tk.BooleanVar(value=False)
        ttk.Checkbutton(options_frame, text="Use RapidAPI for enhanced results",
                       variable=self.phone_use_api).pack(anchor=tk.W)

        return frame

    def create_handle_tab(self):
        """Create username/handle search tab."""
        frame = ttk.Frame(self.notebook)

        # Input section
        input_frame = ttk.Frame(frame)
        input_frame.pack(fill=tk.X, padx=20, pady=20)

        ttk.Label(input_frame, text="Username/Handle:", font=('Arial', 10, 'bold')).pack(anchor=tk.W)
        ttk.Label(input_frame, text="Search across 25+ social platforms",
                 font=('Arial', 8), foreground=self.colors['success']).pack(anchor=tk.W)

        entry_frame = ttk.Frame(input_frame)
        entry_frame.pack(fill=tk.X, pady=5)

        self.handle_entry = ttk.Entry(entry_frame, font=('Arial', 11))
        self.handle_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        self.handle_entry.bind('<Return>', lambda e: self.search_handle())

        search_btn = tk.Button(entry_frame, text="🔍 Search", command=self.search_handle,
                               bg=self.colors['button'], fg=self.colors['fg'],
                               font=('Arial', 10, 'bold'), padx=20, pady=5, cursor='hand2')
        search_btn.pack(side=tk.RIGHT)

        # Options
        options_frame = ttk.Frame(input_frame)
        options_frame.pack(fill=tk.X, pady=5)

        self.handle_use_api = tk.BooleanVar(value=False)
        ttk.Checkbutton(options_frame, text="Use RapidAPI for enhanced results",
                       variable=self.handle_use_api).pack(anchor=tk.W)

        return frame

    def create_results_panel(self):
        """Create results display panel."""
        results_frame = ttk.Frame(self.root)
        results_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        ttk.Label(results_frame, text="Results:", font=('Arial', 10, 'bold')).pack(anchor=tk.W)

        # Results text area with scrollbar
        self.results_text = scrolledtext.ScrolledText(
            results_frame,
            wrap=tk.WORD,
            font=('Consolas', 9),
            bg=self.colors['panel'],
            fg=self.colors['fg'],
            insertbackground=self.colors['fg'],
            selectbackground=self.colors['accent']
        )
        self.results_text.pack(fill=tk.BOTH, expand=True, pady=5)

        # Configure text tags for colored output
        self.results_text.tag_config('success', foreground=self.colors['success'])
        self.results_text.tag_config('warning', foreground=self.colors['warning'])
        self.results_text.tag_config('error', foreground=self.colors['error'])
        self.results_text.tag_config('info', foreground=self.colors['accent'])

    def create_status_bar(self):
        """Create status bar at bottom."""
        status_frame = ttk.Frame(self.root)
        status_frame.pack(fill=tk.X, side=tk.BOTTOM, padx=10, pady=5)

        self.status_label = ttk.Label(status_frame, text="Ready", font=('Arial', 8))
        self.status_label.pack(side=tk.LEFT)

        self.progress = ttk.Progressbar(status_frame, mode='indeterminate', length=200)
        self.progress.pack(side=tk.RIGHT, padx=(10, 0))

    # Search Methods
    def search_email(self):
        """Handle email search."""
        email = self.email_entry.get().strip()

        if not email:
            messagebox.showwarning("Input Required", "Please enter an email address.")
            return

        # Basic validation
        if '@' not in email or '.' not in email:
            messagebox.showerror("Invalid Input", "Please enter a valid email address.")
            return

        self.log_message(f"\n{'='*60}", 'info')
        self.log_message(f"Starting email search for: {email}", 'info')
        self.log_message('='*60, 'info')

        # Run search in thread to prevent GUI freeze
        threading.Thread(target=self._run_email_search, args=(email,), daemon=True).start()

    def _run_email_search(self, email):
        """Run email search in background thread."""
        self.set_status("Searching...")
        self.progress.start(10)

        try:
            # Mock user input for API choice
            if self.email_use_api.get():
                self.log_message("\n[i] Enhanced API search enabled", 'warning')

            result = email_search.find_by_email(email)
            self.display_search_results(result, "Email")

        except Exception as e:
            self.log_message(f"\n[!] Error during search: {e}", 'error')
        finally:
            self.progress.stop()
            self.set_status("Search complete")

    def search_phone(self):
        """Handle phone search."""
        phone = self.phone_entry.get().strip()

        if not phone:
            messagebox.showwarning("Input Required", "Please enter a phone number.")
            return

        self.log_message(f"\n{'='*60}", 'info')
        self.log_message(f"Starting phone search for: {phone}", 'info')
        self.log_message('='*60, 'info')

        threading.Thread(target=self._run_phone_search, args=(phone,), daemon=True).start()

    def _run_phone_search(self, phone):
        """Run phone search in background thread."""
        self.set_status("Searching...")
        self.progress.start(10)

        try:
            if self.phone_use_api.get():
                self.log_message("\n[i] Enhanced API search enabled", 'warning')

            result = phone_search.find_by_phone(phone)
            self.display_search_results(result, "Phone")

        except Exception as e:
            self.log_message(f"\n[!] Error during search: {e}", 'error')
        finally:
            self.progress.stop()
            self.set_status("Search complete")

    def search_handle(self):
        """Handle username search."""
        handle = self.handle_entry.get().strip()

        if not handle:
            messagebox.showwarning("Input Required", "Please enter a username.")
            return

        self.log_message(f"\n{'='*60}", 'info')
        self.log_message(f"Starting username search for: {handle}", 'info')
        self.log_message('='*60, 'info')

        threading.Thread(target=self._run_handle_search, args=(handle,), daemon=True).start()

    def _run_handle_search(self, handle):
        """Run handle search in background thread."""
        self.set_status("Searching...")
        self.progress.start(10)

        try:
            if self.handle_use_api.get():
                self.log_message("\n[i] Enhanced API search enabled", 'warning')

            result = handle_search.find_by_handle(handle)
            self.display_search_results(result, "Username")

        except Exception as e:
            self.log_message(f"\n[!] Error during search: {e}", 'error')
        finally:
            self.progress.stop()
            self.set_status("Search complete")

    def display_search_results(self, result, search_type):
        """Display formatted search results."""
        self.log_message(f"\n[+] {search_type} Search Results:", 'success')
        self.log_message("-" * 60)

        if isinstance(result, dict):
            formatted = json.dumps(result, indent=2, ensure_ascii=False)
            self.log_message(formatted)
        else:
            self.log_message(str(result))

        self.log_message("\n" + "="*60 + "\n")

    # Utility Methods
    def log_message(self, message, tag='normal'):
        """Add message to results text area."""
        self.results_text.insert(tk.END, message + "\n", tag)
        self.results_text.see(tk.END)
        self.root.update_idletasks()

    def set_status(self, message):
        """Update status bar message."""
        self.status_label.config(text=message)
        self.root.update_idletasks()

    def clear_results(self):
        """Clear results text area."""
        self.results_text.delete(1.0, tk.END)
        self.log_message("Results cleared.", 'info')

    def export_results(self):
        """Export results to file."""
        from tkinter import filedialog

        content = self.results_text.get(1.0, tk.END)
        if not content.strip():
            messagebox.showinfo("No Results", "No results to export.")
            return

        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("JSON files", "*.json"), ("All files", "*.*")]
        )

        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(content)
                messagebox.showinfo("Export Successful", f"Results exported to:\n{filename}")
            except Exception as e:
                messagebox.showerror("Export Failed", f"Error: {e}")

    # Settings Methods
    def open_settings(self):
        """Open settings dialog."""
        settings_window = tk.Toplevel(self.root)
        settings_window.title("API Configuration")
        settings_window.geometry("500x400")
        settings_window.configure(bg=self.colors['bg'])

        # Title
        ttk.Label(settings_window, text="RapidAPI Configuration",
                 style='Header.TLabel').pack(pady=10)

        # API Name
        ttk.Label(settings_window, text="API Name:").pack(anchor=tk.W, padx=20, pady=(10, 0))
        api_name_entry = ttk.Entry(settings_window, font=('Arial', 10))
        api_name_entry.pack(fill=tk.X, padx=20, pady=5)

        # API Host
        ttk.Label(settings_window, text="API Host:").pack(anchor=tk.W, padx=20, pady=(10, 0))
        host_entry = ttk.Entry(settings_window, font=('Arial', 10))
        host_entry.pack(fill=tk.X, padx=20, pady=5)

        # API Key
        ttk.Label(settings_window, text="API Key:").pack(anchor=tk.W, padx=20, pady=(10, 0))
        key_entry = ttk.Entry(settings_window, font=('Arial', 10), show="*")
        key_entry.pack(fill=tk.X, padx=20, pady=5)

        # Show/Hide key
        show_key_var = tk.BooleanVar()
        def toggle_key():
            key_entry.config(show="" if show_key_var.get() else "*")

        ttk.Checkbutton(settings_window, text="Show API Key",
                       variable=show_key_var, command=toggle_key).pack(anchor=tk.W, padx=20)

        # Save button
        def save_api_config():
            api_name = api_name_entry.get().strip()
            host = host_entry.get().strip()
            key = key_entry.get().strip()

            if not api_name or not host or not key:
                messagebox.showwarning("Missing Information", "Please fill all fields.")
                return

            if SECURE_MODE and secure_config:
                if secure_config.set_api_key(api_name, host, key):
                    messagebox.showinfo("Success", "API configuration saved securely!")
                    settings_window.destroy()
            else:
                messagebox.showwarning("Secure Mode Unavailable",
                                      "Install cryptography for secure storage:\npip install cryptography")

        btn_frame = ttk.Frame(settings_window)
        btn_frame.pack(pady=20)

        tk.Button(btn_frame, text="Save", command=save_api_config,
                 bg=self.colors['success'], fg='white', padx=30, pady=10).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Cancel", command=settings_window.destroy,
                 bg=self.colors['error'], fg='white', padx=30, pady=10).pack(side=tk.LEFT, padx=5)

    def view_config(self):
        """View current configuration."""
        if SECURE_MODE and secure_config:
            secure_config.list_apis()

        config_window = tk.Toplevel(self.root)
        config_window.title("Current Configuration")
        config_window.geometry("500x300")

        text_area = scrolledtext.ScrolledText(config_window, wrap=tk.WORD, font=('Consolas', 9))
        text_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        if SECURE_MODE and secure_config:
            config_text = json.dumps(secure_config.config, indent=2, ensure_ascii=False)
            # Mask API key for security
            config_text = config_text.replace(secure_config.config.get("rapidapi_key", ""), "***HIDDEN***")
        else:
            config_text = "Configuration not available"

        text_area.insert(1.0, config_text)
        text_area.config(state=tk.DISABLED)

    def reset_config(self):
        """Reset configuration."""
        if messagebox.askyesno("Confirm Reset", "Are you sure you want to reset the configuration?"):
            try:
                import os
                if os.path.exists("config.json"):
                    os.remove("config.json")
                if os.path.exists(".ethos_key"):
                    if messagebox.askyesno("Remove Key", "Remove encryption key file too?"):
                        os.remove(".ethos_key")
                messagebox.showinfo("Success", "Configuration reset complete!")
                load_config()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to reset config: {e}")

    # Help Methods
    def show_about(self):
        """Show about dialog."""
        about_text = """
ETHOS FINDER v2
Open Source Intelligence Tool

A defensive security tool for gathering
publicly available information from
various online sources.

Features:
• Email search
• Phone number lookup
• Username search across 25+ platforms
• RapidAPI integration
• Secure API key storage

© 2025 - For educational purposes only
"""
        messagebox.showinfo("About ETHOS FINDER", about_text)

    def show_docs(self):
        """Show documentation."""
        docs_window = tk.Toplevel(self.root)
        docs_window.title("Documentation")
        docs_window.geometry("600x500")

        text_area = scrolledtext.ScrolledText(docs_window, wrap=tk.WORD, font=('Arial', 10))
        text_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        docs_text = """
ETHOS FINDER v2 - Documentation

GETTING STARTED:
1. Select a search type (Email, Phone, or Username)
2. Enter the search query
3. Click Search or press Enter
4. View results in the results panel

SEARCH TYPES:

📧 Email Search
- Search for email mentions on the web
- Find associated social profiles
- Optional RapidAPI enhanced search

📱 Phone Search
- Parse international phone numbers
- Identify carrier and country
- Generate WhatsApp click-to-chat links
- Optional RapidAPI enhanced search

👤 Username Search
- Check username across 25+ platforms
- Verify account existence
- Direct links to profiles
- Optional RapidAPI enhanced search

SETTINGS:
- Configure RapidAPI keys for enhanced searches
- View current configuration
- Reset configuration

SECURITY:
- API keys are encrypted when stored
- Use environment variable ETHOS_RAPIDAPI_KEY for maximum security
- Never share your API keys

EXPORT:
Use File → Export Results to save search results to a file.

For more information, see SECURITY_IMPROVEMENTS.md
"""
        text_area.insert(1.0, docs_text)
        text_area.config(state=tk.DISABLED)


def main():
    """Main entry point for GUI application."""
    root = tk.Tk()
    app = EthosFinderGUI(root)

    # Center window on screen
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')

    root.mainloop()


if __name__ == "__main__":
    main()
