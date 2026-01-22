#!/usr/bin/env python3
"""
Graphical User Interface for Password Generator
Modern GUI for generating secure passwords
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from password_engine import PasswordGenerator


class PasswordGeneratorGUI:
    """Graphical user interface for password generation"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Password Generator 🔐")
        self.root.geometry("800x700")
        self.root.configure(bg='#f0f0f0')
        
        self.generator = PasswordGenerator()
        
        # Color scheme
        self.colors = {
            'primary': '#2C3E50',
            'secondary': '#3498DB',
            'success': '#27AE60',
            'danger': '#E74C3C',
            'warning': '#F39C12',
            'bg': '#ECF0F1',
            'card': '#FFFFFF',
            'text': '#2C3E50'
        }
        
        # Variables
        self.length_var = tk.IntVar(value=12)
        self.use_lowercase = tk.BooleanVar(value=True)
        self.use_uppercase = tk.BooleanVar(value=True)
        self.use_digits = tk.BooleanVar(value=True)
        self.use_special = tk.BooleanVar(value=True)
        self.exclude_ambiguous = tk.BooleanVar(value=False)
        
        self.setup_ui()
    
    def setup_ui(self):
        """Set up the user interface"""
        # Header
        self.create_header()
        
        # Main container
        main_container = tk.Frame(self.root, bg=self.colors['bg'])
        main_container.pack(fill='both', expand=True, padx=15, pady=15)
        
        # Left panel - Options
        self.create_options_panel(main_container)
        
        # Right panel - Output and presets
        self.create_output_panel(main_container)
        
        # Bottom panel - History
        self.create_history_panel()
    
    def create_header(self):
        """Create header section"""
        header = tk.Frame(self.root, bg=self.colors['primary'], height=80)
        header.pack(fill='x', side='top')
        
        title_label = tk.Label(
            header,
            text="🔐 Password Generator",
            font=('Arial', 24, 'bold'),
            bg=self.colors['primary'],
            fg='white',
            pady=20
        )
        title_label.pack()
    
    def create_options_panel(self, parent):
        """Create options panel"""
        options_frame = tk.Frame(parent, bg=self.colors['card'], relief='raised', bd=2)
        options_frame.pack(side='left', fill='both', expand=True, padx=(0, 8))
        
        # Title
        tk.Label(
            options_frame,
            text="Password Options",
            font=('Arial', 16, 'bold'),
            bg=self.colors['card'],
            fg=self.colors['text']
        ).pack(pady=15)
        
        # Length slider
        length_frame = tk.Frame(options_frame, bg=self.colors['card'])
        length_frame.pack(fill='x', padx=20, pady=10)
        
        tk.Label(
            length_frame,
            text="Password Length:",
            font=('Arial', 11, 'bold'),
            bg=self.colors['card']
        ).pack(anchor='w')
        
        length_display_frame = tk.Frame(length_frame, bg=self.colors['card'])
        length_display_frame.pack(fill='x', pady=5)
        
        self.length_label = tk.Label(
            length_display_frame,
            text="12",
            font=('Arial', 20, 'bold'),
            bg=self.colors['card'],
            fg=self.colors['secondary']
        )
        self.length_label.pack(side='left')
        
        tk.Label(
            length_display_frame,
            text="characters",
            font=('Arial', 10),
            bg=self.colors['card']
        ).pack(side='left', padx=5)
        
        self.length_slider = tk.Scale(
            length_frame,
            from_=4,
            to=64,
            orient='horizontal',
            variable=self.length_var,
            command=self.update_length_label,
            bg=self.colors['card'],
            highlightthickness=0,
            length=300
        )
        self.length_slider.pack(fill='x', pady=5)
        
        # Character options
        options_label = tk.Label(
            options_frame,
            text="Include Characters:",
            font=('Arial', 11, 'bold'),
            bg=self.colors['card']
        )
        options_label.pack(anchor='w', padx=20, pady=(15, 5))
        
        char_frame = tk.Frame(options_frame, bg=self.colors['card'])
        char_frame.pack(fill='x', padx=20)
        
        checkboxes = [
            ("Lowercase (a-z)", self.use_lowercase),
            ("Uppercase (A-Z)", self.use_uppercase),
            ("Digits (0-9)", self.use_digits),
            ("Special (!@#$%)", self.use_special),
            ("Exclude Ambiguous (il1Lo0O)", self.exclude_ambiguous)
        ]
        
        for text, var in checkboxes:
            cb = tk.Checkbutton(
                char_frame,
                text=text,
                variable=var,
                font=('Arial', 10),
                bg=self.colors['card'],
                activebackground=self.colors['card']
            )
            cb.pack(anchor='w', pady=3)
        
        # Generate button
        generate_btn = tk.Button(
            options_frame,
            text="🔑 Generate Password",
            command=self.generate_custom,
            bg=self.colors['success'],
            fg='white',
            font=('Arial', 13, 'bold'),
            cursor='hand2',
            relief='flat',
            padx=30,
            pady=15
        )
        generate_btn.pack(pady=25, padx=20, fill='x')
        
        # Quick presets
        tk.Label(
            options_frame,
            text="Quick Presets:",
            font=('Arial', 11, 'bold'),
            bg=self.colors['card']
        ).pack(anchor='w', padx=20, pady=(10, 5))
        
        preset_frame = tk.Frame(options_frame, bg=self.colors['card'])
        preset_frame.pack(fill='x', padx=20, pady=(0, 20))
        
        presets = [
            ("Easy", self.generate_easy, self.colors['secondary']),
            ("Medium", self.generate_medium, self.colors['warning']),
            ("Strong", self.generate_strong, self.colors['danger']),
        ]
        
        for text, command, color in presets:
            btn = tk.Button(
                preset_frame,
                text=text,
                command=command,
                bg=color,
                fg='white',
                font=('Arial', 10, 'bold'),
                cursor='hand2',
                relief='flat',
                padx=15,
                pady=8
            )
            btn.pack(side='left', expand=True, fill='x', padx=2)
    
    def create_output_panel(self, parent):
        """Create output panel"""
        output_frame = tk.Frame(parent, bg=self.colors['card'], relief='raised', bd=2)
        output_frame.pack(side='left', fill='both', expand=True, padx=(8, 0))
        
        # Title
        tk.Label(
            output_frame,
            text="Generated Password",
            font=('Arial', 16, 'bold'),
            bg=self.colors['card'],
            fg=self.colors['text']
        ).pack(pady=15)
        
        # Password display
        password_display_frame = tk.Frame(output_frame, bg=self.colors['bg'], relief='sunken', bd=2)
        password_display_frame.pack(fill='x', padx=20, pady=10)
        
        self.password_text = tk.Text(
            password_display_frame,
            height=3,
            font=('Courier', 16, 'bold'),
            bg=self.colors['bg'],
            fg=self.colors['primary'],
            wrap='word',
            relief='flat',
            padx=10,
            pady=10
        )
        self.password_text.pack(fill='x')
        self.password_text.insert('1.0', 'Your password will appear here...')
        self.password_text.config(state='disabled')
        
        # Action buttons
        action_frame = tk.Frame(output_frame, bg=self.colors['card'])
        action_frame.pack(fill='x', padx=20, pady=10)
        
        copy_btn = tk.Button(
            action_frame,
            text="📋 Copy",
            command=self.copy_password,
            bg=self.colors['secondary'],
            fg='white',
            font=('Arial', 11, 'bold'),
            cursor='hand2',
            relief='flat',
            padx=20,
            pady=10
        )
        copy_btn.pack(side='left', expand=True, fill='x', padx=(0, 5))
        
        save_btn = tk.Button(
            action_frame,
            text="💾 Save",
            command=self.save_password,
            bg=self.colors['success'],
            fg='white',
            font=('Arial', 11, 'bold'),
            cursor='hand2',
            relief='flat',
            padx=20,
            pady=10
        )
        save_btn.pack(side='left', expand=True, fill='x', padx=5)
        
        check_btn = tk.Button(
            action_frame,
            text="🔍 Check",
            command=self.check_strength,
            bg=self.colors['warning'],
            fg='white',
            font=('Arial', 11, 'bold'),
            cursor='hand2',
            relief='flat',
            padx=20,
            pady=10
        )
        check_btn.pack(side='left', expand=True, fill='x', padx=(5, 0))
        
        # Strength indicator
        tk.Label(
            output_frame,
            text="Password Strength:",
            font=('Arial', 11, 'bold'),
            bg=self.colors['card']
        ).pack(anchor='w', padx=20, pady=(20, 5))
        
        self.strength_frame = tk.Frame(output_frame, bg=self.colors['card'])
        self.strength_frame.pack(fill='x', padx=20)
        
        self.strength_label = tk.Label(
            self.strength_frame,
            text="N/A",
            font=('Arial', 14, 'bold'),
            bg=self.colors['card'],
            fg='gray'
        )
        self.strength_label.pack(anchor='w')
        
        self.strength_bar = tk.Canvas(
            self.strength_frame,
            height=20,
            bg=self.colors['bg'],
            highlightthickness=0
        )
        self.strength_bar.pack(fill='x', pady=5)
        
        # Additional tools
        tk.Label(
            output_frame,
            text="Additional Tools:",
            font=('Arial', 11, 'bold'),
            bg=self.colors['card']
        ).pack(anchor='w', padx=20, pady=(20, 5))
        
        tools_frame = tk.Frame(output_frame, bg=self.colors['card'])
        tools_frame.pack(fill='x', padx=20, pady=(0, 10))
        
        pin_btn = tk.Button(
            tools_frame,
            text="🔢 Generate PIN",
            command=self.generate_pin,
            bg=self.colors['primary'],
            fg='white',
            font=('Arial', 10),
            cursor='hand2',
            relief='flat',
            padx=10,
            pady=8
        )
        pin_btn.pack(side='left', expand=True, fill='x', padx=(0, 5))
        
        passphrase_btn = tk.Button(
            tools_frame,
            text="📝 Passphrase",
            command=self.generate_passphrase,
            bg=self.colors['primary'],
            fg='white',
            font=('Arial', 10),
            cursor='hand2',
            relief='flat',
            padx=10,
            pady=8
        )
        passphrase_btn.pack(side='left', expand=True, fill='x', padx=5)
        
        multiple_btn = tk.Button(
            tools_frame,
            text="🔄 Multiple",
            command=self.generate_multiple,
            bg=self.colors['primary'],
            fg='white',
            font=('Arial', 10),
            cursor='hand2',
            relief='flat',
            padx=10,
            pady=8
        )
        multiple_btn.pack(side='left', expand=True, fill='x', padx=(5, 0))
    
    def create_history_panel(self):
        """Create history panel at bottom"""
        history_frame = tk.Frame(self.root, bg=self.colors['card'], relief='raised', bd=2)
        history_frame.pack(fill='both', padx=15, pady=(0, 15))
        
        # Header
        header = tk.Frame(history_frame, bg=self.colors['card'])
        header.pack(fill='x', padx=10, pady=10)
        
        tk.Label(
            header,
            text="Password History",
            font=('Arial', 12, 'bold'),
            bg=self.colors['card']
        ).pack(side='left')
        
        clear_btn = tk.Button(
            header,
            text="🗑️ Clear History",
            command=self.clear_history,
            bg=self.colors['danger'],
            fg='white',
            font=('Arial', 9),
            cursor='hand2',
            relief='flat',
            padx=10,
            pady=5
        )
        clear_btn.pack(side='right')
        
        # History text area
        self.history_text = scrolledtext.ScrolledText(
            history_frame,
            height=6,
            font=('Courier', 9),
            bg=self.colors['bg'],
            wrap='word',
            padx=10,
            pady=5
        )
        self.history_text.pack(fill='both', padx=10, pady=(0, 10))
        self.update_history_display()
    
    def update_length_label(self, value):
        """Update length label when slider changes"""
        self.length_label.config(text=str(value))
    
    def generate_custom(self):
        """Generate custom password"""
        try:
            password = self.generator.generate_password(
                length=self.length_var.get(),
                use_lowercase=self.use_lowercase.get(),
                use_uppercase=self.use_uppercase.get(),
                use_digits=self.use_digits.get(),
                use_special=self.use_special.get(),
                exclude_ambiguous=self.exclude_ambiguous.get()
            )
            self.display_password(password)
        except ValueError as e:
            messagebox.showerror("Error", str(e))
    
    def generate_easy(self):
        """Generate easy password"""
        password = self.generator.generate_easy_password(self.length_var.get())
        self.display_password(password)
    
    def generate_medium(self):
        """Generate medium password"""
        password = self.generator.generate_medium_password(self.length_var.get())
        self.display_password(password)
    
    def generate_strong(self):
        """Generate strong password"""
        password = self.generator.generate_strong_password(max(16, self.length_var.get()))
        self.display_password(password)
    
    def generate_pin(self):
        """Generate PIN"""
        length = tk.simpledialog.askinteger("PIN Length", "Enter PIN length:", initialvalue=4, minvalue=4, maxvalue=16)
        if length:
            pin = self.generator.generate_pin(length)
            self.display_password(pin)
    
    def generate_passphrase(self):
        """Generate passphrase"""
        num_words = tk.simpledialog.askinteger("Passphrase", "Number of words:", initialvalue=4, minvalue=2, maxvalue=8)
        if num_words:
            passphrase = self.generator.generate_passphrase(num_words)
            self.display_password(passphrase)
    
    def generate_multiple(self):
        """Generate multiple passwords"""
        count = tk.simpledialog.askinteger("Multiple Passwords", "How many passwords?", initialvalue=5, minvalue=1, maxvalue=20)
        if count:
            passwords = self.generator.generate_multiple(count, self.length_var.get())
            
            # Show in new window
            window = tk.Toplevel(self.root)
            window.title("Multiple Passwords")
            window.geometry("500x400")
            
            text = scrolledtext.ScrolledText(window, font=('Courier', 11), padx=10, pady=10)
            text.pack(fill='both', expand=True)
            
            for i, pwd in enumerate(passwords, 1):
                text.insert('end', f"{i:2d}. {pwd}\n")
            
            text.config(state='disabled')
    
    def display_password(self, password):
        """Display generated password"""
        self.password_text.config(state='normal')
        self.password_text.delete('1.0', 'end')
        self.password_text.insert('1.0', password)
        self.password_text.config(state='disabled')
        
        # Update strength
        self.update_strength_display(password)
    
    def update_strength_display(self, password):
        """Update strength indicator"""
        analysis = self.generator.check_strength(password)
        
        # Update label
        self.strength_label.config(
            text=f"{analysis['strength']} ({analysis['score']}/100)",
            fg=analysis['color']
        )
        
        # Update bar
        self.strength_bar.delete('all')
        bar_width = int((analysis['score'] / 100) * self.strength_bar.winfo_width())
        
        # Color gradient based on score
        if analysis['score'] >= 80:
            color = '#27AE60'  # Green
        elif analysis['score'] >= 60:
            color = '#3498DB'  # Blue
        elif analysis['score'] >= 40:
            color = '#F39C12'  # Orange
        else:
            color = '#E74C3C'  # Red
        
        self.strength_bar.create_rectangle(0, 0, bar_width, 20, fill=color, outline='')
    
    def copy_password(self):
        """Copy password to clipboard"""
        self.password_text.config(state='normal')
        password = self.password_text.get('1.0', 'end-1c')
        self.password_text.config(state='disabled')
        
        if password and password != 'Your password will appear here...':
            self.root.clipboard_clear()
            self.root.clipboard_append(password)
            messagebox.showinfo("Success", "Password copied to clipboard!")
        else:
            messagebox.showwarning("Warning", "No password to copy!")
    
    def save_password(self):
        """Save password to history"""
        self.password_text.config(state='normal')
        password = self.password_text.get('1.0', 'end-1c')
        self.password_text.config(state='disabled')
        
        if password and password != 'Your password will appear here...':
            desc = tk.simpledialog.askstring("Save Password", "Enter description (optional):")
            self.generator.save_to_history(password, desc or "")
            self.update_history_display()
            messagebox.showinfo("Success", "Password saved to history!")
        else:
            messagebox.showwarning("Warning", "No password to save!")
    
    def check_strength(self):
        """Check password strength"""
        self.password_text.config(state='normal')
        password = self.password_text.get('1.0', 'end-1c')
        self.password_text.config(state='disabled')
        
        if password and password != 'Your password will appear here...':
            analysis = self.generator.check_strength(password)
            
            feedback = "\n".join(f"• {f}" for f in analysis['feedback'])
            
            message = f"""Password Strength Analysis:

Length: {analysis['length']} characters
Score: {analysis['score']}/100
Strength: {analysis['strength']}

Character Types:
• Lowercase: {'✓' if analysis['has_lowercase'] else '✗'}
• Uppercase: {'✓' if analysis['has_uppercase'] else '✗'}
• Digits: {'✓' if analysis['has_digits'] else '✗'}
• Special: {'✓' if analysis['has_special'] else '✗'}

Recommendations:
{feedback}"""
            
            messagebox.showinfo("Strength Analysis", message)
        else:
            messagebox.showwarning("Warning", "No password to check!")
    
    def update_history_display(self):
        """Update history display"""
        self.history_text.delete('1.0', 'end')
        
        if self.generator.history:
            for i, entry in enumerate(reversed(self.generator.history[-10:]), 1):
                desc = f" - {entry['description']}" if entry['description'] else ""
                self.history_text.insert('end', f"{entry['created_at']} | {entry['password']} | {entry['strength']}{desc}\n")
        else:
            self.history_text.insert('end', "No passwords saved yet...")
    
    def clear_history(self):
        """Clear password history"""
        if self.generator.history:
            if messagebox.askyesno("Confirm", "Clear all password history?"):
                self.generator.clear_history()
                self.update_history_display()
                messagebox.showinfo("Success", "History cleared!")
        else:
            messagebox.showinfo("Info", "History is already empty.")


def main():
    """Entry point for GUI application"""
    root = tk.Tk()
    app = PasswordGeneratorGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
