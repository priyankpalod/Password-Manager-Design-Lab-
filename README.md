**Design lab Report** - **Priyank Palod**
Roll no.: 13CS30046
To: Prof. Sudeshna Sarkar 
Submission Date: 17/11/2017

Problem Statement
=================

To develop a password manager system based on steganography and cryptography. The password manager should take an image and a master password as input and store a user’s passwords for various different websites and accounts in the image. The user’s data should be encrypted using the master password before storing it in the image and only with the correct master password should you be able to retrieve the information.

Motivation
==========

Online security is a major concern for most online services providers, some providers protect their online users through multi-factor authentications, and up-to-date most provide 1 level authentication - the password. The password is the first line of defense between your data and hackers.

As we use more online services (including internal networks – Intranets), we are forced to create and use more and more passwords, and if we go via the simple route, we will end up with using the same password everywhere. And may be something simple to remember (weak password), especially where some online services providers allow for weak or bad passwords. The matter is even more serious when it comes to online bank accounts like PayPal and banks’ sites, or corporate portals and online network resources, email, blogs, online storage services, social networking sites, or your operating system. While you can always argue that the solution to the problem is to use different strong passwords for every site, but as newer sites pop up every day, it becomes difficult for anyone to actually follow this in practice. Add that to the fact that most of the users on the internet are non-technical. To them, passwords are an annoyance and most of them either write them down or simply use one password for all their web sites. Either option creates a vulnerability.

Also, many website developers with limited understanding of the potential hazards of security breaches may store your password in plaintext. Now any attacker which gets access to their system can get your password. The problem does not stop here! The bigger problem here is that since most users use the password for all the sites, the security breach puts all of your online accounts at risk no matter ho strong your password may be! There have been many incidents of such security breaches and one of the most famous ones is the “RockYou” security breach which put more than 32 million user accounts and their passwords in public view[1]. Thus it becomes important that users have different passwords for different online accounts.

The solution to this, is to free users of the burden of remembering or managing their passwords and instead give them a tool which does all of that for them and creates much stronger passwords than they can ever remember. Thus the need of this password manager system emerges.

Goals
=====

The goal of the project is to create a password manager system which not only keeps the password information safe and secure, but also satisfies most of the criteria of “good password practices”. These practices are as follows:

-   **Make the password at least 10 alphanumeric long**: The longer, the more complex and more secure. Longer passwords are harder for thieves to crack.

-   **Include numbers, upper and lower case letters, and symbols**: The more varied your password is, the harder it is to guess. Use symbols like !\#\$%\^&()\_+| -=\\\~[]:";’\<\>?,./

-   **Use random looking passwords**: The more randomness their is in the password, the more is it safe from various attacks like the dictionary attack.

-   **Use different passwords for different websites**: As explained before, using different passwords secures your other accounts even if one of them is under security breach.

Previous Related Works
======================

A lot of password managers have been in use since a long time[2]. They assist in generating and retrieving complex passwords, potentially storing such passwords in an encrypted database or calculating them on demand. While most of them offer various services like integration with browsers, portability and cross platform access, the central idea for almost all of them has been storing passwords encrypted with a master password. The same is true of this system, but with an added layer of steganography along with encryption. Thus, the attacker needs access to not just your master password but also needs access to the image file to crack your password. Such a combination of encryption and steganography was not found during the investigation for this project.

My Solution
===========

My solution to this problem is to combine cryptography and stegnaography to create a system which uses two layers of security. The user choses a secret image which she can use to store all her passwords for different websites and user accounts. The data is stored in the least significant bits of the image file in an encrypted format, using a master password as the key. Moreover, the passwords are not chosen by the user and are instead generated by our tool itself. This frees the user of the burden of remembering any password for any site, except her master password and the steganographed image. The system achieves the goals as follows:

-   Keeping the data secured and private: The password manager uses steganography to hide data and AES encryption to secure it. To attack the system, the attacker needs to have the knowledge and access to the secret image file as well as the knowledge of the master password.

-   Making password at least 10 characters long: Since the password is not chosen by the user but generated by the tool, the tool can easily make sure that it generates passwords of length longer than 10. (The tool uses 15 by default). The tool also enforces the master password to be at least 15 characters long so that breaking it is infeasible.

-   Including numbers, upper and lower case letters, and symbols: The password generator uses all these special characters with equal probability and hence the generated passwords usually do contain these.

