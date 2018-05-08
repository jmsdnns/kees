# Kees

A command line interface for reading passwords from [1Password](https://agilebits.com/onepassword) vaults.

[Agile Bits](https://agilebits.com) does not officially support Linux. This lack of agility bites, so I built a vault _reader_, but cannot build a vault _writer_.

This project was highly influenced by George Brock's [1pass](https://github.com/georgebrock/1pass)

_It's written in Python 3 too, in case that's something you care about_


# Install It

Go get it

```
$ cd $SOMEWHERE
$ git clone https://github.com/jmsdnns/kees
```

Then install it

```
$ cd kees
$ pipenv install .
```

And then make it a command by editing kees.sh and copying it to your shell.


# Using it

Get some password out of your vault like this

```
$ kees gmail
Password:
y0uRp@ssw0rd
```

Put your password in your copy buffer. _Note: kees will overwrite your copy buffer after 15 seconds_

```
$ kees soundcloud
```

Kees assumes the keychain is stored at `~/Dropbox/1Password.agilekeychain`, _unless_ you tell it otherwise with the `--path` flag.

```
$ kees --path ~/whatever/1Password.agilekeychain gmail
```