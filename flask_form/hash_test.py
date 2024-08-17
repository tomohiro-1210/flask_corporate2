from werkzeug.security import generate_password_hash, check_password_hash

pw = '4444'
pw_hash = generate_password_hash(pw)

pw_check = '4344'
print(check_password_hash(pw_hash, pw_check))