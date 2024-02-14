from parking_login import ParkingLogin
import time
email = input("What is your altaparking.com email address?\n")
password = input("What is your altaparking.com password?\n")
parking_date = input("Which date would you like to make a reservation for? (YYYY-MM-DD)\n")

parking = ParkingLogin()
parking.login(email, password)
parking.getHonkGuid()
parking.getAuthHeader()

vehicleId = parking.getVehicles()
rateId = parking.getPromoHashId()
cartHashId = parking.createCart(date=parking_date)
parking.claimCart(cartId=cartHashId)
accountPromoCode = parking.getAccountPromoCode()
parking.addPromoToCart(cartId=cartHashId, promoCode=accountPromoCode)
cartId = parking.addRateToCart(rateId=rateId, cartId=cartHashId)

success = False
attempt = 0

while success == False:
    attempt += 1
    response = parking.purchaseCart(vehicleId=vehicleId, cartId=cartId)
    if response['ok'] == False:
        print(attempt, response['errors'])
        time.sleep(2)
    else:
        print('Success!')
        success = True

