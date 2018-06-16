# Kees

A command line interface for reading passwords from [1Password](https://agilebits.com/onepassword) vaults.

[Agile Bits](https://agilebits.com) does not officially support Linux. This lack of agility bites, so I built a vault _reader_, but cannot build a vault _writer_. Fortunately, I use my phone for creating accounts so I only need read support on Linux.

_This project was influenced by George Brock's [1pass](https://github.com/georgebrock/1pass)_


## Using it

Get the password for one of your accounts like this: `kees <account name>`.

```
$ kees gmail
```

You now have 15 seconds to enter your password before a background process cleans your pastebuffer. This reduces the chance an attackers can retrieve your password from your pastebuffer.

If multiple possible matches are found, kees will list them.

```
$ kees "soundcloud - foo"
Password: 
Possible matches:
- Soundcloud - jmsdnns
- Soundcloud - american food
- Soundcloud - locke
```


## Install It

Go get it

```
$ cd $SOMEWHERE
$ git clone https://github.com/jmsdnns/kees
```

Then install it

```
$ cd kees
$ pip install .
```

And then make it a command by editing kees.sh and copying it to your shell.


## Vault Path

Kees assumes the keychain is stored at `~/1Password.agilekeychain`, _unless_ you tell it otherwise.

### Using kees.sh

Add this line after `kees.sh` is sourced

```
export ONEPASSWORD_KEYCHAIN=/path/to/your/keychain
```

### Python flag

The Python code accepts a `--path` flag.

```
$ kees --path ~/whatever/1Password.agilekeychain gmail
```