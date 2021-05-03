# How to run? - TERMINAL ~ python -m main args*
# EX = python -m main password1 password2 password3
import hashlib
import requests
import sys
# import getpass


def request_api_data(query_char):
    url = 'https://api.pwnedpasswords.com/range/' + query_char
    response = requests.get(url)
    if response.status_code != 200:
        raise RuntimeError(f'Error fetching: Response [{response.status_code}], check API Documentation and try again.')
    return response


def get_pwned_password_count(hashes, hash_to_check):
    hashes = (line.split(':') for line in hashes.text.splitlines())
    for remaining_hashes, count in hashes:
        if remaining_hashes == hash_to_check:
            return count
    return 0


def pwned_api_check(password):
    sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first5_char, remaining_char = sha1password[:5], sha1password[5:]
    response = request_api_data(first5_char)
    return get_pwned_password_count(response, remaining_char)


def main(args):
    for password in args:
        count = pwned_api_check(password)
        if count:
            print(f'{password} was found {count} times... '
                  f'It\'s advised to change your password to a unique and strong one.')
        else:
            print(f'Good News! {password} has not been pwned! ')
    return 'Done.'


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))


# ~~~~~~~~~~~~~~ Access from text file
# def main():
#     with open('password_text.txt', 'r') as f:
#         password_list = []
#         for line in f:
#             content = line.strip()
#             password_list.append(content)
#
#     for password in password_list:
#         count = pwned_api_check(password)
#         if count:
#             print(f'{password[:3]}... was found {count} times... '
#                   f'It\'s advised to change your password to a unique and strong one.')
#         else:
#             print(f'Good News! {password[:3]}... has not been pwned! ')
#     return 'Done.'
#
#
# if __name__=='__main__':
#     main()

# ~~~~~~~~~~~~~~ Access from python input - without echo
# For Pycharm = Go to Run/Edit Configurations and select 'Emulate terminal in output console' for getpass to work
# def main():
#     raw_input = getpass.getpass(prompt='Input Password(s): ', stream=None).split(' ')
#
#     for password in raw_input:
#         count = pwned_api_check(password)
#         if count:
#             print(f'Password [{password[:3]}...] was found {count} times... '
#                   f'It\'s advised to change your password to a unique and strong one.')
#         else:
#             print(f'Good News! [{password[:3]}...] has not been pwned! ')
#     return 'Done.'
#
#
# if __name__ == '__main__':
#     main()
