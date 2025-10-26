import re
import getpass

class PasswordStrengthChecker:
    def __init__(self):
        self.criteria = {
            'length': 8,
            'uppercase': 1,
            'lowercase': 1, 
            'numbers': 1,
            'special_chars': 1
        }
    
    def check_strength(self, password):
        """Check password strength and return score and feedback"""
        score = 0
        feedback = []
        
        # Length check
        if len(password) >= 12:
            score += 3
            feedback.append("✅ Excellent length (12+ characters)")
        elif len(password) >= 8:
            score += 2
            feedback.append("✅ Good length (8+ characters)")
        else:
            feedback.append("❌ Too short (minimum 8 characters)")
        
        # Uppercase letters
        if re.search(r'[A-Z]', password):
            score += 2
            feedback.append("✅ Contains uppercase letters")
        else:
            feedback.append("❌ Add uppercase letters (A-Z)")
        
        # Lowercase letters  
        if re.search(r'[a-z]', password):
            score += 2
            feedback.append("✅ Contains lowercase letters")
        else:
            feedback.append("❌ Add lowercase letters (a-z)")
        
        # Numbers
        if re.search(r'[0-9]', password):
            score += 2
            feedback.append("✅ Contains numbers")
        else:
            feedback.append("❌ Add numbers (0-9)")
        
        # Special characters
        if re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            score += 2
            feedback.append("✅ Contains special characters")
        else:
            feedback.append("❌ Add special characters (!@#$% etc.)")
        
        # Common patterns check
        if self.is_common_password(password):
            score -= 3
            feedback.append("⚠️  This is a commonly used password")
        
        # Sequential characters check
        if self.has_sequential_chars(password):
            score -= 1
            feedback.append("⚠️  Avoid sequential characters (abc, 123)")
        
        # Repeated characters check
        if self.has_repeated_chars(password):
            score -= 1
            feedback.append("⚠️  Avoid repeated characters (aaa, 111)")
        
        return score, feedback
    
    def is_common_password(self, password):
        """Check if password is in common passwords list"""
        common_passwords = {
            'password', '123456', 'password123', 'admin', 'qwerty', 
            'letmein', 'welcome', 'monkey', '123456789', '12345678'
        }
        return password.lower() in common_passwords
    
    def has_sequential_chars(self, password):
        """Check for sequential characters"""
        for i in range(len(password) - 2):
            # Check numeric sequences
            if password[i:i+3].isdigit():
                if int(password[i+1]) == int(password[i]) + 1 and int(password[i+2]) == int(password[i]) + 2:
                    return True
            # Check alphabetical sequences (case insensitive)
            if password[i:i+3].isalpha():
                if (ord(password[i+1].lower()) == ord(password[i].lower()) + 1 and 
                    ord(password[i+2].lower()) == ord(password[i].lower()) + 2):
                    return True
        return False
    
    def has_repeated_chars(self, password):
        """Check for repeated characters"""
        for i in range(len(password) - 2):
            if password[i] == password[i+1] == password[i+2]:
                return True
        return False
    
    def get_strength_level(self, score):
        """Convert score to strength level"""
        if score >= 10:
            return "🔒 VERY STRONG", "#00FF00"
        elif score >= 7:
            return "🔐 STRONG", "#7CFC00" 
        elif score >= 5:
            return "⚠️  MEDIUM", "#FFA500"
        elif score >= 3:
            return "🔓 WEAK", "#FF4500"
        else:
            return "💀 VERY WEAK", "#FF0000"
    
    def generate_strong_password(self, length=12):
        """Generate a strong password"""
        import random
        import string
        
        if length < 8:
            length = 8
        
        # Character sets
        lowercase = string.ascii_lowercase
        uppercase = string.ascii_uppercase
        digits = string.digits
        special = '!@#$%^&*()_+-=[]{}|;:,.<>?'
        
        # Ensure at least one of each type
        password = [
            random.choice(lowercase),
            random.choice(uppercase), 
            random.choice(digits),
            random.choice(special)
        ]
        
        # Fill the rest randomly
        all_chars = lowercase + uppercase + digits + special
        password += [random.choice(all_chars) for _ in range(length - 4)]
        
        # Shuffle the password
        random.shuffle(password)
        
        return ''.join(password)

def display_password_strength(password):
    """Display password strength with visual indicators"""
    checker = PasswordStrengthChecker()
    score, feedback = checker.check_strength(password)
    strength, color = checker.get_strength_level(score)
    
    print("\n" + "="*50)
    print("🔐 PASSWORD STRENGTH ANALYSIS")
    print("="*50)
    
    # Display strength with color coding
    print(f"\nStrength: {strength}")
    print(f"Score: {score}/11")
    
    # Visual strength bar
    bars = min(score, 11)
    bar = "█" * bars + "▒" * (11 - bars)
    print(f"Progress: [{bar}]")
    
    # Display feedback
    print("\n📋 Detailed Feedback:")
    for item in feedback:
        print(f"  {item}")
    
    # Additional security tips
    print("\n💡 Security Tips:")
    print("  • Use at least 12 characters")
    print("  • Combine letters, numbers, and symbols")
    print("  • Avoid common words and patterns")
    print("  • Don't reuse passwords across sites")
    print("  • Consider using a password manager")

def main():
    print("🔐 PASSWORD STRENGTH CHECKER")
    print("="*40)
    
    while True:
        print("\n1. Check Password Strength")
        print("2. Generate Strong Password") 
        print("3. Exit")
        
        choice = input("\nChoose option (1-3): ").strip()
        
        if choice == '1':
            print("\nEnter your password (hidden input):")
            password = getpass.getpass("Password: ")
            
            if not password:
                print("❌ Please enter a password!")
                continue
                
            display_password_strength(password)
            
        elif choice == '2':
            checker = PasswordStrengthChecker()
            length = input("Enter password length (default 12): ").strip()
            
            try:
                length = int(length) if length else 12
                if length < 8:
                    print("⚠️  Minimum length is 8, using 12 instead")
                    length = 12
            except ValueError:
                length = 12
                
            strong_password = checker.generate_strong_password(length)
            print(f"\n🔒 Generated Strong Password: {strong_password}")
            
            # Show strength of generated password
            display_password_strength(strong_password)
            
        elif choice == '3':
            print("👋 Stay secure! Goodbye!")
            break
            
        else:
            print("❌ Invalid choice! Please enter 1, 2, or 3.")

# Quick test function
def test_passwords():
    """Test various passwords"""
    test_cases = [
        "password",
        "123456", 
        "Password123",
        "P@ssw0rd!",
        "VeryStrongP@ssw0rd2024!",
        "abc123",
        "Admin123!",
    ]
    
    checker = PasswordStrengthChecker()
    
    print("🧪 TESTING PASSWORD STRENGTHS:")
    print("="*50)
    
    for pwd in test_cases:
        score, feedback = checker.check_strength(pwd)
        strength, color = checker.get_strength_level(score)
        print(f"\nPassword: {pwd}")
        print(f"Strength: {strength} (Score: {score}/11)")

if __name__ == "__main__":
    # Run quick tests
    test_passwords()
    
    # Run main program
    main()