-   Use random looking passwords: Our password generator uses a cryptographically strong random number generator to generate passwords which have no meaning at all!

-   Using different passwords for different sites: Since during adding a different account each time, the random number generator is different, different random looking passwords are generated for each account.

Flexibility of the system
=========================

Different websites have different constraints on how their passwords should be. For eg., some websites enforce the user to use a password which has at least one numeral or at least one special character, while some in fact do not allow the use of certain special characters. Hence, an important issue here is to create a system which is flexible enough to accommodate the password needs of all different websites. This is done by asking the user a series of questions about the password needs while registering a new account. The first question is whether there are any restrictions. If the user replies yes, then the following questions are asked to her:

-   Is at least one character of upper case and one of lower case compulsory (y/n)?

-   Is at least one numeral compulsory (y/n)?

-   Is at least one special character compulsory (y/n)?

The password thus generated satisfies all the constraints provided by the user, while still maintaining the randomness in the reduced password space.

Also, certain critical websites may enforce the user to change their passwords frequently. For this, we have provided the user with an option to generate a new password for an already existing account. Although this might seem trivial but this poses a major risk. An attacker might be able to change the image file by using the change password option even without knowing the master password. Note that until now, knowing the master password wasn’t necessary to read the data from the file. This is so because if the attacker reads the password by using an incorrect master-password, the user would get a wrong password as the application decrypts the passwords using the master password. If the master password is wrong, the attacker would just get a wrongly decrypted password posing no risk to the user. But providing the option to change the password requires the master password to be correct. In order to do that, we append the password data in the image file with the md5 hash of the master password. Hence the system can now check if the master password entered by the user is the correct or not. Since the md5 hash is a very secure one-way function, storing the hash does not pose a security risk of gaining the information of the master password.

One more issue is normalization of urls. Let us understand this with an example. The url for gmail are many. The two famous ones are *www.gmail.com* and *mail.google.com*. But not just that, the same account is used for not only gmail but all of google’s websites *drive.google.com*, *docs.google.com* etc. The way websites implement this is through redirecting log ins from all different websites to a single url, which is *accounts.google.com* in this example. The way our system handles this is through making a network call to get the url to which the user provided url is directed to, thus normalizing all the different urls that the user can input.

Implementation details
======================

Python was used to develop the system as it provides a lot of library support and makes it easy to maintain. Libraries used in the project are as follows:

-   Python Image Library(PIL): To handle reading from and writing to images in the disk.

-   stepic: For steganographic needs of the system.

-   Crypto: To use the AES cipher and to generate random numbers.

-   hashlib: For using the md5 and SHA256 hash algorithm.

-   pyperclip: To copy the password to clipboard.

-   urllib2: To perform network call to get redirection url.

-   urlparse: To parse the redirected url to get netloc

-   getpass: To take password input.

The system takes the image and the master password as inputs from stdin, and the option as a command line argument. Option is one of the following: ‘retr’ to retrieve password, ‘add’ to add a new account and ‘change’ to change password for an existing account.

For AES, we use a block size of 32 and use the SHA256 hash of the master password as the key. The data in the image is stored in the following format: The first 32 bytes store the md5 hash of the master password, and the rest of the image contains the data terminated by the EOF character. The data is stored as a json with keys as unencrypted website names. The values for these keys are themselves jsons with unencrypted usernames as keys and the encrypted passwords as values. Note that only the passwords have been encrypted and not the websites and usernames so as to maintain more secrecy about the key.

Testing
=======

The system underwent white box testing by giving it different inputs so that it takes all possible paths in the control flow. Also, black box beta testing was performed by 3 friends who installed it on their systems. All errors were successfully handled and the system always performed as expected.

Limitations & Future Work
=========================

While the system makes passwords more secure by enforcing the users to keep safer and different passwords, thereby reducing security compromises due to dictionary attacks and weakly secured websites, the user is still under some vulnerability. These include keystroke logging and shoulder sniffing attacks where the attacker records your keystrokes or sees your master password as you type it respectively. To secure the users against such shoulder sniffing and key logging attacks, an advanced system may add biometric security like fingerprints in addition to the master password.

[1] https://techcrunch.com/2009/12/14/rockyou-hack-security-myspace-facebook-passwords/

[2] https://en.wikipedia.org/wiki/List\_of\_password\_managers
