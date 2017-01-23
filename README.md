# Simple ML Plotter

Visualizing tool for numeric logs of iterative program.
This is especially intended for machine learning tools.

## Prerequisite

```
pip install -r requirements.txt
```

## Usage

In you code:
```python
...

from simple_ml_plotter.reporter import Reporter

reporter = Reporter('path/to/log.json')

...

reporter.add_record('loss', loss, global_step=n_epoch, group='train')

reporter.save()

```

In shell:

```terminal
python bin/simple_ml_plotter.py path/to/log.json
```

You can now browse log via http://localhost:8080/

