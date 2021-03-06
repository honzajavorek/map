# Map

A prototype of a static website hosted on [GitHub Pages](https://pages.github.com), which contains an [OpenStreetMap](https://www.openstreetmap.org/) map rendered by [Leaflet](http://leafletjs.com/) from a [GeoJSON](http://geojson.org/) file [cron-generated](https://docs.travis-ci.com/user/cron-jobs/) by [Travis CI](http://travis-ci.org/) from data in [Google Sheets](https://docs.google.com/spreadsheets/).

## Installation and Usage

1.  Have a Google Spreadsheet like [this](https://docs.google.com/spreadsheets/d/1wvEgQtTtXVbkcq2sCis3T6P3AHMJXOzylkshH8sC2s0/edit?usp=sharing):

    | Name          | Location             | Web                       |
    |---------------|----------------------|---------------------------|
    | FÆNCY FRIES   | Přívozská 9, Ostrava | https://faencyfries.cz/   |
    | Garage        | Křižíkova 58, Praha  | http://poutine.cz/        |

    Set its URL as an environment variable:

    ```shell
    export SHEET_URL='https://docs.google.com/spreadsheets/d/1wvEgQtTtXVbkcq2sCis3T6P3AHMJXOzylkshH8sC2s0/edit?ouid=107119873943551212790&usp=sheets_home&ths=true'
    ```

1.  Head to [Google Developers Console](https://console.developers.google.com/project) and create a new project.

    1.  In the navigation menu (top left corner) go to <kbd>APIs & Services</kbd> and <kbd>Library</kbd>.
    1.  Find **Google Sheets API**, enable it.
    1.  Find **Geocoding API**, enable it.
    1.  In the navigation menu (top left corner) go to <kbd>APIs & Services</kbd> and <kbd>Credentials</kbd>.
    1.  Click <kbd>New Credentials</kbd> and choose <kbd>API key</kbd>.
    1.  Edit the key. Name it (e.g. _Geocoding_)
    1.  Restrict the key only to the Geocoding API: <kbd>Key restrictions</kbd> » <kbd>API restrictions</kbd>
    1.  Set the key as an environment variable:

        ```shell
        export GEOCODING_API_KEY=aBcdE...
        ```

    1.  Click <kbd>New Credentials</kbd> and choose <kbd>Service account key</kbd>.
    1.  Service account: <kbd>New service account<kbd>
    1.  Service account name: e.g. _Sheets Reader_
    1.  Role: <kbd>Project</kbd> » <kbd>Viewer</kbd>
    1.  Download it as JSON.
    1.  Set the contents of the JSON file as an environment variable:

        ```shell
        export SHEETS_API_KEY=$(cat map-sample-12345678900a.json)
        ```

1.  Go to your Google Spreadsheet and invite the email from the JSON file's `client_email` field to be able to view the document.

1.  Have **Python 3.7** and [pipenv](https://pipenv.readthedocs.io/). Clone the project and install dependencies:

    ```shell
    $ pipenv install --dev
    ```

    Now you can use following to develop the website locally and to preview it in your browser:

    ```shell
    $ pipenv run serve
    ```

1.  Go to [your GitHub settings](https://github.com/settings/tokens) and generate a new token with the `public_repo` scope. Save the token, you'll need it in the next step.

1.  See the `.travis.yml` file. Go to [Travis CI](http://travis-ci.org/), sign in with GitHub and add a new project with this repository. Go to settings page for the repository (for admins of `honzajavorek/map` it's [here](https://travis-ci.org/honzajavorek/map/settings).

    1.  In the <kbd>Environment Variables</kbd> section add all the environment variables from above: `SHEET_URL`, `SHEETS_API_KEY`, `GEOCODING_API_KEY`. Be sure to set the `SHEETS_API_KEY` quoted with apostrophes `'{ ... }'`.
    1.  Add the GitHub token from previous step as a `GITHUB_TOKEN` environment variable.
    1.  [Set a cron job](https://docs.travis-ci.com/user/cron-jobs/) to build the website daily.

1.  Once the build is passing on the `master` branch, go to the project GitHub Pages, e.g. https://honzajavorek.github.io/map/, and see the result.
