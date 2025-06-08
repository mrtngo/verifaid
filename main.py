#Imports
from xrpl_txs.donation import donate
from xrpl_txs.invoiceNft import uploadInvoiceAsNFT
from xrpl_txs.NGOCreation import create_ngo
from xrpl_txs.trustline import *
from xrpl_txs.payroll import payroll


def main():

    while True:
        print("Welcome to our Command Line Interface!")
        print("\nPlease select an option:")
        print("1. Create a new NGO")
        print("2. View existing NGOs")
        print("3. Donate to an NGO")
        print("4. Act as an NGO")
        print("5. Exit")
        choice = input("Enter your choice (1-5): ")
        if choice == '1':
            create_ngo()
        elif choice == '2':
            view_ngos()
        elif choice == '3':
            donate()
        elif choice == '4':
            act_as_ngo()
        elif choice == '5':
            print("Exiting the program. Thank you!")
            break
        else:
            print("Invalid choice. Please try again.")

def act_as_ngo():
    while True:
        print("\nYou are now acting as an NGO.")
        print("Please select an action:")
        print("1. View Donations")
        print("2. Upload Expense Receipt")
        print("3. Pay Employee Salary")
        print("4. Return to Main Menu")
        choice = input("Enter your choice (1-4): ")
        
        if choice == '1':
            view_donations()
        elif choice == '2':
            uploadInvoiceAsNFT()
        elif choice == '3':
            payroll()
        elif choice == '4':
            break
        else:
            print("Invalid choice. Please try again.")
   
if __name__ == "__main__":
    main()