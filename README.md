# wrind
Hack RU F20 project: web application that compiles the most common words in a foreign language, either in general or from a piece of media, to be studied

## Set Up

In order to use the Google Translate API, you will need to acquire credentials to access it from your Google Cloud account.
Once you have received them in the form of a json file, run the following command, and you will not have to worry any further
about authorization:
```
$ export GOOGLE_APPLICATION_CREDENTIALS="[PATH]"
```

`[PATH]` should be exchanged with the file path of your credentials. Read more about this process [here](https://cloud.google.com/translate/docs/setup?hl=en_US).
