n = input("Enter a number.\n")

while True:   
    try:
        n = int(n)
        break
    except ValueError:
        print("Please only enter a number.")
        n = input("")

if n > 0:
    print("The number is positive.")
elif n < 0: 
    print("The number is negative.")
else:
    print("The number is neither positive or negative.")