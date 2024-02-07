from parking_login import ParkingLogin

parking = ParkingLogin()
parking.login()
honkGuid = parking.getHonkGuid()
authHeader = parking.getAuthHeader()
print(honkGuid)
print(authHeader)
promoHashId = parking.getPromoHashId(honkGuid=honkGuid, authHeader=authHeader)
print(promoHashId)  