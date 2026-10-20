# portclash

Find repeated or conflicting port numbers across source and configuration files.

## Features

- Scans common source and config file types for port assignments.
- Detects `PORT=3000`, `port: 3000`, `listen(3000)`, and `:3000` style references.
- Groups repeated ports so conflicts are easy to review.
- Supports text and JSON output.
- No external dependencies beyond Python 3.9+.

## Install

```sh
git clone https://github.com/example/portclash.git
cd portclash
```

## Usage

Audit the current directory:

```sh
python3 portclash.py .
```

Audit another project:

```sh
python3 portclash.py /path/to/project
```

JSON output:

```sh
python3 portclash.py . --format json
```

Fail in CI when conflicts are found:

```sh
python3 portclash.py . --strict
```

## License

MIT
