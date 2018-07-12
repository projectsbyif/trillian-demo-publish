# Trillian Demo Tools: Publish

This demo downloads hourly vehicle counts for a fictional road.

It queries a Trillian log to find out the latest log entry, then pushes any new counts.

A log entry starts life as JSON, looking like:

```
{
    "datetime": "2018-07-10T06:00:00Z",
    "Eastbridge Road – Pedestrians": 18,
    "Eastbridge Road – Bicycles": 7,
    "Eastbridge Road – Motorbikes": 13,
    "Eastbridge Road – Cars" 23,
    "Eastbridge Road – Trucks": 4
}
```

(The Python API serializes this to binary before it's sent to the log.)

## Run

Checkout this repo:

```
git clone https://github.com/projectsbyif/trillian-demo-publish
cd trillian-demo-publish
```

### Configure settings.sh

Copy the `settings.sh.example` file to `settings.sh` and edit it to point it at the Trillian log you want to push data into.

- `TRILLIAN_LOG_URL` is the URL of the demo log server, in the form `https://<host>:<port>/v1beta1/logs/<log_id>`
- `TRILLIAN_LOG_PUBLIC_KEY` is the public key of the Trillian log, which you can query from the log server. It takes the form `<public key algo>:<hash algo>:<der encoded key>`

Look at the [log server](https://github.com/projectsbyif/trillian-demo-server) documentation to find these values for your log.

### Type `make run`

This should set up a virtual environment, install dependencies and run the demo.
