import requests
import hashlib
import sys
import time

# Banner
def print_banner():
    print("""
    ╔══════════════════════════════════════════════════════╗
    ║          Have I Been Pwned - Leak Checker            ║
    ║ Coded by Pakistani Ethical Hacker: Mr. Sabaz Ali Khan║
    ║         Protecting the digital world ethically        ║
    ╚══════════════════════════════════════════════════════╝
    """)

# Function to check if an email has been involved in a data breach
def check_email(email):
    url = f"https://haveibeenpwned.com/api/v3/breachedaccount/{email}"
    headers = {
        "user-agent": "Pwned-Checker-Python",
        "hibp-api-key": "your_api_key_here"  # Replace with your HIBP API key
    }
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            breaches = response.json()
            print(f"\n[!] Email '{email}' was found in the following breaches:")
            for breach in breaches:
                print(f"- {breach['Name']} (Breached on: {breach['BreachDate']})")
        elif response.status_code == 404:
            print(f"\n[+] Good news! Email '{email}' was not found in any breaches.")
        else:
            print(f"\n[-] Error checking email: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"\n[-] Error checking email: {str(e)}")

# Function to check if a password has been leaked using k-anonymity
def check_password(password):
    # Hash the password using SHA-1
    password_hash = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    prefix = password_hash[:5]
    suffix = password_hash[5:]

    # Query HIBP Pwned Passwords API
    url = f"https://api.pwnedpasswords.com/range/{prefix}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            hashes = response.text.splitlines()
            for h in hashes:
                hash_suffix, count = h.split(':')
                if hash_suffix == suffix:
                    print(f"\n[!] Password '{password}' was found in {count} breaches.")
                    return
            print(f"\n[+] Good news! Password '{password}' was not found in any breaches.")
        else:
            print(f"\n[-] Error checking password: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"\n[-] Error checking password: {str(e)}")

# Main function
def main():
    print_banner()
    print("Welcome to the Have I Been Pwned Leak Checker!")
    print("This tool checks if your email or password has been exposed in data breaches.")
    print("Note: Passwords are checked anonymously using k-anonymity.\n")

    while True:
        print("\nOptions:")
        print("1. Check an email address")
        print("2. Check a password")
        print("3. Exit")
        choice = input("Select an option (1-3): ")

        if choice == "1":
            email = input("\nEnter the email address to check: ")
            if "@" in email and "." in email:  # Basic email validation
                check_email(email)
            else:
                print("\n[-] Invalid email address format.")
        elif choice == "2":
            password = input("\nEnter the password to check: ")
            check_password(password)
        elif choice == "3":
            print("\nThank you for using the Leak Checker by Mr. Sabaz Ali Khan!")
            sys.exit(0)
        else:
            print("\n[-] Invalid option. Please select 1, 2, or 3.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[!] Program terminated by user.")
        sys.exit(0)