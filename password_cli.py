#!/usr/bin/env python3
"""
Command Line Interface for Password Generator
Interactive menu-driven password generation tool
"""

import sys
from password_engine import PasswordGenerator


class PasswordGeneratorCLI:
    """Command-line interface for password generation"""
    
    def __init__(self):
        self.generator = PasswordGenerator()
        self.running = True
    
    def display_banner(self):
        """Display application banner"""
        print("\n" + "="*60)
        print("             🔐 PASSWORD GENERATOR 🔐")
        print("         Generate Strong & Secure Passwords")
        print("="*60)
    
    def display_menu(self):
        """Display main menu"""
        print("\n" + "-"*60)
        print("MAIN MENU:")
        print("-"*60)
        print("1.  Quick Generate (Default Settings)")
        print("2.  Custom Password Generator")
        print("3.  Generate Easy Password (Easy to type)")
        print("4.  Generate Medium Password")
        print("5.  Generate Strong Password")
        print("6.  Generate PIN (Numeric only)")
        print("7.  Generate Passphrase (Memorable)")
        print("8.  Generate Multiple Passwords")
        print("9.  Check Password Strength")
        print("10. View Password History")
        print("11. Clear Password History")
        print("0.  Exit")
        print("-"*60)
    
    def quick_generate(self):
        """Quick password generation with default settings"""
        print("\n--- Quick Password Generator ---")
        try:
            length = input("Enter password length (default: 12): ").strip()
            length = int(length) if length else 12
            
            if length < 4:
                print("❌ Password length must be at least 4 characters!")
                return
            
            password = self.generator.generate_password(length=length)
            self.display_password(password)
            
            # Save to history
            save = input("\nSave to history? (y/n): ").lower()
            if save == 'y':
                desc = input("Enter description (optional): ").strip()
                self.generator.save_to_history(password, desc)
                print("✅ Password saved to history!")
        
        except ValueError as e:
            print(f"❌ Error: {e}")
    
    def custom_generate(self):
        """Custom password generation with user-specified options"""
        print("\n--- Custom Password Generator ---")
        
        try:
            # Get length
            length = input("Enter password length (minimum 4): ").strip()
            length = int(length) if length else 12
            
            if length < 4:
                print("❌ Password length must be at least 4 characters!")
                return
            
            # Get options
            print("\nSelect character types to include:")
            use_lowercase = input("Include lowercase letters? (Y/n): ").lower() != 'n'
            use_uppercase = input("Include uppercase letters? (Y/n): ").lower() != 'n'
            use_digits = input("Include digits? (Y/n): ").lower() != 'n'
            use_special = input("Include special characters? (Y/n): ").lower() != 'n'
            exclude_ambiguous = input("Exclude ambiguous characters (il1Lo0O)? (y/N): ").lower() == 'y'
            
            # Generate password
            password = self.generator.generate_password(
                length=length,
                use_lowercase=use_lowercase,
                use_uppercase=use_uppercase,
                use_digits=use_digits,
                use_special=use_special,
                exclude_ambiguous=exclude_ambiguous
            )
            
            self.display_password(password)
            
            # Save to history
            save = input("\nSave to history? (y/n): ").lower()
            if save == 'y':
                desc = input("Enter description (optional): ").strip()
                self.generator.save_to_history(password, desc)
                print("✅ Password saved to history!")
        
        except ValueError as e:
            print(f"❌ Error: {e}")
    
    def generate_easy(self):
        """Generate easy-to-type password"""
        print("\n--- Easy Password Generator ---")
        print("(Lowercase letters + digits only)")
        
        try:
            length = input("Enter password length (default: 12): ").strip()
            length = int(length) if length else 12
            
            password = self.generator.generate_easy_password(length)
            self.display_password(password)
            
            save = input("\nSave to history? (y/n): ").lower()
            if save == 'y':
                desc = input("Enter description (optional): ").strip()
                self.generator.save_to_history(password, desc)
                print("✅ Password saved to history!")
        
        except ValueError as e:
            print(f"❌ Error: {e}")
    
    def generate_medium(self):
        """Generate medium-strength password"""
        print("\n--- Medium Password Generator ---")
        print("(Letters + digits)")
        
        try:
            length = input("Enter password length (default: 12): ").strip()
            length = int(length) if length else 12
            
            password = self.generator.generate_medium_password(length)
            self.display_password(password)
            
            save = input("\nSave to history? (y/n): ").lower()
            if save == 'y':
                desc = input("Enter description (optional): ").strip()
                self.generator.save_to_history(password, desc)
                print("✅ Password saved to history!")
        
        except ValueError as e:
            print(f"❌ Error: {e}")
    
    def generate_strong(self):
        """Generate strong password"""
        print("\n--- Strong Password Generator ---")
        print("(All character types)")
        
        try:
            length = input("Enter password length (default: 16): ").strip()
            length = int(length) if length else 16
            
            password = self.generator.generate_strong_password(length)
            self.display_password(password)
            
            save = input("\nSave to history? (y/n): ").lower()
            if save == 'y':
                desc = input("Enter description (optional): ").strip()
                self.generator.save_to_history(password, desc)
                print("✅ Password saved to history!")
        
        except ValueError as e:
            print(f"❌ Error: {e}")
    
    def generate_pin(self):
        """Generate numeric PIN"""
        print("\n--- PIN Generator ---")
        
        try:
            length = input("Enter PIN length (default: 4): ").strip()
            length = int(length) if length else 4
            
            pin = self.generator.generate_pin(length)
            print("\n" + "="*60)
            print(f"Generated PIN: {pin}")
            print("="*60)
            
            save = input("\nSave to history? (y/n): ").lower()
            if save == 'y':
                desc = input("Enter description (optional): ").strip()
                self.generator.save_to_history(pin, desc)
                print("✅ PIN saved to history!")
        
        except ValueError as e:
            print(f"❌ Error: {e}")
    
    def generate_passphrase(self):
        """Generate memorable passphrase"""
        print("\n--- Passphrase Generator ---")
        
        try:
            num_words = input("Enter number of words (default: 4): ").strip()
            num_words = int(num_words) if num_words else 4
            
            separator = input("Enter separator character (default: -): ").strip() or '-'
            
            passphrase = self.generator.generate_passphrase(num_words, separator)
            print("\n" + "="*60)
            print(f"Generated Passphrase: {passphrase}")
            print("="*60)
            print("\nPassphrases are easier to remember!")
            
            save = input("\nSave to history? (y/n): ").lower()
            if save == 'y':
                desc = input("Enter description (optional): ").strip()
                self.generator.save_to_history(passphrase, desc)
                print("✅ Passphrase saved to history!")
        
        except ValueError as e:
            print(f"❌ Error: {e}")
    
    def generate_multiple(self):
        """Generate multiple passwords"""
        print("\n--- Multiple Password Generator ---")
        
        try:
            count = input("How many passwords to generate? (default: 5): ").strip()
            count = int(count) if count else 5
            
            if count > 50:
                print("❌ Maximum 50 passwords at once!")
                return
            
            length = input("Enter password length (default: 12): ").strip()
            length = int(length) if length else 12
            
            passwords = self.generator.generate_multiple(count, length)
            
            print("\n" + "="*60)
            print(f"Generated {count} Passwords:")
            print("="*60)
            for i, pwd in enumerate(passwords, 1):
                print(f"{i:2d}. {pwd}")
            print("="*60)
        
        except ValueError as e:
            print(f"❌ Error: {e}")
    
    def check_strength(self):
        """Check password strength"""
        print("\n--- Password Strength Checker ---")
        
        password = input("Enter password to check: ").strip()
        
        if not password:
            print("❌ Password cannot be empty!")
            return
        
        analysis = self.generator.check_strength(password)
        
        print("\n" + "="*60)
        print("PASSWORD STRENGTH ANALYSIS")
        print("="*60)
        print(f"Password: {'*' * len(password)}")
        print(f"Length: {analysis['length']} characters")
        print(f"Strength: {analysis['strength']} ({analysis['score']}/100)")
        print(f"\nCharacter Types:")
        print(f"  Lowercase: {'✓' if analysis['has_lowercase'] else '✗'}")
        print(f"  Uppercase: {'✓' if analysis['has_uppercase'] else '✗'}")
        print(f"  Digits:    {'✓' if analysis['has_digits'] else '✗'}")
        print(f"  Special:   {'✓' if analysis['has_special'] else '✗'}")
        
        if analysis['feedback']:
            print(f"\nRecommendations:")
            for feedback in analysis['feedback']:
                print(f"  • {feedback}")
        
        print("="*60)
    
    def view_history(self):
        """View password history"""
        print("\n--- Password History ---")
        
        if not self.generator.history:
            print("No passwords in history.")
            return
        
        print(f"\nTotal passwords saved: {len(self.generator.history)}")
        print("="*60)
        
        for i, entry in enumerate(self.generator.history, 1):
            print(f"\n{i}. Password: {entry['password']}")
            if entry['description']:
                print(f"   Description: {entry['description']}")
            print(f"   Strength: {entry['strength']}")
            print(f"   Created: {entry['created_at']}")
        
        print("="*60)
    
    def clear_history(self):
        """Clear password history"""
        print("\n--- Clear Password History ---")
        
        if not self.generator.history:
            print("History is already empty.")
            return
        
        confirm = input(f"Delete all {len(self.generator.history)} passwords from history? (yes/no): ").lower()
        
        if confirm == 'yes':
            self.generator.clear_history()
            print("✅ Password history cleared!")
        else:
            print("ℹ️  Cancelled.")
    
    def display_password(self, password: str):
        """Display generated password with strength analysis"""
        print("\n" + "="*60)
        print("GENERATED PASSWORD")
        print("="*60)
        print(f"\n{password}\n")
        print("="*60)
        
        # Show strength analysis
        analysis = self.generator.check_strength(password)
        print(f"\nStrength: {analysis['strength']} ({analysis['score']}/100)")
        print(f"Length: {analysis['length']} characters")
        
        # Try to copy to clipboard
        if self.generator.copy_to_clipboard(password):
            print("\n✅ Password copied to clipboard!")
        else:
            print("\n💡 Tip: Install 'pyperclip' for clipboard support")
            print("   Run: pip install pyperclip")
    
    def run(self):
        """Main application loop"""
        self.display_banner()
        
        while self.running:
            self.display_menu()
            choice = input("\nEnter your choice: ").strip()
            
            if choice == '1':
                self.quick_generate()
            elif choice == '2':
                self.custom_generate()
            elif choice == '3':
                self.generate_easy()
            elif choice == '4':
                self.generate_medium()
            elif choice == '5':
                self.generate_strong()
            elif choice == '6':
                self.generate_pin()
            elif choice == '7':
                self.generate_passphrase()
            elif choice == '8':
                self.generate_multiple()
            elif choice == '9':
                self.check_strength()
            elif choice == '10':
                self.view_history()
            elif choice == '11':
                self.clear_history()
            elif choice == '0':
                print("\n👋 Thank you for using Password Generator!")
                print("Stay secure! 🔐")
                self.running = False
            else:
                print("\n❌ Invalid choice! Please try again.")
            
            if self.running and choice != '0':
                input("\nPress Enter to continue...")


def main():
    """Entry point for CLI application"""
    try:
        app = PasswordGeneratorCLI()
        app.run()
    except KeyboardInterrupt:
        print("\n\n👋 Application terminated by user.")
        sys.exit(0)


if __name__ == "__main__":
    main()
