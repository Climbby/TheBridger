from data.weaponsList import weaponsList

def findWeapon(yourWeapon):
    return next(weapon for weapon in weaponsList if weapon.get("type") == yourWeapon)